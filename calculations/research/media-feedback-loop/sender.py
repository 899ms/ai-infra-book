"""Pinned public multi-stream sender reuse; reliable recovery frame selection only."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parent.parent
sys.path.insert(0, str(PROJECT / 'src'))
from infra_calc.topics import transport_sender as _public


def verify_dependencies():
    rows = json.loads((ROOT / 'sender-dependencies.lock.json').read_text())
    for row in rows:
        data = (PROJECT / row['file']).read_bytes()
        if len(data) != row['bytes'] or hashlib.sha256(data).hexdigest() != row['sha256']:
            raise ValueError('frozen sender dependency changed: ' + row['file'])
    return rows


def create_sender(inputs):
    verify_dependencies()
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
