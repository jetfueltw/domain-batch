import argparse


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


def buy_domains(domains):
    for d in domains:
        print(d)


def main():
    args = parse_cli_args()

    print("Start to buy domains...")
    domains = read_file(args.file)
    buy_domains(domains)


if __name__ == "__main__":
    main()
