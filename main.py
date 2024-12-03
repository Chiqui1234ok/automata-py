import pyautogui
import subprocess
import time
import json
import os
import argparse

def open_app(path):
    """Abre una aplicación dada la ruta."""
    if os.path.isfile(path):
        try:
            subprocess.Popen([path], shell=True)
            time.sleep(3)
        except Exception as e:
            print(f"Error: {e}")
    else:
        print(f"Archivo no encontrado: {path}")

def point_and_click(x, y):
    """Mueve el mouse a una posición y hace clic."""
    pyautogui.moveTo(x, y)
    # pyautogui.click()  # Descomenta para activar el clic

def main(config_path):
    """Lee el archivo JSON y ejecuta las acciones."""
    if not os.path.isfile(config_path):
        print(f"El archivo de configuración '{config_path}' no existe.")
        return

    with open(config_path) as config_file:
        config = json.load(config_file)
    
    # Procesamos las acciones definidas en config.json
    for action in config["actions"]:
        if action["type"] == "open":
            open_app(action["path"])
        elif action["type"] == "point_and_click":
            point_and_click(action["x"], action["y"])

if __name__ == '__main__':
    # Configuración de argumentos de línea de comandos
    parser = argparse.ArgumentParser(description="Ejecuta acciones definidas en un archivo JSON.")
    parser.add_argument(
        "config_path",
        type=str,
        help="Ruta al archivo JSON con las acciones."
    )
    args = parser.parse_args()

    # Llama a la función principal con la ruta del archivo JSON
    main(args.config_path)
