from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ValidationError


class SpaceStation(BaseModel):
    station_id: str = Field("ISS001", min_length=3, max_length=10,
                            description="station_id take 3<string<10")
    name: str = Field("station", min_length=1, max_length=50,
                      description="name take 1<string<50")
    crew_size: int = Field(10, ge=1, le=20,
                           description="size take an 1<int<20")
    power_level: float = Field(50.0, ge=0.0, le=100.0,
                               description="power_level take 0.0<float<100.0")
    oxygen_level: float = Field(50.0, ge=0.0, le=100.0,
                                description="oxygn_level take 0.0<float<100.0")
    last_maintenance: datetime = Field(datetime.now(),
                                       description="Time of recent mainteance")
    is_operational: bool = Field(default=True,
                                 description="is_operational is bolien")
    notes: Optional[str] = Field(default=None, max_length=200,
                                 description="notes are operational")


def main() -> None:
    print("Space Station Data Validation")
    print("========================================")

    try:
        station = SpaceStation(
            station_id="ISS001",
            name="International Space Station",
            crew_size=6,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance=datetime.now(),
        )

        print("Valid station created:")
        print(f"ID: {station.station_id}")
        print(f"Name: {station.name}")
        print(f"Crew: {station.crew_size} people")
        print(f"Power: {station.power_level}%")
        print(f"Oxygen: {station.oxygen_level}%")
        value = 'Operational' if station.is_operational else 'Offline'
        print(f"Status: {value}")

    except ValidationError as e:
        print("Expected validation error:")
        print(e.errors()[0]["msg"])

    print("\n========================================")

    try:
        SpaceStation(
            station_id="BAD001",
            name="Broken Station",
            crew_size=25,
            power_level=50.0,
            oxygen_level=50.0,
            last_maintenance=datetime.now(),
        )

    except ValidationError as e:
        print("Expected validation error:")
        print(e.errors()[0]["msg"])


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
