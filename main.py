# -- Librerias -- #
import os
import pandas as pd
import requests
import json
import random
import configparser

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


# -- Variables -- #
"""La variable superusuario debe ser previamente configurada
en la base de datos
"""
config = configparser.ConfigParser()
config.read('config.ini')

superusario = config['superuser']['superusario']
password = config['superuser']['password']
authbearer = config['superuser']['authbearer']

"""Abrir un archivo log para almacenar un historial de la recolección de datos
"""
log = open('log.txt', 'w')

# -- Funciones -- #

"""Se encarga de hacer una petición al backend para que devuelva 
todas las redes sociales registradas y devolverlas
"""
def almacenarRedesSociales():
    print("Almacenar redes sociales -- Comenzando...")

    # Creando login form
    userForm = {'username':superusario, 'password':password}

    # Obtener token
    session = requests.Session()
    token = session.post('http://localhost:5500/login', data=userForm)
    #token = session.post('https://bighug.ujaen.es/api/login', data=userForm)
    print("Token:", token)
    print("Obtener token: ", token.status_code, token.reason)
    jsonContent = token.content
    tokenBearer = json.loads(jsonContent)
    tokenBearer = tokenBearer['access_token']
    tokenBearer = " ".join([authbearer, tokenBearer])

    # Metodo get
    #r = requests.get('http://localhost:5500/all-social-networks', headers=({'Authorization': tokenBearer}))
    r = requests.get('https://bighug.ujaen.es/api/all-social-networks', headers=({'Authorization': tokenBearer}))
    print(r)
    print("Obtener redes sociales: ", r.status_code, r.reason)
    redesSociales = r.content
    redesSociales = json.loads(redesSociales)

    print("Almacenar redes sociales -- Finalizado")
    return redesSociales

"""Le pasas el archivo con la clave privada y el texto en bytes de la
contraseña a desencriptar. Devuelve la clave en string
"""
def decrypt(filename, passcrypt):

    with open(filename, "rb") as file:
        private_key = RSA.importKey(file.read(), '')

    rsa_cipher = PKCS1_OAEP.new(private_key)
    decrypted_text = rsa_cipher.decrypt(passcrypt)

    return decrypted_text.decode("utf-8")

"""Lanza un scraper, dependiendo de si la cuenta es de twitter o de
instagram, para cada red social. Cada scraper almacenará el resultado
en la carpeta ./csv
"""
def scraper(redesSociales):
    print("Obteniendo datos redes sociales -- Comenzando...")
    
    # Bucle por cada entrada obteniendo cada nombre
    for n in range(len(redesSociales)):
        id = (redesSociales[n]['id'])
        passw = (redesSociales[n]['encrypted_password'])
        
        # -- Desencriptar las contraseñas -- #
        passw = decrypt('id_rsa', passw)
        
        email = (redesSociales[n]['email'])
        name = (redesSociales[n]['name'])
        
        try:
            if(name == 'twitter'): os.system('python3 prueba1.py')
            if(name == 'instagram'): os.system('python3 prueba2.py')   
            
            # -- Descomentar cuando las cuentas sean reales -- #
            # if(name == 'twitter'): os.system('python3 scraperTwitter.py email passw id')
            # if(name == 'instagram'): os.system('python3 scraperInstagram.py email passw id')
            
            # - Log - #
            log.write('ID: ', id, ' ok')
            
        except:
            # LOG fallo
            log.write('ID: ', id, ' ERROR')

"""Elimina todas las conversaciones privadas almacenados de la carpeta
./csv
"""           
def eliminar_csv():
    dir = './csv'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))  

"""Funcion de prueba, no se utiliza
"""
def prueba_añadir_score():
    
        # Creando login form
        userForm = {'username':superusario, 'password':password}
        
        # Obtener token
        session = requests.Session()
        token = session.post('http://localhost:5500/login', data=userForm)
        jsonContent = token.content
        tokenBearer = json.loads(jsonContent)
        tokenBearer = tokenBearer['access_token']
        tokenBearer = authbearer + tokenBearer
        
        # Prueba añadir scores    
        scores1 = {"score_1": round(random.uniform(0,1), 2),
                "score_2": round(random.uniform(0,1), 2),
                "score_3": round(random.uniform(0,1), 2),
                "score_4": round(random.uniform(0,1), 2)}
        session.post('http://localhost:5500/upload-scores/5', data=json.dumps(scores1), headers=({'Authorization': tokenBearer}))

# ---- Main ---- #
if __name__ == "__main__":
    print("Comienza la ejecución")
    redesSociales = almacenarRedesSociales()
    print(redesSociales)
    #scraper(redesSociales)
    #prueba_añadir_score()
    #Enviar a modelo
    #eliminar_csv()
    
    #os.system('python3 scraperTwitter.py AlbertoJoseGuti Albertobaza10 1')
    #os.system('python3 scraperInstagram.py albertoguti1995 alberto10 2')
    
    #log.close()