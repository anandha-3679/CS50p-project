#!/usr/bin/env python3
"""Health Tracker — a small CLI program to record daily health metrics.

Requirements satisfied:
- Implemented in Python
- `main` function present in project.py
- At least three other top-level functions: add_entry, moving_average, summarize_week
- At least three functions have pytest tests in test_project.py

Usage:
    python project.py         # runs an interactive demo
"""
from __future__ import annotations
import csv
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

DATE_FMT = "%Y-%m-%d"

@dataclass
class Entry:
    date: str  # YYYY-MM-DD
    metric: str
    value: float


def add_entry(entries: List[Entry], date: str, metric: str, value: float) -> Entry:
    """Create a new Entry and append to entries list after validating date format.

    Returns the created Entry.
    Raises ValueError on invalid date or value.
    """
    try:
        # validate date
        datetime.strptime(date, DATE_FMT)
    except Exception as exc:
        raise ValueError(f"date must be in YYYY-MM-DD format: {exc}")
    try:
        value_f = float(value)
    except Exception as exc:
        raise ValueError(f"value must be numeric: {exc}")

    entry = Entry(date=date, metric=metric.strip().lower(), value=value_f)
    entries.append(entry)
    return entry


def moving_average(entries: List[Entry], metric: str, window: int = 3) -> Dict[str, float]:
    """Compute a simple moving average for the specified metric.

    Returns a dict mapping date -> moving average (only for dates with enough prior data).
    Entries are sorted by date.
    """
    if window < 1:
        raise ValueError("window must be >= 1")
    metric = metric.strip().lower()
    # filter and convert
    vals = sorted([e for e in entries if e.metric == metric], key=lambda e: e.date)
    if not vals:
        return {}
    # accumulate
    results: Dict[str, float] = {}
    numbers = [e.value for e in vals]
    dates = [e.date for e in vals]
    for i in range(len(numbers)):
        if i + 1 >= window:
            window_vals = numbers[i - window + 1 : i + 1]
            avg = sum(window_vals) / len(window_vals)
            results[dates[i]] = avg
    return results


def summarize_week(entries: List[Entry], metric: str, end_date: Optional[str] = None) -> Dict[str, Any]:
    """Summarize metric values for the 7-day period ending at end_date (inclusive).

    If end_date is None, uses the latest date present in entries. Returns a dict with
    min, max, mean, count and the list of raw values.
    """
    metric = metric.strip().lower()
    if not entries:
        return {"count": 0, "values": []}
    if end_date is None:
        end = max(datetime.strptime(e.date, DATE_FMT) for e in entries)
    else:
        end = datetime.strptime(end_date, DATE_FMT)
    start = end - timedelta(days=6)
    selected = [e.value for e in entries if e.metric == metric and start <= datetime.strptime(e.date, DATE_FMT) <= end]
    if not selected:
        return {"count": 0, "values": []}
    count = len(selected)
    mean = sum(selected) / count
    return {"count": count, "min": min(selected), "max": max(selected), "mean": mean, "values": selected}


def export_csv(entries: List[Entry], filename: str) -> None:
    """Export the entries to a CSV file (headers: date,metric,value)."""
    with open(filename, "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["date", "metric", "value"])
        writer.writeheader()
        for e in entries:
            writer.writerow({"date": e.date, "metric": e.metric, "value": e.value})


def main() -> None:
    """Interactive demo: create some entries, print summaries and moving averages."""
    sample: List[Entry] = []
    print("Health Tracker — demo")
    # Add a handful of sample entries
    today = datetime.now()
    for i, val in enumerate([70, 71, 70.5, 69, 68.5, 69.2, 70]):
        date = (today - timedelta(days=6 - i)).strftime(DATE_FMT)
        add_entry(sample, date, "weight", val)
    print(f"Created {len(sample)} sample entries (weight).")

    ma = moving_average(sample, "weight", window=3)
    print("Moving averages (window=3):")
    for d, v in ma.items():
        print(f"  {d}: {v:.2f}")

    summary = summarize_week(sample, "weight")
    print("7-day summary:")
    for k, v in summary.items():
        print(f"  {k}: {v}")

    fname = "health_entries.csv"
    export_csv(sample, fname)
    print(f"Exported entries to {fname}")


if __name__ == "__main__":
    main()
