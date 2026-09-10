"""Figure 12-5 first panel: shared airtime and finite media outcomes."""
from copy import deepcopy
from fractions import Fraction as F
import json
from pathlib import Path

from .paths import PROJECT
from .media_feedback_plot import digest, rows

DIRECTORY = PROJECT / "figures/shared-airtime"
FULL = ("image-baseline", "mixed-fifo-immediate", "mixed-fifo-aggregate",
        "mixed-priority-immediate", "mixed-priority-aggregate")
SCAN = tuple(f"media-{size}B-ack{n}" for size in (320, 640, 960) for n in (1, 2, 4))
ARTIFACTS = ("figure.png", "figure.svg", "data.json")


def input_paths():
    return sorted({Path(__file__), PROJECT / "src/infra_calc/media_feedback_plot.py",
                   PROJECT / "configs/sources.lock.json", PROJECT / "scenarios/book.json",
                   PROJECT / "configs/shared-airtime-provenance.json",
                   PROJECT / "scenarios/shared-airtime-profiles.json",
                   *(PROJECT / "sources/shared-airtime").glob("*"),
                   *(PROJECT / "src/infra_calc/transport").glob("*.py"),
                   *(PROJECT / f"results/shared-airtime-{name}.json" for name in FULL),
                   *(PROJECT / f"results/media-feedback-{name}.json" for name in FULL),
                   *(PROJECT / f"results/shared-airtime-scan-{name}.json" for name in SCAN)})


def verify():
    manifest = json.loads((DIRECTORY / "manifest.json").read_text())
    for key, paths in {"inputs": input_paths(), "artifacts": [DIRECTORY / n for n in ARTIFACTS]}.items():
        if manifest.get(key) != rows(paths):
            raise ValueError("Stale or incomplete shared-airtime figure " + key)
    return {"verified_figures": 2}


def compact(result):
    businesses = {b["kind"]: b for b in result["businesses"]}
    audio = businesses.get("tts")
    return {
        "image_complete": businesses["image"]["complete_at"],
        "played_blocks": None if audio is None else sum(b["play_end"] is not None for b in audio["blocks"]),
        "missing_audio_seconds": None if audio is None else audio["missing_audio_seconds"],
        "screenshot_usable": businesses.get("screenshot", {}).get("usable"),
        "wan_serialized_ip_bytes": result["summary"].get("wan_serialized_ip_bytes_by_horizon"),
        "reserved_seconds": result.get("wireless_summary", {}).get("observed_reserved_seconds"),
        "transport_ack_packets": sum(t["kind"] == "ack" for t in result["transmissions"]),
    }


def extract():
    full, scan = [], []
    for name in FULL:
        result = json.loads((PROJECT / f"results/shared-airtime-{name}.json").read_text())
        baseline = json.loads((PROJECT / f"results/media-feedback-{name}.json").read_text())
        paired = deepcopy(result["inputs"])
        paired["network"].pop("wireless_access")
        if paired != baseline["inputs"]:
            raise ValueError("Unpaired wireless baseline: " + name)
        full.append({"name": name, "wireless": compact(result), "wan_only": compact(baseline)})
    scan_reference = None
    for name in SCAN:
        result = json.loads((PROJECT / f"results/shared-airtime-scan-{name}.json").read_text())
        size = int(name.split("-")[1][:-1])
        threshold = int(name.rsplit("ack", 1)[1])
        paired = deepcopy(result["inputs"])
        if paired["network"]["ack_policy"].pop("every") != threshold:
            raise ValueError("Scan ACK threshold does not match its label")
        app = paired["application"]
        app.pop("id")
        payload_delta = 0
        audio_messages = 0
        for message in app["messages"]:
            if message["transport"] == "datagram":
                if message["sender"] != "server" or message["bytes"] != size:
                    raise ValueError("Unexpected scan audio payload")
                payload_delta += size - 320
                audio_messages += 1
                message["bytes"] = 320
                message["packetization"]["final_fragment_bytes"] = 320
        if audio_messages != 8:
            raise ValueError("Expected eight scan audio messages")
        app["accounting"]["application_bytes"] -= payload_delta
        app["accounting"]["application_bytes_by_direction"]["server_to_client"] -= payload_delta
        if scan_reference is None:
            scan_reference = paired
        if paired != scan_reference:
            raise ValueError("Scan varies fields other than audio bytes and ACK threshold")
        scan.append({"name": name, **compact(result)})
    return {"full": full, "scan": scan,
            "scope": "Declared global FIFO legacy OFDM54/6 Mbps; separate WAN20/100 Mbps, 50 ms each way. No random DCF, aggregation, encryption or measured Wi-Fi. Scan uses a separate 300KB/50KB background and payload sensitivity, not equal-quality codecs."}


