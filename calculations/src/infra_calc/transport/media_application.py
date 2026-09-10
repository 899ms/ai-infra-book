"""Local application DAG and nonpreemptive FIFO work; no network predictions."""

from collections import defaultdict, deque
from fractions import Fraction as F


class Application:
    def __init__(self, app, schedule, send_message, now):
        self.app, self.schedule, self.send_message, self.now = (
            app,
            schedule,
            send_message,
            now,
        )
        self.messages = {x["id"]: x for x in app["messages"]}
        self.tasks = {x["id"]: x for x in app["compute_tasks"]}
        self.nodes = {**self.messages, **self.tasks}
        self.dependents = defaultdict(list)
        self.remaining = {}
        self.time_ready = set()
        self.status = {k: "waiting" for k in self.nodes}
        self.completed = {}
        self.cancelled = {"client": set(), "server": set()}
        self.work_queues = defaultdict(deque)
        self.running = {}
        self.events, self.work = [], []
        for key, node in self.nodes.items():
            self.remaining[key] = len(node["dependencies"])
            for dep in node["dependencies"]:
                self.dependents[dep["id"]].append(key)
            schedule(F(node["ready_seconds"]), 1, "app_ready", key)

    def suppressed(self, node):
        endpoint = node["sender"] if node["id"] in self.messages else node["endpoint"]
        return node.get("cancel_tag") in self.cancelled[endpoint]

    def eligible(self, key):
        if (
            self.status[key] != "waiting"
            or key not in self.time_ready
            or self.remaining[key]
        ):
            return
        node = self.nodes[key]
        if self.suppressed(node):
            self.status[key] = "cancelled"
            self.events.append(
                dict(at=str(self.now()), kind="cancel_before_start", id=key)
            )
            return
        self.status[key] = "ready"
        if key in self.messages:
            self.send_message(node)
        else:
            resource = (node["endpoint"], node["resource"])
            self.work_queues[resource].append(key)
            self.schedule(self.now(), 3, "app_dispatch", resource)

    def ready(self, key):
        self.time_ready.add(key)
        self.eligible(key)

    def dispatch(self, resource):
        if resource in self.running:
            return
        queue = self.work_queues[resource]
        while queue:
            key = queue.popleft()
            node = self.tasks[key]
            if self.suppressed(node):
                self.status[key] = "cancelled"
                continue
            self.status[key] = "running"
            self.running[resource] = key
            start = self.now()
            end = start + F(node["duration_seconds"])
            record = dict(
                id=key,
                endpoint=resource[0],
                resource=resource[1],
                start=str(start),
                end=str(end),
                finished=False,
            )
            self.work.append(record)
            self.schedule(end, 1, "app_task_done", (resource, key, len(self.work) - 1))
            break

    def finish(self, key, kind):
        self.status[key] = "delivered" if key in self.messages else "finished"
        self.completed[key] = self.now()
        self.events.append(dict(at=str(self.now()), kind=kind, id=key))
        if key in self.messages:
            node = self.messages[key]
            endpoint = node["receiver"]
            for tag in node["on_delivery_cancel_tags"]:
                self.cancelled[endpoint].add(tag)
                self.events.append(
                    dict(
                        at=str(self.now()),
                        kind="cancel_received",
                        endpoint=endpoint,
                        tag=tag,
                        message=key,
                    )
                )
        for successor in self.dependents[key]:
            self.remaining[successor] -= 1
            self.eligible(successor)

    def task_done(self, resource, key, index):
        self.running.pop(resource)
        self.work[index]["finished"] = True
        self.finish(key, "task_completed")
        self.schedule(self.now(), 3, "app_dispatch", resource)

    def delivered(self, key):
        if key not in self.completed:
            self.finish(key, "message_delivered")

    def observers(self, until):
        result = []
        for observer in self.app["business_observers"]:
            ids = [d["id"] for d in observer["completion_dependencies"]]
            all_delivered = all(x in self.completed for x in ids)
            end = (
                max((self.completed[x] for x in ids), default=F(0))
                if all_delivered
                else None
            )
            record = dict(
                id=observer["id"],
                kind=observer["kind"],
                endpoint=observer["endpoint"],
                all_required_delivered=all_delivered,
                complete_at=None if end is None else str(end),
                complete=all_delivered,
                missing=[x for x in ids if x not in self.completed],
            )
            if observer["kind"] == "screenshot":
                version = observer["version"]
                for change in sorted(
                    observer["version_changes"], key=lambda c: F(c["at_seconds"])
                ):
                    if end is not None and F(str(change["at_seconds"])) <= end:
                        version = change["version"]
                record.update(
                    version_at_result=version,
                    expected_version=observer["version"],
                    usable=all_delivered and version == observer["version"],
                    complete=all_delivered and version == observer["version"],
                )
            if observer["kind"] == "tts":
                rows = []
                previous = None
                stall = F(0)
                missing_audio = F(0)
                for block in observer["blocks"]:
                    received = all(x in self.completed for x in block["message_ids"])
                    arrival = (
                        max(
                            (self.completed[x] for x in block["message_ids"]),
                            default=F(0),
                        )
                        if received
                        else None
                    )
                    duration = F(block["duration_seconds"])
                    slot = F(block["slot_start_seconds"])
                    if observer["playback"] == "slots":
                        play = (
                            slot
                            if arrival is not None and arrival <= slot and slot <= until
                            else None
                        )
                        if play is None and slot <= until:
                            missing_audio += min(duration, until - slot)
                    else:
                        play = (
                            None
                            if arrival is None or (rows and previous is None)
                            else max(arrival, slot if previous is None else previous)
                        )
                        if play is not None and previous is not None:
                            stall += max(F(0), min(until, play) - previous)
                    if play is not None and play > until:
                        play = None
                    previous = None if play is None else play + duration
                    rows.append(
                        dict(
                            message_ids=block["message_ids"],
                            arrival=None if arrival is None else str(arrival),
                            play_start=None if play is None else str(play),
                            scheduled_play_end=(
                                None if previous is None else str(previous)
                            ),
                            play_end=(
                                None
                                if previous is None or previous > until
                                else str(previous)
                            ),
                        )
                    )
                played = [r for r in rows if r["play_start"] is not None]
                record.update(
                    blocks=rows,
                    first_play=None if not played else played[0]["play_start"],
                    playback_end=None if not played else played[-1]["play_end"],
                    stall_seconds=str(stall),
                    missing_audio_seconds=str(missing_audio),
                    complete=all_delivered
                    and len(played) == len(rows)
                    and (not played or played[-1]["play_end"] is not None),
                )
            result.append(record)
        return result
