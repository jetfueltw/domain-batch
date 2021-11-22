import argparse
import requests
from datetime import datetime
from colors import colors
from config import purchase as conf


def parse_cli_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument('file', help='File of domains to be purchase', type=str)

    return parser.parse_args()


def read_domains(file_path):
    with open(file_path, 'r') as file:
        return file.read().splitlines()


def purchase_domains(domains):
    consent = godaddy_domains_agreements(domains)

    for i, domain in enumerate(domains):
        print(f'{i+1}. {domain}')
        try:
            res = godaddy_purchase_domain(domain, consent)
            print(
                f'{colors.OK}order_id: {res["orderId"]}, cost: {res["total"]}{res["currency"]}{colors.ENDC}'
            )
        except RuntimeError as ex:
            status_code, body = ex.args
            print(f'{colors.FAIL}status_code: {status_code}, body: {body}{colors.ENDC}')


def godaddy_domains_agreements(domains):
    res = requests.get(
        f'{conf["api"]["url"]}/v1/domains/agreements',
        headers={
            'Authorization': f'sso-key {conf["api"]["key"]}:{conf["api"]["secret"]}',
            'Accept': 'application/json',
        },
        params={'tlds': domains, 'privacy': False},
    )

    if res.status_code != 200:
        raise RuntimeError(res.status_code, res.json())

    agreementKeys = []
    for item in res.json():
        agreementKeys.append(item['agreementKey'])

    return {
        'agreedAt': datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
        'agreedBy': requests.get('https://api.ipify.org').text,
        'agreementKeys': agreementKeys,
    }


def godaddy_purchase_domain(domain, consent):
    contact = {
        'addressMailing': {
            'address1': conf['contact']['address']['address1'],
            'city': conf['contact']['address']['city'],
            'country': conf['contact']['address']['country'],
            'postalCode': conf['contact']['address']['postal_code'],
            'state': conf['contact']['address']['state'],
        },
        'email': conf['contact']['email'],
        'nameFirst': conf['contact']['name_first'],
        'nameLast': conf['contact']['name_last'],
        'phone': conf['contact']['phone'],
    }

    res = requests.post(
        f'{conf["api"]["url"]}/v1/domains/purchase',
        headers={
            'Authorization': f'sso-key {conf["api"]["key"]}:{conf["api"]["secret"]}',
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        },
        json={
            'consent': consent,
            'contactAdmin': contact,
            'contactBilling': contact,
            'contactRegistrant': contact,
            'contactTech': contact,
            'domain': domain,
            'nameServers': conf['name_servers'],
            'period': 1,
            'privacy': False,
            'renewAuto': conf['renew_auto'],
        },
    )

    if res.status_code != 200:
        raise RuntimeError(res.status_code, res.json())

    return res.json()


def main():
    args = parse_cli_args()

    domains = read_domains(args.file)

    print(f'{colors.HEADER}Start purchase domains...{colors.ENDC}')
    purchase_domains(domains)
    print(f'{colors.HEADER}Done!{colors.ENDC}')


if __name__ == "__main__":
    main()
