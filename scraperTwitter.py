# -- Librerias -- #
import os.path
import sys
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# -- Variables -- #
n_messages = 3

# -- Funciones -- #
def conf_chrome():
    # Configuracion de chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless") # Eliminamos la interfaz
    chrome_options.add_argument("--no-sandbox")
    
    # Añadir path de chromedirver a la configuracion
    homedir = os.path.expanduser("~")
    webdriver_service = Service(f"{homedir}/chromedriver/stable/chromedriver")
    
    # Eleccion de chrome como buscador
    browser = webdriver.Chrome(service=webdriver_service, options=chrome_options)
    
    return browser


def login():
    if len(sys.argv) != 3:
        print("Introduce <usuario> <contraseña> de Twitter")
        exit()
    else:
        username = sys.argv[1]
        password = sys.argv[2]
    
    # Login de twitter
    print("Accediendo a Twitter")
    browser.get("https://www.twitter.com/login")
    time.sleep(4)
        
    # Credenciales
    print("Accediendo a usuario - Pendiente")
    select = browser.find_element(By.NAME, 'text')
    select.click()
    select.send_keys(username)
    time.sleep(2)
      
    # Click en siguiente
    select = browser.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div')
    select.click()
    time.sleep(2)
    print("Accediendo a usuario - Éxito")
    
    # Enviar contraseña
    print("Accediendo a contraseña - Pendiente")
    select = browser.find_element(By.NAME, 'password')
    select.send_keys(password)
    time.sleep(2)
    
    # Click en entrar
    select = browser.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div')
    select.click()
    time.sleep(4)
    print("Accediendo a contraseña - Éxito")  


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

def to_csv(all):
    df = pd.DataFrame(all, columns=['Mensajes_texto'])
    df = df.dropna()
    df.to_csv("csv/twitter_datos.csv")

# ---- Main ---- #
if __name__ == "__main__":
    # Guardo el buscador
    browser = conf_chrome() 
    # Almacenamos credenciales
    login()
    # Obtenemos los mensajes
    all_messages = get_messages(n_messages)
    # Almacenamos los mensajes
    to_csv(all_messages)