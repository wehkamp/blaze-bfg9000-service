from __future__ import print_function

import logging
import os
import random
import requests

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from flask import Flask


SERVICE_PORT = int(os.environ.get('SERVICE_PORT', 5000))
MARATHON = str(os.environ.get('MARATHON_HOST', 'marathon.service.consul'))
MIN_CONTAINERS = int(os.environ.get('MIN_CONTAINERS', 2))
MIN_LIFETIME_SECS = int(os.environ.get('MIN_LIFETIME_SECS', 300))
INTERVAL_SECONDS = int(os.environ.get('RUNTIME_INTERVAL_SECS', 300))
AMMO = int(os.environ.get('AMMO', 5))

url = 'http://%s:8080/v2/tasks' % MARATHON
logging.basicConfig(level=logging.os.environ.get('LOG_LEVEL', 'INFO'))


def shoot(container):
    logging.info("BANG! [fragged:%s]" % (container))
    requests.post(url + '/d', {
        "ids": [container]
    }).json()


def take_aim():
    clip = AMMO
    targets = {}
    tasks = requests.get(url).json()
    quad_damage = False

    if random.random() * 10 > 8:
        logging.info('#~> picked up QUAD DAMAGE')
        quad_damage = True

    if random.random() * 10 > 8:
        logging.info('#~> picked up AMMO')
        clip += AMMO

    for t in tasks['tasks']:
        app_name = t['appId'].strip('/')
        id = t['id']

        # TODO: don't kill $self unless GOD-mode is enabled
        # if app_name == SELF:
        #    continue

        if t['state'] != 'TASK_RUNNING':
            logging.info('#~> Player connecting to game')
            continue

        started = datetime.strptime(t['startedAt'], '%Y-%m-%dT%H:%M:%S.%fZ')
        now = datetime.now()
        if (now - started).total_seconds() < MIN_LIFETIME_SECS:
            logging.info('#~> Spawn kills disabled by server [%s]' % app_name)
            continue

        if app_name in targets:
            targets[app_name].add(id)
        else:
            targets[app_name] = {id}

    imps = targets.items()
    random.shuffle(imps)
    for app, containers in imps:
        if len(containers) > MIN_CONTAINERS:
            if clip > 0:
                clip -= 1
                shoot(random.choice(tuple(containers)))
                if quad_damage:
                    shoot(random.choice(tuple(containers)))


app = Flask(__name__)


@app.route("/")
def home():
    return """<h3>BFG9000</h3>"""


@app.route("/status")
def status():
    return "OK"


@app.route("/metrics")
def metrics():
    return """# not implemented"""


def run():
    logging.info('#~> /give BFG9000')

    take_aim()

    scheduler = BackgroundScheduler({'apscheduler.timezone': 'UTC'})
    scheduler.add_job(take_aim, 'interval', seconds=INTERVAL_SECONDS)
    scheduler.start()

    try:
        app.run(host="0.0.0.0", port=SERVICE_PORT, threaded=False)
    finally:
        scheduler.shutdown()
