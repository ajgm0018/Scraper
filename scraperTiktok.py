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

# -- Ayudas -- #

"""
# -- VER HTML -- #
html = browser.page_source
fileToWrite = open("page_source.html", "w")
fileToWrite.write(html)
fileToWrite.close()
fileToRead = open("page_source.html", "r")
print(fileToRead.read())
fileToRead.close()
# -------------- #
"""

# -- Funciones -- #

"""Configuración de Chromedriver para poder explorar el navegador
sin interfaz grafica dentro del servidor
"""
def conf_chrome():
    # Configuracion de chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless") # Eliminamos la interfaz
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-xss-auditor")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--no-first-run")
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--enable-extensions')
    chrome_options.add_argument('--incognito')
    chrome_options.add_argument("start-maximized")

    # Chrome is controlled by automated test software
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    # avoiding detection
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')

    # Default User Profile
    chrome_options.add_argument("--profile-directory=Default")
    chrome_options.add_argument("--user-data-dir=C:/Users/Admin/AppData/Local/Google/Chrome/User Data")
    
    # Añadir path de chromedirver a la configuracion
    homedir = os.path.expanduser("~")
    webdriver_service = Service(f"{homedir}/chromedriver/stable/chromedriver")
    
    # Eleccion de chrome como buscador
    browser = webdriver.Chrome(service=webdriver_service, options=chrome_options)
    
    return browser

def login():
    browser.get("https://www.tiktok.com/@paula_delaney")
    hola = browser.current_window_handle
    
    browser.get("https://www.tiktok.com/login")
    time.sleep(2)

    banner = browser.find_element(By.XPATH, '/html/body/tiktok-cookie-banner')
    browser.execute_script("arguments[0].setAttribute('disabled', 'true')", banner)
    time.sleep(2)
        
    iniciar = browser.find_elements(By.XPATH, '//div[@data-e2e="channel-item"]')
    iniciar[2].click()
    
    original = browser.current_window_handle
    for window_handle in browser.window_handles:
        if window_handle != original:
            browser.switch_to.window(window_handle)
        
    print("Introduciendo email")
    correo = browser.find_element(By.XPATH, '//input[@type="email"]')
    correo.send_keys("prevementalscraper@gmail.com")
    time.sleep(3)

    print("Pulsando boton aceptar")
    boton = browser.find_element(By.ID, 'next')
    boton.click()
    time.sleep(3)

    print("Introduciendo contraseña")
    correo = browser.find_element(By.XPATH, '//input[@type="password"]')
    correo.send_keys("94*!21vw^n")
    time.sleep(3)

    print("Iniciando sesion")
    boton = browser.find_element(By.ID, 'submit')
    boton.click()
    time.sleep(5)
    
    try:
        print("Dando permiso")
        boton = browser.find_element(By.ID, 'submit_approve_access')
        boton.click()
    except:
        print("No hay petición de acceso")
    
    time.sleep(5)
    
    browser.switch_to.window(hola)
    html = browser.page_source
    fileToWrite = open("page_source.html", "w")
    fileToWrite.write(html)
    fileToWrite.close()
    fileToRead = open("page_source.html", "r")
    print(fileToRead.read())
    fileToRead.close()
    

def get_user_info(username):
    #browser = conf_chrome()
    print("Entrando en el perfil de", username)
    url = "https://www.tiktok.com/@" + username
    
    browser.get(url)
    
    select = browser.find_element(By.XPATH, '//*[@data-e2e="user-bio"]')
    
    print("Esto es la BIO:", select.text)
    
    browser.refresh();
    time.sleep(5)
    
    boton_cerrar = browser.find_element(By.XPATH, '//*[@class="verify-bar-close--icon"]')
    boton_cerrar.click()
    
    videos = browser.find_elements(By.XPATH, '//div[@data-e2e="user-post-item"]')
    
    for n in range(len(videos) - 1):
        browser.fullscreen_window

        videos = browser.find_elements(By.XPATH, '//div[@data-e2e="user-post-item"]')
        print("Soy el video:", n)
        time.sleep(3)     
        
        banner = browser.find_element(By.XPATH, '/html/body/tiktok-cookie-banner')
        browser.execute_script("arguments[0].setAttribute('disabled', 'true')", banner)
        
        videos[n].click()
        print("Soy el video:", n, "-- Click")
        time.sleep(3)
        
        descripcion = browser.find_element(By.XPATH, '//*[@data-e2e="browse-video-desc"]')
        print("Descripcion: ", descripcion.text)
        time.sleep(3)    
        
        comentarios = browser.find_elements(By.XPATH, '//p[@data-e2e="comment-level-1"]')
        comentario = browser.find_element(By.XPATH, '//p[@data-e2e="comment-level-1"]')
        print("Hay ", len(comentarios), " comentarios")
        print(comentario.get_attribute('innerHTML'))
        for i in range(len(comentarios) - 1):
            print("Comentarios: ", comentarios[i])
        time.sleep(3)
        
        boton_cerrar = browser.find_element(By.XPATH, '//*[@class="verify-bar-close--icon"]')
        boton_cerrar.click()
        time.sleep(3)
        boton_cerrar = browser.find_element(By.XPATH, '//button[@data-e2e="browse-close"]')
        boton_cerrar.click()

# ---- Main ---- #
if __name__ == "__main__":
    # Guardo el buscador
    browser = conf_chrome()

    # Login
    login()

    # Conseguir información
    #browser.close
    #get_user_info("paula_delaney")