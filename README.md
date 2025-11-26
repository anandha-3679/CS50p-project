# CS50p-project
My final project for the cs50p course completion sponsored by Harvard

Health Tracker — Python Project
Video Demo: https://youtu.be/lEi4RGI9lCM
Description:
Health Tracker is a Python command-line/demo application to record daily health metrics (e.g., weight, sleep hours, steps), compute short-term summaries like a 3-day moving average, and export entries to CSV. The project meets course requirements with a project.py file containing main() and three top-level functions, plus pytest tests. It demonstrates clean design, input validation, and common data-processing patterns for health/time-series analysis.

Project structure
project.py — Primary program file containing:

Entry dataclass — stores a single metric record (date, metric, value).
Functions:
add_entry(entries, date, metric, value) — validates inputs and adds an entry.
moving_average(entries, metric, window=3) — computes a sliding-window average.
summarize_week(entries, metric, end_date=None) — summarizes metric values over 7 days.
export_csv(entries, filename) — writes entries to a CSV file.
main() — builds a small dataset, prints summaries and moving averages, and exports to CSV.
test_project.py — Pytest tests:

test_add_entry_valid()
test_moving_average_basic()
test_summarize_week_counts_and_mean()
requirements.txt — Lists dependencies (pytest).

How to run
Create and activate a virtual environment

Install dependencies: pip install -r requirements.txt

Run the demo: python project.py

Run tests: pytest -q

Design choices
Dataclass for entries — concise representation with automatic equality checks.
Date format and validation — YYYY-MM-DD enforced via datetime.strptime.
CSV export — headers-first CSV for portability without DB dependencies.
Moving average — sliding window for short-term trend detection.
Input validation — raises ValueError for invalid data, simplifying debugging.
Limitations & future improvements
Data stored in-memory; CSV is only persistent storage.
Dates are not timezone-aware.
CLI is demo-oriented; full interactive CLI, web UI, or SQLite persistence would enhance usability.
Future enhancements: additional metrics, richer aggregations (median, percentiles), plotting (matplotlib), and more extensive tests.
Closing note
This project demonstrates core programming skills: input validation, small-scale data modeling (dataclass), time-series computation (moving_average), unit testing with pytest, and file export. The code is small, readable, and easy to extend for additional features or other time-series datasets.
