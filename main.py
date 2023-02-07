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

# No funciona en el servidor (?)
superusario = config['superuser']['superusario']
password = config['superuser']['password']
# authbearer = config['superuser']['authbearer']
authbearer = "Bearer"

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
    #userForm = {'username':superusario, 'password':password}
    userForm = {'username':"a@a.com", 'password':"alberto10"}

    # Obtener token
    session = requests.Session()
    #token = session.post('http://localhost:5500/login', data=userForm)
    token = session.post('https://bighug.ujaen.es/api/login', data=userForm)
    print("Obtener token: ", token.status_code, token.reason)
    jsonContent = token.content
    tokenBearer = json.loads(jsonContent)
    tokenBearer = tokenBearer['access_token']
    tokenBearer = " ".join([authbearer, tokenBearer])

    # Metodo get
    #r = requests.get('http://localhost:5500/all-social-networks', headers=({'Authorization': tokenBearer}))
    r = requests.get('https://bighug.ujaen.es/api/all-social-networks', headers=({'Authorization': tokenBearer}))
    print("Respuesta: ", r)
    print("Obtener redes sociales: ", r.status_code, r.reason)
    redesSociales = r.content
    redesSociales = json.loads(redesSociales)

    print("Almacenar redes sociales -- Finalizado")
    return redesSociales

