import json
import time
import socket
import requests


HASH_SERVICE = 'http://127.0.0.1:8000/?value='
EXTERNALAPI_SERVICE = 'https://api.ipify.org'

class IdGen:
    def __init__(self):
        self.machine_id = self.get_machine_id()
        self.last_time : int = 0
        self.sequence = 0

    @staticmethod
    def get_machine_external_ip():
        # Improve here by using internal service
        return requests.get(EXTERNALAPI_SERVICE).content.decode('utf8')

    def set_timestamp(self, tt):
        if tt == self.last_time:
            self.last_time = tt
            self.sequence = 0

    @staticmethod
    def get_timestamp():
        # Improve here
        return int((time.time() * 1000) % (10 ** 11))

    @staticmethod
    def get_machine_id():
        url = HASH_SERVICE + IdGen.get_machine_external_ip() + '_' + socket.gethostname()
        response = requests.request("POST", url, headers={}, data={})
        return response.json()['id']

    def generate(self):
        self.set_timestamp(self.get_timestamp())
        final = (((self.last_time << 10) + self.machine_id) << 5) + self.sequence
        self.sequence += 1
        return final


if __name__ == '__main__':
    gene = IdGen()
    print(gene.machine_id)
    list_id = list()
    for i in range(100000000):
        if i in list_id:
            print("FFF" * 100)
            break
        print(gene.generate())
