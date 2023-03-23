#!/usr/bin/env python3

import os
import dotenv
import requests

from argparse import ArgumentParser
from sty import fg, bg, ef, rs

# Environment variables

dotenv.load_dotenv()

# TODO: Remove hard coded fallback values

VERSION = "1.0.0"
DOMAIN = os.getenv("DO_DOMAIN")
SUBDOMAINS = os.getenv("DO_SUBDOMAINS")
TOKEN = os.getenv("DO_API_TOKEN")

# Arguments

parser = ArgumentParser()
parser.add_argument("-d", "--dry", action="store_true")
args = parser.parse_args()

# Request session

records_url = f'https://api.digitalocean.com/v2/domains/{DOMAIN}/records/'
session = requests.Session()
session.headers = {
    'Authorization': 'Bearer ' + TOKEN
}

# Functions

def precondition_env_vars():

    if not DOMAIN:

        print()
        print(fg.red + "🚫 Missing variable \"DO_DOMAIN\", exiting..." + fg.rs)
        print()
        exit()

    if not SUBDOMAINS:

        # Is it okay that subdomains is empty, how do I update the
        # raw domain, i.e. "mitchtreece.io"

        print()
        print(fg.red + "🚫 Missing variable \"DO_SUBDOMAINS\", exiting..." + fg.rs)
        print()
        exit()

    if not TOKEN:

        print()
        print(fg.red + "🚫 Missing variable \"DO_API_TOKEN\", exiting..." + fg.rs)
        print()
        exit()


def get_wan_ip():
    return requests.get('https://api.ipify.org').text.rstrip()


# def get_subdomain_info():

#     records = session.get(records_url).json()

#     for record in records['domain_records']:
#         if record['name'] == subdomain:
#             return record


def get_subdomain_record(name):

    records = session.get(records_url).json()

    for record in records['domain_records']:
        if record['name'] == name:
            return record


# def update_dns():
#     current_ip_address = get_ip()
#     sub_info = get_sub_info()
#     subdomain_ip_address = sub_info['data']
#     subdomain_record_id = sub_info['id']
#     if current_ip_address == subdomain_ip_address:
#         print('Subdomain DNS record does not need updating.')
#     else:
#         response = session.put(records_url + subdomain_record_id, json={'data': current_ip_address})
#         if response.ok:
#             print('Subdomain IP address updated to ' + current_ip_address)
#         else:
#             print('IP address update failed with message: ' + response.text)

def main():

    print()
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

    precondition_env_vars()

    print(fg.yellow + "DO_DOMAIN: " + fg.blue + DOMAIN + fg.rs)
    print(fg.yellow + "DO_SUBDOMAINS: " + fg.blue + SUBDOMAINS + fg.rs)
    print(fg.yellow + "DO_TOKEN: " + fg.blue + TOKEN + fg.rs)
    print(fg.yellow + "================================" + fg.rs)
    print()

    # Get wan ip address

    print(fg.blue + "🌎 Getting WAN IP address" + fg.rs, end="")

    ip = get_wan_ip()

    if not ip:
        print(fg.blue + " ... " + fg.red + "failed" + fg.rs)
        exit()

    print(fg.blue + " ... " + fg.green + ip + fg.rs)

    # Get subdomain name list

    sanitized_subdomains = SUBDOMAINS.replace(" ", "")
    subdomain_list = sanitized_subdomains.split(',') 
    subdomain_list = list(filter(lambda x: len(x) > 0, subdomain_list))

    # Update

    print(fg.blue + "📖 Updating records for " + fg.green + DOMAIN + fg.rs)
    
    for name in subdomain_list:

        print(fg.blue + "👀 Checking subdomain " + fg.green + name + fg.rs, end="")

        record = get_subdomain_record(name)

        if not record:
            print(fg.blue + " ... " + fg.yellow + "not found, skipping" + fg.rs)
            continue

        record_id = str(record["id"])
        record_type = record["type"]
        record_ip = record["data"]

        if not record_id or not record_type or not record_ip:
            print(fg.blue + " ... " + fg.red + "invalid record, skipping" + fg.rs)
            continue

        if record_type != "A":
            print(fg.blue + " ... " + fg.yellow + "not an A record, skipping" + fg.rs)
            continue

        if record_ip != ip:

            print(fg.blue + " ... " + fg.yellow + "update required" + fg.rs)
            print(fg.blue + "🚀 Updating subdomain " + fg.green + name + fg.blue + " ... " + fg.yellow + record_ip + fg.blue + " → " + fg.yellow + ip + fg.rs, end="")

            if not args.dry:

                res = session.put(records_url + record_id, json={"data": ip})

                if res.ok:
                    print(fg.blue + " ... " + fg.green + "done 🎉" + fg.rs)
                else:
                    print(fg.blue + " ... " + fg.red + "failed, " + res.text + fg.rs)

            else:

                print(fg.blue + " ... " + fg.yellow + "dry run, skipping" + fg.rs)

        else:
            print(fg.blue + " ... " + fg.green + "up to date 🎉" + fg.rs)

    # print("Updating domain \"" + domain + "\" with IP address: " + ip_address)
    # print("Subdomains: " + ','.join(subdomain_names))

    # for name in subdomain_names:

    #     record = get_subdomain_record(name)

    #     if not record:
    #         print("Failed to get record for subdomain: " + name)
    #         continue

    #     record_id = record['id']
    #     subdomain_ip_address = record['data']

    #     if ip == subdomain_ip_address:
    #         print("Subdomain record does not need updating")
    #     else:

    #         res = session.put(records_url + record_id, json={'data': ip})
            
    #         if res.ok:
    #             print("Subdomain IP address updated to: " + ip)
    #         else:
    #             print("Failed to update subdomain IP address: " + res.text)


if __name__ == '__main__':
    main()
