import subprocess

people = [
        "eika",
        "fredrik",
        "peter",
        "knut",
        "dsr"
        ]

if __name__ == "__main__":
    output = subprocess.check_output("./find_hosts.sh", shell=True)

    print(output.decode("utf-8"))
