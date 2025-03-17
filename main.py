import sys
import os
from typing import Dict, List, Any

# Ensure the script can find our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our story engine classes
from character_world_classes import Character, World
from story_engine import OCCAppraisalModel, StoryEngine

def setup_space_station_scenario():
    """Set up the space station scenario with characters and initial states"""
    
    # Create the characters
    
    # Sid (Engineer) - Player character
    sid = Character(
        name="Sid",
        initial_emotions={
            "calm": 0.7,
            "anxiety": 0.3,
            "guilt": 0.2
        },
        initial_beliefs={
            "station_malfunctioning_naturally": 0.8,
            "raymond_trusts_me": 0.6,
            "bao_trusts_me": 0.7,
            "sabotage_possible": 0.3
        },
        initial_goals={
            "task": {
                "fix_station": 0.9,
                "investigate_anomalies": 0.8
            },
            "emotional": {
                "maintain_crew_trust": 0.7,
                "protect_reputation": 0.6
            }
        }
    )
    
    # Captain Raymond
    raymond = Character(
        name="Captain Raymond",
        initial_emotions={
            "suspicion": 0.5,
            "concern": 0.6,
            "determination": 0.8
        },
        initial_beliefs={
            "sid_hiding_something": 0.5,
            "station_in_danger": 0.7,
            "bao_reliable": 0.8,
            "sabotage_possible": 0.4
        },
        initial_goals={
            "task": {
                "ensure_crew_safety": 0.9,
                "maintain_station_integrity": 0.8
            },
            "emotional": {
                "maintain_authority": 0.7,
                "discover_truth": 0.8
            }
        }
    )
    
    # Dr. Bao
    bao = Character(
        name="Dr. Bao",
        initial_emotions={
            "curiosity": 0.7,
            "concern": 0.5,
            "calmness": 0.6
        },
        initial_beliefs={
            "sid_trustworthy": 0.7,
            "raymond_sometimes_paranoid": 0.4,
            "scientific_explanation_exists": 0.8,
            "station_fixable": 0.6
        },
        initial_goals={
            "task": {
                "conduct_accurate_analysis": 0.8,
                "support_medical_needs": 0.7
            },
            "emotional": {
                "maintain_objectivity": 0.8,
                "preserve_crew_harmony": 0.6
            }
        }
    )
    
    # Create the world
    setting = "Space Station Horizon - Critical System Failure"
    background = """
    Space Station Horizon, orbiting Earth's upper atmosphere, has been experiencing unexplained 
    malfunctions for the past 48 hours. Life support systems are showing signs of gradual failure, 
    and several key systems have mysteriously shut down. The three remaining crew members must 
    work together to identify the cause and restore functionality before oxygen levels become critical.
    
    As Sid, the station's engineer, you recently discovered some concerning anomalies in the 
    station's diagnostic logs, but haven't shared all the information with the others. Captain Raymond 
    is growing increasingly suspicious of the situation, while Dr. Bao is trying to maintain objectivity 
    while analyzing the environmental systems.
    
    Tensions are rising as the life support countdown shows only 24 hours of guaranteed oxygen remaining.
    """
    
    # Create the world with these characters
    world = World(
        setting=setting, 
        background=background,
        characters=[sid, raymond, bao]
    )
    
    # Initial world state
    world.update_world_state({
        "life_support_hours_remaining": 24.0,
        "system_malfunctions": True,
        "diagnostic_logs_accessed": True,
        "emergency_protocols_active": True,
        "communications_status": "intermittent"
    })
    
    return world

def main():
    """Main function to run the interactive story"""
    # Set up the scenario
    world = setup_space_station_scenario()
    
    # Create the story engine with Sid as the player character
    story_engine = StoryEngine(world, "Sid")
    
    # Run the interactive story
    story_engine.run_interactive_story()

if __name__ == "__main__":
    main()