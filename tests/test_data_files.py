"""queue.json, schedule.txt and posted.json stay consistent with each other and with the specs."""
import datetime as dt, json, os

from conftest import PIPELINE, SPECS


def load(name):
    return json.load(open(os.path.join(PIPELINE, name)))


def schedule():
    rows = []
    for line in open(os.path.join(PIPELINE, "schedule.txt")):
        line = line.strip()
        if line and not line.startswith("#"):
            sid, when = line.split()
            rows.append((sid, dt.datetime.fromisoformat(when)))
    return rows


def test_schedule_entries_have_specs_and_timezones():
    rows = schedule()
    assert rows
    for sid, when in rows:
        assert os.path.exists(os.path.join(SPECS, sid + ".py")), f"{sid} is scheduled but has no spec"
        assert when.tzinfo is not None, f"{sid}: publish time needs a timezone"
    ids = [sid for sid, _ in rows]
    assert len(ids) == len(set(ids)), "an id is scheduled twice"
    times = [w for _, w in rows]
    assert len(times) == len(set(times)), "two videos share one slot"


def test_queue_is_well_formed():
    q = load("queue.json")
    items = q["shorts"] + q["long"]
    slugs = [i["slug"] for i in items]
    assert len(slugs) == len(set(slugs))
    for i in items:
        assert i["kind"] in ("short", "long") and i["currency"] in ("usd", "inr")
        if i.get("spec"):
            assert os.path.exists(os.path.join(SPECS, i["spec"] + ".py")), f"queue points at missing spec {i['spec']}"


def test_posted_log_has_no_live_duplicates():
    posted = load("posted.json")
    live = [(e["id"]) for e in posted if not e.get("test") and not e.get("superseded") and e.get("publish_at")]
    assert len(live) == len(set(live)), "the same video is scheduled twice"
    for e in posted:
        assert e["video_id"] and e["url"].endswith(e["video_id"])
