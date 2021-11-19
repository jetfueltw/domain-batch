import argparse
import requests
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
        'Authorization': f'sso-key {env.go_daddy_key}:{env.go_daddy_secret}',
        'X-Market-Id': 'en-US',
        'accept': 'application/json'
    }

    r = requests.get(f'{env.go_daddy_api}/v1/domains/agreements?tlds={domain}&privacy=false', headers=headers)

    agreementKeys = []

    for item in r.json():
        agreementKeys.append(item["agreementKey"])

    return {
        'agreementKeys': agreementKeys,
        'agreedAt': datetime.strptime(r.headers['Date'], "%a, %d %b %Y %X %Z").isoformat()+"Z",
        'agreedBy': requests.get('https://api.ipify.org').text
    }

@dispatch(str, int, int)
def domain_purchase(domain, total, index):
    headers = {
        'Authorization': f'sso-key {env.go_daddy_key}:{env.go_daddy_secret}',
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

    r = requests.post(f'{env.go_daddy_api}/v1/domains/purchase', json=params, headers=headers)

    if(r.status_code != 200):
        print(f'{bcolors.ENDC}({index}/{total}){bcolors.FAIL}[Fail] Message: ' + r.json()['message'])
        return False
    else:
        print(f'{bcolors.ENDC}({index}/{total}){bcolors.OKGREEN}({domain}) Success')
        return True

@dispatch(tuple)
def domain_purchase(domains):
    total = len(domains)
    index = 1
    for item in domains:
        domain_purchase(item, total, index)
        index+=1

def main():
    print('Start buy domains...')
    args = parse_cli_args()

    env.init()

    if(args.domain_name != None):
        domain_purchase(args.domain_name, 1, 1)
    if(args.file != None):
        f = open(args.file, 'r')
        data = tuple(f.read().split('\n')[:-1])
        total = len(data)
        print(f'{bcolors.HEADER}Have {bcolors.OKCYAN}{total} {bcolors.HEADER}domains')
        domain_purchase(data)

    print(f'{bcolors.OKGREEN}Done!')

if __name__ == "__main__":
    main()