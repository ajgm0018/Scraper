# -- Librerias -- #
import os
import pandas as pd
import requests
import json
import random


# -- Variables -- #
"""La variable superusuario debe ser previamente configurada
en la base de datos
"""
superusario = "a@a.com"
password = "alberto10"
authbearer = "Bearer "

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
    print("Obtener token: ", token.status_code, token.reason)
    jsonContent = token.content
    tokenBearer = json.loads(jsonContent)
    tokenBearer = tokenBearer['access_token']
    tokenBearer = authbearer + tokenBearer
    
    # Metodo get
    r = requests.get('http://localhost:5500/all-social-networks', headers=({'Authorization': tokenBearer}))
    print("Obtener redes sociales: ", r.status_code, r.reason)
    redesSociales = r.content
    redesSociales = json.loads(redesSociales)
     
    print("Almacenar redes sociales -- Finalizado")
    return redesSociales

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
        email = (redesSociales[n]['email'])
        name = (redesSociales[n]['name'])
        
        try:
            if(name == 'twitter'): os.system('python3 prueba1.py')
            if(name == 'instagram'): os.system('python3 prueba2.py')   
            
            # -- Descomentar cuando las cuentas sean reales -- #
            # if(name == 'twitter'): os.system('python3 scraperTwitter.py email passw id')
            # if(name == 'instagram'): os.system('python3 scraperInstagram.py email passw id')
            # LOG acierto
        except:
            print("No se ha completado la red social numero: ", n)
            # LOG fallo
 
"""Elimina todas las conversaciones privadas almacenados de la carpeta
./csv
"""           
def eliminar_csv():
    dir = './csv'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))  


def log(tipo, id, finalizado):
    f = open('login.txt', 'w')
    f.write('Redsocial', tipo, ', id', id, 'a finalizado con:', finalizado)
    f.close
            
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
    #redesSociales = almacenarRedesSociales()
    #scraper(redesSociales)
    #prueba_añadir_score()
    #Enviar a modelo
    #eliminar_csv()
    
    
    #os.system('python3 scraperTwitter.py AlbertoJoseGuti Albertobaza10 1')
    os.system('python3 scraperInstagram.py albertoguti1995 alberto10 2')