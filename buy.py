import argparse
import os
from dotenv import load_dotenv
import requests
import json
from multipledispatch import dispatch
from datetime import datetime 

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
        'Authorization': 'sso-key ' + go_daddy_key + ':' + go_daddy_secret,
        'X-Market-Id': 'en-US',
        'accept': 'application/json'
    }

    r = requests.get(go_daddy_api +'/v1/domains/agreements?tlds='+ domain +'&privacy=false', headers=headers)

    timestamp = datetime.strptime(r.headers['Date'], "%a, %d %b %Y %X %Z").isoformat()

    return {
        'agreementKeys':[r.json()[0]['agreementKey']],
        'agreedAt': timestamp+"Z",
        'agreedBy': requests.get('https://api.ipify.org').text
    }

@dispatch(str)
def domain_purchase(domain):
    headers = {
        'Authorization': 'sso-key ' + go_daddy_key + ':' + go_daddy_secret,
        'Content-Type': 'application/json',
        'accept': 'application/json'
    }

    agreement = api_agreement(domain)

    default_info = {
            "addressMailing": {
                "address1": contact_address1,
                "city": contact_city,
                "country": contact_country,
                "postalCode": contact_postalCode,
                "state": contact_state
            },
            "email": contact_email,
            "nameFirst": contact_nameFirst,
            "nameLast": contact_nameLast,
            "phone": contact_phone
    }

    params = {
        "consent": agreement,
        "contactAdmin": default_info,
        "contactBilling": default_info,
        "contactRegistrant": default_info,
        "contactTech": default_info,
        "domain": domain,
        "nameServers": name_server,
        "period": 1,
        "privacy": False,
        "renewAuto": True
    }

    r = requests.post(go_daddy_api+'/v1/domains/purchase', data=json.dumps(params), headers=headers)

    if(r.status_code != 200):
        print(bcolors.FAIL + "[Fail] Message: " + r.json()['message'])
    else:
        print(bcolors.OKGREEN + '(' + domain + ')' + ' Success')

@dispatch(tuple)
def domain_purchase(domains):
    for item in domains:
        domain_purchase(item)
    
def init():
    load_dotenv()

    global go_daddy_api
    go_daddy_api = os.getenv('GO_DADDY_API')

    global go_daddy_key
    go_daddy_key = os.getenv('GO_DADDY_KEY')

    global go_daddy_secret
    go_daddy_secret = os.getenv('GO_DADDY_SECRET')

    global name_server
    name_server = json.loads(os.getenv('NAME_SERVER'))

    global contact_address1
    contact_address1 = os.getenv('CONTACT_ADDRESS1')

    global contact_city
    contact_city = os.getenv('CONTACT_CITY')

    global contact_country
    contact_country = os.getenv('CONTACT_COUNTRY')

    global contact_postalCode
    contact_postalCode = os.getenv('CONTACT_POSTAL_CODE')

    global contact_state
    contact_state = os.getenv('CONTACT_STATE')

    global contact_email
    contact_email = os.getenv('CONTACT_EMAIL')

    global contact_nameFirst
    contact_nameFirst = os.getenv('CONTACT_NAME_FIRST')

    global contact_nameLast
    contact_nameLast = os.getenv('CONTACT_NAME_LAST')

    global contact_phone
    contact_phone = os.getenv('CONTACT_PHONE')

def main():
    args = parse_cli_args()

    init()

    if(args.domain_name != None):
        domain_purchase(args.domain_name)
    if(args.file != None):
        f = open(args.file, 'r')
        data = tuple(f.read().split('\n')[:-1])
        domain_purchase(data)

    print(bcolors.OKGREEN + 'Done!')

if __name__ == "__main__":
    main()