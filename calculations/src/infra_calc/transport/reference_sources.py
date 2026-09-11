"""Pinned official sources shared by transport state and QUIC adapters."""

from ..sources import records, read_source

SOURCE_FILES = {
    "shared_airtime": (
        "sources/shared-airtime/wifi-phy.cc",
        "sources/shared-airtime/ofdm-phy.cc",
        "sources/shared-airtime/wifi-mac-header.cc",
        "sources/shared-airtime/wifi-mac-trailer.cc",
        "sources/shared-airtime/llc-snap-header.cc",
        "sources/shared-airtime/frame-exchange-manager.cc",
        "sources/shared-airtime/channel-access-manager.cc",
        "sources/shared-airtime/wifi-remote-station-manager.cc",
        "sources/shared-airtime/ns3-release-commit.json",
        "sources/shared-airtime/wifi-mac-trailer.h",
        "sources/shared-airtime/llc-snap-header.h",
        "sources/shared-airtime/tack-sigcomm2020.pdf",
        "sources/shared-airtime/LICENSE.ns3",
        "sources/shared-airtime/wifi-design-3.44.md",
    ),
    "cubic": (
        "sources/congestion-controllers/rfc9438.txt",
        "sources/connection-window/rfc5681.txt",
    ),
    "hystart": (
        "sources/congestion-controllers/rfc9406.txt",
        "sources/congestion-controllers/errata-check.md",
    ),
    "bbr": (
        "sources/congestion-controllers/tcp_bbr.c",
        "sources/congestion-controllers/tcp_rate.c",
        "sources/congestion-controllers/tcp.h",
        "sources/congestion-controllers/win_minmax.c",
        "sources/congestion-controllers/win_minmax.h",
    ),
    "quic": (
        "sources/protocol-rfc/rfc9000.txt",
        "sources/protocol-rfc/rfc9002.txt",
        "sources/protocol-rfc/rfc9002-errata7539.md",
    ),
}


def reference_sources(group):
    """Verify each exact source through the public source lock before returning it."""
    selected = SOURCE_FILES[group]
    available = {row["file"]: row for row in records()}
    result = []
    for path in selected:
        read_source(path)
        row = available[path]
        result.append(
            {key: row[key] for key in ("file", "url", "revision", "bytes", "sha256")}
        )
    return result
