"""Tiny normalized application DAG builders; no predicted network outcomes."""
from copy import deepcopy
from fractions import Fraction as F


def message(identity, *, sender='client', size=1, flow=None, offset=0, ready=0,
            transport='stream', priority=0, dependencies=(), deadline=None):
    if type(size) is not int or size <= 0:
        raise ValueError('positive integer application bytes required')
    if transport not in ('stream', 'datagram') or (transport=='datagram' and size>1168):
        raise ValueError('unsupported transport or oversized atomic datagram')
    return dict(id=identity,sender=sender,receiver='server' if sender=='client' else 'client',
                flow_id=flow or identity,transport=transport,bytes=size,
                stream_offset=offset if transport=='stream' else None,
                application_offset=offset,ready_seconds=str(F(str(ready))),
                dependencies=deepcopy(list(dependencies)),priority=priority,source_order=0,
                deadline_seconds=None if deadline is None else str(F(str(deadline))),
                allow_expire=False,cancel_tag=None,on_delivery_cancel_tags=[],
                packetization=dict(payload_limit_bytes=1168,fragment_count=(size+1167)//1168,
                    final_fragment_bytes=size-((size-1)//1168)*1168,coalesce_across_messages=False))


def dependency(identity,endpoint,event='message_delivered'):
    return dict(id=identity,event=event,endpoint=endpoint)


def application(identity,messages,observers=(),tasks=()):
    messages=deepcopy(list(messages));totals={'client_to_server':0,'server_to_client':0}
    for order,m in enumerate(messages):
        m['source_order']=order
        totals['client_to_server' if m['sender']=='client' else 'server_to_client']+=m['bytes']
    return dict(schema_version=1,id=identity,messages=messages,compute_tasks=deepcopy(list(tasks)),
        business_observers=deepcopy(list(observers)),
        scheduling=dict(send='fifo',compute='fifo',compute_nonpreemptive=True,resource_capacity_tasks=1),
        links={},connection_ready_seconds='0',external_legacy_assumptions={},
        accounting=dict(application_bytes_by_direction=totals,application_bytes=sum(totals.values()),
            message_count=len(messages),task_count=len(tasks),fragment_count=sum(m['packetization']['fragment_count'] for m in messages)))


def complete_observer(identity,message_ids,endpoint='server',kind='image'):
    return dict(id=identity,kind=kind,endpoint=endpoint,
                completion_dependencies=[dependency(x,endpoint) for x in message_ids],version_changes=[])


def teaching_network(app,*,until=12,cwnd=2400,ack_policy='immediate_each_packet'):
    """Base WAN/sender fields only. Wireless schema belongs to network integration."""
    flows={'up':{},'down':{}}
    for m in app['messages']:
        d='up' if m['sender']=='client' else 'down'
        if m['transport']=='stream':flows[d][m['flow_id']]=max(flows[d].get(m['flow_id'],0),m['stream_offset']+m['bytes'])
    return dict(links={d:dict(rate_bps=9824,propagation=0) for d in flows},until=until,
        initial_cwnd=cwnd,initial_max_data={d:1000000 for d in flows},
        initial_max_stream_data=flows,receive_memory_bytes={d:1000000 for d in flows},
        consume_delay=None,pad_in_flight=True,ack_bytes=64,
        sender={'rtt_seed':{'latest_rtt':100,'smoothed_rtt':100,'rttvar':50,'min_rtt':100}},
        ack_policy=deepcopy(ack_policy),drop_packets=[],routers={})
