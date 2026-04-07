import os
import requests

def main():
    api_base_url = os.environ.get("API_BASE_URL", "http://127.0.0.1:8080").rstrip('/')
    
    try:
        # First call /reset
        reset_response = requests.post(f"{api_base_url}/reset")
        reset_response.raise_for_status()
        
        # Then create a valid action
        action = {
            "review_comment": "Path traversal vulnerability due to unsanitized user input",
            "issue_type": "security",
            "severity": "high"
        }
        
        # Then call /step with this action
        step_response = requests.post(f"{api_base_url}/step", json={"action": action})
        step_response.raise_for_status()
        
        # Print the reward returned by the environment
        step_data = step_response.json()
        print(f"Reward: {step_data.get('reward')}")
        
    except requests.exceptions.RequestException as e:
        print(f"HTTP Request failed: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
