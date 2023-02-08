# -- Librerias -- #
import os.path
import sys
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import configparser
# import tweepy

# -- Variables -- #
n_messages = 3
id_nombre = ""

# -- Funciones -- #
def conf_chrome():
    # Configuracion de chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless") # Eliminamos la interfaz
    chrome_options.add_argument("--no-sandbox")
    #chrome_options.add_argument("window-size=1920,1080")

    # Añadir path de chromedirver a la configuracion
    # homedir = os.path.expanduser("~")
    webdriver_service = Service("/home/agmegias/chromedriver/stable/chromedriver") # Cambiado por el servidor

    # Eleccion de chrome como buscador
    browser = webdriver.Chrome(service=webdriver_service, options=chrome_options)
    return browser

def login(username, password):

    # Login de twitter
    print("\nAccediendo a Twitter")
    browser.get("https://www.twitter.com/login")
    time.sleep(4)
        
    # Credenciales
    print("Accediendo a usuario - Pendiente")
    select = browser.find_element(By.NAME, 'text')
    select.click()
    select.send_keys(username)
    time.sleep(4)
    
    # Click en siguiente
    select = browser.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div')
    select.click()
    time.sleep(4)
    print("Accediendo a usuario - Éxito")
    
    # Enviar contraseña
    print("Accediendo a contraseña - Pendiente")
    select = browser.find_element(By.NAME, 'password')
    select.send_keys(password)
    time.sleep(4)
    
    # Click en entrar
    select = browser.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div')
    select.click()
    time.sleep(4)
    print("Accediendo a contraseña - Éxito")  

def params():
    if len(sys.argv) != 4:
        print("Introduce <usuario> <contraseña> de Twitter")
        exit()
    else:
        username = sys.argv[1]
        password = sys.argv[2]
        id_nombre = sys.argv[3]
    return username, password, id_nombre

def get_messages(n_messages):
    print("Accediendo a mensajes - Pendiente")
    # Accedemos a los mensajes directos
    browser.get("https://www.twitter.com/messages")
    time.sleep(2)
    print("Accediendo a mensajes - Éxito")
    
    all_messages = []
    
    # Solo los últimos 20 mensajes por conversación
    for n_message in range (n_messages):
        print("Mensaje [",n_message,"] - Realizando")
        # Entrar
        messages = browser.find_elements(By.XPATH, '//div[@data-testid="conversation"]')
        messages[n_message].click()
        time.sleep(2)
        
        # Mensajes
        tips = browser.find_elements(By.XPATH, '//div[@role="presentation"]')
        for n in range (len(tips)):
            if tips[n].text != "":
                all_messages.append(tips[n].text)
        
        # Salir
        select = browser.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div/div/div/div[1]/div/div')
        select.click()
        time.sleep(2)
        
    return all_messages

def to_csv(all, id_nombre):
    df = pd.DataFrame(all, columns=['Mensajes_texto'])
    df = df.dropna()
    nombre = 'csv/id_' + str(id_nombre) + '.csv'
    df.to_csv(nombre)
    
def to_csv_error(id_nombre):
    df = pd.DataFrame()
    df['Mensaje Texto'] = ['Error']
    nombre = 'csv/id_' + id_nombre + '.csv'
    df.to_csv(nombre)

def twitter_api():
    """
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    api_key = config['twitter']['api_key']
    api_key_secret = config['twitter']['api_key_secret']
    access_token = config['twitter']['access_token']
    access_token_secret = config['twitter']['access_token_secret']
    
    auth = tweepy.OAuthHandler(api_key, api_key_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    
    user_name = 'jcollado95'

    tweets = api.user_timeline(screen_name=user_name, count=200, tweet_mode='extended')
    
    # DataFrame
    columns = ['TweetId', 'User', 'Tweet']
    data = []

    for tweet in tweets:
        data.append([tweet.id, tweet.user.screen_name, tweet.full_text])

    df = pd.DataFrame(data, columns=columns)

    print(df)
    """
    print("Descomentame")
    
# ---- Main ---- #
if __name__ == "__main__":
    #try:
        # Guardo el buscador
        browser = conf_chrome() 
        # Parametros
        username, password, id_nombre = params()
        # Almacenamos credenciales
        login(username, password)
        # Obtenemos los mensajes
        all_messages = get_messages(n_messages)
        # Almacenamos los mensajes
        to_csv(all_messages, id_nombre)
        # Twitter API para los tweets
        #twitter_api() # Esto va a dejar de funcionar pronto
"""
except:
    if(id_nombre != ""):
        to_csv_error(id_nombre)
        print(" -- Se ha producido un error con la red social ", id_nombre ," --")
    else:
        print("¿ERROR?!")
"""