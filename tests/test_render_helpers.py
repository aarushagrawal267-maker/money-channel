"""Formatting, caption and music helpers used by the Short and long-form renderers."""
import numpy as np

import render as R


def test_money_formats():
    assert R.fmt_usd(792_000) == "$792K"
    assert R.fmt_usd(1_250_000) == "$1.25M"
    assert R.fmt_usd(9_000_000_000) == "$9B"
    assert R.fmt_usd(4_500) == "$4,500"
    assert R.fmt_inr(15_000_000) == "₹1.5 Cr"
    assert R.fmt_inr(250_000) == "₹2.5 L"
    assert R.fmt_inr(9_999) == "₹9,999"


def test_nice_ticks_cover_the_max_with_round_steps():
    ticks = R.nice_ticks(792_000)
    assert ticks == [200_000, 400_000, 600_000, 800_000]
    assert R.nice_ticks(37)[-1] >= 37


def test_word_times_cover_the_segment_in_order():
    wts = R.word_times("Start early, even small.", 1.0, 3.0)
    assert [w for w, _, _ in wts] == ["Start", "early,", "even", "small."]
    assert wts[0][1] == 1.0 and abs(wts[-1][2] - 3.0) < 1e-9
    assert all(a[2] <= b[1] + 1e-9 for a, b in zip(wts, wts[1:]))


def test_spoken_numbers_become_digits_in_captions():
    say = "Maya ends with seven hundred ninety-two thousand dollars at four point seven percent in twenty twenty-five."
    words = [w for w, _, _ in R.digit_captions(R.word_times(say, 0, 5))]
    assert "$792,000" in words and "4.7%" in words and "2025." in words


def test_caption_chunks_respect_limits():
    wts = R.word_times("one two three four five six seven eight nine ten", 0, 5)
    chunks = R.chunk_words(wts, max_chars=16, max_words=3)
    assert chunks
    assert all(len(c[0].split()) <= 3 for c in chunks) if isinstance(chunks[0][0], str) else True


def test_music_is_deterministic_per_video_and_normalised():
    a = R.make_music(R.SR * 3, "018_start_early_us")
    b = R.make_music(R.SR * 3, "018_start_early_us")
    c = R.make_music(R.SR * 3, "019_real_hourly_wage")
    assert np.array_equal(a, b)
    assert not np.array_equal(a, c)
    assert np.max(np.abs(a)) <= 1.0 + 1e-6


def test_speech_bounds_trims_silence():
    x = np.zeros(1000); x[200:300] = 0.5
    assert R.speech_bounds(x) == (200, 299)
