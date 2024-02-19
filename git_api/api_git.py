import requests
import json
def get_repo_last_tag_version(author_name, repo_name) -> str | None:
    api_url = f"https://api.github.com/repos/{author_name}/{repo_name}/tags"
    response = requests.get(api_url)
    raw_content = response.content.decode()
    if response.status_code is not 200:
        return None
    if raw_content is None or raw_content == "":
        return None
    json_tags = json.loads(raw_content)
    return json_tags[0]["name"]