"""Validate local application causality without inventing network outcomes.

This is a preflight check for the normalized media schema, not a scheduler.
A valid graph can still remain incomplete because of flow control or loss.
"""
from collections import deque
from fractions import Fraction


def _name(value, label):
    if not isinstance(value, str) or not value:
        raise ValueError(f"{label} must be a nonempty string")
    return value


def _integer(value, label, minimum=0):
    if type(value) is not int or value < minimum:
        raise ValueError(f"{label} must be an integer >= {minimum}")
    return value


def _seconds(value, label):
    if isinstance(value, bool) or not isinstance(value, (str, int, float)):
        raise ValueError(f"{label} must be finite nonnegative seconds")
    try:
        result = Fraction(str(value))
    except (ValueError, ZeroDivisionError, OverflowError) as error:
        raise ValueError(f"{label} must be finite nonnegative seconds") from error
    if result < 0:
        raise ValueError(f"{label} must be nonnegative")
    return result


def validate_application(application):
    """Raise ValueError for malformed or nonlocal dependencies; mutate nothing.

    Reliable gaps are permitted and may prevent later delivery. Explicit graph
    cycles are rejected; successful termination is never inferred from a DAG.
    """
    if type(application.get("schema_version")) is not int or application["schema_version"] != 1:
        raise ValueError("unsupported application schema")
    endpoints = {"client", "server"}
    messages = application["messages"]
    tasks = application["compute_tasks"]
    records = {}
    event_locations = {}
    stream_intervals = {}
    for message in messages:
        identity = _name(message["id"], "message ID")
        if identity in records:
            raise ValueError("duplicate application ID")
        records[identity] = message
        origin, destination = message["sender"], message["receiver"]
        if origin not in endpoints or destination not in endpoints or origin == destination:
            raise ValueError("messages require distinct client/server endpoints")
        event_locations[identity] = ("message_delivered", destination)
        transport = message["transport"]
        if transport not in ("stream", "datagram"):
            raise ValueError("unknown message transport")
        flow = _name(message["flow_id"], "flow ID")
        size = _integer(message["bytes"], "message bytes", 1)
        _integer(message["application_offset"], "application offset")
        if type(message["allow_expire"]) is not bool:
            raise ValueError("allow_expire must be boolean")
        if transport == "stream":
            offset = _integer(message["stream_offset"], "stream offset")
            if offset + size > 2**62 - 1:
                raise ValueError("STREAM offset exceeds declared transport range")
            stream_intervals.setdefault((origin, flow), []).append((offset, offset + size))
            if message["allow_expire"]:
                raise ValueError("reliable STREAM cannot silently expire")
        elif message["stream_offset"] is not None:
            raise ValueError("DATAGRAM must not consume STREAM offsets")
        layout = message["packetization"]
        capacity = _integer(layout["payload_limit_bytes"], "payload limit", 1)
        count = (size + capacity - 1) // capacity
        if transport == "datagram" and count != 1:
            raise ValueError("DATAGRAM is an atomic application unit")
        if (type(layout["fragment_count"]) is not int or layout["fragment_count"] != count
                or type(layout["final_fragment_bytes"]) is not int
                or layout["final_fragment_bytes"] != size - (count - 1) * capacity
                or layout["coalesce_across_messages"] is not False):
            raise ValueError("packetization metadata disagrees with business bytes")
        _seconds(message["ready_seconds"], "message ready")
        deadline = message["deadline_seconds"]
        if deadline is not None:
            _seconds(deadline, "message deadline")
        if message["allow_expire"] and deadline is None:
            raise ValueError("expiry requires a declared deadline")
        _integer(message["source_order"], "message source order")
        if type(message["priority"]) is not int:
            raise ValueError("priority must be integer")
        if message.get("cancel_tag") is not None:
            _name(message["cancel_tag"], "cancel tag")
        if not isinstance(message["on_delivery_cancel_tags"], list):
            raise ValueError("cancellation targets must be a list")
        for tag in message["on_delivery_cancel_tags"]:
            _name(tag, "cancellation target tag")
    for intervals in stream_intervals.values():
        intervals.sort()
        if any(left[1] > right[0] for left, right in zip(intervals, intervals[1:])):
            raise ValueError("overlapping application messages on one reliable stream")
    for task in tasks:
        identity = _name(task["id"], "task ID")
        if identity in records:
            raise ValueError("duplicate application ID")
        records[identity] = task
        if task["endpoint"] not in endpoints:
            raise ValueError("unknown task endpoint")
        event_locations[identity] = ("task_completed", task["endpoint"])
        _name(task["resource"], "compute resource")
        _seconds(task["duration_seconds"], "task duration")
        _seconds(task["ready_seconds"], "task ready")
        _integer(task["source_order"], "task source order")
        if type(task["priority"]) is not int:
            raise ValueError("task priority must be integer")
        if task.get("cancel_tag") is not None:
            _name(task["cancel_tag"], "cancel tag")

    def dependency_ids(dependencies, consumer_endpoint):
        seen = set()
        for dependency in dependencies:
            identity = dependency["id"]
            if identity not in event_locations:
                raise ValueError("unknown dependency ID")
            location = (dependency["event"], dependency["endpoint"])
            if location != event_locations[identity] or location[1] != consumer_endpoint:
                raise ValueError("dependency needs actual delivery at the consumer endpoint")
            if identity in seen:
                raise ValueError("duplicate dependency")
            seen.add(identity)
        return seen

    successors = {identity: [] for identity in records}
    indegree = {}
    for identity, record in records.items():
        endpoint = (record["sender"] if event_locations[identity][0] == "message_delivered"
                    else record["endpoint"])
        dependencies = dependency_ids(record["dependencies"], endpoint)
        indegree[identity] = len(dependencies)
        for dependency in dependencies:
            successors[dependency].append(identity)
    ready = deque(identity for identity, degree in indegree.items() if degree == 0)
    visited = 0
    while ready:
        visited += 1
        for successor in successors[ready.popleft()]:
            indegree[successor] -= 1
            if indegree[successor] == 0:
                ready.append(successor)
    if visited != len(records):
        raise ValueError("cyclic application dependencies")
    observer_ids = set()
    for observer in application["business_observers"]:
        identity = _name(observer["id"], "observer ID")
        if identity in observer_ids:
            raise ValueError("duplicate observer ID")
        observer_ids.add(identity)
        if observer["endpoint"] not in endpoints:
            raise ValueError("unknown observer endpoint")
        dependency_ids(observer["completion_dependencies"], observer["endpoint"])
        for block in observer.get("blocks", []):
            if not isinstance(block["message_ids"], list) or not block["message_ids"]:
                raise ValueError("playback block requires message IDs")
            if len(set(block["message_ids"])) != len(block["message_ids"]):
                raise ValueError("duplicate playback message ID")
            for message_id in block["message_ids"]:
                if event_locations.get(message_id) != ("message_delivered", observer["endpoint"]):
                    raise ValueError("playback requires actual message delivery at observer")
            _seconds(block["duration_seconds"], "playback duration")
            _seconds(block["slot_start_seconds"], "playback slot")
        for change in observer.get("version_changes", []):
            if change["endpoint"] != observer["endpoint"]:
                raise ValueError("version observation must be local to observer")
            _seconds(change["at_seconds"], "version change")
            _name(change["version"], "version")
    scheduling = application["scheduling"]
    if (scheduling["send"] not in ("fifo", "priority")
            or scheduling["compute"] != "fifo"
            or scheduling["compute_nonpreemptive"] is not True
            or type(scheduling["resource_capacity_tasks"]) is not int
            or scheduling["resource_capacity_tasks"] != 1):
        raise ValueError("unsupported scheduling contract")
    _seconds(application["connection_ready_seconds"], "connection ready")
