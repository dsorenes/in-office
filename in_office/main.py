import subprocess
import logging
from difflib import SequenceMatcher

from flask_apscheduler import APScheduler
from flask import Flask

class Config:
    SCHEDULER_API_ENABLED = True

app = Flask(__name__)
app.config.from_object(Config())

scheduler = APScheduler()
scheduler.init_app(app)

people = {
        "eika": "Kenneth",
        "frederiglitner": "Fredrik",
        "peter": "Peter",
        "knut": "Knut",
        "dsr": "Daniel",
        "reidar": "Reidar",
        "axel": "Axel"
        }

people_at_the_office = []

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

@scheduler.task('interval', id='scan_network_job', minutes=10)
def run_nmap():
    logging.info("Scanning connected hosts...")
    subprocess.run("nmap -aP 192.168.1.0/24")

@scheduler.task('interval', id='in_the_office_job', seconds=30)
def in_the_office():

    global people_at_the_office
    people_at_the_office = []
    logging.info("Checking who's at the office")
    connected_hosts = subprocess.run("./find_hosts.sh", universal_newlines=True, stdout=subprocess.PIPE)

    hosts = connected_hosts.stdout.split("\n")

    for host in hosts:
        host_name = host.split(" ")[0][:-4].split("-")[0]
        if len(host_name) == 0:
            continue
        for person in people.keys():
            similarity = similar(person, host_name)
            p = people.get(person)
            logging.info(f"Person: {p}, Host: {host_name}, Similarity: {similarity}")
            if similarity > 0.65 and p not in people_at_the_office:
                people_at_the_office.append(p)
                break
    logging.info(f"people at the office: {people_at_the_office}")

@app.route("/check")
def check():
    return people_at_the_office

if __name__ == "__main__":
    scheduler.start()

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    app.run()
