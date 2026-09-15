"""Independent closed-form payload check and causal recovery invariants."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
data = json.loads((HERE/'results.json').read_text())
for path, digest in data['source_sha256'].items():
    assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest() == digest, path
# Pinned Flash backbone: 2 window-only, 21 CSA, 20 HCA layers.
config = json.loads((ROOT/'calculations/configs/models/deepseek-v4-flash/inference/config.json').read_text())
assert [config['compress_ratios'][:43].count(r) for r in [0, 4, 128]] == [2, 21, 20]
assert (config['head_dim'], config['index_head_dim'], config['window_size']) == (512, 128, 128)
buffer_bytes = 21 * (2*8*1024*4 + 2*8*256*4) + 20*2*128*512*4
for row in data['endpoints']:
    n = row['endpoint']
    history = 43*min(n, 128)*512*2 + 21*(n//4)*640*2 + 20*(n//128)*512*2
    assert row['summary']['history_resident_bytes'] == history
    assert row['summary']['compressor_buffer_bytes'] == buffer_bytes
    assert row['summary']['resident_bytes'] == history + buffer_bytes
    assert all(p['unfinished_positions'] == 0 for p in row['compressor_positions'] if p['ratio'] == 4)
    assert all(p['overlap_positions'] == 4 for p in row['compressor_positions'] if p['ratio'] == 4)
assert (data['scenario_count'], data['request_records']) == (24, 288)
for scenario in data['scenarios']:
    previous_retained = []
    for row in scenario['requests']:
        turn = row['turn']
        if turn == 6 and scenario['fault'] == 'invalidate7':
            previous_retained = []
            assert row['read_bytes'] == row['restored_tokens'] == 0
        restored = row['restored_snapshot_turn']
        assert restored is None or (restored in previous_retained and restored < turn)
        assert row['restored_tokens'] + row['recompute_tokens'] == data['endpoints'][turn]['input_tokens']
        assert row['retained_bytes'] <= scenario['budget_mib']*2**20
        assert (row['write_bytes'] > 0) == row['checkpoint_saved']
        if scenario['policy'] == 'recompute' or scenario['budget_mib'] <= 16:
            assert row['read_bytes'] == row['write_bytes'] == 0
        previous_retained = row['retained_snapshot_turns']
print('Verified source hashes, independent layer payload formula, 24 scenarios / 288 causal recovery records.')
