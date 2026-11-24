from datetime import UTC, date, datetime
from zoneinfo import ZoneInfo

import pytest

from endurance import training


def _activity(
    source_id: int,
    sport: str,
    started_at: datetime,
    moving_seconds: int,
    distance_meters: float | None,
) -> training.Activity:
    return training.Activity(
        source_id=source_id,
        sport=sport,
        started_at=started_at,
        moving_seconds=moving_seconds,
        distance_meters=distance_meters,
        average_speed_meters_per_second=None,
        average_heart_rate_bpm=None,
        maximum_heart_rate_bpm=None,
        minimum_heart_rate_bpm=None,
        elevation_gain=None,
        elevation_loss=None,
    )


def test_normalization_preserves_missing_distance_and_converts_to_utc():
    summary = {
        "id": 42,
        "sport_type": "WeightTraining",
        "start_date": "2026-10-25T14:00:00+01:00",
        "moving_time": 1800,
        "distance": None,
    }

    activity = training.normalize_activity(summary)

    assert activity.source_id == 42
    assert activity.sport == "strength"
    assert activity.started_at == datetime(2026, 10, 25, 13, tzinfo=UTC)
    assert activity.started_at.tzinfo is UTC
    assert activity.moving_seconds == 1800
    assert activity.distance_meters is None


@pytest.mark.parametrize("source_sport", ["Trail Run", "TrailRun"])
def test_trail_run_retains_its_own_sport_bucket(source_sport):
    summary = {
        "id": 45,
        "sport_type": source_sport,
        "start_date": "2026-10-31T08:00:00Z",
        "moving_time": 7200,
        "distance": 16500.0,
    }

    assert training.normalize_activity(summary).sport == "trail_run"


def test_unknown_sport_still_contributes_training_time():
    summary = {
        "id": 43,
        "sport_type": "FutureSport",
        "start_date": "2026-10-25T18:00:00Z",
        "moving_time": 900,
        "distance": 0,
    }

    activity = training.normalize_activity(summary)

    assert (activity.sport, activity.moving_seconds, activity.distance_meters) == ("other", 900, 0)


@pytest.mark.parametrize(
    ("start_date", "moving_time", "distance"),
    [
        ("2026-10-25T13:00:00", 1800, None),
        ("invalid", 1800, None),
        ("2026-10-25T13:00:00Z", -1, None),
        ("2026-10-25T13:00:00Z", 1800, -1),
    ],
)
def test_rejects_invalid_time_or_measurements(start_date, moving_time, distance):
    summary = {
        "id": 44,
        "sport_type": "TrailRun",
        "start_date": start_date,
        "moving_time": moving_time,
        "distance": distance,
    }

    with pytest.raises(ValueError):
        training.normalize_activity(summary)


def test_week_boundary_uses_local_date_and_totals_match_drilldown():
    boundary = _activity(1, "run", datetime(2026, 10, 25, 23, 30, tzinfo=UTC), 1800, 5100)
    previous = _activity(2, "ride", datetime(2026, 10, 25, 22, 30, tzinfo=UTC), 5100, 30100)
    same_start = _activity(3, "run", boundary.started_at, 1500, 4200)
    strength = _activity(4, "strength", datetime(2026, 10, 28, 17, 15, tzinfo=UTC), 2400, None)

    weeks = training.summarize_weeks(iter([previous, same_start, boundary, strength]), ZoneInfo("Europe/Berlin"))

    assert [week["week_start"] for week in weeks] == [date(2026, 10, 26), date(2026, 10, 19)]
    assert weeks[0]["seconds_by_sport"] == {"run": 3300, "strength": 2400}
    assert [activity.source_id for activity in weeks[0]["activities"]] == [4, 1, 3]
    assert weeks[1]["seconds_by_sport"] == {"ride": 5100}
    assert weeks[1]["activities"] == (previous,)


def test_no_activities_produces_no_weeks():
    assert training.summarize_weeks(iter(()), ZoneInfo("UTC")) == []


def test_reporting_timezone_changes_the_week_of_the_same_activity():
    activity = _activity(1, "run", datetime(2026, 10, 25, 23, 30, tzinfo=UTC), 1800, 5100)

    utc = training.summarize_weeks([activity], ZoneInfo("UTC"))
    berlin = training.summarize_weeks([activity], ZoneInfo("Europe/Berlin"))

    assert utc[0]["week_start"] == date(2026, 10, 19)
    assert berlin[0]["week_start"] == date(2026, 10, 26)
    assert utc[0]["activities"] == berlin[0]["activities"] == (activity,)
