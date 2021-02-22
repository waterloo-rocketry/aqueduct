import json


def parse_event(gh_event):
    if gh_event['action'] != 'opened':
        return None  # We only care about new issues

    return {
        'repo': gh_event['repository']['name'],
        'title': gh_event['issue']['title'],
        'desc': gh_event['issue']['body'],
        'url': gh_event['issue']['html_url']
    }
