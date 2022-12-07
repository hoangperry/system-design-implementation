import time
import socket
import requests
from datetime import datetime


HASH_SERVICE = 'http://127.0.0.1:8000/?value='
EXTERNAL_API_SERVICE = 'https://api.ipify.org'


# Limit of ID Generator is 2199023255552 millisecond from this date, around ~69 years
dt_obj = datetime.strptime('7.12.2022 00:00:00,01', '%d.%m.%Y %H:%M:%S,%f')
ANCHOR_TIME = int(dt_obj.timestamp() * 1000)


class IdGen:
    def __init__(self, hash_service=None, machine_id=None):
        self.hash_service = HASH_SERVICE if hash_service is None else hash_service
        # Machine ID muse less than ~1000 (less than 10 bit)
        # Ideally the machine ID must split to 2 element is Cluster/Datacenter IDs and Machine/Service IDs
        self.machine_id = self.__get_machine_id() if machine_id is None else machine_id
        self.last_time: int = self.get_timestamp()
        self.sequence = 0

    @staticmethod
    def get_timestamp():
        # Improve here
        return int(((time.time() * 1000)-ANCHOR_TIME) % (10 ** 11))

    @staticmethod
    def get_machine_external_ip():
        # Improve here by using internal service
        return requests.get(EXTERNAL_API_SERVICE).content.decode('utf8')

    def set_timestamp(self, tt):
        if tt != self.last_time:
            self.last_time = tt
            self.sequence = 0

    def __get_machine_id(self):
        url = self.hash_service + self.get_machine_external_ip() + '_' + socket.gethostname()
        response = requests.request("POST", url, headers={}, data={})
        return response.json()['id']

    def generate(self):
        self.set_timestamp(self.get_timestamp())
        final = (((self.last_time << 10) + self.machine_id) << 5) + self.sequence
        self.sequence += 1
        return final


"""
Test ID gen
"""
if __name__ == '__main__':
    gene = IdGen(machine_id=123)
    print(gene.machine_id)
    list_id = list()
    for i in range(100000000):
        if i in list_id:
            print("FFF" * 100)
            break
        print(gene.generate())
