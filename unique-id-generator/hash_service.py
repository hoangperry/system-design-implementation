import os
import pickle
import uvicorn
from fastapi import FastAPI


class FakeHashTable:
    def __init__(self, bit_limitation=10):
        self.limitation = 2 ** bit_limitation
        self.hashtable = dict()
        self.id_list = set()
        self.history = list()
        self.avail_id = list(range(self.limitation))

    def hash(self, value, replacement=None):
        """
        :param value: value to hash
        :param replacement: if replacement = 'oldest' this instance will replace the object by the oldest record. If
        replacement is the value that existed in hashtable, it will remove old record and replace by new value.
        :return:
        """
        # For user replace ID by a new value
        if replacement is not None:
            if replacement == 'oldest' and self.history.__len__() > 2:
                old_id = self.hashtable[self.history[0]]
                del self.hashtable[self.history[0]]
                self.history = self.history[1:]
                self.history.append(value)
                self.hashtable[value] = old_id

            if replacement in self.hashtable:
                old_id = self.hashtable[replacement]
                self.history.remove(old_id)
                self.history.append(value)
                del self.hashtable[replacement]
                self.hashtable[value] = old_id
                return old_id
            return None

        if value in list(self.hashtable.keys()):
            return self.hashtable[value]

        # If larger than 10 bit, return None
        if self.hashtable.items().__len__() > self.limitation:
            return None

        # Add new ID
        new_id = self.avail_id.pop(0)
        self.history.append(value)
        self.id_list.add(new_id)
        self.hashtable[value] = new_id
        return new_id

    def remove(self, value):
        if value not in self.hashtable:
            return False
        old_id = self.hashtable[value]
        del self.hashtable[value]
        self.id_list.remove(value)
        self.avail_id.append(old_id)
        self.history.remove(value)


def backup_htb_object(in_htb):
    with open('./database/FakeHashTable.pickle', 'wb') as ff:
        pickle.dump(in_htb, ff)


def load_htb_object():
    with open('./database/FakeHashTable.pickle', 'rb') as ff:
        data = pickle.load(ff)
    return data


app = FastAPI()

if os.path.exists('./database/FakeHashTable.pickle'):
    htb = load_htb_object()
else:
    htb = FakeHashTable()


@app.post("/")
async def get_machine_id(value):
    iid = htb.hash(value)
    backup_htb_object(htb)
    return {"id": iid}


if __name__ == '__main__':
    uvicorn.run(
        "hash_service:app",
        host='0.0.0.0',
        port=8000,
        reload=True,
        debug=True,
        workers=3
    )
