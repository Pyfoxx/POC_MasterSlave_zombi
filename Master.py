import flask
import requests
import itertools

slaves = ["127.0.0.1:5001"]
app = flask.Flask(__name__)


def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))


def listener(port):
    app.run(port=port)


def makeEmIter(it, to):
    it = list(split(it, len(slaves)))
    for v, i in enumerate(slaves):
        req = requests.post(f"http://{i}", data={"target" : to, "iter" : it}, files={'file': open('md5.py', 'rb')})
        if req.status_code != 200:
            print(f"ERROR ON {i}")
    print("slaves started")


@app.route('/receive', methods=['POST'])
def receiver():
    print(flask.request.data)
    return "200"


def makeIt():
    string = "abcdefghijklmnopqrstuvwxyz"
    it = list(itertools.product(string, repeat=2))
    it = ["".join(i) for i in it]
    return it


@app.route('/start')
def start():
    makeEmIter(makeIt(), to="b2a5abfeef9e36964281a31e17b57c97")
    return "oui"

if __name__ == '__main__':
    listener(5005)