def render():
    from .reproduce import verify_results
    verify_results(include_figures=False)
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    data = extract()
    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    ax = axes[0, 0]
    labels = ["Image only", "FIFO / immediate", "FIFO / aggregate", "Priority / immediate", "Priority / aggregate"]
    for i, row in enumerate(data["full"]):
        ax.barh(i - .17, float(F(row["wan_only"]["image_complete"])), height=.32, color="#899aa8", label="WAN only" if i == 0 else None)
        t = float(F(row["wireless"]["image_complete"]))
        ax.barh(i + .17, t, height=.32, color="#387c98", label="WAN + shared radio" if i == 0 else None)
        ax.text(t + .08, i + .17, f"{t:.3f}", va="center", fontsize=8)
    ax.set_yticks(range(5), labels); ax.set_ylim(4.6, -1.4); ax.set_xlim(0, 18)
    ax.set_xlabel("Full image delivered (s)"); ax.legend(fontsize=8, loc="upper left", ncol=2)
    ax.set_title("A. Full 30 MB / 5 MB workload", loc="left")
    ax = axes[0, 1]
    for i, row in enumerate(data["full"][1:]):
        radio = row["wireless"]
        value = float(F(radio["reserved_seconds"]))
        ax.barh(i, value, color="#387c98")
        ax.text(value + .1, i, f'{value:.3f} s; audio {radio["played_blocks"]}/8', va="center", fontsize=8)
    ax.set_yticks(range(4), labels[1:]); ax.invert_yaxis(); ax.set_xlim(0, 18)
    ax.set_xlabel("Accumulated radio reservation (s)")
    ax.set_title("B. Resource use and played audio are separate", loc="left")
    colors = ("#387c98", "#b87735", "#65916b")
    for size, color in zip((320, 640, 960), colors):
        points = [r for r in data["scan"] if r["name"].startswith(f"media-{size}B-")]
        for ax, key, scale in ((axes[1, 0], "reserved_seconds", 1000), (axes[1, 1], "image_complete", 1)):
            ax.plot([1, 2, 4], [float(F(p[key])) * scale for p in points], "o-", color=color, label=f"{size} B / audio block", alpha=.8)
            ax.set_xticks([1, 2, 4]); ax.set_xlabel("Transport ACK packet threshold (10 ms timer)")
    axes[1, 0].set_ylabel("Radio reservation (ms)"); axes[1, 0].legend(fontsize=8)
    axes[1, 0].set_title("C. Separate 300 KB / 50 KB background scan", loc="left")
    axes[1, 1].set_ylabel("Full image delivered (s)")
    axes[1, 1].set_title("D. Less ACK service can still delay completion", loc="left")
    coincident = all(len({r["image_complete"] for r in data["scan"] if r["name"].endswith(f"ack{n}")}) == 1 for n in (1, 2, 4))
    played = sum(r["played_blocks"] for r in data["scan"])
    note = ("Size curves coincide; " if coincident else "") + f"scan audio: {played}/72 blocks played"
    axes[1, 1].text(.03, .94, note, transform=axes[1, 1].transAxes, va="top", fontsize=8)
    for ax in axes.flat:
        ax.grid(alpha=.18); ax.set_axisbelow(True)
    fig.suptitle("Shared radio, two ACK layers and media deadlines", fontsize=14)
    usable = sum(bool(r["wireless"]["screenshot_usable"]) for r in data["full"][1:])
    fig.text(.04, .025, f"Declared OFDM54/6 Mbps; no random contention or aggregation. Usable full mixed screenshot actions: {usable}/4.\nRadio service overlaps WAN and may continue after image delivery. Scan payload sizes are not equal-quality codec comparisons.", fontsize=9)
    fig.tight_layout(rect=(0, .07, 1, .96))
    DIRECTORY.mkdir(parents=True, exist_ok=True)
    for suffix in ("png", "svg"):
        fig.savefig(DIRECTORY / f"figure.{suffix}", dpi=160)
    plt.close(fig)
    (DIRECTORY / "data.json").write_text(json.dumps(data, indent=2) + "\n")
    (DIRECTORY / "manifest.json").write_text(json.dumps({"inputs": rows(input_paths()), "artifacts": rows([DIRECTORY / n for n in ARTIFACTS])}, indent=2) + "\n")
    return verify()
