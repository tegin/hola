import yaml
import github3
import sys
from github3.exceptions import NotFoundError

org = sys.argv[1]
token = sys.argv[2]

with open("generate.yml", "r") as f:
    data = yaml.safe_load(f.read())

gh = github3.login(token=token)
gh_org = gh.organization(org)
for team in data:
    try:
        gh_team = gh_org.team_by_name(team)
    except NotFoundError:
        gh_team = gh_org.create_team(team, privacy="closed")
    for member in gh_team.members():
        if member.login not in data[team].users:
            gh_team.revoke_membership(member.login)
    for user in data[team].users:
        gh_team.add_or_update_membership(user)