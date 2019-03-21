import pickle


def save(path, data):
    with open(path, 'wb') as f:
        pickle.dump(data, f)


def load(path):
    with open(path, 'rb') as f:
        return pickle.load(f)


data = {
    'a': 'a'
}
