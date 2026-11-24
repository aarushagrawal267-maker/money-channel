"""Every video spec: its number checks pass, the committed JSON is current, and the renderers accept it."""
import glob, json, os, subprocess, sys

import pytest

from conftest import ROOT, SPECS
import render as R
import render_long as RL
from upload import build_body, MAX_TITLE

SPEC_PY = sorted(glob.glob(os.path.join(SPECS, "*.py")))
SPEC_JSON = sorted(glob.glob(os.path.join(SPECS, "*.json")))
IDS = [os.path.basename(p)[:-3] for p in SPEC_PY]


def test_found_specs():
    assert len(SPEC_PY) >= 30
    assert {os.path.basename(p)[:-5] for p in SPEC_JSON} == set(IDS), "every spec .py has a committed .json and vice versa"


@pytest.mark.parametrize("path", SPEC_PY, ids=IDS)
def test_spec_checks_pass_and_json_is_current(path, tmp_path):
    """Run the spec in a scratch copy: its asserts must pass and it must write the same JSON that is committed."""
    sid = os.path.basename(path)[:-3]
    scratch = tmp_path / os.path.basename(path)
    scratch.write_text(open(path).read())
    r = subprocess.run([sys.executable, scratch.name], cwd=tmp_path, capture_output=True, text=True, timeout=120)
    assert r.returncode == 0, f"{sid} number checks failed:\n{r.stderr[-2000:]}"
    written = tmp_path / (sid + ".json")
    assert written.exists(), f"{sid}.py did not write {sid}.json next to itself"
    committed = json.load(open(os.path.join(SPECS, sid + ".json")))
    assert json.loads(written.read_text()) == committed, f"{sid}.json is stale: run `cd pipeline/specs && python3 {sid}.py`"


@pytest.mark.parametrize("path", SPEC_JSON, ids=[os.path.basename(p)[:-5] for p in SPEC_JSON])
def test_spec_shape(path):
    spec = json.load(open(path))
    sid = os.path.basename(path)[:-5]
    assert spec["id"] == sid
    assert spec.get("currency", "usd") in ("usd", "inr")
    assert spec["title"].strip() and len(spec["title"]) <= MAX_TITLE
    visuals = RL.VISUALS if sid.startswith("L") else R.VISUALS
    assert spec["scenes"], "no scenes"
    for i, sc in enumerate(spec["scenes"]):
        assert sc["say"].strip(), f"scene {i} has no narration"
        assert sc["visual"]["type"] in visuals, f"scene {i}: unknown visual type {sc['visual']['type']!r}"
    # the upload metadata must fit YouTube's limits (build_body exits if not)
    body = build_body(spec, "0:00 Intro\n1:00 Part one" if sid.startswith("L") else None)
    assert len(body["snippet"]["title"]) <= MAX_TITLE


@pytest.mark.parametrize("sid", ["018_start_early_us", "013_minimum_due_trap", "L001_costco"])
def test_preview_draws_every_scene(sid):
    """The layout preview draws every scene of a Short (USD + INR) and a long video without errors."""
    import preview
    spec = json.load(open(os.path.join(SPECS, sid + ".json")))
    frames = list(preview.frames(spec, 3.0))
    assert len(frames) == len(spec["scenes"])
    w, h = frames[0].size
    assert (w, h) == ((RL.W, RL.H) if sid.startswith("L") else (R.W, R.H))
    # not a blank frame: the visual drew something brighter than the background
    assert max(frames[0].convert("L").getextrema()) > 150
