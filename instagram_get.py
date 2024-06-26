import requests
import json
import re



def get_content(url: str):
    shortcode = re.search(r'/(?:p|reel)/([^/]+)/', url).group(1)
    v = {"shortcode": shortcode}
    u = f"https://www.instagram.com/graphql/query/?doc_id=24852649951017035&variables={requests.utils.quote(json.dumps(v))}"
    r = requests.get(u, headers={"user-agent": "Mozilla/5.0"})
    if r.status_code == 200:
        result = json.dumps(json.loads(r.text), indent=4)
    else:
        result = "None"
    return result
print(get_content("https://www.instagram.com/reel/C76xvJfvAjZ/?igsh=NTc4MTIwNjQ2YQ=="))

