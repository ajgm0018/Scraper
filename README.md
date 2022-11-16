# Scraper

Para el funcionamiento de los scripts es necesario:

- Tener un SSOO Linux/Ubuntu o WSL2 instalado
- Cambiar el directorio: cd "$HOME"

Instalar Chrome siguiendo los siguientes pasos:

- wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
- sudo dpkg -i google-chrome-stable_current_amd64.deb
- sudo apt --fix-broken install
- google-chrome-stable --version (para confirmar la última versión)

Instalar compatible Chromedriver siguiendo los siguientes pasos:

- chrome_driver=$(curl "https://chromedriver.storage.googleapis.com/LATEST_RELEASE") && \
  echo "$chrome_driver"
- curl -Lo chromedriver_linux64.zip "https://chromedriver.storage.googleapis.com/\
  ${chrome_driver}/chromedriver_linux64.zip"
- sudo apt install unzip
- mkdir -p "chromedriver/stable" && \
  unzip -q "chromedriver_linux64.zip" -d "chromedriver/stable" && \
  chmod +x "chromedriver/stable/chromedriver"
  
Configurar Python y Selenium:

- python3 --version
- sudo apt install python3.8-venv -y (utilizar la version correspondiente, en el desarrollo se ha utilizado la instrucciones mostradas)
- python3 -m venv .venv
- source .venv/bin/activate
- pip install selenium
