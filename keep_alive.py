from flask import Flask
from threading import Thread

app = Flask(__name__)


@app.route('/')
def index():
  return "Alive"


def run():
  app.run(host='0.0.0.0', port=8081)


def keep_alive():
  t = Thread(target=run, daemon=True)
  t.start()
