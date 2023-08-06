# fitgit

Use the Github API to programmatically upload content to a Github repository.

## Installation

```
pip install fitgit
```

Obtain a Github [personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token), and then set the environment variable

```bash
GITHUB_TOKEN="..."
```

## Basic usage

```python
import fitgit

C = fitgit.Commit()
C.add_json_file('example1-upload/file1.json', {'file': 1})
C.add_json_file('example1-upload/file2.json', {'file': 2})
C.add_json_file('example1-upload/file3.json', {'file': 3})
C.push_to_github('scratchrealm/test-content', branch='main', message='example1')

print('https://github.com/scratchrealm/test-content/tree/main/example1-upload')
```

See [examples/example1.py](examples/example1.py)

## Notes

The Github API is rate limited. See https://docs.github.com/en/rest/overview/resources-in-the-rest-api#rate-limiting

