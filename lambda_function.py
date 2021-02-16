import json

from src import basecamp, github, auth


def lambda_handler(event, context):
    sess = auth.make_session()
    gh_event = github.parse_event(json.loads(event['body']))
    try:
        r = basecamp.handle_gh_event(sess, gh_event)
    except basecamp.NotFoundError as err:
        return {
            'statusCode': 404,
            'error': str(err)
        }

    if r is None:
        return {
            'statusCode': 200,
            'body': ''
        }

    return {
        'statusCode': r.status_code,
        'body': json.dumps(r.text)
    }
