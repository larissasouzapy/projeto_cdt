import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pyautogui


options = webdriver.ChromeOptions()

options.add_experimental_option("detach", True)

print("Abrindo o navegador...")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://web.whatsapp.com/")

print("Por favor, escaneie o QR Code do WhatsApp Web se necessário.")
print("Você tem 15 segundos para garantir que a página carregou completamente...")
time.sleep(15) 

nome_grupo = "Programação" 
mensagem = "@larissasoyza Olá! Esta é uma mensagem automatizada do seu projeto de reconhecimento facial. 🚀"

try:
    print(f"Buscando pelo grupo: {nome_grupo}...")
    
   
    pesquisa_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
    pesquisa_box.click()
    time.sleep(1)
    

    pesquisa_box.send_keys(nome_grupo)
    time.sleep(2)
    pesquisa_box.send_keys(Keys.ENTER)
    time.sleep(2)
    
    print("Entrando no chat e enviando a mensagem...")
  
    chat_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
    chat_box.click()
    time.sleep(1)
    
  
    chat_box.send_keys(mensagem)
    time.sleep(1)
    

    chat_box.send_keys(Keys.ENTER)
    
    print("Mensagem enviada com sucesso!")

except Exception as e:
    print(f"Ocorreu um erro durante a automação: {e}")