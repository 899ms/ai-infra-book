"""Compile unchanged upstream BBR callback bodies against explicit TCP stubs."""

from pathlib import Path
import hashlib, json, subprocess, tempfile
from bbr_state import BBR, Ack
from bbr_reference import stamp_us_delta, sources

sources()
from bbr_state_scenarios import callback

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent / "congestion-controller-inputs/sources/tcp_bbr.c"
assert (
    hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    == "ba7d0706259dfef5bf455f26ac4bab65f43b9209b9cfd4f761c64c89816bdfe4"
)
for row in json.loads((ROOT / "bbr-sources.lock.json").read_text())["sources"]:
    payload = (ROOT / row["file"]).read_bytes()
    assert (
        len(payload) == row["bytes"]
        and hashlib.sha256(payload).hexdigest() == row["sha256"]
    )
tcp_header = (ROOT.parent / "congestion-controller-inputs/sources/tcp.h").read_text()
start = tcp_header.index("static inline u32 tcp_stamp_us_delta(")
opening = tcp_header.index("{", start)
end = tcp_header.index("}", opening) + 1
stamp_helper = tcp_header[start:end]
source = SOURCE.read_text()
body = source[
    source.index("#define BW_SCALE") : source.index("static size_t bbr_get_info")
]
start = source.index("__bpf_kfunc static void bbr_set_state(")
opening = source.index("{", start)
cursor = opening + 1
depth = 1
while depth:
    depth += (source[cursor] == "{") - (source[cursor] == "}")
    cursor += 1
