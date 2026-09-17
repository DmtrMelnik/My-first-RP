#!/usr/bin/env python3
"""Stdlib unittest coverage for the trace problem registry."""

from __future__ import annotations

import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import build_problem_registry as reg  # noqa: E402

FIXTURES = Path(__file__).resolve().parent / "fixtures"
COMPLETE = FIXTURES / "complete-analysis.md"
MALFORMED = FIXTURES / "malformed-analysis.md"


class MarkdownTableTests(unittest.TestCase):
    def test_ragged_row_is_padded_not_crashed(self) -> None:
        text = (
            "| A | B | C |\n"
            "|---|---|---|\n"
            "| 1 | 2 |\n"
            "| 3 | 4 | 5 | extra |\n"
        )
        tables = list(reg.iter_markdown_tables(text))
        self.assertEqual(len(tables), 1)
        headers, rows = tables[0]
        self.assertEqual(headers, ["a", "b", "c"])
        self.assertEqual(rows[0]["c"], "")
        self.assertIn("extra", rows[1]["c"])


class RegistryFixtureTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmpdir = tempfile.TemporaryDirectory()
        self.out = Path(self.tmpdir.name) / "out"
        self.summary = reg.run(FIXTURES, self.out, include_info=False)
        self.findings = json.loads((self.out / "problems.json").read_text(encoding="utf-8"))
        self.by_q = {}
        for item in self.findings:
            self.by_q.setdefault(item["q_code"], []).append(item)

    def tearDown(self) -> None:
        self.tmpdir.cleanup()

    def _from_complete(self, q_code: str):
        return [
            item
            for item in self.by_q.get(q_code, [])
            if item["report_file"].endswith("complete-analysis.md")
        ]

    def test_metadata_fields_copied_onto_findings(self) -> None:
        q1 = self._from_complete("Q1")
        self.assertTrue(q1)
        sample = q1[0]
        self.assertEqual(sample["trace_file"], "demo-trace__android__1.0.0__user-1___.pbf.gz")
        self.assertEqual(sample["user_id"], "user-1")
        self.assertEqual(sample["vehicle"], "DEMOCAR01")
        self.assertEqual(sample["project"], "com.mapbox.porsche")
        self.assertEqual(sample["platform"], "android")
        self.assertEqual(sample["nav_native"], "324.26.0-demo")
        self.assertEqual(sample["report_file"], "complete-analysis.md")
        self.assertEqual(sample["metadata"].get("session_id"), "session-9")

    def test_q1_instability_and_rows(self) -> None:
        q1 = self._from_complete("Q1")
        types = {item["problem_type"] for item in q1}
        self.assertIn("instability_cluster", types)
        self.assertIn("off_route", types)
        self.assertIn("route_change", types)
        self.assertIn("net_eta_impact", types)
        cluster = next(item for item in q1 if item["problem_type"] == "instability_cluster")
        self.assertEqual(cluster["timestamp_utc"], "2026-09-09T04:55:49Z")
        off = next(item for item in q1 if item["problem_type"] == "off_route")
        self.assertEqual(off["metadata"].get("reason"), "Reroute")
        self.assertIn("Q4 GPS divergence", off["metadata"].get("context", ""))

    def test_q3_actionable_congestion_not_slowdowns(self) -> None:
        q3 = self._from_complete("Q3")
        types = {item["problem_type"] for item in q3}
        self.assertEqual(types, {"congestion_signal"})
        self.assertEqual(len(q3), 2)
        coords = [(item["lat"], item["lon"]) for item in q3]
        self.assertIn((48.88913, 9.18984), coords)
        self.assertTrue(all(item["metadata"].get("signal") for item in q3))

    def test_q4_divergence_table_and_summaries(self) -> None:
        q4 = self._from_complete("Q4")
        types = {item["problem_type"] for item in q4}
        self.assertIn("gps_divergence", types)
        self.assertIn("navigator_fallback", types)
        self.assertIn("map_matcher_teleport", types)
        divergences = [item for item in q4 if item["problem_type"] == "gps_divergence"]
        self.assertEqual(len(divergences), 2)
        teleport = next(item for item in q4 if item["problem_type"] == "map_matcher_teleport")
        self.assertEqual(teleport["metadata"].get("teleport_count"), 4)
        fallback = next(item for item in q4 if item["problem_type"] == "navigator_fallback")
        self.assertEqual(fallback["metadata"].get("fallback_count"), 1)

    def test_q10_incident_table_and_closure_state(self) -> None:
        q10 = self._from_complete("Q10")
        types = {item["problem_type"] for item in q10}
        self.assertIn("route_incident", types)
        self.assertIn("road_closure", types)
        self.assertIn("non_routable_incident", types)
        incidents = [item for item in q10 if item["problem_type"] == "route_incident"]
        self.assertEqual(len(incidents), 2)
        first = next(item for item in incidents if "A 81" in item["summary"])
        self.assertAlmostEqual(first["lat"], 48.80787)
        self.assertAlmostEqual(first["lon"], 9.04640)
        closure = next(item for item in q10 if item["problem_type"] == "road_closure")
        self.assertIn("closed road", closure["summary"].lower())
        self.assertEqual(closure["severity"], "high")

    def test_q7_degraded_only_by_default(self) -> None:
        q7 = self._from_complete("Q7")
        self.assertEqual(len(q7), 1)
        self.assertEqual(q7[0]["problem_type"], "tunnel_degraded")
        self.assertEqual(q7[0]["severity"], "high")

    def test_outputs_written(self) -> None:
        for name in (
            "problems-report.md",
            "problems.csv",
            "problems.json",
            "problems.geojson",
            "run-summary.json",
        ):
            path = self.out / name
            self.assertTrue(path.is_file(), name)
            self.assertGreater(path.stat().st_size, 0, name)

        report = (self.out / "problems-report.md").read_text(encoding="utf-8")
        self.assertIn("## Run metadata", report)
        self.assertIn("### By Q", report)
        self.assertIn("### By severity", report)
        self.assertIn("### By category", report)
        self.assertIn("Q6, Q8, and Q9 do not exist", report)
        self.assertIn("complete-analysis.md", report)

        with (self.out / "problems.csv").open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            self.assertIn("metadata_json", reader.fieldnames or [])
            rows = list(reader)
        self.assertEqual(len(rows), len(self.findings))
        json.loads(rows[0]["metadata_json"])

        geo = json.loads((self.out / "problems.geojson").read_text(encoding="utf-8"))
        self.assertEqual(geo["type"], "FeatureCollection")
        self.assertTrue(geo["features"])
        for feat in geo["features"]:
            lon, lat = feat["geometry"]["coordinates"]
            self.assertTrue(reg.valid_lat_lon(lat, lon))

        summary = json.loads((self.out / "run-summary.json").read_text(encoding="utf-8"))
        self.assertEqual(summary["files_scanned"], 2)
        self.assertEqual(summary["findings_count"], len(self.findings))
        self.assertEqual(summary["unsupported_q_codes"], ["Q6", "Q8", "Q9"])
        self.assertGreaterEqual(summary["files_with_errors"], 1)

    def test_q6_q8_q9_not_emitted(self) -> None:
        codes = {item["q_code"] for item in self.findings}
        self.assertTrue({"Q6", "Q8", "Q9"}.isdisjoint(codes))

    def test_malformed_input_does_not_crash(self) -> None:
        malformed_findings = [
            item for item in self.findings if "malformed" in item["report_file"]
        ]
        self.assertTrue(
            any("malformed" in err.get("file", "") for err in self.summary["parse_errors"])
        )
        q4 = [item for item in malformed_findings if item["q_code"] == "Q4"]
        self.assertTrue(any(item["problem_type"] == "map_matcher_teleport" for item in q4))
        q3 = [item for item in malformed_findings if item["q_code"] == "Q3"]
        self.assertTrue(q3)
        q10 = [item for item in malformed_findings if item["q_code"] == "Q10"]
        self.assertTrue(q10)
        self.assertIsNone(q10[0]["lat"])

    def test_include_info_adds_informational_rows(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "info"
            summary = reg.run(FIXTURES, out, include_info=True)
            findings = json.loads((out / "problems.json").read_text(encoding="utf-8"))
        complete = [
            item
            for item in findings
            if item["report_file"].endswith("complete-analysis.md")
        ]
        q3_types = {item["problem_type"] for item in complete if item["q_code"] == "Q3"}
        q7 = [item for item in complete if item["q_code"] == "Q7"]
        h1 = [item for item in complete if item["q_code"] == "H1"]
        self.assertIn("slowdown", q3_types)
        self.assertEqual(len(q7), 2)
        self.assertGreaterEqual(len(h1), 2)
        self.assertGreater(summary["findings_count"], self.summary["findings_count"])

    def test_lane_and_h1_and_feedback_parsed(self) -> None:
        lane = self._from_complete("Q_lane")
        self.assertEqual(len(lane), 1)
        self.assertEqual(lane[0]["problem_type"], "G:lanes:wrong")
        self.assertEqual(lane[0]["confidence"], "high")
        self.assertAlmostEqual(lane[0]["lat"], 48.83255)
        feedback = self._from_complete("Q_feedback")
        self.assertEqual(len(feedback), 1)
        self.assertAlmostEqual(feedback[0]["lat"], 48.89)
        h1 = self._from_complete("H1")
        self.assertEqual(len(h1), 1)
        self.assertIn("genuine", h1[0]["summary"])
        ev = self._from_complete("Q_EV")
        types = {item["problem_type"] for item in ev}
        self.assertIn("soc_prediction_error", types)
        self.assertIn("soc_arrival_error", types)
        self.assertIn("charging_soc_mismatch", types)


if __name__ == "__main__":
    unittest.main()
