"""Reuse the public multi-stream sender and select reliable recovery payload."""
from copy import deepcopy
from ..topics import transport_sender as _public


def create_sender(inputs):
    return _public.create_sender(inputs)


def retransmittable_frames(record):
    """Select reliable payload from an already validated sent record.

    Control metadata, ACKed interval subtraction, cancellation, PN allocation,
    packet layout and scheduling remain explicit network responsibilities.
    """
    if not isinstance(record, dict) or not isinstance(record.get('frames', []), list):
        raise ValueError('recovery record must contain a frame list')
    frames = record.get('frames', [])
    if any(not isinstance(f, dict) or f.get('type') not in ('stream', 'datagram') for f in frames):
        raise ValueError('unsupported recovery payload frame')
    return deepcopy([f for f in frames if f['type'] == 'stream'])


union = _public.union
reference_sources = _public.reference_sources
