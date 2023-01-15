import string
import random
import pickle

class User:
    def __init__(self):
        try:
            with open('data.pickle', 'rb') as f:
                self.password = pickle.load(f)
        except:
            print('couldn\'t find password')
            self.password = self.generate_password(20)

    def generate_password(self, length):
        password = ''.join(random.choice(string.ascii_letters) for i in range(length))
        self.password = password
        with open('data.pickle', 'wb') as f:
            pickle.dump(password, f, pickle.HIGHEST_PROTOCOL)
            