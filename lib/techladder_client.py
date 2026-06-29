import os
import time
from datetime import datetime

import requests
from dotenv import load_dotenv


class TechladderClient:
    def __init__(self):
        load_dotenv()

        self.api_key = os.getenv("API_KEY")
        self.base_url = os.getenv("BASE_URL")
        self.agent_name = os.getenv("AGENT_NAME")

        self.voice = os.getenv("VOICE", "Kavya")
        self.did_number_id = os.getenv("DID_NUMBER_ID")
        self.phone_number = os.getenv("PHONE_NUMBER")

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    # -------------------------
    # Authentication
    # -------------------------

    def authenticate(self):
        response = requests.get(
            f"{self.base_url}/api/v1/public/me",
            headers=self.headers,
        )

        response.raise_for_status()

        print("Authentication Passed")

        return response.json()

    # -------------------------
    # Agents
    # -------------------------

    def list_agents(self):
        response = requests.get(
            f"{self.base_url}/api/v1/public/agents",
            headers=self.headers,
        )

        response.raise_for_status()

        return response.json()

    def get_agent(self):
        data = self.list_agents()

        agents = data["data"]["items"]

        for agent in agents:
            if agent["agent_name"] == self.agent_name:
                print(f"Agent Found: {agent['agent_id']}")
                print(f"Version Found: {agent['current_version']}")

                return {
                    "agent_id": agent["agent_id"],
                    "version_id": agent["current_version"],
                }

        raise Exception(f"Agent '{self.agent_name}' not found")

    # -------------------------
    # Batch
    # -------------------------

    def create_batch(self):
        agent = self.get_agent()

        payload = {
            "agent_name": agent["agent_id"],
            "version_name": agent["version_id"],
            "voice": self.voice,
            "did_number_id": self.did_number_id,
            "interruption": True,
            "use_alternate_number": False,
            "start_mode": "immediate",
            "schedule_date": datetime.now().strftime("%Y-%m-%d"),
            "schedule_time": datetime.now().strftime("%H:%M"),
            "timezone": "Asia/Kolkata",
            "contacts": [
                {
                    "external_id": "101",
                    "name": "Automation Test",
                    "phone_number": self.phone_number,
                }
            ],
        }

        response = requests.post(
            f"{self.base_url}/api/v1/public/call-batches",
            headers=self.headers,
            json=payload,
        )

        response.raise_for_status()

        batch_id = response.json()["data"]["batch_id"]

        print(f"Batch Created: {batch_id}")

        return batch_id

    def get_batch(self, batch_id):
        response = requests.get(
            f"{self.base_url}/api/v1/public/call-batches/{batch_id}",
            headers=self.headers,
        )

        response.raise_for_status()

        print("Batch Retrieved")

        return response.json()

    def get_call_result(self, call_id):
        response = requests.get(
            f"{self.base_url}/api/v1/public/calls/{call_id}/result",
            headers=self.headers,
        )

        response.raise_for_status()

        print("\n========== CALL RESULT ==========")
        print(response.json())
        print("=================================\n")

        return response.json()

    # -------------------------
    # Poll Results
    # -------------------------
    def poll_results(self, batch_id, timeout=180, interval=5):
        start = time.time()

        while time.time() - start < timeout:

            response = requests.get(
                f"{self.base_url}/api/v1/public/call-batches/{batch_id}/results",
                headers=self.headers,
            )

            response.raise_for_status()

            data = response.json()
            items = data.get("data", {}).get("items", [])

            if not items:
                print("Waiting for results...")
                time.sleep(interval)
                continue

            result = items[0]

            call_id = result.get("call_id")

            if (
                result.get("call_status") in ["completed", "failed"]
                and call_id
            ):
                self.get_call_result(call_id)

            print("\n========== CALL DETAILS ==========")
            print("Batch Status      :", data["data"].get("status"))
            print("Call Status       :", result.get("call_status"))
            print("Transcript Status :", result.get("transcript_status"))
            print("Duration          :", result.get("duration_seconds"))
            print("Completed At      :", result.get("completed_at"))
            print("Disconnect Reason :", result.get("disconnect_reason"))
            print("Outcomes          :", result.get("outcomes"))
            print("Summary           :", result.get("summary"))
            print("Transcript        :", result.get("llm_transcript"))
            print("Recording         :", result.get("recording_available"))
            print("==================================\n")

            # Verify relevant fields for fake call
            if (
                data["data"].get("status") == "completed"
                and result.get("call_status") == "failed"
                and result.get("completed_at") is not None
                and result.get("duration_seconds") == 0
            ):
                print("\n========== VALIDATION ==========")
                print("Batch Status Verified : completed")
                print("Call Status Verified  : failed")
                print("Completed At Verified : Present")
                print("Duration Verified     : 0")
                print("Validation PASSED")
                print("================================\n")
                return True

            print("Waiting for call completion and summary...\n")
            time.sleep(interval)

        raise Exception("FAILED: Summary not generated within timeout.")