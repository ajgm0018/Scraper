# -- Librerias -- #
import os.path
import sys
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# -- Variables -- #
n_messages = 6
id_nombre = ""

# -- Funciones -- #

"""Configuración de Chromedriver para poder explorar el navegador
sin interfaz grafica dentro del servidor
"""
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

"""Petición de parámetros cuando se llama al scraper
"""
def params():
    if len(sys.argv) != 4:
        print("Introduce <usuario> <contraseña> de Twitter")
        exit()
    else:
        username = sys.argv[1]
        password = sys.argv[2]
        id_nombre = sys.argv[3]
    return username, password, id_nombre

"""Pasos en webdriver para poder acceder a la cuenta de usuario
de la red social
"""
def login(username, password):
    # Login de instagram
    print("\nAccediendo a Instagram")
    browser.get("https://www.instagram.com/login")
    time.sleep(4)
    
    # Pop-up
    print("Cruzando pop-up - Inicio sesión")
    select = browser.find_element(By.XPATH, '//*[@class="_a9-- _a9_0"]')
    select.click()
    
    # Credenciales
    print("Accediendo a usuario - Pendiente")
    select = browser.find_element(By.NAME, 'username')
    select.send_keys(username)
    select = browser.find_element(By.NAME, 'password')
    select.send_keys(password)
    time.sleep(3)
    
    # Click en siguiente
    select = browser.find_element(By.XPATH, '//*[@id="loginForm"]')
    select.click()
    time.sleep(3)
    print("Accediendo a usuario - Éxito")
    
    try:
        print("Validando popup - Dentro de sesión")
        select = WebDriverWait(browser, timeout=15).until(lambda d: d.find_element(By.XPATH,'//*[@class="_ac8f"]'))
        #select = browser.find_element(By.XPATH, '//*[@class="_ac8f"]');
        select.click()
        time.sleep(2)
    except:
        print("No hay pop-up - Dentro de sesion")
    
    # Entrar en mensajes
    select = browser.find_element(By.XPATH, '//a[@href="/direct/inbox/"]')
    select.click()
    time.sleep(4)
    
    print("Accediendo a mensajes - Éxito") 

"""Pasos en webdriver para poder acceder a las conversaciones
del usuario de la red social
@n_messages: Numero de conversaciones que exporta
"""
def get_messages(n_messages):
    
    all_messages = []
    
    messages = browser.find_elements(By.XPATH, '//*[@class="_abm4"]');
    print("Se han encontrado:", len(messages), "conversaciones")
    
    for n_messages in range (len(messages) - 1):
        print("Procesando conversacion:",n_messages)
        messages[n_messages].click()
        time.sleep(2)
        
        tips = browser.find_elements(By.XPATH, '//div[@role="button"]')
        
        for n in range(len(tips) - 1):
            if(tips[n].text != ""):
                all_messages.append(tips[n].text)
    
    print("Recopilación de mensajes - Éxito")
    return all_messages

"""Recoge todos los mensajes almacenador y el id de la redsocial y
lo exporta a csv, añadiendo este id, al nombre del archivo
"""
def to_csv(all, id_nombre):
    df = pd.DataFrame(all, columns=['Mensajes_texto'])
    df = df.dropna()
    nombre = 'csv/id_' + str(id_nombre) + '.csv'
    df.to_csv(nombre)
    
def to_csv_error(error, id_nombre):
    df = pd.DataFrame()
    df['Mensaje Texto'] = ['Error']
    nombre = 'csv/id_' + id_nombre + '.csv'
    df.to_csv(nombre)

# ---- Main ---- #
if __name__ == "__main__":
    try:
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
    except:
        if(id_nombre != ""):
            print(" -- Se ha producido un error con la red social ", id_nombre ," --")
            to_csv_error("Error desconocido",id_nombre)
        else:
            print("¿ERROR?!")