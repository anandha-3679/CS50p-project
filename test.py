import pytest
from project import Entry, add_entry, moving_average, summarize_week

def make_sample():
    entries = []
    # dates: 2025-09-01 .. 2025-09-07 (7 days)
    dates = [f"2025-09-{day:02d}" for day in range(1, 8)]
    weights = [70, 71, 70.5, 69, 68.5, 69.2, 70]
    for d, w in zip(dates, weights):
        entries.append(Entry(date=d, metric="weight", value=w))
    return entries


def test_add_entry_valid():
    entries = []
    e = add_entry(entries, "2025-09-09", "sleep", 7.5)
    assert e.date == "2025-09-09"
    assert e.metric == "sleep"
    assert abs(e.value - 7.5) < 1e-9
    assert len(entries) == 1


def test_moving_average_basic():
    entries = make_sample()
    ma = moving_average(entries, "weight", window=3)
    # moving average will exist for dates 2025-09-03 .. 2025-09-07
    assert "2025-09-03" in ma
    assert pytest.approx(ma["2025-09-03"], rel=1e-3) == (70 + 71 + 70.5) / 3


def test_summarize_week_counts_and_mean():
    entries = make_sample()
    summary = summarize_week(entries, metric="weight", end_date="2025-09-07")
    assert summary["count"] == 7
    assert pytest.approx(summary["mean"], rel=1e-3) == sum([70, 71, 70.5, 69, 68.5, 69.2, 70]) / 7
