from django.conf import settings
import requests

class Payment:
    ETRANZACT_SECRET_KEY = settings.ETRANZACT_SECRET_KEY
    base_url = 'https://api.credocentral.com/credo-payment/v1/payments/initiate'
    
    def verify_payment(self, ref, *args, **kwargs):
        path = f'/transactions/{ref}/verify'
        
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {settings.ETRANZACT_PUBLIC_KEY}'
        }
        url = self.base_url + path
        response = requests.get(url, headers=headers)
        
        if response.status_code ==200:
            response_data = response.json()
            return response_data['status'], response_data['data']
        response_data = response.json()
        return response_data['status'], response_data['message']
        