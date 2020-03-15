import yaml

def load_yaml(doc):
    with open(doc, "r") as stream:
        try:
            conf = yaml.safe_load(stream)
            return conf
        except yaml.YAMLError as e:
            print(e)
            return None
