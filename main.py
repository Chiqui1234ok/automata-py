import pyautogui
import subprocess
import time
import json

def open(path):
    subprocess.Popen(path)
    time.sleep(10) # 10 segundos para esperar a que abra la app

def point_and_click(x, y):
    pyautogui.moveTo(x, y)
    pyautogui.click()

def main():
    # debe haber un archivo de configuración 'config.json' junto al ejecutable
    with open('config.json') as config:
        config = json.load(config)
    
if __name__ == '__main__':
    main()