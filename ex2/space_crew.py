from datetime import datetime
from enum import Enum
from typing import List
from pydantic import (BaseModel, Field,
                      ValidationError, model_validator)


class Rank(str, Enum):
    cadet = "cadet"
    officer = "officer"
    lieutenant = "lieutenant"
    captain = "captain"
    commander = "commander"


class CrewMember(BaseModel):
    member_id: str = Field("001", min_length=3, max_length=10,
                           description="station_id take 3<string<10")
    name: str = Field("station", min_length=2, max_length=50,
                      description="name take 2<string<50")
    rank: Rank = Field(..., description="rank degree")
    age: int = Field(30, ge=18, le=80,
                     description="age must be in rage 18-80 year")
    specialization: str = Field("worker", min_length=3, max_length=30,
                                description="specialite of worker")
    years_experience: int = Field(1, ge=0, le=50,
                                  description="work expirence must int")
    is_active: bool = Field(True, description="contact type")


class SpaceMission(BaseModel):
    mission_id: str = Field("ISS001", min_length=5, max_length=15,
                            description="mission_id is String 5-15 characters")
    mission_name: str = Field(min_length=3, max_length=100,
                              description="mission_name str 3-100 characters")
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime = Field(datetime.now(),
                                  description="Time of launch")
    duration_days: int = Field(365, ge=1, le=3650,
                               description="duration_days int 1-3650 days")
    crew: List[CrewMember] = Field(..., min_length=1, max_length=12,
                                   description="the crew is a list")
    mission_status: str = Field("planned",
                                description="mission_status")
    budget_millions: float = Field(1000.0, ge=1.0, le=10000.0,
                                   description="budget Float in milion dolars")

    @model_validator(mode="after")
    def validate_mission(self):
        if not self.mission_id.startswith("M"):
            raise ValueError("Mission ID must start with 'M'")

        has_leader = any(
            member.rank in (Rank.captain, Rank.commander)
            for member in self.crew
        )
        if not has_leader:
            raise ValueError("Mission must have at "
                             "least one Commander or Captain")

        if self.duration_days > 365:
            experienced = sum(
                1 for member in self.crew if member.years_experience >= 5
            )
            if experienced < len(self.crew) / 2:
                raise ValueError("Long missions require at "
                                 "least 50%// experienced crew (5+ years)")

        if not all(member.is_active for member in self.crew):
            raise ValueError("All crew members must be active")

        return self


def main() -> None:
    print("Space Mission Crew Validation")
    print("=========================================")

    try:
        mission = SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date=datetime.now(),
            duration_days=900,
            mission_status="planned",
            budget_millions=2500.0,
            crew=[
                CrewMember(
                    member_id="C10",
                    name="Sarah Connor",
                    rank=Rank.commander,
                    age=40,
                    specialization="Mission Command",
                    years_experience=10,
                    is_active=True,
                ),
                CrewMember(
                    member_id="C20",
                    name="John Smith",
                    rank=Rank.lieutenant,
                    age=35,
                    specialization="Navigation",
                    years_experience=6,
                    is_active=True,
                ),
                CrewMember(
                    member_id="C30",
                    name="Alice Johnson",
                    rank=Rank.officer,
                    age=30,
                    specialization="Engineering",
                    years_experience=5,
                    is_active=True,
                ),
            ],
        )

        print("Valid mission created:")
        print(f"Mission: {mission.mission_name}")
        print(f"ID: {mission.mission_id}")
        print(f"Destination: {mission.destination}")
        print(f"Duration: {mission.duration_days} days")
        print(f"Budget: ${mission.budget_millions}M")
        print(f"Crew size: {len(mission.crew)}")

        print("\nCrew members:")
        for member in mission.crew:
            print(
                f"- {member.name} ({member.rank.value})",
                f"- {member.specialization}"
            )

    except ValidationError as e:
        print("Expected validation error:")
        print(e.errors()[0]["msg"])

    print("\n=========================================")

    try:
        SpaceMission(
            mission_id="M_FAIL_001",
            mission_name="Test Mission",
            destination="Moon",
            launch_date=datetime.now(),
            duration_days=100,
            mission_status="planned",
            budget_millions=500.0,
            crew=[
                CrewMember(
                    member_id="C10",
                    name="Bob",
                    rank=Rank.officer,
                    age=30,
                    specialization="Engineering",
                    years_experience=3,
                    is_active=True,
                ),
            ],
        )

    except ValidationError as e:
        print("Expected validation error:")
        print(e.errors()[0]["msg"].split(",")[1])


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
