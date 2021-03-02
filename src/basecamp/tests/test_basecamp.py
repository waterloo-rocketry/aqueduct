from src import basecamp


def test_extract_repos():
    repo_str = '<div>Payload,Recovery, Propulsion</div>'
    repos = ['Payload', 'Recovery', 'Propulsion']

    assert basecamp.extract_repos(repo_str) == repos
