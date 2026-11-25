"""upload.py: metadata building, schedule parsing, retry policy and the posted log (no network)."""
import datetime as dt, json, socket

import pytest

import upload as U

SPEC = {
    "id": "999_test", "title": "Rule of <72> explained",
    "description": "How fast money doubles.\n\nSources: example.\n#money #investing #finance #shorts #extra",
    "tags": ["rule of 72", "compound interest"] + [f"tag{i}" for i in range(200)],
}


def test_build_body_short():
    b = U.build_body(SPEC)
    sn, st = b["snippet"], b["status"]
    assert sn["title"] == "Rule of 72 explained"          # angle brackets are not allowed by YouTube
    assert sn["categoryId"] == "27"
    assert U.AI_LINE in sn["description"] and U.SUBSCRIBE_LINE in sn["description"]
    assert sn["description"].rstrip().endswith("#money #investing #finance #extra #shorts")
    assert st["selfDeclaredMadeForKids"] is False and st["privacyStatus"] == "private"
    tags = sn["tags"]
    assert sum(len(t) + (2 if " " in t else 0) for t in tags) + len(tags) - 1 <= U.MAX_TAGS_CHARS


def test_build_body_long_with_chapters_and_schedule():
    spec = dict(SPEC, id="L999_test")
    b = U.build_body(spec, "0:00 Intro\n1:10 Why", "private", "2030-01-01T01:00:00.000Z")
    d = b["snippet"]["description"]
    assert d.index("Chapters\n0:00 Intro") < d.index("Sources")      # chapters right after the summary
    assert "#shorts" not in d
    assert b["status"]["publishAt"] == "2030-01-01T01:00:00.000Z"


def test_title_too_long_is_refused():
    with pytest.raises(SystemExit):
        U.build_body(dict(SPEC, title="x" * 101))


def test_localizations_keep_ai_disclosure_even_when_shortened():
    spec = dict(SPEC, description="x" * 4400 + "\n#money",
                localizations={"es": {"title": "Regla del 72", "summary": "Resumen. " * 100}})
    loc = U.build_body(spec)["localizations"]["es"]
    assert loc["title"] == "Regla del 72"
    assert U.AI_LINE in loc["description"]
    assert len(loc["description"].encode()) <= U.MAX_DESC


def test_parse_publish_at():
    when = (dt.datetime.now(dt.timezone.utc) + dt.timedelta(days=2)).replace(microsecond=0)
    ist = when.astimezone(dt.timezone(dt.timedelta(hours=5, minutes=30)))
    assert U.parse_publish_at(ist.isoformat()) == when.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    assert U.parse_publish_at(None) is None
    with pytest.raises(SystemExit):
        U.parse_publish_at(when.replace(tzinfo=None).isoformat())          # no timezone
    with pytest.raises(SystemExit):
        U.parse_publish_at(dt.datetime.now(dt.timezone.utc).isoformat())   # not far enough ahead


class _Resp:
    def __init__(self, status):
        self.status = status


class _HttpErr(Exception):
    def __init__(self, status):
        self.resp = _Resp(status)


def test_retry_policy():
    assert U.is_transient(_HttpErr(503))
    assert not U.is_transient(_HttpErr(403))
    assert U.is_transient(ConnectionResetError())
    assert U.is_transient(socket.timeout())
    assert not U.is_transient(KeyError("bug"))


def test_retry_policy_token_refresh():
    """A network error while refreshing the login token is retried; a refused login is not."""
    exc = pytest.importorskip("google.auth.exceptions")
    assert U.is_transient(exc.TransportError("proxy reset"))
    assert not U.is_transient(exc.RefreshError("invalid_grant"))


def test_save_posted_is_atomic_and_round_trips(tmp_path, monkeypatch):
    p = tmp_path / "posted.json"
    monkeypatch.setattr(U, "POSTED", str(p))
    U.log_posted({"id": "a", "video_id": "v1"})
    U.log_posted({"id": "b", "video_id": "v2", "title": "₹ title"})
    data = json.loads(p.read_text())
    assert [e["id"] for e in data] == ["a", "b"] and data[1]["title"] == "₹ title"
    assert [f.name for f in tmp_path.iterdir()] == ["posted.json"]          # no temp files left behind


def test_cli_refuses_missing_files(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["upload.py", str(tmp_path / "nope.json"), str(tmp_path / "nope.mp4")])
    with pytest.raises(SystemExit) as e:
        U.main()
    assert "not found" in str(e.value)


def test_cli_repeat_refused_but_dry_run_still_prints(tmp_path, monkeypatch, capsys):
    posted = tmp_path / "posted.json"
    posted.write_text(json.dumps([{"id": SPEC["id"], "video_id": "v1"}]))
    monkeypatch.setattr(U, "POSTED", str(posted))
    spec, video = tmp_path / "spec.json", tmp_path / "v.mp4"
    spec.write_text(json.dumps(SPEC)); video.write_bytes(b"x")
    monkeypatch.setattr("sys.argv", ["upload.py", str(spec), str(video)])
    with pytest.raises(SystemExit) as e:                      # a real upload of a posted id is refused
        U.main()
    assert "refusing to upload it twice" in str(e.value)
    monkeypatch.setattr("sys.argv", ["upload.py", str(spec), str(video), "--dry-run"])
    U.main()                                                  # a dry run only warns and prints the metadata
    out = capsys.readouterr()
    assert "NOTE (dry run)" in out.err and json.loads(out.out)["snippet"]["title"] == "Rule of 72 explained"


def test_retry_thumbs_picks_only_live_failures():
    import retry_thumbs
    posted = [{"id": "a", "video_id": "1", "thumbnail": False},
              {"id": "b", "video_id": "2", "thumbnail": True},
              {"id": "c", "video_id": "3", "thumbnail": False, "superseded": True},
              {"id": "d", "video_id": "4"}]
    assert [e["id"] for e in retry_thumbs.pending(posted)] == ["a"]
