import string
import random
import argparse
import whois
from faker import Faker


LETTER = string.ascii_lowercase + string.digits
WHOIS_NOT_SUPPORT = ['xyz']


def parse_cli_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument('count', help='Number of generate domains', type=int)
    parser.add_argument('--top-level', help='Top-level domain', default='com')
    parser.add_argument('--file', help='Output file name', default='domains')
    parser.add_argument(
        '--skip', help='Skip domain available check', action='store_true'
    )

    return parser.parse_args()


def generate_domains(count, top_level, skip_check):
    domains = []
    i = 1
    while i <= count:
        domain = generate_domain(top_level)

        if skip_check:
            domains.append(domain)
            print(f'{i}. {domain}')
            i += 1
        elif is_domain_available(domain):
            domains.append(domain)
            print(f'{i}. {domain}')
            i += 1
        else:
            print(f'{i}. {domain} ...unavailable')

    return domains


def generate_domain(top_level):
    faker = Faker()
    domain = faker.domain_word().replace('-', '')

    if len(domain) < 10:
        domain = domain + rand_alphabet(3, 4)
    else:
        domain = domain + rand_alphabet(1, 2)

    return domain + '.' + top_level


def rand_alphabet(min_size, max_size):
    size = random.randint(min_size, max_size)
    return ''.join([random.choice(LETTER) for _ in range(size)])


def is_domain_available(domain):
    try:
        whois.whois(domain)
        return False
    except whois.parser.PywhoisError:
        return True


def output_file(data, path):
    with open(path, 'w') as file:
        for row in data:
            file.write(row + '\n')


def main():
    args = parse_cli_args()

    print(rand_alphabet(2, 2))

    if args.top_level in WHOIS_NOT_SUPPORT:
        args.skip = True
        print('Skip domain available check')

    print('Start generate domains...')
    domains = generate_domains(args.count, args.top_level, args.skip)
    output_file(domains, f'./output/{args.file}.txt')
    print('Done!')


if __name__ == "__main__":
    main()
