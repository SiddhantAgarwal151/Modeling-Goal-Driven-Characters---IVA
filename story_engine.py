import json
import re
import openai
import os
from dotenv import load_dotenv
from typing import Dict, List, Tuple, Any, Optional
from character_world_classes import Character, World

# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

class OCCAppraisalModel:
    def __init__(self):
        """
        Initialize the OCC Appraisal Model for emotion updates.
        This model evaluates events and updates character emotional states.
        """
        pass
    
    def generate_appraisal_prompt(self, character: Character, world: World, action: str) -> str:
        """
        Generate a prompt for GPT to appraise an action based on OCC model and structured decision making.
        
        Args:
            character: The character doing the appraisal
            world: The current world state
            action: The action being appraised
            
        Returns:
            Prompt string for GPT
        """
        world_state = world.get_state_for_prompt()
        character_state = character.get_state_for_prompt()
        
        # Create prompt for GPT to evaluate the action
        prompt = f"""
        # OCC Appraisal Model Evaluation
        
        ## World State
        {json.dumps(world_state, indent=2)}
        
        ## Character Performing Appraisal
        {json.dumps(character_state, indent=2)}
        
        ## Action to Appraise
        {action}
        
        ## Task
        The following describes standardized procedures for updating the character's state based on the action. This follows the OCC model for cognitive appraisal of emotion.

        **Standardized State Update Procedure:**
        After analyzing the action, update the states of the character by following these guidelines:

        **a. Appraisal of the action:**
        - **Goal Congruence:**
            - If the event is assessed as *strongly hindering* a character’s goal, then:
            - Decrease the goal's priority by **0.10**.
            - Increase related negative emotions (e.g., anger, sadness) by **0.15**.
            - If the event is assessed as *moderately hindering* a character’s goal, then:
            - Decrease the goal's priority by **0.05**.
            - Increase related negative emotions by **0.10**.
            - If the event is assessed as *strongly facilitating* a goal, then:
            - Increase the goal's priority by **0.10**.
            - Increase related positive emotions (e.g., happiness) by **0.15**.
            - If the event is assessed as *moderately facilitating* a goal, then:
            - Increase the goal's priority by **0.05**.
            - Increase related positive emotions by **0.10**.
        - **Unexpectedness:**
            - For highly unexpected events, add a factor of +0.20 to arousal-based emotions (e.g., fear, surprise).
            - For moderately unexpected events, add +0.10.
        - **Responsibility Attribution:**
            - Note whether the event is self-caused, caused by another agent, or due to external factors, and adjust the corresponding emotions (e.g., guilt or defensiveness) by **0.10** accordingly.

        **b. Updating Emotions:**
        - For each character, update their emotional intensities (values are decimals between 0 and 1) as follows:
            - If an event strongly hinders an important goal, increase relevant negative emotions (e.g., anger, sadness) by +0.15.
            - If it moderately hinders a goal, increase them by +0.10.
            - If an event strongly facilitates a goal, increase relevant positive emotions (e.g., happiness) by +0.15; if moderately, by +0.10.
            - For a highly unexpected event, increase arousal-based emotions (e.g., fear, surprise) by +0.20.
        - After adjustments, ensure all emotion values are clamped between 0 and 1.

        **c. Updating Beliefs:**
        - If an event confirms a belief, increase the belief’s probability by +0.10.
        - If an event contradicts a belief, decrease it by -0.10.
        - Clamp belief probabilities between 0 and 1.

        **d. Updating Goals:**
        - If an event facilitates a goal, increase its priority by +0.10.
        - If an event blocks a goal, decrease its priority by -0.10.
        - Clamp goal priorities between 0 and 1.

        **e. Updating Theory of Mind:**
        - For each belief about another character, if an observed behavior supports that belief, increase its value by +0.10; if it contradicts, decrease it by -0.10.
        - Clamp these values between 0 and 1.
        
        ## Output Format
        Return a JSON object with the following structure:
        ```json
        {{
            "emotional_updates": {{
                "emotion_name": new_value,
                ...
            }},
            "belief_updates": {{
                "belief_name": new_value,
                ...
            }},
            "theory_of_mind_updates": {{
                "character_name": {{
                    "belief_name": new_value,
                    ...
                }},
                ...
            }},
            "goal_updates": {{
                "goal_type": {{
                    "goal_name": new_value,
                    ...
                }},
                ...
            }},
            "appraisal_explanation": "Explanation of why these changes occurred based on OCC model"
        }}
        ```
        """
        return prompt
    
    def appraise_action(self, character: Character, world: World, action: str) -> Dict[str, Any]:
        """
        Use GPT to appraise an action and return state updates.
        
        Args:
            character: The character performing the appraisal
            world: The current world state
            action: The action being appraised
            
        Returns:
            Dictionary of state updates for the character
        """
        prompt = self.generate_appraisal_prompt(character, world, action)
        
        try:
            # Call OpenAI API for appraisal
            response = openai.ChatCompletion.create(
                model="gpt-4", 
                messages=[
                    {"role": "system", "content": "You are an expert at modeling character emotions and beliefs using the OCC appraisal model."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            # Extract the result from the API response
            result_text = response.choices[0].message.content
            
            # Parse the JSON from the response
            # Look for JSON structure between ```json and ```
            json_match = re.search(r'```json\s*([\s\S]*?)\s*```', result_text)
            if json_match:
                result_json = json.loads(json_match.group(1))
            else:
                # If no JSON formatting, try to parse the whole text
                result_json = json.loads(result_text)
            
            return result_json
            
        except Exception as e:
            print(f"Error in appraisal: {e}")
            # Return empty updates if there's an error
            return {
                "emotional_updates": {},
                "belief_updates": {},
                "theory_of_mind_updates": {},
                "goal_updates": {},
                "appraisal_explanation": f"Error in appraisal: {e}"
            }


class StoryEngine:
    def __init__(self, world: World, player_character: str):
        """
        Initialize the interactive storytelling engine.
        
        Args:
            world: The World object containing characters and setting
            player_character: Name of the character controlled by the player
        """
        self.world = world
        self.player_character = player_character
        self.appraisal_model = OCCAppraisalModel()
    
    def generate_story_intro(self) -> str:
        """Generate and return the story introduction"""
        setting = self.world.setting
        background = self.world.background
        
        intro = f"""
        # {setting}
        
        {background}
        
        You are playing as {self.player_character}.
        """
        return intro
    
    def generate_action_prompt(self, user_input: str) -> str:
        """
        Generate a prompt for GPT to create the next story action.
        
        Args:
            user_input: The player's input as their character
            
        Returns:
            Prompt string for GPT
        """
        world_state = self.world.get_state_for_prompt()
        player_character = self.world.characters[self.player_character].get_state_for_prompt()
        
        prompt = f"""
        # Interactive Story Generation
        
        ## World State
        {json.dumps(world_state, indent=2)}
        
        ## Player Character
        {json.dumps(player_character, indent=2)}
        
        ## Player's Action
        {user_input}
        
        ## Task
        Generate the next part of the interactive story based on the player's action. 
        
        1. Determine how other characters would realistically react.
        2. Update the world state if necessary.
        3. Provide a narrative description of what happens.
        
        ## Output Format
        Return a JSON object with the following structure:
        ```json
        {{
            "narrative": "Description of what happens in the story",
            "character_actions": {{
                "character_name": "Description of this character's reaction",
                ...
            }},
            "world_state_updates": {{
                "state_key": new_value,
                ...
            }}
        }}
        ```
        """
        return prompt
    
    def process_player_input(self, user_input: str) -> Tuple[str, Dict[str, Any]]:
        """
        Process player input and update the story.
        
        Args:
            user_input: The player's input as their character
            
        Returns:
            Tuple of (narrative text, state updates)
        """
        prompt = self.generate_action_prompt(user_input)
        
        try:
            # Call OpenAI API for story generation
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an interactive storytelling engine creating a realistic sci-fi narrative."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            # Extract the result
            result_text = response.choices[0].message.content
            
            # Parse the JSON from the response
            json_match = re.search(r'```json\s*([\s\S]*?)\s*```', result_text)
            if json_match:
                result_json = json.loads(json_match.group(1))
            else:
                # If no JSON formatting, try to parse the whole text
                result_json = json.loads(result_text)
            
            # Update world state if needed
            if "world_state_updates" in result_json:
                self.world.update_world_state(result_json["world_state_updates"])
            
            # Add to world history
            self.world.add_to_history(user_input)
            self.world.add_to_history(result_json["narrative"])
            
            # Process character actions and update states
            for char_name, action in result_json.get("character_actions", {}).items():
                if char_name in self.world.characters:
                    # Skip player character as they're controlled by the player
                    if char_name == self.player_character:
                        continue
                    
                    # Appraise the action for this character
                    character = self.world.characters[char_name]
                    appraisal_result = self.appraisal_model.appraise_action(character, self.world, action)
                    
                    # Update character state based on appraisal
                    character.update_state(
                        appraisal_result.get("emotional_updates", {}),
                        appraisal_result.get("belief_updates", {}),
                        appraisal_result.get("theory_of_mind_updates", {}),
                        appraisal_result.get("goal_updates", {})
                    )
            
            return result_json["narrative"], result_json
            
        except Exception as e:
            print(f"Error processing input: {e}")
            return f"Error processing your input: {e}", {}
    
    def generate_npc_actions(self) -> Tuple[str, Dict[str, Any]]:
        """
        Generate actions for non-player characters.
        
        Returns:
            Tuple of (narrative text, state updates)
        """
        world_state = self.world.get_state_for_prompt()
        
        prompt = f"""
        # NPC Character Actions
        
        ## World State
        {json.dumps(world_state, indent=2)}
        
        ## Task
        Generate the next actions for the non-player characters in the story.
        Consider each character's goals, beliefs, and emotional state.
        Characters should act in ways that are consistent with their beliefs and goals.
        
        ## Output Format
        Return a JSON object with the following structure:
        ```json
        {{
            "narrative": "Description of what the NPCs do",
            "character_actions": {{
                "character_name": "Description of this character's action",
                ...
            }},
            "world_state_updates": {{
                "state_key": new_value,
                ...
            }}
        }}
        ```
        """
        
        try:
            # Call OpenAI API for NPC actions
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an interactive storytelling engine creating realistic character actions."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            # Extract the result
            result_text = response.choices[0].message.content
            
            # Parse the JSON from the response
            json_match = re.search(r'```json\s*([\s\S]*?)\s*```', result_text)
            if json_match:
                result_json = json.loads(json_match.group(1))
            else:
                # If no JSON formatting, try to parse the whole text
                result_json = json.loads(result_text)
            
            # Update world state if needed
            if "world_state_updates" in result_json:
                self.world.update_world_state(result_json["world_state_updates"])
            
            # Add to world history
            self.world.add_to_history(result_json["narrative"])
            
            # Process character actions and update states
            for char_name, action in result_json.get("character_actions", {}).items():
                if char_name in self.world.characters and char_name != self.player_character:
                    # Appraise the action for this character
                    character = self.world.characters[char_name]
                    appraisal_result = self.appraisal_model.appraise_action(character, self.world, action)
                    
                    # Update character state based on appraisal
                    character.update_state(
                        appraisal_result.get("emotional_updates", {}),
                        appraisal_result.get("belief_updates", {}),
                        appraisal_result.get("theory_of_mind_updates", {}),
                        appraisal_result.get("goal_updates", {})
                    )
            
            return result_json["narrative"], result_json
            
        except Exception as e:
            print(f"Error generating NPC actions: {e}")
            return f"Error generating NPC actions: {e}", {}
    
    def run_interactive_story(self):
        """Run the interactive storytelling loop"""
        # Print the intro
        print(self.generate_story_intro())
        
        # Main story loop
        while True:
            # Get player input
            user_input = input(f"\n[{self.player_character}] What do you do? ")
            
            # Check for quit command
            if "quit" in user_input.lower() or "exit" in user_input.lower():
                print("Ending the story. Thanks for playing!")
                break
            
            # Process player input and update world
            narrative, _ = self.process_player_input(user_input)
            print(f"\n{narrative}")
            
            # Let NPCs react
            npc_narrative, _ = self.generate_npc_actions()
            print(f"\n{npc_narrative}")
            
            # Optional: Print debug information about character states
            debug = input("Show character states? (y/n): ")
            if debug.lower() == "y":
                for name, character in self.world.characters.items():
                    print(f"\n{character}")