import argparse
import requests
import json
from multipledispatch import dispatch
from datetime import datetime
import env

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def parse_cli_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument('--domain-name', help='Will buy domain name')
    parser.add_argument('--file', help='Import file name')

    return parser.parse_args()

def api_agreement(domain):
    headers = {
        'Authorization': 'sso-key ' + env.go_daddy_key + ':' + env.go_daddy_secret,
        'X-Market-Id': 'en-US',
        'accept': 'application/json'
    }

    r = requests.get(env.go_daddy_api +'/v1/domains/agreements?tlds='+ domain +'&privacy=false', headers=headers)

    timestamp = datetime.strptime(r.headers['Date'], "%a, %d %b %Y %X %Z").isoformat()

    return {
        'agreementKeys':[r.json()[0]['agreementKey']],
        'agreedAt': timestamp+"Z",
        'agreedBy': requests.get('https://api.ipify.org').text
    }

@dispatch(str)
def domain_purchase(domain):
    headers = {
        'Authorization': 'sso-key ' + env.go_daddy_key + ':' + env.go_daddy_secret,
        'Content-Type': 'application/json',
        'accept': 'application/json'
    }

    agreement = api_agreement(domain)

    default_info = {
            "addressMailing": {
                "address1": env.contact_address1,
                "city": env.contact_city,
                "country": env.contact_country,
                "postalCode": env.contact_postalCode,
                "state": env.contact_state
            },
            "email": env.contact_email,
            "nameFirst": env.contact_nameFirst,
            "nameLast": env.contact_nameLast,
            "phone": env.contact_phone
    }

    params = {
        "consent": agreement,
        "contactAdmin": default_info,
        "contactBilling": default_info,
        "contactRegistrant": default_info,
        "contactTech": default_info,
        "domain": domain,
        "nameServers": env.name_server,
        "period": 1,
        "privacy": False,
        "renewAuto": True
    }

    r = requests.post(env.go_daddy_api+'/v1/domains/purchase', data=json.dumps(params), headers=headers)

    if(r.status_code != 200):
        print(bcolors.FAIL + "[Fail] Message: " + r.json()['message'])
    else:
        print(bcolors.OKGREEN + '(' + domain + ')' + ' Success')

@dispatch(tuple)
def domain_purchase(domains):
    for item in domains:
        domain_purchase(item)

def main():
    args = parse_cli_args()

    env.init()

    if(args.domain_name != None):
        domain_purchase(args.domain_name)
    if(args.file != None):
        f = open(args.file, 'r')
        data = tuple(f.read().split('\n')[:-1])
        domain_purchase(data)

    print(bcolors.OKGREEN + 'Done!')

if __name__ == "__main__":
    main()