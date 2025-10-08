import time
import random

# --- Configuration ---
# Mock identifiers for different devices (replace with actual IoT device IDs/topics)
DEVICE_TOPICS = {
    "living_room_light": "iot/lights/lr",
    "thermostat": "iot/hvac/temp",
    "emergency_button": "iot/alerts/panic"
}

# --- Core System Classes ---

class IoTController:
    """
    Handles communication with physical IoT devices (lights, thermostat, etc.).
    In a real system, this would use MQTT, CoAP, or a proprietary API.
    """
    def send_command(self, topic: str, command: dict):
        """Mocks sending a command to an IoT device."""
        print(f"📡 IoT: Sending command to '{topic}' -> {command}")
        # Placeholder for actual MQTT/API publishing code
        # Example: mqtt_client.publish(topic, json.dumps(command))
        
    def get_status(self, topic: str) -> dict:
        """Mocks getting the current status from an IoT device."""
        # Placeholder for actual MQTT subscription or API GET request
        if topic == DEVICE_TOPICS["thermostat"]:
            return {"temperature": random.uniform(19.0, 25.0), "unit": "C"}
        return {"status": "ON" if random.choice([True, False]) else "OFF"}

class AIModule:
    """
    Implements adaptive logic based on user profile, time, and sensor data.
    """
    def __init__(self, user_profile: dict):
        self.profile = user_profile
    
    def analyze_and_suggest_climate(self, current_temp: float) -> float:
        """Adaptive AI logic for climate control."""
        desired_temp = self.profile.get("preferred_temp", 22.0)
        
        # Simple adaptive logic: adjust based on a delta
        if current_temp < desired_temp - 1.0:
            adjustment = desired_temp + 0.5 # Warm it up slightly more
        elif current_temp > desired_temp + 1.0:
            adjustment = desired_temp - 0.5 # Cool it down slightly more
        else:
            adjustment = desired_temp # Maintain preferred temp

        print(f"🧠 AI: Current temp {current_temp}°C. Setting new target: {adjustment:.1f}°C")
        return adjustment
        
    def determine_lighting_state(self, time_of_day: str, motion_detected: bool) -> str:
        """Adaptive AI logic for lighting control."""
        if time_of_day == "Night" and motion_detected:
            return "LOW" # Soft light at night for safety
        elif time_of_day == "Day" and motion_detected:
            return "ON"
        return "OFF"
        
class NotificationService:
    """
    Handles alerts and notifications to caregivers/medical services.
    """
    def send_emergency_alert(self, reason: str, location: str):
        """Mocks sending a critical alert via SMS, email, or a dedicated app."""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        message = (f"🚨 EMERGENCY ALERT! Reason: {reason}. Location: {location}. "
                   f"Time: {timestamp}. Contacting Caregiver.")
        print("-" * 50)
        print(f"!!! {message} !!!")
        print("-" * 50)
        # Placeholder for actual Twilio SMS, Email API, or secure cloud messaging

class SmartHomeSystem:
    """
    The main coordinator for the entire smart home project.
    """
    def __init__(self, user_profile: dict):
        self.iot = IoTController()
        self.ai = AIModule(user_profile)
        self.notifications = NotificationService()
        print("✅ Smart Home System Initialized.")
    
    def handle_voice_command(self, command_text: str):
        """
        Mocks the result of a Voice Recognition API (e.g., Google's Speech-to-Text).
        """
        print(f"\n🎙️ Voice Command Received: '{command_text}'")
        command_text = command_text.lower()
        
        if "light" in command_text and ("on" in command_text or "off" in command_text):
            action = "ON" if "on" in command_text else "OFF"
            self.iot.send_command(DEVICE_TOPICS["living_room_light"], {"state": action})
            
        elif "temperature" in command_text and "set" in command_text:
            # Simple keyword extraction (in a real system, NLP would be used)
            try:
                temp_val = float(''.join(filter(str.isdigit, command_text.split("degrees")[0].split("set to")[-1])))
                self.iot.send_command(DEVICE_TOPICS["thermostat"], {"target_temp": temp_val})
            except ValueError:
                print("Error: Could not extract temperature value.")
                
        elif "help" in command_text or "emergency" in command_text:
            self.notifications.send_emergency_alert("Voice Triggered Panic", "Living Room")
            
        else:
            print("System: Command not understood.")
            
    def automated_climate_control(self):
        """Runs the adaptive climate control loop."""
        print("\n⚙️ Running Automated Climate Control...")
        
        # 1. Get current status
        status = self.iot.get_status(DEVICE_TOPICS["thermostat"])
        current_temp = status.get("temperature", 22.0)
        
        # 2. Analyze with AI
        new_target = self.ai.analyze_and_suggest_climate(current_temp)
        
        # 3. Send new command
        self.iot.send_command(DEVICE_TOPICS["thermostat"], {"target_temp": new_target})

    def automated_lighting_control(self, motion: bool, current_hour: int):
        """Runs the adaptive lighting control loop."""
        print("\n💡 Running Automated Lighting Control...")
        
        # Determine time of day
        if 6 <= current_hour < 18:
            time_of_day = "Day"
        else:
            time_of_day = "Night"
            
        # 1. Analyze with AI
        new_state = self.ai.determine_lighting_state(time_of_day, motion)
        
        # 2. Send new command
        self.iot.send_command(DEVICE_TOPICS["living_room_light"], {"state": new_state})
    
    def simulate_emergency(self):
        """Triggers a non-voice emergency, e.g., from a fall sensor."""
        self.notifications.send_emergency_alert("Fall Detected by Sensor", "Bedroom")

# --- Main Execution ---

if __name__ == "__main__":
    # Define a profile for the user with disabilities
    user_profile_data = {
        "name": "Alex",
        "preferred_temp": 24.0, # Example preference
        "time_to_bed": 21
    }

    system = SmartHomeSystem(user_profile_data)
    
    # 1. Voice Command Feature Test
    print("\n--- 1. Voice Recognition Test ---")
    system.handle_voice_command("Turn the living room light ON")
    system.handle_voice_command("Emergency, I need help!")
    system.handle_voice_command("Please set the temperature to 21 degrees")
    
    # 2. Automated Climate Control Feature Test
    print("\n--- 2. Automated Climate Control Test (AI) ---")
    # Simulate current room temp is too cold (e.g., 20.5 C)
    system.iot.get_status = lambda topic: {"temperature": 20.5, "unit": "C"} 
    system.automated_climate_control()

    # 3. Automated Lighting Control Feature Test
    print("\n--- 3. Automated Lighting Control Test (AI) ---")
    # Test during the day (e.g., hour 14:00) with motion
    system.automated_lighting_control(motion=True, current_hour=14)
    # Test during the night (e.g., hour 22:00) with motion
    system.automated_lighting_control(motion=True, current_hour=22)
    
    # 4. Emergency Alert Feature Test (Non-Voice)
    print("\n--- 4. Sensor-Based Emergency Alert Test ---")
    system.simulate_emergency()

    print("\nSystem simulation complete.")