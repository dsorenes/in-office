import subprocess
from difflib import SequenceMatcher

import schedule

people = {
        "eika": "Kenneth",
        "fredrik": "Fredrik",
        "peter": "Peter",
        "knut": "Knut",
        "dsr": "Daniel"
        }

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

@schedule.repeat(schedule.every(10).minutes)
def run_nmap():
    print("Scanning connected hosts...")
    subprocess.run("nmap -aP 192.168.1.0/24")

@schedule.repeat(schedule.every(5).seconds)
def in_the_office():
    print("Checking who's at the office")
    connected_hosts = subprocess.run("./find_hosts.sh", universal_newlines=True, stdout=subprocess.PIPE)

    hosts = connected_hosts.stdout.split("\n")

    people_at_the_office = []

    for host in hosts:
        host_name = host.split(" ")[0][:-4].split("-")[0]
        for person in people.keys():
            similarity = similar(person, host_name)
            if similarity > 0.5:
                people_at_the_office.append(people.get(person))
    print(f"people at the office: {people_at_the_office}")


if __name__ == "__main__":
    while True:
        schedule.run_pending()
