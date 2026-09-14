"""Public CLI errors for JSON keyword inputs, without hiding calculator bugs."""
from contextlib import redirect_stderr, redirect_stdout
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT / "src"))
from infra_calc import cli
from infra_calc.report import markdown
from infra_calc.topics import speculative_sampling


class CliJsonInputsTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.directory = Path(temporary.name)
        self.inputs = self.directory / "input.json"

    def write_inputs(self, payload):
        self.inputs.write_text(json.dumps(payload))

    def invoke(self, *arguments):
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            cli.main(list(arguments))
        return stdout.getvalue(), stderr.getvalue()

    def assert_usage_error(self, arguments, *messages):
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            with self.assertRaises(SystemExit) as raised:
                cli.main(arguments)
        self.assertEqual(raised.exception.code, 2)
        self.assertEqual(stdout.getvalue(), "")
        self.assertNotIn("Traceback", stderr.getvalue())
        for message in messages:
            self.assertIn(message, stderr.getvalue())

    def test_process_reports_invalid_inputs_as_usage_errors(self):
        for payload, message in (({"targte": ["1"]}, "targte"),
                                 ([], "JSON object"), (None, "JSON object")):
            with self.subTest(payload=payload):
                self.write_inputs(payload)
                process = subprocess.run(
                    [sys.executable, str(PROJECT / "calc.py"),
                     "speculative-sampling", "--inputs", str(self.inputs)],
                    cwd=self.directory, capture_output=True, text=True, timeout=30,
                )
                self.assertEqual(process.returncode, 2, process.stderr)
                self.assertEqual(process.stdout, "")
                self.assertIn(message, process.stderr)
                self.assertIn(str(self.inputs), process.stderr)
                self.assertNotIn("Traceback", process.stderr)

    def test_rejects_every_non_object_json_type(self):
        for payload in ([], None, "text", 42, 1.5, True, False):
            with self.subTest(payload=payload):
                self.write_inputs(payload)
                self.assert_usage_error(
                    ["speculative-sampling", "--inputs", str(self.inputs)],
                    "JSON object", str(self.inputs),
                )

    def test_rejects_unknown_fields_before_calculating(self):
        def must_not_run(target=None, draft=None):
            self.fail("Invalid keyword inputs reached the calculator")

        self.write_inputs({"targte": ["1"]})
        with patch.object(speculative_sampling, "calculate", new=must_not_run):
            self.assert_usage_error(
                ["speculative-sampling", "--inputs", str(self.inputs)],
                "targte", str(self.inputs),
            )

    def test_other_calculators_and_dynamic_commands_validate_inputs(self):
        commands = ("online-softmax", "kv-pages", "flux-vae-decode", "architecture-variants")
        for command in commands:
            for payload, message in ((None, "JSON object"), ({"unknown_field": 1}, "unknown_field")):
                with self.subTest(command=command, payload=payload):
                    self.write_inputs(payload)
                    self.assert_usage_error(
                        [command, "--inputs", str(self.inputs)], message, str(self.inputs),
                    )

    def test_default_and_empty_object_preserve_default_calculation(self):
        expected = speculative_sampling.calculate()
        default, stderr = self.invoke("speculative-sampling")
        self.assertEqual(stderr, "")
        self.assertEqual(json.loads(default), expected)
        self.write_inputs({})
        explicit, stderr = self.invoke("speculative-sampling", "--inputs", str(self.inputs))
        self.assertEqual(stderr, "")
        self.assertEqual(explicit, default)

    def test_custom_inputs_preserve_json_and_markdown_results(self):
        payload = {"target": ["3/4", "1/4"], "draft": ["1/4", "3/4"]}
        self.write_inputs(payload)
        arguments = ["speculative-sampling", "--inputs", str(self.inputs)]
        expected = speculative_sampling.calculate(**payload)
        output, stderr = self.invoke(*arguments)
        self.assertEqual(stderr, "")
        result = json.loads(output)
        self.assertEqual(result, expected)
        self.assertEqual([row["output_exact"] for row in result["sampling_tokens"]], ["3/4", "1/4"])
        output, stderr = self.invoke(*arguments, "--format", "md")
        self.assertEqual(stderr, "")
        self.assertEqual(output, markdown(expected))

    def test_nested_null_values_remain_valid_masks(self):
        self.write_inputs({"scores": [None, None], "values": [[1], [2]], "block_sizes": [0, 1, 1]})
        output, stderr = self.invoke("online-softmax", "--inputs", str(self.inputs))
        self.assertEqual(stderr, "")
        summary = json.loads(output)["summary"]
        self.assertIsNone(summary["direct_output"])
        self.assertEqual(summary["nonempty_blocks"], 0)

    def test_domain_validation_still_reports_usage_errors(self):
        self.write_inputs({"target": ["1/2"], "draft": ["1"]})
        self.assert_usage_error(
            ["speculative-sampling", "--inputs", str(self.inputs)], "sum exactly to 1",
        )

    def test_invalid_json_and_missing_files_remain_usage_errors(self):
        for contents in ("", "{"):
            with self.subTest(contents=contents):
                self.inputs.write_text(contents)
                self.assert_usage_error(["speculative-sampling", "--inputs", str(self.inputs)])
        self.inputs.unlink()
        self.assert_usage_error(
            ["speculative-sampling", "--inputs", str(self.inputs)], str(self.inputs),
        )

    def test_valid_output_files_match_stdout_rendering(self):
        self.write_inputs({"target": ["1"], "draft": ["1"]})
        for fmt in ("json", "md"):
            with self.subTest(format=fmt):
                arguments = ["speculative-sampling", "--inputs", str(self.inputs), "--format", fmt]
                expected, stderr = self.invoke(*arguments)
                self.assertEqual(stderr, "")
                self.assertTrue(expected)
                output = self.directory / "reports" / f"result.{fmt}"
                stdout, stderr = self.invoke(*arguments, "--output", str(output))
                self.assertEqual((stdout, stderr), ("", ""))
                self.assertEqual(output.read_text(), expected)

    def test_input_errors_do_not_create_or_overwrite_output_files(self):
        new_output = self.directory / "new-directory" / "result.json"
        existing_output = self.directory / "existing.json"
        existing_output.write_text("keep this result")
        for payload in (None, {"targte": ["1"]}):
            for output in (new_output, existing_output):
                with self.subTest(payload=payload, output=output.name):
                    self.write_inputs(payload)
                    self.assert_usage_error([
                        "speculative-sampling", "--inputs", str(self.inputs), "--output", str(output),
                    ])
                    self.assertFalse(new_output.parent.exists())
                    self.assertEqual(existing_output.read_text(), "keep this result")

    def test_calculator_type_errors_propagate_without_reclassification(self):
        error = TypeError("calculator implementation failed")

        def broken_calculation(target=None, draft=None):
            raise error

        self.write_inputs({"target": ["1"]})
        with patch.object(speculative_sampling, "calculate", new=broken_calculation):
            with self.assertRaises(TypeError) as raised:
                self.invoke("speculative-sampling", "--inputs", str(self.inputs))
        self.assertIs(raised.exception, error)
