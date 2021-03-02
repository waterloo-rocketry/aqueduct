import json
import os

from src import github


def test_parse_event():
    with open(os.path.join(os.path.dirname(__file__), 'opened_issue.json')) as test_file:
        test_data = json.load(test_file)

    parsed = github.parse_event(test_data)

    expected = {
        'repo': 'topside',
        'title': 'Add pressure relief valves',
        'desc': 'A pressure relief valve is a valve with two states (open and closed).',
        'url': 'https://github.com/waterloo-rocketry/topside/issues/85'
    }

    assert parsed == expected
