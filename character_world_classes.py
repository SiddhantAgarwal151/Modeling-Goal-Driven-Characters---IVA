import random
from typing import Dict, List, Tuple, Any, Optional
import json

class Character:
    def __init__(self, name: str, initial_emotions: Dict[str, float], 
                 initial_beliefs: Dict[str, float], 
                 initial_goals: Dict[str, Dict[str, float]]):
        """
        Initialize a character with name, emotions, beliefs, and goals.
        
        Args:
            name: Character's name
            initial_emotions: Dictionary of emotions and their intensity (0.0 to 1.0)
            initial_beliefs: Dictionary of beliefs and their probability (0.0 to 1.0)
            initial_goals: Dictionary of goals categorized as task or emotional with priority
        """
        self.name = name
        self.emotions = initial_emotions  # e.g., {"fear": 0.2, "suspicion": 0.5}
        self.beliefs = initial_beliefs    # e.g., {"station_safe": 0.8, "sid_hiding": 0.5}
        self.goals = initial_goals        # e.g., {"task": {"fix_station": 0.9}, "emotional": {"maintain_authority": 0.8}}
        self.theory_of_mind = {}          # Will store beliefs about other characters' beliefs
        
    def initialize_theory_of_mind(self, other_characters: List["Character"]):
        """Initialize beliefs about what other characters believe"""
        for character in other_characters:
            if character.name != self.name:
                self.theory_of_mind[character.name] = {}
                # For each belief this character has
                for belief_key, belief_value in self.beliefs.items():
                    # Initialize a belief about what the other character thinks
                    # This could be the same or different from their own belief
                    variation = random.uniform(-0.2, 0.2)  # Add some variation
                    tom_value = max(0.0, min(1.0, belief_value + variation))  # Keep within [0,1]
                    
                    # Store what this character thinks the other character believes
                    self.theory_of_mind[character.name][belief_key] = tom_value
    
    def update_state(self, new_emotions: Dict[str, float], new_beliefs: Dict[str, float], 
                     new_tom: Dict[str, Dict[str, float]], new_goals: Dict[str, Dict[str, float]]):
        """Update character's emotional state, beliefs, theory of mind, and goals"""
        # Update emotions
        for emotion, value in new_emotions.items():
            if emotion in self.emotions:
                self.emotions[emotion] = max(0.0, min(1.0, value))  # Keep within [0,1]
            else:
                self.emotions[emotion] = value
        
        # Update beliefs
        for belief, value in new_beliefs.items():
            self.beliefs[belief] = max(0.0, min(1.0, value))  # Keep within [0,1]
        
        # Update theory of mind
        for character_name, beliefs in new_tom.items():
            if character_name not in self.theory_of_mind:
                self.theory_of_mind[character_name] = {}
            for belief, value in beliefs.items():
                self.theory_of_mind[character_name][belief] = max(0.0, min(1.0, value))
        
        # Update goals
        for goal_type, goals in new_goals.items():
            if goal_type not in self.goals:
                self.goals[goal_type] = {}
            for goal, value in goals.items():
                self.goals[goal_type][goal] = max(0.0, min(1.0, value))
    
    def get_state_for_prompt(self) -> Dict[str, Any]:
        """Return a formatted version of the character state for GPT prompting"""
        return {
            "name": self.name,
            "emotions": self.emotions,
            "beliefs": self.beliefs,
            "theory_of_mind": self.theory_of_mind,
            "goals": self.goals
        }
    
    def __str__(self) -> str:
        """String representation of character for debugging"""
        return (f"Character: {self.name}\n"
                f"Emotions: {json.dumps(self.emotions, indent=2)}\n"
                f"Beliefs: {json.dumps(self.beliefs, indent=2)}\n"
                f"Theory of Mind: {json.dumps(self.theory_of_mind, indent=2)}\n"
                f"Goals: {json.dumps(self.goals, indent=2)}")


class World:
    def __init__(self, setting: str, background: str, characters: List[Character]):
        """
        Initialize the world with setting, background story, and characters.
        
        Args:
            setting: Brief description of the world setting
            background: Background story information
            characters: List of Character objects in this world
        """
        self.setting = setting
        self.background = background
        self.characters = {character.name: character for character in characters}
        self.state = {}  # Will store world state variables
        self.history = []  # Store a history of events and interactions
        
        # Initialize Theory of Mind for all characters
        for character in characters:
            character.initialize_theory_of_mind(characters)
    
    def update_world_state(self, new_state: Dict[str, Any]):
        """Update the world state with new information"""
        for key, value in new_state.items():
            self.state[key] = value
    
    def add_to_history(self, event: str):
        """Add an event to the world history"""
        self.history.append(event)
    
    def get_state_for_prompt(self) -> Dict[str, Any]:
        """Return a formatted version of the world state for GPT prompting"""
        return {
            "setting": self.setting,
            "background": self.background,
            "state": self.state,
            "characters": {name: char.get_state_for_prompt() for name, char in self.characters.items()},
            "recent_history": self.history[-5:] if self.history else []  # Last 5 events or empty list
        }
    
    def __str__(self) -> str:
        """String representation of world for debugging"""
        return (f"World Setting: {self.setting}\n"
                f"Background: {self.background}\n"
                f"State: {json.dumps(self.state, indent=2)}\n"
                f"Characters: {', '.join(self.characters.keys())}\n"
                f"History: {len(self.history)} events")