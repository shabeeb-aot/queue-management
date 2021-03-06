# Copyright © 2019 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Submit Citizen feedback.

This module consists of API that calls Camunda BPM to save citizen feedback comments.
"""
import os, requests, json
from typing import Dict
from .feedback_base_service import FeedbackBaseService
from flask import jsonify


class FeedbackCamundaService(FeedbackBaseService):
    """Implementation from FeedbackService."""

    def submit(self, payload):
        """Submit feedback to Camunda API"""
        camunda_service_endpoint = os.getenv('FEEDBACK_CAMUNDA_URL')
        keycloak_endpoint = os.getenv('FEEDBACK_AUTH_URL')
        keycloak_client_id = os.getenv('FEEDBACK_AUTH_CLIENT_ID')
        keycloak_client_secret = os.getenv('FEEDBACK_AUTH_CLIENT_SECRET')
        
        auth_payload = {"grant_type":"client_credentials",
                "client_id":keycloak_client_id,
                "client_secret":keycloak_client_secret}
        auth_response = requests.post(keycloak_endpoint,data=auth_payload)
        access_token = auth_response.json()['access_token']
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {access_token}'}
        feedback_response = requests.post(camunda_service_endpoint,
                            headers=headers,
                            data=json.dumps(payload))
        print(feedback_response.json())
        return feedback_response.status_code
        
