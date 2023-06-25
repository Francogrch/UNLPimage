import os
import json
import PySimpleGUI as sg
from screens.main_menu import window_main_menu
from screens.path import get_image_default_folder, get_memes_default_folder, get_collage_default_folder, get_config_json, get_theme, get_interface_folder, get_main_folder, get_collage_folder, get_image_folder,get_memes_folder
from screens.log import update_log
from screens.error import window_error


def create_config_json():
    """Crea un archivo json donde se guarda la configuracion la configuracion lo crea con valores por defecto
    en caso de no existir

    Esta funcion utiliza la siguiente funcion definida en screens/path:
    - get_config_json(): funcion que devuelve la direccion donde se guarda el archivo json.
    """
    try:
        if not os.path.exists(get_config_json()):
            with open(get_config_json(), 'x') as archivo_json:

                config = {"Images": get_image_default_folder(), "Collage": get_collage_default_folder(
                ),  "Memes": get_memes_default_folder()}
                for key in config.keys():
                    config[key].insert(0, 'grupo16')
                config['Theme'] = 'DarkGrey2'
                json.dump(config, archivo_json, indent=3)
    except TypeError:
        window_error('carpeta config no se encuentra')


def window_config(nick):
    """Permite cambiar y guardan las rutas de donde se guardan las imagenes, los collages y los memes
    las direcciones guardadas aparecen en los input 

    Esta funcion utiliza las siguientes funciones definidas en screens:
    - window_main_menu(): funcion que crea y abre la ventana del menu principal.
    - create_config_json(): funcion que crea el archivo json en caso de no existir
    """
    sg.change_look_and_feel(get_theme())
    LIST_THEMES = ['DarkGrey2', 'Topanga', 'DarkAmber', 'DarkBrown1',
                   'DarkGrey3', 'Reds', 'LightBrown8', 'LightBrown5']
    TOOLTIP_SAVE = " Guardar los cambios realizados "
    TOOLTIP_BACK = " Volver al menu principal "
    TOOLTIP_SELECT_IMAGE = " Permite seleccionar la ruta de la carpeta donde buscar imagenes "
    TOOLTIP_SELECT_COLLAGE = " Permite seleccionar la ruta de la carpeta donde se guardan los collage creados "
    TOOLTIP_SELECT_MEMES = " Permite seleccionar la ruta de la carpeta donde se guardan los memes generados "
    FONT_GENERAL = ('Italic 15 normal')
    FONT_INPUT = ('Italic 13 normal')
    SZ_INPUT = 43

    try:
        with open(get_config_json()) as json_file:
            config = json.load(json_file)
    except FileNotFoundError or IOError:
        create_config_json()

    def change_path(window, event):
        if is_valid(values[event]):
            window[event].update(split_dir(values[event]))
            values[event] = split_dir(values[event])
        else:
            if event == '-COLLAGE-':
                window[event].update(os.path.join(get_collage_folder()[(len(get_main_folder())-7):]))
            if event == '-MEMES-':
                window[event].update(os.path.join(get_memes_folder()[(len(get_main_folder())-7):]))
            if event == '-IMAGE-':
                window[event].update(os.path.join(get_image_folder()[(len(get_main_folder())-7):]))
            window_error(
                'La carpeta no esta dentro del directorio del programa.')

    def is_valid(path):
        return os.path.normcase(get_main_folder()) == os.path.normcase(os.path.join(path[:len(get_main_folder())]))

    def split_dir(path):
        return os.path.normcase(os.path.join(path[(len(get_main_folder())-7):]))

    def save_config(config, path_images, path_collage, path_memes, theme):
        """Guarda las rutas ingresadas en un archivo.json
        la existencia/creacion del archivo se verifica en screens.start.py con la funcion create_config_json()
        Updatea el log, guardando solo las rutas nuevas

        Parametros:
        - config(dict): diccionario que guarda los del archivo json
        - path_images(str): direccion donde guardar las imagenes, ingresada por el usuario
        - path_collage(str): direccion donde guardar los collages, ingresada por el usuario
        - path_memes(str): direccion donde guardar los memes, ingresada por el usuario
        - theme(str): tema de la interfar, ingresado por el usuario
        """
        if path_images != os.path.join(*config["Images"]):
            config["Images"] = path_images.split(os.path.sep)
            update_log(nick, f"change_config_image_path")
        if path_collage != os.path.join(*config["Collage"]):
            config["Collage"] = path_collage.split(os.path.sep)
            update_log(nick, f"change_config_collage_path")
        if path_memes != os.path.join(*config["Memes"]):
            config["Memes"] = path_memes.split(os.path.sep)
            update_log(nick, f"change_config_meme_path")
        config["Theme"] = theme
        try:
            with open(get_config_json(), "w") as json_file:
                json.dump(config, json_file, indent=3)
        except FileNotFoundError or IOError:
            with open(get_config_json(), 'x') as archivo_json:
                config = {'Theme': 'DarkGrey2'}
                json.dump(config, archivo_json, indent=3)

    topcolum1 = [[sg.Button(key="-BACK-", border_width=0, button_color=(sg.theme_background_color(), sg.theme_background_color()),
                            image_filename=os.path.join(get_interface_folder(), "back.png"), image_subsample=6, tooltip=TOOLTIP_BACK)]]
    topcolum2 = [
        [sg.Push(), sg.Text("| CONFIGURACION |", font='Courier 15 bold')]]
    row1 = [[sg.Column(topcolum1, size=(378, 50)), sg.Column(
        topcolum2, element_justification="Center")]]
    row2 = [[sg.Push(), sg.Text("Carpeta de imagenes: ", font=FONT_GENERAL), sg.Push(), sg.Push(), sg.Push(), sg.Push(), sg.Push()],
            [sg.Push(), sg.InputText(key='-IMAGE-', font=FONT_INPUT, size=SZ_INPUT, default_text=(os.path.join(*config["Images"])), text_color='black',
                                     disabled=True, enable_events=True), sg.FolderBrowse('Seleccionar', font=FONT_INPUT, tooltip=TOOLTIP_SELECT_IMAGE), sg.Push()],
            [sg.Push(), sg.Text("Carpeta de Collage: ", font=FONT_GENERAL),
             sg.Push(), sg.Push(), sg.Push(), sg.Push(), sg.Push()],
            [sg.Push(), sg.InputText(key='-COLLAGE-', font=FONT_INPUT, size=SZ_INPUT, default_text=(os.path.join(*config["Collage"])), text_color='black',
                                     disabled=True, enable_events=True), sg.FolderBrowse('Seleccionar', font=FONT_INPUT, tooltip=TOOLTIP_SELECT_COLLAGE), sg.Push()],
            [sg.Push(), sg.Text("Carpeta de Memes: ", font=FONT_GENERAL),
             sg.Push(), sg.Push(), sg.Push(), sg.Push(), sg.Push()],
            [sg.Push(), sg.InputText(key='-MEMES-', font=FONT_INPUT, size=SZ_INPUT, default_text=(os.path.join(*config["Memes"])), text_color='black',
                                     disabled=True, enable_events=True), sg.FolderBrowse('Seleccionar', font=FONT_INPUT, tooltip=TOOLTIP_SELECT_MEMES), sg.Push()]]
    row3 = [[sg.Push(), sg.Text("Tema: ", font=FONT_INPUT), sg.Combo(LIST_THEMES, default_value=config["Theme"], key='-THEME-', readonly=True),
             sg.Push(), sg.Button("Guardar", key="-SAVE-", size=round(10), font=FONT_INPUT, tooltip=TOOLTIP_SAVE), sg.Push()]]

    last_row = [sg.Push(), sg.Text(
        "UNLP Informatica-Seminario Python ©", font="Italic 7 bold"), sg.Push()]

    layout = [row1, [sg.VPush()], row2, [sg.VPush()],
              row3, [sg.VPush()], last_row]

    window = sg.Window("UNLP Image", layout, size=(700, 500))
    while True:
        event, values = window.read()
        if event == '-BACK-':
            window.close()
            window_main_menu(nick)
            break
        if event == sg.WIN_CLOSED:
            break
        if event == '-COLLAGE-' or event == '-MEMES-' or event == '-IMAGE-':
            change_path(window, event)
        if event == '-SAVE-':
            save_config(config, values["-IMAGE-"],
                        values["-COLLAGE-"], values["-MEMES-"], values["-THEME-"])
            window.close()
            window_main_menu(nick)
    window.close()
