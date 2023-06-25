import csv
import os
import datetime
from screens.path import get_logs_csv
from screens.error import window_error


def create_log_csv():
    """Crea el archivo csv en caso de que no exista en el sistema.
    """
    if not os.path.exists(get_logs_csv()):
        HEADER = ['timestamp', 'nick', 'event', 'value', 'text']
        try:
            with open(get_logs_csv(), 'a', newline='') as file:
                data = csv.writer(file)
                data.writerow(HEADER)
        except IOError:
            window_error(
                "Error al crear el archivo CSV de logs, intente dando los permisos correctos.")


def update_log(nick, event, value=None, text=None):
    """Agrega la accion realizada en el log con el nombre de usuario y el horario.

    Parametros:
    - nick(str): Nombre del usuario.
    - event(str): Evento realizado por el usuario.
    - value(str,optional): Nombre de las imagenes utilizadas 
    - text(str,optional): Texto agregado a la/s imagenes
    """
    now = datetime.datetime.now()
    actual_time = int(now.timestamp())
    row = [actual_time, nick, event, value, text]
    try:
        with open(get_logs_csv(), 'a', newline='') as file:
            data = csv.writer(file, lineterminator='\n')
            data.writerow(row)
    except FileNotFoundError:
        create_log_csv()
    except IOError:
        window_error(
            "Error al crear el archivo CSV de logs, intente dando los permisos correctos.")