body += "\n" + source[start:cursor]
header = (
    (ROOT / "bbr-sources/win_minmax.h")
    .read_text()
    .replace("#include <linux/types.h>", "")
)
minmax = (
    (ROOT / "bbr-sources/win_minmax.c")
    .read_text()
    .replace("#include <linux/module.h>", "")
    .replace("#include <linux/win_minmax.h>", "")
)
prefix = r"""
#include <stdint.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>
_Static_assert(sizeof(long)==8,"LP64 harness required");
typedef uint64_t u64; typedef uint32_t u32; typedef uint16_t u16; typedef uint8_t u8; typedef int32_t s32; typedef int64_t s64;
#define __bpf_kfunc
#define EXPORT_SYMBOL(x)
#define unlikely(x) (x)
#define likely(x) (x)
#define min(a,b) ((a)<(b)?(a):(b))
#define max(a,b) ((a)>(b)?(a):(b))
#define min_t(t,a,b) min((t)(a),(t)(b))
#define max_t(t,a,b) max((t)(a),(t)(b))
#define READ_ONCE(x) (x)
#undef abs
#define abs(x) (((s32)(x))<0?-((s32)(x)):((s32)(x)))
#define WARN_ONCE(...) ((void)0)
#define cmpxchg(p,a,b) (*(p)=(b))
#define do_div(n,d) ((n)/=(d))
#define div_u64(n,d) ((n)/(d))
#define div64_long(n,d) ((n)/(d))
#define USEC_PER_SEC 1000000
#define USEC_PER_MSEC 1000
#define NSEC_PER_USEC 1000
#define TCP_INIT_CWND 10
#define TCP_INFINITE_SSTHRESH 0x7fffffff
#define GSO_LEGACY_MAX_SIZE 65536
#define MAX_TCP_HEADER 256
#define SK_PACING_NONE 0
#define SK_PACING_NEEDED 1
#define TCP_CA_Open 0
#define TCP_CA_Recovery 3
#define TCP_CA_Loss 4
static u32 HZ=1000,tcp_jiffies32=0,random_draw=0;
#define msecs_to_jiffies(x) (((x)*HZ+999)/1000)
static bool before(u32 a,u32 b){return (s32)(a-b)<0;}
#define after(a,b) before(b,a)
STAMP_HELPER
static u32 get_random_u32_below(u32 bound){if(random_draw>=bound)abort();return random_draw;}
enum tcp_ca_event{CA_EVENT_TX_START};
struct rate_sample {u64 prior_mstamp;u32 prior_delivered,prior_delivered_ce; s32 delivered,delivered_ce;long interval_us;u32 snd_interval_us,rcv_interval_us;long rtt_us;int losses;u32 acked_sacked,prior_in_flight,last_end_seq;bool is_app_limited,is_retrans,is_ack_delayed;};
struct tcp_sock {u32 mss_cache,snd_cwnd,snd_cwnd_clamp,snd_ssthresh,srtt_us,delivered,lost,inflight,app_limited,min_rtt;u64 delivered_mstamp,tcp_mstamp,tcp_clock_cache,tcp_wstamp_ns;};
struct inet_connection_sock {u8 icsk_ca_state;};
struct sock {struct tcp_sock tcp;struct inet_connection_sock icsk; unsigned long sk_pacing_rate,sk_max_pacing_rate;u32 sk_pacing_shift,sk_pacing_status; unsigned char ca[512];};
static struct tcp_sock *tcp_sk(struct sock*s){return &s->tcp;}
static struct inet_connection_sock *inet_csk(struct sock*s){return &s->icsk;}
#define inet_csk_ca(s) ((void*)((s)->ca))
static u32 tcp_snd_cwnd(struct tcp_sock*t){return t->snd_cwnd;}
static void tcp_snd_cwnd_set(struct tcp_sock*t,u32 v){t->snd_cwnd=v;}
static u32 tcp_packets_in_flight(struct tcp_sock*t){return t->inflight;}
static u32 tcp_min_rtt(struct tcp_sock*t){return t->min_rtt;}
"""
FIELDS = [
    "min_rtt_us",
    "min_rtt_stamp",
    "rtt_cnt",
    "next_rtt_delivered",
    "mode",
    "full_bw",
    "full_bw_cnt",
    "full_bw_reached",
    "round_start",
    "packet_conservation",
    "prior_cwnd",
    "prev_ca_state",
    "cycle_idx",
    "cycle_mstamp",
    "probe_rtt_done_stamp",
    "probe_rtt_round_done",
    "idle_restart",
    "ack_epoch_mstamp",
    "ack_epoch_acked",
    "extra_acked_win_rtts",
    "extra_acked_win_idx",
    "has_seen_rtt",
    "pacing_gain",
    "cwnd_gain",
    "lt_bw",
    "lt_use_bw",
    "lt_is_sampling",
    "lt_last_stamp",
    "lt_last_delivered",
    "lt_last_lost",
    "lt_rtt_cnt",
]
# Build C print text normally to keep generated source reviewable.
printcode = 'printf("{");\n' + "".join(
    f'printf("\\"{f}\\":%llu,",(unsigned long long)b->{f});\n' for f in FIELDS
)
printcode += 'printf("\\"cwnd\\":%u,\\"pacing_rate\\":%lu,\\"snd_ssthresh\\":%u,\\"app_limited_until\\":%u,\\"extra0\\":%u,\\"extra1\\":%u,\\"bw_filter\\":[",s.tcp.snd_cwnd,s.sk_pacing_rate,s.tcp.snd_ssthresh,s.tcp.app_limited,b->extra_acked[0],b->extra_acked[1]);\n'
printcode += 'for(int j=0;j<3;j++)printf("%s{\\"t\\":%u,\\"v\\":%u}",j?",":"",b->bw.s[j].t,b->bw.s[j].v);printf("]}\\n");\n'
main = r"""
int main(void){struct sock s={0};struct bbr*b=inet_csk_ca(&s);char command[20];
while(scanf("%19s",command)==1){
if(!strcmp(command,"delta")){unsigned long long a,b;scanf("%llu %llu",&a,&b);printf("{\"delta\":%u}\n",tcp_stamp_us_delta(a,b));continue;}
if(!strcmp(command,"init")){memset(&s,0,sizeof(s));scanf("%u %u %u %u %u",&s.tcp.snd_cwnd,&s.tcp.min_rtt,&s.tcp.srtt_us,&HZ,&random_draw);s.tcp.mss_cache=1500;s.tcp.snd_cwnd_clamp=1000000;s.sk_max_pacing_rate=1000000000000UL;s.sk_pacing_shift=10;tcp_jiffies32=0;bbr_init(&s);}
else if(!strcmp(command,"ssthresh")){bbr_ssthresh(&s);}
else if(!strcmp(command,"loss")){bbr_set_state(&s,TCP_CA_Loss);}
else if(!strcmp(command,"undo")){bbr_undo_cwnd(&s);}
else if(!strcmp(command,"tx")){unsigned long long now;unsigned int app;scanf("%llu %u",&now,&app);s.tcp.tcp_mstamp=now;s.tcp.app_limited=app;tcp_jiffies32=now*HZ/1000000;bbr_cwnd_event(&s,CA_EVENT_TX_START);}
else {struct rate_sample r={0};unsigned long long now,edt;unsigned int state,app,delayed;
scanf("%llu %u %u %d %ld %u %d %ld %u %u %u %u %u %u %llu %u",&now,&s.tcp.delivered,&r.prior_delivered,&r.delivered,&r.interval_us,&r.acked_sacked,&r.losses,&r.rtt_us,&s.tcp.inflight,&r.prior_in_flight,&state,&app,&delayed,&s.tcp.srtt_us,&edt,&s.tcp.lost);
s.tcp.tcp_mstamp=now;s.tcp.tcp_clock_cache=now*1000;s.tcp.tcp_wstamp_ns=edt;if(r.acked_sacked)s.tcp.delivered_mstamp=now;tcp_jiffies32=now*HZ/1000000;if(s.tcp.app_limited && after(s.tcp.delivered,s.tcp.app_limited))s.tcp.app_limited=0;s.icsk.icsk_ca_state=state;r.is_app_limited=app;r.is_ack_delayed=delayed;bbr_main(&s,&r);
}
PRINT
}return 0;}
""".replace(
    "PRINT", printcode
)


