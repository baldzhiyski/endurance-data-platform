"""Invented activity summaries for the local demo and repeatable tests."""

from endurance.training import ActivitySummary

DEMO_ACTIVITIES: tuple[ActivitySummary, ...] = (
    {"id": 1, "sport_type": "Run", "start_date": "2026-10-06T16:30:00Z", "moving_time": 2400, "average_speed": 1.5, "average_heart_rate": 150.0, "maximum_heart_rate": 180.0, "minimum_heart_rate": 60.0, "distance": 6800.0, "elevation_gain": 100.0, "elevation_loss": 80.0},
    {"id": 2, "sport_type": "Trail Run", "start_date": "2026-10-10T07:00:00Z", "moving_time": 6000,"average_speed": 1.2, "average_heart_rate": 140.0, "maximum_heart_rate": 170.0, "minimum_heart_rate": 50.0, "distance": 13500.0, "elevation_gain": 150.0, "elevation_loss": 120.0},
    {"id": 3, "sport_type": "Strength", "start_date": "2026-10-13T17:10:00Z", "moving_time": 3000, "average_speed": 1.0, "average_heart_rate": 120.0, "maximum_heart_rate": 150.0, "minimum_heart_rate": 30.0, "distance": None, "elevation_gain": 100.0, "elevation_loss": 80.0},
    {"id": 4, "sport_type": "Trail Run", "start_date": "2026-10-17T07:45:00Z", "moving_time": 7800,"average_speed": 1.1, "average_heart_rate": 130.0, "maximum_heart_rate": 160.0, "minimum_heart_rate": 40.0, "distance": 17600.0, "elevation_gain": 200.0, "elevation_loss": 150.0},
    {"id": 5, "sport_type": "Outdoor run", "start_date": "2026-10-20T15:20:00Z", "moving_time": 2700, "average_speed": 1.0, "average_heart_rate": 120.0, "maximum_heart_rate": 150.0, "minimum_heart_rate": 30.0, "distance": 7600.0, "elevation_gain": 100.0, "elevation_loss": 80.0},
    {"id": 6, "sport_type": "Ride", "start_date": "2026-10-25T08:30:00Z", "moving_time": 5100,"average_speed": 1.0, "average_heart_rate": 120.0, "maximum_heart_rate": 150.0, "minimum_heart_rate": 30.0, "distance": 30100.0, "elevation_gain": 300.0, "elevation_loss": 250.0},
    {"id": 7, "sport_type": "Run", "start_date": "2026-10-25T23:30:00Z", "moving_time": 1800,"average_speed": 1.0, "average_heart_rate": 120.0, "maximum_heart_rate": 150.0, "minimum_heart_rate": 30.0, "distance": 5100.0, "elevation_gain": 50.0, "elevation_loss": 30.0},
    {"id": 8, "sport_type": "Strength", "start_date": "2026-10-28T17:15:00Z", "moving_time": 2400,"average_speed": 1.0, "average_heart_rate": 120.0, "maximum_heart_rate": 150.0, "minimum_heart_rate": 30.0, "distance": None, "elevation_gain": 100.0, "elevation_loss": 80.0},
    {"id": 9, "sport_type": "Trail Run", "start_date": "2026-10-31T08:00:00Z", "moving_time": 7200,"average_speed": 1.0, "average_heart_rate": 120.0, "maximum_heart_rate": 150.0, "minimum_heart_rate": 30.0, "distance": 16500.0, "elevation_gain": 200.0, "elevation_loss": 150.0},
    {"id": 10, "sport_type": "Indoor Run", "start_date": "2026-11-01T14:00:00Z", "moving_time": 1500, "average_speed": 1.0, "average_heart_rate": 120.0, "maximum_heart_rate": 150.0, "minimum_heart_rate": 30.0, "distance": 4200.0, "elevation_gain": 50.0, "elevation_loss": 30.0},
)
