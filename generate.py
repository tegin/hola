import yaml
import github3
import sys
from github3.exceptions import NotFoundError
import logging

_logger = logging.getLogger(__name__)

org = sys.argv[1]
token = sys.argv[2]

with open("generate.yml", "r") as f:
    data = yaml.safe_load(f.read())

gh = github3.login(token=token)
gh_org = gh.organization(org)
print(data)
for team in data:
    _logger.info("Generating team %s" % team)
    try:
        gh_team = gh_org.team_by_name(team)
    except NotFoundError:
        gh_team = gh_org.create_team(team, privacy="closed")
    members = []
    for member in gh_team.members():
        if member.login not in data[team].users:
            _logger.info("Revoking membership for %s" % member.login)
            gh_team.revoke_membership(member.login)
        else:
            members.append(member.login)
    for user in data[team].users:
        if user not in members:
            _logger.info("Adding membership to %s" % member.login)
            gh_team.add_or_update_membership(user)