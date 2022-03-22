from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome('./chromedriver')
driver.get("http://40.71.0.94:8080/#")
assert "SempreLeio" in driver.title

## Autentica usuário
elem = driver.find_element(By.XPATH, "//a[@href='/Login']")
elem.click()
elem = driver.find_element(By.NAME, "username")
elem.clear()
elem.send_keys("vicente")
elem = driver.find_element(By.NAME, "password")
elem.clear()
elem.send_keys("teste@123")
elem.send_keys(Keys.RETURN)

time.sleep(5)
## Mostra detalhes da comunidade
try:
    elem = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//a[@href='/PerfilComunidade/6']"))
    )
except:
    assert False

elem.click()

time.sleep(5)
## Mostra os membros da comunidade em detalhe
try:
    elem = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//button[normalize-space()="Membros"]'))
    )
except:
    assert False

elem.click()

time.sleep(5)
## Volta ao detalhe da comunidade
try:
    elem = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '/html/body'))
    )
except:
    assert False

elem.send_keys(Keys.ESCAPE)

time.sleep(5)
## Aciona botão para postar
try:
    elem = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Postar')]"))
    )
except:
    assert False

time.sleep(5)
driver.close()