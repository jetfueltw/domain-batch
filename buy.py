import argparse
from typing import Match
import requests
import yaml
from datetime import datetime


def parse_cli_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "file",
        help="txt file to buy domains (output by generate.py), ex ./output/domain.txt",
        type=str,
    )

    return parser.parse_args()


def read_file(path):
    domains = []
    with open(f"{path}") as f:
        lines = f.readlines()
        for line in lines:
            domain = line.replace("\n", "").replace(" ", "")
            domains.append(domain)

    return domains


def get_buy_conf(confYamlPath):
    # parse yaml
    with open(confYamlPath, "r") as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            raise Exception(exc)


def get_api_host(env):
    if env == "prod":
        return "https://api.godaddy.com"
    else:
        return "https://api.ote-godaddy.com"


def api_domain_agreement(apiHost, domain, conf):
    res = requests.get(
        apiHost + "/v1/domains/agreements",
        headers={
            "Authorization": f"sso-key {conf['apiKey']}:{conf['apiSecret']}",
            "accept": "application/json",
            "X-Market-Id": "en-US",
        },
        params={
            "tlds": domain,
            "privacy": "true",
        },
    )

    if res.status_code == 200:
        agreementKeys = []

        for item in res.json():
            agreementKeys.append(item["agreementKey"])

        return {
            "agreedAt": datetime.strptime(
                res.headers["Date"], "%a, %d %b %Y %X %Z"
            ).isoformat()
            + "Z",
            "agreedBy": requests.get("https://api.ipify.org").text,
            "agreementKeys": agreementKeys,
        }

    raise Exception(f"get agreement err: {res.status_code} {res.content}")


def buy_domains(apiHost, domains, conf):
    for domain in domains:

        agreement = api_domain_agreement(apiHost, domain, conf)

        data = {
            "consent": agreement,
            "contactAdmin": {
                "addressMailing": {
                    "address1": conf["contactAdmin"]["addressMailing"]["address1"],
                    "address2": conf["contactAdmin"]["addressMailing"]["address2"],
                    "city": conf["contactAdmin"]["addressMailing"]["city"],
                    "country": conf["contactAdmin"]["addressMailing"]["country"],
                    "postalCode": conf["contactAdmin"]["addressMailing"]["postalCode"],
                    "state": conf["contactAdmin"]["addressMailing"]["state"],
                },
                "email": conf["contactAdmin"]["email"],
                "fax": conf["contactAdmin"]["fax"],
                "jobTitle": conf["contactAdmin"]["jobTitle"],
                "nameFirst": conf["contactAdmin"]["nameFirst"],
                "nameLast": conf["contactAdmin"]["nameLast"],
                "nameMiddle": conf["contactAdmin"]["nameMiddle"],
                "organization": conf["contactAdmin"]["organization"],
                "phone": conf["contactAdmin"]["phone"],
            },
            "contactBilling": {
                "addressMailing": {
                    "address1": conf["contactBilling"]["addressMailing"]["address1"],
                    "address2": conf["contactBilling"]["addressMailing"]["address2"],
                    "city": conf["contactBilling"]["addressMailing"]["city"],
                    "country": conf["contactBilling"]["addressMailing"]["country"],
                    "postalCode": conf["contactBilling"]["addressMailing"][
                        "postalCode"
                    ],
                    "state": conf["contactBilling"]["addressMailing"]["state"],
                },
                "email": conf["contactBilling"]["email"],
                "fax": conf["contactBilling"]["fax"],
                "jobTitle": conf["contactBilling"]["jobTitle"],
                "nameFirst": conf["contactBilling"]["nameFirst"],
                "nameLast": conf["contactBilling"]["nameLast"],
                "nameMiddle": conf["contactBilling"]["nameMiddle"],
                "organization": conf["contactBilling"]["organization"],
                "phone": conf["contactBilling"]["phone"],
            },
            "contactRegistrant": {
                "addressMailing": {
                    "address1": conf["contactRegistrant"]["addressMailing"]["address1"],
                    "address2": conf["contactRegistrant"]["addressMailing"]["address2"],
                    "city": conf["contactRegistrant"]["addressMailing"]["city"],
                    "country": conf["contactRegistrant"]["addressMailing"]["country"],
                    "postalCode": conf["contactRegistrant"]["addressMailing"][
                        "postalCode"
                    ],
                    "state": conf["contactRegistrant"]["addressMailing"]["state"],
                },
                "email": conf["contactRegistrant"]["email"],
                "fax": conf["contactRegistrant"]["fax"],
                "jobTitle": conf["contactRegistrant"]["jobTitle"],
                "nameFirst": conf["contactRegistrant"]["nameFirst"],
                "nameLast": conf["contactRegistrant"]["nameLast"],
                "nameMiddle": conf["contactRegistrant"]["nameMiddle"],
                "organization": conf["contactRegistrant"]["organization"],
                "phone": conf["contactRegistrant"]["phone"],
            },
            "contactTech": {
                "addressMailing": {
                    "address1": conf["contactTech"]["addressMailing"]["address1"],
                    "address2": conf["contactTech"]["addressMailing"]["address2"],
                    "city": conf["contactTech"]["addressMailing"]["city"],
                    "country": conf["contactTech"]["addressMailing"]["country"],
                    "postalCode": conf["contactTech"]["addressMailing"]["postalCode"],
                    "state": conf["contactTech"]["addressMailing"]["state"],
                },
                "email": conf["contactTech"]["email"],
                "fax": conf["contactTech"]["fax"],
                "jobTitle": conf["contactTech"]["jobTitle"],
                "nameFirst": conf["contactTech"]["nameFirst"],
                "nameLast": conf["contactTech"]["nameLast"],
                "nameMiddle": conf["contactTech"]["nameMiddle"],
                "organization": conf["contactTech"]["organization"],
                "phone": conf["contactTech"]["phone"],
            },
            "domain": domain,
            "nameServers": conf["nameServers"],
            "period": conf["period"],
            "privacy": conf["privacy"],
            "renewAuto": conf["renewAuto"],
        }

        res = requests.post(
            apiHost + "/v1/domains/purchase",
            headers={
                "Authorization": f"sso-key {conf['apiKey']}:{conf['apiSecret']}",
                "X-Shopper-Id": conf["shopperId"],
                "Content-Type": "application/json",
                "accept": "application/json",
            },
            json=data,
        )

        if res.status_code == 200:
            print(f"{domain} [success]")
        else:
            raise Exception(f"{domain} [fail] {res.status_code} {res.content}")


def main():
    args = parse_cli_args()

    print("Start to buy domains...")
    domains = read_file(args.file)

    conf = get_buy_conf("./buy-conf.yaml")

    apiHost = get_api_host(conf["env"])

    buy_domains(apiHost, domains, conf)


if __name__ == "__main__":
    main()
