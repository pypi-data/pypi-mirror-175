import os
import json
import requests
from typing import Any


# Thanks: https://dev.to/bro3886/create-a-folder-and-push-multiple-files-under-a-single-commit-through-github-api-23kc

def _get_headers():
    token = os.getenv('GITHUB_TOKEN')
    if token is None:
        raise Exception('Environment variable not set: GITHUB_TOKEN')
    return {
        'Authorization': f'token {token}'
    }

def _get_branch_tree_sha(*, user: str, repo: str, branch: str):
    url = f'https://api.github.com/repos/{user}/{repo}/git/trees/{branch}'
    resp = requests.get(url, headers=_get_headers())
    if resp.status_code != 200:
        raise Exception(f'Error getting branch tree: ({resp.status_code}) {resp.reason}')
    a = json.loads(resp.content)
    sha = a['sha']
    # tree = resp.content['tree']
    return sha

def _upload_blob(*, user: str, repo: str, content: Any, encoding: str):
    url = f'https://api.github.com/repos/{user}/{repo}/git/blobs'
    resp = requests.post(url, json={'content': content, 'encoding': encoding}, headers={**_get_headers()})
    if resp.status_code != 201:
        raise Exception(f'Error uploading blob: ({resp.status_code}) {resp.reason}')
    a = json.loads(resp.content)
    sha = a['sha']
    return sha

def _create_tree(*, user: str, repo: str, base_tree_sha: str, blobs: list):
    url = f'https://api.github.com/repos/{user}/{repo}/git/trees'
    tree = [
        {
            'path': blob['path'],
            'mode': '100644',
            'type': 'blob',
            'sha': blob['sha']
        }
        for blob in blobs
    ]
    resp = requests.post(url, json={'base_tree': base_tree_sha, 'tree': tree}, headers={**_get_headers()})
    if resp.status_code != 201:
        raise Exception(f'Error creating tree: ({resp.status_code}) {resp.reason}')
    a = json.loads(resp.content)
    sha = a['sha']
    return sha

def _create_commit(*, user: str, repo: str, tree: str, message: str, parent_tree: str):
    url = f'https://api.github.com/repos/{user}/{repo}/git/commits'
    resp = requests.post(url, json={'tree': tree, 'message': message, 'parents': [parent_tree]}, headers={**_get_headers()})
    if resp.status_code != 201:
        raise Exception(f'Error creating commit: ({resp.status_code}) {resp.reason}')
    a = json.loads(resp.content)
    sha = a['sha']
    return sha

def _update_branch_ref(*, user: str, repo: str, branch: str, commit_sha: str):
    url = f'https://api.github.com/repos/{user}/{repo}/git/refs/heads/{branch}'
    resp = requests.patch(url, json={'sha': commit_sha}, headers={**_get_headers()})
    if resp.status_code != 200:
        raise Exception(f'Error updating branch: ({resp.status_code}) {resp.reason}')
    a = json.loads(resp.content)
    sha = a['object']['sha']

    # ratelimit_limit = int(resp.headers['X-RateLimit-Limit'])
    ratelimit_remaining = int(resp.headers['X-RateLimit-Remaining'])
    # ratelimit_reset = float(resp.headers['X-RateLimit-Reset'])
    print(f'Ratelimit remaining: {ratelimit_remaining}')

    return sha