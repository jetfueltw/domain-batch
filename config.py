import yaml


def read_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)


root = read_config('./config.yaml')
generate = root['generate']
purchase = root['purchase']
