#!/usr/bin/env python

from datetime import datetime

import time

import requests

API_KEY = None
try:
    CONF = json.load(open('conf.json', 'r'))
    URL = CONF['url']
    API_KEY = CONF['api_key']
except:
    pass

class HealthChecker(object):
    def __init__(self, url):
        self.url = url
        self.down_since = None

    def run(self, delay=60):
        while True:
            self.check()
            time.sleep(delay)

    def check(self):
        print "Checking"
        r = requests.get(self.url, timeout=20)
        print "Response code {}, OK={}".format(r.status_code, r.ok)
        if not r.ok:
            self.record_down()
        else:
            self.record_ok()

    def record_down(self):
        now = datetime.now()
        if self.down_since is not None:
            self.down_since = now
        print("Down for {} since {}".format(
            now - self.down_since, self.down_since))
        self.note_time('FAIL.txt', self.down_since)

    def record_ok(self):
        now = datetime.now()
        self.note_time("OK.txt")
        if self.down_since is not None:
            push("Internet back!", self.url,
                    "Down since {}; duration {}".format(
                        self.down_since, now - self.down_since))
        self.down_since = None

    def note_time(self, filename, now=None):
        if now is None:
            now = datetime.now()
        with open(filename, 'w+') as out:
            out.write(str(now))
            out.write("\n")

def push(title, url, message):
    if API_KEY is None:
        print("Can't push to Pushbullet without an API key!")
    else:
        r = requests.post("https://api.pushbullet.com/v2/pushes",
                data=dict(title=title, url=url, body=message, type="link"),
                auth=(API_KEY, None))

if __name__ == '__main__':
    HealthChecker('http://google.com').run(60)
