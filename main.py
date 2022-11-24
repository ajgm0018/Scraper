# -- Librerias -- #
import os
import pandas as pd
import requests
import json


# -- Variables -- #
superusario = "a@a.com"
password = "alberto10"
authbearer = "Bearer "


# -- Funciones -- #
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
        except:
            print("No se ha completado la red social numero: ", n)
        
def prueba():
       os.system('python3 scraperInstagram.py error error 2')  
       os.system('python3 scraperInstagram.py albertoguti1995 alberto10 1')  

# ---- Main ---- #
if __name__ == "__main__":
    #redesSociales = almacenarRedesSociales()
    #scraper(redesSociales)
    prueba()