def compare():
    build = ROOT / "bbr-c-state-build"
    build.mkdir(exist_ok=True)
    cfile = build / "oracle.c"
    cfile.write_text(
        prefix.replace("STAMP_HELPER", stamp_helper) + header + minmax + body + main
    )
    subprocess.run(
        [
            "clang",
            "-std=gnu11",
            "-Wno-unused-function",
            "-Wno-format",
            str(cfile),
            "-o",
            str(build / "oracle"),
        ],
        check=True,
    )
    commands = []
    expected = []
    cases = []

    def init(name, **kw):
        nonlocal state
        state = BBR(random_draws=[kw.pop("draw", 0)] * 100, **kw)
        commands.append(
            f"init {state.cwnd} {state.min_rtt_us} {kw.get('srtt_us_x8',800000)} {state.hz} {state.draws[0]}"
        )
        expected.append(state.snapshot())
        cases.append(name + ":init")

    def ack(name, a):
        state.on_ack(a)
        expected.append(state.snapshot())
        cases.append(name)
        commands.append(
            "ack "
            + " ".join(
                str(int(getattr(a, k)))
                for k in (
                    "now_us",
                    "total_delivered",
                    "prior_delivered",
                    "delivered",
                    "interval_us",
                    "acked_sacked",
                    "losses",
                    "rtt_us",
                    "inflight",
                    "prior_inflight",
                    "ca_state",
                    "app_limited",
                    "ack_delayed",
                    "srtt_us_x8",
                    "edt_ns",
                    "total_lost",
                )
            )
        )

    state = None
    init("modes")
    for i in range(1, 25):
        ack(
            "modes",
            callback(
                i, inflight=0 if i >= 5 else 100, prior_inflight=0 if i >= 5 else 100
            ),
        )
    for i, t in [(25, 11000000), (26, 11200000), (27, 11201000)]:
        ack("probe-rtt", callback(i, now_us=t, inflight=4, prior_inflight=4))
    init("recovery", cwnd=100)
    state.on_ssthresh()
    commands.append("ssthresh")
    expected.append(state.snapshot())
    cases.append("recovery:ssthresh")
    ack(
        "recovery",
        callback(1, ca_state=3, losses=2, total_lost=2, inflight=70, acked_sacked=3),
    )
    ack("restore", callback(2, ca_state=0, total_lost=2, inflight=60, acked_sacked=2))
    init("app")
    ack("app", callback(1, delivered=100, total_delivered=100, acked_sacked=100))
    for i in range(2, 15):
        ack(
            "app",
            callback(
                i,
                app_limited=True,
                total_delivered=100 + (i - 1) * 10,
                prior_delivered=100 + (i - 2) * 10,
            ),
        )
    init("aggregation", cwnd=100)
    ack("aggregation", callback(1))
    ack("aggregation", callback(2, now_us=100001, prior_delivered=0, delivered=20))
    init("hz250", hz=250, draw=1)
    for i, t in [(1, 11000000), (2, 11200000), (3, 11204000)]:
        ack("hz250", callback(i, now_us=t, inflight=4, prior_inflight=4))
    init("policer")
    for i in range(1, 57):
        lost = 1 if i < 4 else 10 if i < 8 else 20
        ack(
            "policer",
            callback(
                i,
                losses={1: 1, 4: 9, 8: 10}.get(i, 0),
                total_lost=lost,
                inflight=0,
                prior_inflight=0,
            ),
        )
    init("policer-app-reset")
    ack("policer-app-reset", callback(1, losses=1, total_lost=1))
    ack("policer-app-reset", callback(2, total_lost=1, app_limited=True))
    init("idle")
    state.on_tx_start(11000000, True)
    commands.append("tx 11000000 1")
    expected.append(state.snapshot())
    cases.append("idle:tx")
    ack("idle", callback(1, now_us=11100000))
    init("loss-undo")
    ack("loss-undo", callback(1))
    state.on_ca_loss()
    commands.append("loss")
    expected.append(state.snapshot())
    cases.append("ca-loss")
    state.on_undo_cwnd()
    commands.append("undo")
    expected.append(state.snapshot())
    cases.append("undo")
    for draw in range(7):
        init("draw-" + str(draw), draw=draw)
        for i in range(1, 6):
            ack("draw-" + str(draw), callback(i, inflight=0, prior_inflight=0))
    init("long-rtt-assignment")
    ack(
        "long-rtt-assignment",
        callback(
            1, now_us=11000000, rtt_us=(1 << 32) + 100000, inflight=4, prior_inflight=4
        ),
    )
    init("long-interval")
    ack("long-interval", callback(1, interval_us=(1 << 63) - 1))
    init("cycle-u32-delta")
    for i in range(1, 6):
        ack("cycle-u32-delta", callback(i, inflight=0, prior_inflight=0))
    cycle_stamp = state.cycle_mstamp
    ack(
        "cycle-u32-delta",
        callback(
            6,
            now_us=cycle_stamp + (1 << 32) + 1,
            rtt_us=-1,
            inflight=100,
            prior_inflight=100,
        ),
    )
    init("continuous-eight-phases")
    for i in range(1, 5):
        ack("continuous-eight-phases", callback(i))
    ack("continuous-eight-phases", callback(5, inflight=0, prior_inflight=0))
    ack("continuous-eight-phases", callback(6))
    ack("continuous-eight-phases", callback(7))
    ack("continuous-eight-phases", callback(8, inflight=0, prior_inflight=0))
    for i in range(9, 23):
        ack("continuous-eight-phases", callback(i))
    assert {
        r["state"]["cycle_idx"]
        for r in state.events
        if r["state"]["mode"] == "PROBE_BW"
    } == set(range(8))
    delta_cases = [
        (1, 2),
        ((1 << 32) + 1, 0),
        (0, (1 << 64) - 1),
        ((1 << 63), 0),
        ((1 << 63) - 1, 0),
        (100000, 0),
    ]
    for t1, t0 in delta_cases:
        commands.append(f"delta {t1} {t0}")
        expected.append({"delta": stamp_us_delta(t1, t0)})
        cases.append("stamp-delta-helper")
    output = subprocess.check_output(
        [str(build / "oracle")], input="\n".join(commands) + "\n", text=True
    )
    actual = [json.loads(line) for line in output.splitlines()]
    assert (
        len(actual) == len(expected) == len(commands)
    ), "Callback output count mismatch"
    diffs = []
    rename = {"prev_ca_state": "prev_ca"}
    modes = ["STARTUP", "DRAIN", "PROBE_BW", "PROBE_RTT"]
    for i, (a, p) in enumerate(zip(actual, expected)):
        for k, v in a.items():
            want = (
                p["extra_acked"][int(k[-1])]
                if k in ("extra0", "extra1")
                else p[rename.get(k, k)]
            )
            if k == "mode":
                v = modes[v]
            if v != want:
                diffs.append(dict(event=i, case=cases[i], field=k, c=v, python=want))
    result = dict(
        status="passed" if not diffs else "failed",
        callbacks=len(actual) - len(delta_cases),
        helper_checks=len(delta_cases),
        differences=diffs,
        source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        candidate_sha256=hashlib.sha256(
            (ROOT / "bbr_state.py").read_bytes()
        ).hexdigest(),
    )
    result.update(
        fields_per_callback=len(actual[0]),
        harness_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        generated_c_sha256=hashlib.sha256(cfile.read_bytes()).hexdigest(),
        cases=cases,
        scope="Unmodified fixed upstream BBR/minmax function bodies with LP64 TCP/clock/ABI primitive stubs; not networking or a real kernel.",
    )
    (ROOT / "bbr-state-c-trace.json").write_text(
        json.dumps(dict(commands=commands, c=actual, python=expected), indent=2) + "\n"
    )
    (build / "oracle").unlink()
    (ROOT / "bbr-state-c-check.json").write_text(json.dumps(result, indent=2) + "\n")
    print(
        json.dumps(
            {
                k: result[k]
                for k in (
                    "status",
                    "callbacks",
                    "fields_per_callback",
                    "differences",
                    "candidate_sha256",
                )
            }
        )
    )
    assert not diffs


if __name__ == "__main__":
    compare()
