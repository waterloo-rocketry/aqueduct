import json


basecamp_project_id = '4075148'
basecamp_url = f'https://3.basecampapi.com/{basecamp_project_id}'

class NotFoundError(Exception):
    pass


def get_software_project(sess):
    proj_resp = sess.get(f'{basecamp_url}/projects.json')
    projects = proj_resp.json()

    for proj in projects:
        if proj['name'] == 'Software':
            return proj
    return None


def extract_todoset_id(project):
    for item in project['dock']:
        if item['name'] == 'todoset':
            return item['id']
    return None


def extract_repos(description):
    # Basecamp uses rich text, so the description comes wrapped in <div> tags.
    description = description.replace('<div>', '')
    description = description.replace('</div>', '')
    return [repo.strip() for repo in description.split(',')]


def get_todolist(sess, project, repo_name):
    todoset_id = extract_todoset_id(project)

    # We expect our project to have a list of todos, so we raise an error if not found
    if todoset_id is None:
        raise NotFoundError('List of to-dos not found for project')
    url = f'{basecamp_url}/buckets/{project["id"]}/todosets/{todoset_id}/todolists.json'
    todolist_resp = sess.get(url)
    todolists = todolist_resp.json()

    for todolist in todolists:
        repos = extract_repos(todolist['description'])
        if repo_name in repos:
            return todolist
    # A to-do list not existing for a repo is acceptable, so we return None
    # to indicate this isn't an error condition
    return None


def create_todo(sess, project, todolist, event):
    url = f'{basecamp_url}/buckets/{project["id"]}/todolists/{todolist["id"]}/todos.json'

    payload = {
        'content': event['title'],
        'description': f'<div>{event["desc"]}</div><div>{event["url"]}</div>'
    }

    r = sess.post(url, json=payload)

    return r


def handle_gh_event(sess, gh_event):
    proj = get_software_project(sess)
    todolist = get_todolist(sess, proj, gh_event['repo'])

    if todolist is None:
        return None

    r = create_todo(sess, proj, todolist, gh_event)

    return r
