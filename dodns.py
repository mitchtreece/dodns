#!/usr/bin/env python3

import os
import dotenv
import requests

from argparse import ArgumentParser
from sty import fg, bg, ef, rs

# Variables

dotenv.load_dotenv()

VERSION = "1.0.0"
DRY_RUN = os.getenv("DODNS_DRY_RUN", 0)
DOMAIN = os.getenv("DO_DOMAIN")
SUBDOMAINS = os.getenv("DO_SUBDOMAINS", "@")
TOKEN = os.getenv("DO_API_TOKEN")

# Arguments

parser = ArgumentParser()
parser.add_argument("-d", "--dry", help="run without performing any update actions", action="store_true")
args = parser.parse_args()

# Request session

records_url = f'https://api.digitalocean.com/v2/domains/{DOMAIN}/records/'
session = requests.Session()

# Dry run

is_dry_run = (args.dry or int(DRY_RUN) > 0)

# Functions

def precondition_vars():

    if not DOMAIN:

        print()
        print(fg.red + "🚫 Missing variable \"DO_DOMAIN\", exiting" + fg.rs)
        print()
        exit()

    if not SUBDOMAINS:

        # This should never happen, the DO_SUBDOMAINS variable
        # falls back to "@" by default if nothing is specified

        print()
        print(fg.red + "🚫 Missing variable \"DO_SUBDOMAINS\", exiting" + fg.rs)
        print()
        exit()

    if not TOKEN:

        print()
        print(fg.red + "🚫 Missing variable \"DO_API_TOKEN\", exiting" + fg.rs)
        print()
        exit()


def get_wan_ip():
    return requests.get('https://api.ipify.org').text.rstrip()


def get_subdomain_records():

    json = session.get(records_url).json()

    if "domain_records" in json:
        return json["domain_records"]
    else:
        return []


def find_subdomain_record_in_list(name, list):

    for record in list:
        if record["name"] == name:
            return record


def main():

    print(fg.red    + "______ ___________ _   _  _____ " + fg.rs)
    print(fg.red    + "|  _  \  _  |  _  \ \ | |/  ___|" + fg.rs)
    print(fg.red    + "| | | | | | | | | |  \| |\ `--. " + fg.rs)
    print(fg.red    + "| | | | | | | | | | . ` | `--. \\" + fg.rs)
    print(fg.red    + "| |/ /\ \_/ / |/ /| |\  |/\__/ /" + fg.rs)
    print(fg.red    + "|___/  \___/|___/ \_| \_/\____/ " + fg.rs)
    print(fg.yellow + "================================" + fg.rs)
    print(fg.green  + "DigitalOcean DNS" + fg.rs)
    print(fg.green  + "Version: " + VERSION + fg.rs)
    print(fg.green  + "Mitch Treece <@mitchtreece>" + fg.rs)
    print(fg.yellow + "================================" + fg.rs)

    precondition_vars()

    print(fg.yellow + "Domain: " + fg.blue + DOMAIN + fg.rs)
    print(fg.yellow + "Subdomains: " + fg.blue + SUBDOMAINS + fg.rs)
    print(fg.yellow + "Token: " + fg.blue + TOKEN + fg.rs)
    print(fg.yellow + "================================" + fg.rs)
    print()

    if is_dry_run:
        print(fg.yellow + "🌵 Running dry" + fg.rs)

    # Request session headers

    session.headers = {
        "Authorization": "Bearer " + TOKEN
    }

    # Get wan ip address

    print(fg.blue + "🌎 Getting WAN IP address" + fg.rs, end="")

    ip = get_wan_ip()

    if not ip:

        print(fg.blue + " ... " + fg.red + "failed" + fg.rs)
        exit()

    print(fg.blue + " ... " + fg.green + ip + fg.rs)

    # Subdomain records

    print(fg.blue + "📚 Fecthing records for " + fg.green + DOMAIN + fg.rs, end="")

    all_records = get_subdomain_records()
    valid_records = []

    if not all_records:

        print(fg.blue + " ... " + fg.yellow + "no records found")
        print(fg.blue + " ↳ " + fg.yellow + "Make sure your domain & api token are valid")
        print(fg.blue + " ↳ " + fg.yellow + "exiting")
        exit()
    
    else:
        print()

    for record in all_records:

        if record["type"] == "A":

            print(fg.blue + " ↳ " + fg.green + record["name"] + fg.blue + " → " + fg.green + record["data"] + fg.blue + " (A)" + fg.rs)
            valid_records.append(record)

        else:

            print(fg.yellow + " ↳ " + record["name"] + " → " + record["data"] + " (" + record["type"] + ")" + fg.rs)

    if not valid_records:

        print(fg.yellow + "🏃🏻‍♂️ No valid records found, exiting")
        exit()

    sanitized_subdomains = SUBDOMAINS.replace(" ", "")
    subdomain_list = sanitized_subdomains.split(',') 
    subdomain_list = list(filter(lambda x: len(x) > 0, subdomain_list))

    # Update

    print(fg.blue + "📝 Updating records for " + fg.green + DOMAIN + fg.rs)
    
    for name in subdomain_list:

        print(fg.blue + " ↳ " + fg.green + name + fg.rs, end="")

        record = find_subdomain_record_in_list(name, valid_records)

        if not record:

            print(fg.blue + " ... " + fg.yellow + "not found, skipping" + fg.rs)
            continue

        record_id = str(record["id"])
        record_type = record["type"]
        record_ip = record["data"]

        if not record_id or not record_type or not record_ip:

            print(fg.blue + " ... " + fg.yellow + "invalid record, skipping" + fg.rs)
            continue

        if record_type != "A":

            print(fg.blue + " ... " + fg.yellow + "not an A record, skipping" + fg.rs)
            continue

        if record_ip != ip:

            print(fg.blue + " ... " + fg.yellow + record_ip + fg.blue + " → " + fg.green + ip + fg.rs, end="")

            if is_dry_run:

                print(fg.blue + " ... " + fg.yellow + "dry run, skipping" + fg.rs)
                
            else:

                res = session.put(records_url + record_id, json={"data": ip})

                if res.ok:
                    print(fg.blue + " ... " + fg.green + "success 🎉" + fg.rs)
                else:
                    print(fg.blue + " ... " + fg.red + "failed, " + res.text + fg.rs)

        else:

            print(fg.blue + " ... " + fg.yellow + "already up to date, skipping" + fg.rs)

    print(fg.blue + "✅ Done" + fg.rs)


if __name__ == '__main__':
    main()
