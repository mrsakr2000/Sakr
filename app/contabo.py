import os
import requests

CONTABO_CLIENT_ID = os.getenv('CONTABO_CLIENT_ID')
CONTABO_CLIENT_SECRET = os.getenv('CONTABO_CLIENT_SECRET')
TOKEN_URL = os.getenv('CONTABO_TOKEN_URL', 'https://auth.contabo.com/auth/realms/contabo/protocol/openid-connect/token')
API_BASE = 'https://api.contabo.com'

class ContaboAPI:
    def __init__(self):
        self.token = None

    def authenticate(self):
        data = {
            'client_id': CONTABO_CLIENT_ID,
            'client_secret': CONTABO_CLIENT_SECRET,
            'grant_type': 'client_credentials'
        }
        response = requests.post(TOKEN_URL, data=data)
        response.raise_for_status()
        self.token = response.json()['access_token']

    def _headers(self):
        if not self.token:
            self.authenticate()
        return {'Authorization': f'Bearer {self.token}'}

    def list_plans(self):
        url = f'{API_BASE}/vps/plans'
        r = requests.get(url, headers=self._headers())
        r.raise_for_status()
        return r.json()

    def create_vps(self, plan_id, region, os_id):
        url = f'{API_BASE}/vps'
        payload = {
            'productId': plan_id,
            'region': region,
            'imageId': os_id
        }
        r = requests.post(url, json=payload, headers=self._headers())
        r.raise_for_status()
        return r.json()

    def get_vps(self, vps_id):
        url = f'{API_BASE}/vps/{vps_id}'
        r = requests.get(url, headers=self._headers())
        r.raise_for_status()
        return r.json()
