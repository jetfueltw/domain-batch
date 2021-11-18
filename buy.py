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


def godaddy_domain_agreement(apiHost, domains, conf):
    res = requests.get(
        apiHost + "/v1/domains/agreements",
        headers={
            "Authorization": f"sso-key {conf['apiKey']}:{conf['apiSecret']}",
            "accept": "application/json",
            "X-Market-Id": "en-US",
        },
        params={
            "tlds": domains,
            "privacy": conf["privacy"],
        },
    )

    if res.status_code == 200:
        agreementKeys = []

        for item in res.json():
            agreementKeys.append(item["agreementKey"])

        return {
            "agreedAt": f"{datetime.strptime(res.headers['Date'], '%a, %d %b %Y %X %Z').isoformat()}Z",
            "agreedBy": requests.get("https://api.ipify.org").text,
            "agreementKeys": agreementKeys,
        }

    raise Exception(f"get agreement err: {res.status_code} {res.content}")


def godaddy_buy_domains(apiHost, domains, conf, agreement):
    idx = 0
    for domain in domains:
        data = {
            "consent": agreement,
            "contactAdmin": conf["contactAdmin"],
            "contactBilling": conf["contactBilling"],
            "contactRegistrant": conf["contactRegistrant"],
            "contactTech": conf["contactTech"],
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
                "Content-Type": "application/json",
                "accept": "application/json",
            },
            json=data,
        )

        idx += 1
        if res.status_code == 200:
            print(f"[{idx}/{len(domains)}] {domain} [success]")
        else:
            print(
                f"[{idx}/{len(domains)}] {domain} [fail] {res.status_code} {res.content}"
            )


def main():
    args = parse_cli_args()

    print("Start to buy domains...")
    domains = read_file(args.file)

    conf = get_buy_conf("./buy-conf.yaml")

    apiHost = get_api_host(conf["env"])

    agreement = godaddy_domain_agreement(apiHost, domains, conf)

    godaddy_buy_domains(apiHost, domains, conf, agreement)


if __name__ == "__main__":
    main()
