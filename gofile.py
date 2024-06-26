import requests

def aku_gofile():
    # create guest account
    rr = requests.Session()
    token_generate = rr.post("https://api.gofile.io/accounts")
    id_user, token = token_generate.json()["data"]["id"], token_generate.json()["data"]["token"]

    # trigger account check
    headers_1 = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': f'Bearer {token}',
        'dnt': '1',
        'origin': 'https://gofile.io',
        'referer': 'https://gofile.io/',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
    }

    rr.get(f'https://api.gofile.io/accounts/{id_user}', headers=headers_1).json()
    
    r_get = rr.get("https://api.gofile.io/contents/O7DVkP?wt=4fd6sg89d7s6", headers=headers_1).json()
    return r_get

result = aku_gofile()
print(result)

