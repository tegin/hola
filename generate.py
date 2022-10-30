import yaml
import github3

with open("generate.yml", "r") as f:
    data = yaml.safe_load(f.read())

for team_key in data:
    print(team_key)