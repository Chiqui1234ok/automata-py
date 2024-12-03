import mouse
import keyboard
import json
import os
import threading
from datetime import datetime
from time import time, sleep

def get_timestamped_filename(base_name="config"):
    """Genera un nombre de archivo con la fecha y hora actual dentro de la carpeta 'library'."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    os.makedirs("library", exist_ok=True)  # Asegura que la carpeta exista
    return os.path.join("library", f"{base_name}_{timestamp}.json")

def save_to_config(actions):
    """Guarda las acciones en un archivo JSON con un nombre timestamped."""
    filename = get_timestamped_filename()
    config = {"actions": actions}
    with open(filename, "w") as file:
        json.dump(config, file, indent=4)
    print(f"Configuración guardada en {filename}")

def load_hotkeys(file="hotkeys.json"):
    """Carga las combinaciones de teclas desde el archivo JSON."""
    if not os.path.exists(file):
        # Crear archivo hotkeys.json por defecto si no existe
        hotkeys = {"close_recorder": ["ctrl", "alt", "q"]}
        with open(file, "w") as f:
            json.dump(hotkeys, f, indent=4)
        print(f"Archivo {file} creado con hotkey predeterminada.")
        return hotkeys
    else:
        with open(file, "r") as f:
            return json.load(f)

def recorder_thread(actions, last_click_time, lock):
    """Hilo principal del grabador de clics."""
    print("Script iniciado. Haz clic en cualquier lugar para registrar coordenadas.")
    print("Presiona la hotkey configurada para detener el grabador.")

    def on_click():
        nonlocal last_click_time
        x, y = mouse.get_position()
        current_time = time()
        delay = int((current_time - last_click_time) * 1000)  # Calcula el delay en milisegundos
        print(f"Clic registrado en ({x}, {y}) con delay {delay} ms")
        with lock:
            actions.append({"type": "point_and_click", "x": x, "y": y, "delay": delay})
        last_click_time = current_time

    # Registrar eventos del mouse (solo clics)
    mouse.on_button(on_click, buttons=("left", "right", "middle"), types=("down",))

    while recording.is_set():
        sleep(0.1)  # Reducir uso de CPU

    # Guardar las acciones restantes al salir
    with lock:
        if actions:
            save_to_config(actions)
    print("Grabador detenido.")

# Variables globales
actions = []
last_click_time = time()  # Inicializamos con el tiempo actual
lock = threading.Lock()
recording = threading.Event()
recording.set()

def main():
    global recording

    # Cargar hotkeys
    hotkeys = load_hotkeys()
    close_hotkey = hotkeys.get("close_recorder", ["ctrl", "alt", "q"])
    close_hotkey_str = "+".join(close_hotkey)

    # Registrar hotkey para cerrar el grabador
    keyboard.add_hotkey(close_hotkey_str, lambda: stop_recording())
    print(f"Hotkey para cerrar configurada: {close_hotkey_str}")

    # Iniciar el hilo del grabador
    recorder = threading.Thread(target=recorder_thread, args=(actions, last_click_time, lock))
    recorder.start()

    # Esperar a que el usuario cierre el grabador
    recorder.join()

def stop_recording():
    """Detiene el grabador."""
    global recording
    recording.clear()

if __name__ == "__main__":
    main()
