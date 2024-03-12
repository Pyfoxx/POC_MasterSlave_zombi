from hashlib import md5
def main(password):
    return md5(password.encode()).hexdigest()