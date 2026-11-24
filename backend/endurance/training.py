from dataclasses import dataclass
from datetime import datetime
from typing import TypedDict

@dataclass
class Activity:
    source_id: int
    sport: str
    started_at: datetime
    moving_seconds: int
    average_speed_meters_per_second: float | None
    average_heart_rate_bpm: float | None
    maximum_heart_rate_bpm: float | None
    minimum_heart_rate_bpm: float | None
    distance_meters: float | None
    elevation_gain: float | None
    elevation_loss: float | None

class ActivitySummary(TypedDict):
    id: int
    sport_type: str
    start_date: str
    moving_time: int
    average_speed: float | None
    average_heart_rate: float | None
    maximum_heart_rate: float | None
    minimum_heart_rate: float | None
    elevation_gain: float | None
    elevation_loss: float | None
    distance: float | None


def normalize_activity(summary: ActivitySummary) -> Activity:
    """Convert an ActivitySummary to an Activity with normalized fields."""

    sport_mapping = {
        "Run": "run",
        "Trail Run": "run",
        "Outdoor run": "run",
        "Indoor Run": "run",
        "Ride": "ride",
        "Strength": "strength",
        "Swim": "swim",
    }

    sport = sport_mapping.get(summary["sport_type"], "other")

    try:
        started_at = datetime.fromisoformat(summary["start_date"].replace("Z", "+00:00"))
    except ValueError:
        raise ValueError(f"Invalid start_date format: {summary['start_date']}") 

    if started_at.tzinfo is None:
        raise ValueError(f"Naive datetime is not allowed: {summary['start_date']}")
    else:
        started_at = started_at.astimezone(datetime.timezone.utc)

    moving_seconds = summary["moving_time"]
    if moving_seconds < 0:
        raise ValueError(f"Negative moving_time is not allowed: {moving_seconds}")

    average_speed_meters_per_second = summary.get("average_speed")
    if average_speed_meters_per_second is not None and average_speed_meters_per_second < 0:
        raise ValueError(f"Negative average_speed is not allowed: {average_speed_meters_per_second}")

    average_heart_rate_bpm = summary.get("average_heart_rate")
    if average_heart_rate_bpm is not None and average_heart_rate_bpm < 0:
        raise ValueError(f"Negative average_heart_rate is not allowed: {average_heart_rate_bpm}")

    maximum_heart_rate_bpm = summary.get("maximum_heart_rate")
    if maximum_heart_rate_bpm is not None and maximum_heart_rate_bpm < 0:
        raise ValueError(f"Negative maximum_heart_rate is not allowed: {maximum_heart_rate_bpm}")   

    minimum_heart_rate_bpm = summary.get("minimum_heart_rate")
    if minimum_heart_rate_bpm is not None and minimum_heart_rate_bpm < 0:
        raise ValueError(f"Negative minimum_heart_rate is not allowed: {minimum_heart_rate_bpm}")   

    distance_meters = summary.get("distance")
    if distance_meters is not None and distance_meters < 0:
        raise ValueError(f"Negative distance is not allowed: {distance_meters}")   

    return Activity(
        source_id=summary["id"],
        sport=sport,
        started_at=started_at,
        moving_seconds=moving_seconds,
        average_speed_meters_per_second=average_speed_meters_per_second,
        average_heart_rate_bpm=average_heart_rate_bpm,
        maximum_heart_rate_bpm=maximum_heart_rate_bpm,
        minimum_heart_rate_bpm=minimum_heart_rate_bpm,
        elevation_gain=summary.get("elevation_gain"),
        elevation_loss=summary.get("elevation_loss"),
        distance_meters=distance_meters
    )
 
    

class TrainingWeek(TypedDict):
    week_start: str
    seconds_by_sport: dict[str, int]
    activities: tuple[Activity, ...]

def summarize_weeks(activities: list[Activity]) -> list[TrainingWeek]:
    """Summarize activities into training weeks.

    Each week starts on Monday. The week_start is the date of that Monday in
    ISO format (YYYY-MM-DD). The seconds_by_sport dictionary maps normalized
    sport names to the total moving seconds for that sport in the week. The
    activities tuple contains all activities that fall within that week,
    sorted by start time (newest first) and then by source ID (ascending) to
    break ties.
    """
    from collections import defaultdict
    from datetime import timedelta

    # Group activities by week start date
    weeks = defaultdict(list)
    for activity in activities:
        # Convert started_at to local time and find the Monday of that week
        local_date = activity.started_at.date()
        monday = local_date - timedelta(days=local_date.weekday())
        weeks[monday].append(activity)

    # Build TrainingWeek summaries
    training_weeks = []
    for monday, week_activities in weeks.items():
        seconds_by_sport = defaultdict(int)
        for activity in week_activities:
            seconds_by_sport[activity.sport] += activity.moving_seconds

        # Sort activities by start time (newest first) and then by source ID (ascending)
        sorted_activities = sorted(
            week_activities,
            key=lambda a: (-a.started_at.timestamp(), a.source_id)
        )

        training_weeks.append(TrainingWeek(
            week_start=monday.isoformat(),
            seconds_by_sport=dict(seconds_by_sport),
            activities=tuple(sorted_activities)
        ))

    # Sort weeks by week_start (newest first)
    training_weeks.sort(key=lambda w: w['week_start'], reverse=True)

    return training_weeks