"""Le pasas el archivo con la clave privada y el texto en bytes de la
contraseña a desencriptar. Devuelve la clave en string
"""
def decrypt(filename, passcrypt):

    print("Entro en decrypt")
    passcrypt = bytes(passcrypt, "utf-8")
    print("Consigo la pass: ", passcrypt)

    with open(filename, "rb") as file:
        print("Abro el documento rsa")
        private_key = RSA.importKey(file.read(), '')
        print("Consigo la private key: ", private_key)

    rsa_cipher = PKCS1_OAEP.new(private_key)
    print("Consigo el cifrador")
    #decrypted_text = rsa_cipher.decrypt(passcrypt)
    decrypted_text = rsa_cipher.decrypt('\xc2\x9dL\xc2\x97\xc2\xb4\xc2\x8d\x0f\x0f\xc2\xb2s\xc2\x95$\xc3\xael\x11\xc2\xbd,I\xc3\x8b2%,\xc2\x84!8\x7f\xc2\x85\x1f\xc2\x8c}:\x05\xc2\xbf\xc3\x9dr}\xc2\x8fQF\xc3\x86\xc2\x89\xc3\xa9\xc3\xba\xc3\x84rS\xc3\x963s\xc2\x84_\x04\xc2\x92\xc3\x99\xc2\x92\x08\xc2\x94\xc2\xae\x0c\xc3\x8bO\xc2\xa9\xc3\x9dNe\x17\xc3\x91\xc2\xa2_\x1b\x02\x17\xc2\xb6xM\xc3\xbf\xc3\x894#\xc3\xbc\xc3\xa7B\x17\xc3\xa3O\xc3\x96\xc3\x9d\xc3\x9a\xc3\xa6w\xc3\x995]\xc2\xb8\xc3\x8b\xc3\x9a\xc2\x87%}\xc2\x84\xc2\x93\xc3\x8e\xc3\xbeIX\xc2\x98\xc2\xa7\x1dM8\xc3\x8dKv\xc3\xac(\\\r\x12\xc3\xb6mS\xc2\x88\xc2\x8e\xc3\xbb\xc3\x8a<I\xc2\xbcX\xc3\xb4H\x1e\xc3\xa4\x1e\xc2\xac\x16\xc3\xab\xc3\xbc#k\xc3\xb0\xc3\xba(W\xc3\xb3\x17\xc3\xb7\xc2\x9e\x18@wxd\xc3\x85Z\xc3\x89tZu\xc3\x88\x03\xc3\x98\xc3\xb8\xc3\xad\xc3\x91\xc3\x92\xc3\x86\xc2\x85A&\xc2\xbb\x19:#\xc2\xaa\xc2\xa8\xc2\x9b\x06+\x17xgNE\xc2\xb2\x10\xc3\xa1\xc3\x949\xc2\xb8\xc2\x97\xc2\xb6`j\xc2\x8f\x1eu\xc2\x8a.#\xc3\xbc\xc2\xbfE\xc3\x82\xc3\x8b6\xc3\x84\x18\xc2\xa9?\x0b\xc3\xba\xc2\xa3\xc3\x87_N\r\xc3\xa0\xc2\x85\xc3\x95\xc3\xbd\xc2\x9c\xc2\x9as\xc2\xac\x19%\xc2\xaf:\xc2\xa4r0"\xc3\x98\xc2\xbb\xc2\x83\n\xc3\xa8\xc2\xa6J\xc2\x80\xc2\x81\xc3\x93\xc3\xa1\xc2\x8a\xc2\x8cR\xc2\xa5\x02\xc3\xad\xc2\xa6\xc3\xa3L9\xc2\xb4\xc3\xa7}\xc3\xa17Jw\xc3\x9eif\xc2\x9b\t:{Hz\x1e]\xc2\xb4\x08\x02UU\x0e\xc2\xa4\xc2\xad\xc2\x97~\xc3\xbe\xc3\x81b\xc3\xb2\xc3\x97)\xc3\xbbhJ\xc2\xaeR\xc2\x98\xc2\x9aF\xc2\x91t*\xc3\xa3\x17"\xc3\x81\xc2\x8c&\xc3\xa07\x15\xc3\xbf\xc3\xa8-on\xc2\x81\x14j\x0e\x02$O\xc3\x8a%N\xc3\x872\xc2\xb5\x18\xc3\xad{\xc2\x88\xc3\x8c\xc2\x90\'Sx^d>5/\xc3\x97K\xc2\xa3\xc2\xbez\x10[\xc3\x8c\x0e\xc2\x8bF\x15\xc2\xb7\xc3\x9doi0B\xc2\xb3\xc3\x86\xc2\x8aha\xc2\xa4\xc2\xa5MiU\xc2\x8b/\xc2\xa8\x04\xc3\x9a\r\xc2\xa4If\xc3\x84b=\x04\xc2\x8f\rwa\xc2\x9d\xc2\x90\xc2\x93\x03\x1a\xc3\x9a8\x13\xc3\xb6\\\xc3\xb6\x08\xc3\xa1|\xc2\x80\xc2\xbd\x10B\xc2\xb1R\xc2\xb8\xc2\x88o\xc2\xbf`\xc3\xb8F\x7f\xc3\xb2\xc2\xa3\xc2\x86])WeY\x1f\xc3\xa6\xc2\xa2\xc2\x90T\xc2\x92l\xc2\xaftY\xc3\x8f\xc3\x99\'\xc2\x85p]\xc3\xa5J\xc3\xa5Q\xc3\x89\xc3\x93\xc2\xa4x\xc2\x9by4\x18\xc3\xbe\xc3\x86e\xc3\xb0\xc3\x9e>\xc2\xaf\xc2\xbd\xc3\xbc\x00\xc3\x83\x1b\x08\x19]\x07\x0f\x1eN\xc3\x88\xc2\xa8\xc2\xb0{\x1b\xc2\xb5\x12B\x08+\xc3\xb7\xc2\xba\x1f\xc3\x90\xc2\xa1\xc2\x8a9\xc2\xbd,=-@@\xc2\x9e\xc3\xaey\xc2\x9b\xc2\xac@\xc3\xa1\xc3\xa0\xc3\xaf\xc2\x85p\xc3\x91\xc3\x85\xc2\xbb\x15\xc2\x8cc\x06{C\xc2\xa9X')
    print("Consigo decodificarlo: ", decrypted_text)

    return decrypted_text.decode("Latin-1")

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
        #passw = decrypt('id_rsa', passw) 
        passw = decrypt('/home/agmegias/prevemental/backend/.ssh/id_rsa', passw) # Path del servidor
        """
        print("Contraseñas: ", passw)
        
        email = (redesSociales[n]['email'])
        name = (redesSociales[n]['name'])
        
        print("Email: ", email)
        print("Name: ", name)

        
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
        """

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
    scraper(redesSociales)
    #prueba_añadir_score()
    #Enviar a modelo
    #eliminar_csv()
    
    #os.system('python3 scraperTwitter.py AlbertoJoseGuti Albertobaza10 1')
    #os.system('python3 scraperInstagram.py albertoguti1995 alberto10 2')
    
    #log.close()