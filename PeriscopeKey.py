import hmac, hashlib, base64
import config as cfg
import requests
import json

class PeriscopeKey:
    public_key = cfg.public_key.encode('utf-8')
    private_key = cfg.private_key.encode('utf-8')

    def gen_signature(self, data):
        return base64.b64encode(hmac.new(self.private_key,
                                msg=data.encode('utf-8'),
                                digestmod=hashlib.sha256).digest())

    def is_valid_key(self):
        measurement = {}
        measurement["argument"] = "None"
        measurement["command"] = "traceroute"
        measurement["name"] = "test"
        measurement["hosts"] = None

        data = json.dumps(measurement)

        headers = {
            'Content-type': 'application/json; charset=utf-8',
            'X-Public': self.public_key,
            'X-Hash': self.gen_signature(data)
        }

        response = requests.post("https://periscope.caida.org/api/v2" + "/measurement",
                                 data=data,
                                 headers=headers)

        decoded_response = response.json()

        try:
            val = decoded_response['errors'][0]

        except:
            val = decoded_response['error'][0]

        if val == "Missing/empty 'hosts'":
            return True

        else:
            print("CAIDA Key could not be validated")
            return False