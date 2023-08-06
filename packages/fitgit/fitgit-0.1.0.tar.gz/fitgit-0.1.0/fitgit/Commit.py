from typing import Any
from ._json_stringify_deterministic import _json_stringify_deterministic
from ._api_functions import _create_commit, _get_branch_tree_sha, _create_tree, _update_branch_ref, _upload_blob


class Commit:
    def __init__(self) -> None:
        self._files = []
    def add_file(self, path: str, *, content: Any, encoding: str='utf-8'):
        self._files.append({
            'path': path,
            'content': content,
            'encoding': encoding
        })
    def add_text_file(self, path: str, text: Any):
        self.add_file(path, content=text, encoding='utf-8')
    def add_json_file(self, path: str, content: Any):
        self.add_text_file(path, _json_stringify_deterministic(content))
    def push_to_github(self, repo_slug: str, *, branch: str, message: str):
        if len(self._files) == 0:
            print('No files to add.')
            return
        user = repo_slug.split('/')[0]
        repo = repo_slug.split('/')[1]

        print(f'Getting tree for branch {branch}')
        sha_tree = _get_branch_tree_sha(user=user, repo=repo, branch=branch)

        print(f'Uploading blobs')
        blobs = [
            {
                'sha': _upload_blob(user=user, repo=repo, content=file['content'], encoding=file['encoding']),
                'path': file['path']
            }
            for file in self._files
        ]

        print(f'Creating new tree for commit')
        sha_new_tree = _create_tree(
            user=user,
            repo=repo,
            base_tree_sha=sha_tree,
            blobs=blobs
        )

        print(f'Creating commit')
        sha_commit = _create_commit(user=user, repo=repo, tree=sha_new_tree, message=message, parent_tree=sha_tree)

        print(f'Updating branch {branch}')
        sha_commit2 = _update_branch_ref(user=user, repo=repo, branch=branch, commit_sha=sha_commit)

        assert sha_commit == sha_commit2