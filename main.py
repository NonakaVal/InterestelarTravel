import numpy as np
from typing import Dict, List, TypedDict
from dataclasses import dataclass

# Constants (in easy-to-understand units)
SPEED_OF_LIGHT = 299792.458  # km/s
LIGHT_YEAR_KM = 9.461e12  # 1 light-year in km
HUBBLE_CONSTANT = 70  # km/s/Mpc (simplified)
MPC_TO_LY = 3.26156e6  # 1 megaparsec in light-years

@dataclass
class TravelStage:
    """Contains data for one stage of the journey"""
    stage_number: int
    speed_percentage: float  # % of light speed
    distance_covered: float  # light-years
    time_elapsed: float  # years
    expansion_effect: float  # additional distance due to expansion

@dataclass
class MissionReport:
    """Final mission summary report"""
    destination: str
    distance: float  # original distance in light-years
    mission_id: str
    stages: List[TravelStage]
    total_time: float  # years
    total_distance: float  # actual distance traveled (light-years)
    expansion_addition: float  # % extra distance from expansion

def simulate_interstellar_travel(
    destination: str,
    distance_ly: float,
    mission_id: str,
    num_stages: int = 5,
    min_speed: float = 1.0,  # % of light speed
    max_speed: float = 5.0   # % of light speed
) -> MissionReport:
    """
    Simulates a journey through expanding space with varying speeds.
    
    Args:
        destination: Name of target star/system
        distance_ly: Distance in light-years
        mission_id: Mission identifier
        num_stages: Number of speed change phases
        min_speed: Minimum cruise speed (% of light speed)
        max_speed: Maximum cruise speed (% of light speed)
    
    Returns:
        MissionReport with complete journey details
    """
    # Validate inputs
    if not (0.1 <= min_speed <= max_speed <= 100):
        raise ValueError("Speeds must be between 0.1% and 100% of light speed")
    
    # Generate random speed profile for the journey
    speed_profile = np.linspace(min_speed, max_speed, num_stages)
    np.random.shuffle(speed_profile)
    
    stages = []
    remaining_distance = distance_ly
    total_time = 0.0
    total_actual_distance = 0.0
    
    for stage_num, speed_pct in enumerate(speed_profile, 1):
        speed_fraction = speed_pct / 100
        speed_km_s = speed_fraction * SPEED_OF_LIGHT
        
        # Calculate this stage's distance (equal segments)
        stage_distance = distance_ly / num_stages
        
        # Account for universe expansion during travel
        distance_mpc = stage_distance / MPC_TO_LY
        expansion_speed = HUBBLE_CONSTANT * distance_mpc  # km/s
        expansion_factor = 1 + (expansion_speed / speed_km_s)
        actual_distance = stage_distance * expansion_factor
        
        # Time required for this stage
        stage_time = actual_distance / speed_fraction
        
        # Update totals
        remaining_distance -= stage_distance
        total_actual_distance += actual_distance
        total_time += stage_time
        
        # Record stage details
        stages.append(TravelStage(
            stage_number=stage_num,
            speed_percentage=round(speed_pct, 2),
            distance_covered=round(actual_distance, 2),
            time_elapsed=round(stage_time, 2),
            expansion_effect=round((expansion_factor-1)*100, 4)
        ))
    
    # Calculate expansion impact
    expansion_impact = ((total_actual_distance / distance_ly) - 1) * 100
    
    return MissionReport(
        destination=destination,
        distance=distance_ly,
        mission_id=mission_id,
        stages=stages,
        total_time=round(total_time, 2),
        total_distance=round(total_actual_distance, 2),
        expansion_addition=round(expansion_impact, 4)
    )

def generate_mission_summary(report: MissionReport) -> str:
    """Creates an easy-to-read mission summary"""
    summary = []
    summary.append(f"\n🚀 MISSION REPORT: {report.mission_id}")
    summary.append(f"Destination: {report.destination}")
    summary.append(f"Original Distance: {report.distance:,} light-years")
    summary.append("="*50)
    
    for stage in report.stages:
        summary.append(
            f"Stage {stage.stage_number}: "
            f"Speed: {stage.speed_percentage}% light | "
            f"Distance: {stage.distance_covered:,} ly | "
            f"Time: {stage.time_elapsed:,} yrs | "
            f"Expansion: +{stage.expansion_effect}%"
        )
    
    summary.append("="*50)
    summary.append(f"TOTAL MISSION TIME: {report.total_time:,} years")
    summary.append(f"ACTUAL DISTANCE TRAVELED: {report.total_distance:,} light-years")
    summary.append(f"EXPANSION IMPACT: +{report.expansion_addition}% extra distance")
    
    return "\n".join(summary)

# Example mission to Andromeda
if __name__ == "__main__":
    mission = simulate_interstellar_travel(
        destination="Andromeda Galaxy",
        distance_ly=2_500_000,
        mission_id="AND-001",
        num_stages=5,
        min_speed=10,
        max_speed=10
    )
    
    print(generate_mission_summary(mission))