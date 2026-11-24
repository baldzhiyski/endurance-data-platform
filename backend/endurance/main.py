from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import uvicorn
from fastapi import FastAPI, HTTPException

from endurance.demo_data import DEMO_ACTIVITIES
from endurance.training import normalize_activity, summarize_weeks

app = FastAPI(
    title="Endurance Data Platform",
    description="A backend for endurance athletes to track and analyze their training data.",
    version="0.1.0",
)


@app.get("/api/health", status_code=200)
def health() -> dict[str, str]:
    """Return a simple health check response."""
    return {"status": "ok"}


@app.get("/api/demo/weeks", status_code=200)
def demo_weeks(timezone: str = "Europe/Berlin") -> dict[
    str, str | list[dict[str, str | dict[str, int] | list[dict[str, str | int | float | None]]]]
]:
    """Return a synthetic training week summary for the demo."""
    try:
        zone = ZoneInfo(timezone)
    except (ZoneInfoNotFoundError, ValueError) as error:
        raise HTTPException(status_code=422, detail="Use an IANA timezone such as Europe/Berlin.") from error

    normalized_activities = [normalize_activity(summary) for summary in DEMO_ACTIVITIES]
    weeks = summarize_weeks(normalized_activities, zone)

    return {
        "source": "synthetic",
        "timezone": timezone,
        "weeks": [
            {
                "week_start": week["week_start"].isoformat(),
                "seconds_by_sport": week["seconds_by_sport"],
                "activities": [
                    {
                        "source_id": activity.source_id,
                        "sport": activity.sport,
                        "started_at": activity.started_at.isoformat(),
                        "moving_seconds": activity.moving_seconds,
                        "average_speed": activity.average_speed_meters_per_second,
                        "average_heart_rate": activity.average_heart_rate_bpm,
                        "maximum_heart_rate": activity.maximum_heart_rate_bpm,
                        "minimum_heart_rate": activity.minimum_heart_rate_bpm,
                        "distance_meters": activity.distance_meters,
                        "elevation_gain": activity.elevation_gain,
                        "elevation_loss": activity.elevation_loss,
                    }
                    for activity in week["activities"]
                ],
            }
            for week in weeks
        ],
    }


@app.get("/", status_code=200)
def serve_dashboard() -> dict[str, str]:
    """Serve the built dashboard if it exists, otherwise return a placeholder."""
    return {"message": "Dashboard not built yet. Please build the frontend."}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)

