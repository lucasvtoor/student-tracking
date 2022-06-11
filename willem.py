import requests

headers = {
    'accept': 'application/json',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
}

json_data = {
    'query': 'mutation{passwordAuthorize(email:"Marloes.flier@hva.nl",password:"Trampoline!23"){success,token}}',
    'variables': None,
}

response = requests.post('https://www.badgecraft.eu/api/graphql', headers=headers, json=json_data)
print(response.json()['data']['passwordAuthorize']['token'])
