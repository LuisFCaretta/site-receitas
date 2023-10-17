from selenium.webdriver.edge.service import Service
from selenium import webdriver
from pathlib import Path
from time import sleep
import os


ROOT_PATH = Path(__file__).parent.parent
EDGEDRIVER_NAME = 'msedgedriver.exe'
EDGEDRIVER_PATH = ROOT_PATH / 'bin' / EDGEDRIVER_NAME

# Executar sem abrir a janela do navegador
# --headless


def make_edge_browser(*options):
    edge_options = webdriver.EdgeOptions()

    if options is not None:
        for option in options:
            edge_options.add_argument(option)

    if os.environ.get('SELENIUM_HEADLESS') == '1':
        edge_options.add_argument('--headless')
    edge_service = Service(executable_path=EDGEDRIVER_PATH)  # type: ignore
    browser = webdriver.Edge(service=edge_service, options=edge_options)
    return browser


if __name__ == "__main__":
    browser = make_edge_browser()
    browser.get('https://www.google.com/')
    sleep(5)
    browser.quit()
