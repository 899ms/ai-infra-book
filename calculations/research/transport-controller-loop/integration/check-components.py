"""Migration-only structural and finite payload parity, no full network run."""

from pathlib import Path
import ast
import hashlib
import importlib
import importlib.util
import json
import sys

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "research/transport-controller-loop"))
sys.path.insert(0, str(ROOT / "research/congestion-controllers"))


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def functions(path, module):
    tree = ast.parse(path.read_text())
    found = {}

    def visit(nodes, prefix=""):
        for node in nodes:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if not prefix and node.name in (
                    "sources",
                    "verify_sources",
                    "main",
                    "pinned_module",
                ):
                    continue
                if (
                    module == "bbr_adapter"
                    and prefix == "BbrAdapter."
                    and node.name == "__init__"
                ):
                    # Source verification wrapper replaced before unchanged config parse.
                    index = next(
                        i
                        for i, n in enumerate(node.body)
                        if isinstance(n, ast.Assign)
                        and any(
                            isinstance(t, ast.Name) and t.id == "config"
                            for t in n.targets
                        )
                    )
                    node.body = node.body[index:]
                if module == "persistent_congestion" and node.name == "evaluate":
                    # Docstring and one source-verification statement precede math.
                    node.body = node.body[2:]
                found[prefix + node.name] = ast.dump(node, include_attributes=False)
            elif isinstance(node, ast.ClassDef):
                visit(node.body, prefix + node.name + ".")
                found[prefix + node.name + ".fields"] = ast.dump(
                    ast.Module(
                        body=[
                            n for n in node.body if not isinstance(n, ast.FunctionDef)
                        ],
                        type_ignores=[],
                    ),
                    include_attributes=False,
                )

    visit(tree.body)
    constants = [
        n
        for n in tree.body
        if isinstance(n, (ast.Assign, ast.AnnAssign))
        and not any(
            isinstance(t, ast.Name)
            and t.id in {"ROOT", "CONTROLLERS", "RFC", "RFC_SHA", "CUBIC", "HYSTART"}
            for t in getattr(n, "targets", [getattr(n, "target", None)])
        )
    ]
    found["module.constants"] = ast.dump(ast.Module(body=constants, type_ignores=[]))
    return found


def clean(value):
    if isinstance(value, dict):
        return {k: clean(v) for k, v in value.items() if k != "reference_sources"}
    if isinstance(value, list):
        return [clean(v) for v in value]
    return value


def run():
    manifest = json.loads((HERE / "migration-manifest.json").read_text())
    structural = []
    for row in manifest["modules"]:
        src, dst = ROOT / row["research_file"], ROOT / row["public_file"]
        assert hashlib.sha256(src.read_bytes()).hexdigest() == row["research_sha256"]
        assert hashlib.sha256(dst.read_bytes()).hexdigest() == row["public_sha256"]
        old, new = functions(src, dst.stem), functions(dst, dst.stem)
        assert old == new, (dst.stem, [k for k in old if old.get(k) != new.get(k)])
        structural.append(
            dict(module=dst.stem, identical_function_or_constant_blocks=len(old))
        )
    parity = []
    for name, path in (
        ("cubic", "congestion-controllers/cubic.py"),
        ("hystart", "hystart-plus-plus/calculate.py"),
    ):
        old = load(ROOT / "research" / path, "migration_old_" + name)
        new = importlib.import_module("infra_calc.transport." + name)
        scenarios = old.scenarios()
        for key, inputs in scenarios.items():
            assert clean(old.calculate(inputs)) == clean(new.calculate(inputs)), (
                name,
                key,
            )
        parity.append(dict(module=name, scenarios=len(scenarios)))
    path = ROOT / "research/transport-controller-loop/check-bbr-adapter.py"
    old_check = load(path, "migration_bbr_hooks")
    expected = old_check.run()
    from infra_calc.transport.bbr_adapter import BbrAdapter

    old_check.BbrAdapter = BbrAdapter
    assert expected == old_check.run()
    parity.append(
        dict(module="bbr_adapter", checks="all local hook returned payloads identical")
    )
    from infra_calc.transport.reference_sources import reference_sources

    sources = {
        group: reference_sources(group) for group in ("quic", "cubic", "hystart", "bbr")
    }
    return dict(
        status="passed",
        structural=structural,
        payload_parity=parity,
        source_groups=sources,
        scope="Shared component migration; no network or full public reproduce claim",
        checker_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    )


if __name__ == "__main__":
    result = run()
    (HERE / "component-check.json").write_text(json.dumps(result, indent=2) + "\n")
    print(
        json.dumps(
            {
                "status": result["status"],
                "structural_modules": len(result["structural"]),
                "payload_parity": result["payload_parity"],
            }
        )
    )
