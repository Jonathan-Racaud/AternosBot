import json
import random

def load_facts():
    json_file = open('minecraft-facts.json', 'r')
    json_data = json_file.read()
    json_file.close()

    json_data = json_data.replace('\u200b', '').replace('\n', '')

    return json.loads(json_data)

def get_random_fact_with_number(facts):
    key = random.choice(list(facts.keys()))
    return (key, facts[key])

def get_random_fact(facts):
    key = random.choice(list(facts.keys()))
    return facts[key]
