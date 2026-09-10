"""Compile selected unchanged upstream C functions and compare finite inputs.

The socket/filter stubs supply declared state. This tests arithmetic and the
full-bandwidth predicate, not Linux networking, max filtering or callback order.
"""
from pathlib import Path
import hashlib
import importlib.util
import json
import random
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent
UPSTREAM = ROOT.parent / "congestion-controller-inputs/sources/tcp_bbr.c"
SOURCE_SHA = "ba7d0706259dfef5bf455f26ac4bab65f43b9209b9cfd4f761c64c89816bdfe4"
assert hashlib.sha256(UPSTREAM.read_bytes()).hexdigest() == SOURCE_SHA
source = UPSTREAM.read_text()
spec = importlib.util.spec_from_file_location("bbr_reference", ROOT / "bbr_reference.py")
module = importlib.util.module_from_spec(spec)
import sys
sys.modules[spec.name] = module
spec.loader.exec_module(module)
candidate_sha = hashlib.sha256((ROOT / "bbr_reference.py").read_bytes()).hexdigest()


def extract(signature):
    start = source.index(signature)
    opening = source.index("{", start)
    depth = 1
    cursor = opening + 1
    while depth:
        depth += (source[cursor] == "{") - (source[cursor] == "}")
        cursor += 1
    return source[start:cursor]


functions = [extract(s) for s in (
    "static u64 bbr_rate_bytes_per_sec(",
    "static u32 bbr_bdp(",
    "static void bbr_check_full_bw_reached(",
)]
prefix = r'''
#include <stdint.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
typedef uint64_t u64;
typedef uint32_t u32;
#define BBR_SCALE 8
#define BW_SCALE 24
#define BW_UNIT (1U << BW_SCALE)
#define USEC_PER_SEC 1000000
#define TCP_INIT_CWND 10
#define unlikely(x) (x)
static const int bbr_pacing_margin_percent = 1;
static const u32 bbr_full_bw_thresh = 320;
static const u32 bbr_full_bw_cnt = 3;
struct bbr {u32 min_rtt_us, full_bw, full_bw_cnt; bool round_start, full_bw_reached;};
struct tcp_sock {unsigned int mss_cache;};
struct sock {struct bbr bbr; struct tcp_sock tcp; u32 max_bw;};
struct rate_sample {bool is_app_limited;};
static struct bbr *inet_csk_ca(struct sock *s) {return &s->bbr;}
static struct tcp_sock *tcp_sk(struct sock *s) {return &s->tcp;}
static bool bbr_full_bw_reached(struct sock *s) {return s->bbr.full_bw_reached;}
static u32 bbr_max_bw(struct sock *s) {return s->max_bw;}
'''
main = r'''
int main(int argc, char **argv) {
    if (argc != 5) return 2;
    struct sock sk = {0};
    u32 a = strtoul(argv[2], 0, 10), b = strtoul(argv[3], 0, 10);
    int c = atoi(argv[4]);
    if (argv[1][0] == 'p') {
        sk.tcp.mss_cache = b;
        printf("%llu\n", (unsigned long long)bbr_rate_bytes_per_sec(&sk, a, c));
    } else if (argv[1][0] == 'b') {
        sk.bbr.min_rtt_us = b;
        printf("%u\n", bbr_bdp(&sk, a, c));
    } else {
        sk.bbr.full_bw = a; sk.max_bw = b; sk.bbr.round_start = true;
        struct rate_sample rs = {.is_app_limited = false};
        for (int i = 0; i < c; ++i) bbr_check_full_bw_reached(&sk, &rs);
        printf("%u %u %d\n", sk.bbr.full_bw, sk.bbr.full_bw_cnt, sk.bbr.full_bw_reached);
    }
    return 0;
}
'''
cases = []
rng = random.Random(9002)
with tempfile.TemporaryDirectory() as directory:
    path = Path(directory)
    (path / "oracle.c").write_text(prefix + "\n".join(functions) + main)
    subprocess.run(["clang", "-std=c11", "-Wall", "-Wextra", "-Werror", str(path / "oracle.c"), "-o", str(path / "oracle")], check=True)

    def c_result(kind, a, b, c):
        return subprocess.check_output([str(path / "oracle"), kind, str(a), str(b), str(c)], text=True).strip()

    for bw, mss, gain in [(1677, 1500, 739)] + [(rng.randrange(1, 1000000), rng.randrange(576, 9001), rng.choice([88, 192, 256, 320, 739])) for _ in range(80)]:
        actual = module.pacing_bytes_per_second(bw, mss, gain)
        expected = int(c_result("p", bw, mss, gain))
        assert actual == expected, (bw, mss, gain, actual, expected)
        cases.append(dict(kind="pacing", inputs=[bw, mss, gain], value=actual))
    for bw, rtt, gain in [(1677, 100000, 256), (1677, 0xffffffff, 739)] + [(rng.randrange(1, 1000000), rng.randrange(1, 1000001), rng.choice([88, 192, 256, 320, 739])) for _ in range(80)]:
        actual = module.bdp_packets(bw, rtt, gain)
        expected = int(c_result("b", bw, rtt, gain))
        assert actual == expected, (bw, rtt, gain, actual, expected)
        cases.append(dict(kind="bdp", inputs=[bw, rtt, gain], value=actual))
    for old, sample, rounds in [(10, 12, 1), (1000, 1200, 3), (1000, 1250, 3), (1000, 1249, 2)]:
        state = module.StartupDrain(full_bw=old)
        for i in range(rounds):
            state.update(sample=dict(valid=True, prior_delivered=i, is_app_limited=False), total_delivered=i+1,
                         filtered_max_bw=sample, packets_in_net_at_edt=100, drain_target=10)
        actual = [state.full_bw, state.full_bw_cnt, int(state.full_bw_reached)]
        expected = list(map(int, c_result("f", old, sample, rounds).split()))
        assert actual == expected, (old, sample, rounds, actual, expected)
        cases.append(dict(kind="full_bw", inputs=[old, sample, rounds], value=actual))

assert hashlib.sha256((ROOT / "bbr_reference.py").read_bytes()).hexdigest() == candidate_sha
result = dict(status="passed", upstream_sha256=SOURCE_SHA, candidate_sha256=candidate_sha,
              extracted_functions_sha256=hashlib.sha256("\n".join(functions).encode()).hexdigest(),
              compiler=subprocess.check_output(["clang", "--version"], text=True).splitlines()[0],
              scope="Three unchanged upstream functions with explicit socket/filter state stubs; finite nonoverflow arithmetic cases, not complete Linux BBR.",
              cases=cases)
(ROOT / "bbr-c-oracle-check.json").write_text(json.dumps(result, indent=2) + "\n")
print(f"Passed {len(cases)} compiled upstream C comparisons")
