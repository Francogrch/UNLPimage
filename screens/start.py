from screens.new_profile import window_new_profile
from screens.main_menu import window_main_menu
import os
import PySimpleGUI as sg
import json
import screens.path as path
from screens.config import create_config_json
from screens.tagger import create_tagger_csv
from screens.log import create_log_csv


def window_start():
    """Muestra en pantalla la ventana de inicio de sesion del programa.

    Esta funcion utiliza las siguientes funciones:
    - window_main_menu : funcion que crea y muestra la ventana con el menu principal.
    - window_new_profile: funcion que rea y muestra la ventana para crear un nuevo perfil.

    Exepciones:
    - FileNotFound: Si el archivo JSON no existe, crea las variables dinamicas vacias.
    """

    def upgrade_carr(list_json, c_pant, first_profile):
        """Hace una actualizacion del carrouser
        Parametros:
        - list_json (list): Lista con los usuarios registrados en el json
        - c_pant (list): Lista los con objetos botones del carrousel
        - first_profile (int): Indice de la lista de usuarios, del primer perfil que se muestra en el carrousel 

        Retorna:
        - c_pant (list) : lista de carrousel actualizada
        - first_profile (int) : indice del primer perfil actualizado
        """
        c_pant[1].update(image_filename=list_json[first_profile]
                         [1], image_subsample=4)
        c_pant[2].update(
            image_filename=list_json[first_profile + 1][1], image_subsample=4)
        c_pant[3].update(
            image_filename=list_json[first_profile + 2][1], image_subsample=4)
        return c_pant, first_profile

    # Creates Files
    create_config_json()
    create_log_csv()
    create_tagger_csv()
    path.valid_image()
    # Style window
    sg.change_look_and_feel(path.get_theme())

    # Directions
    dir_json = path.get_profile_json()
    dir_interface = path.get_interface_folder()
    try:
        with open(dir_json) as file_profile:
            dic_json = json.load(file_profile)
            dir_avatar = path.get_avatar_folder()

            list_json = list(zip(dic_json.keys(), [os.path.join(
                dir_avatar, valor['image']) for key, valor in dic_json.items()]))
    except FileNotFoundError or IOError:
        dic_json = {}
        list_json = []

    # Buttons Carrousel
    len_json = len(list_json)
    if (len_json > 3):
        button_back = sg.Button(key='-BACKWARD-', border_width=0, button_color=(sg.theme_background_color(
        ), sg.theme_background_color()), image_filename=os.path.join(dir_interface, "arrow_left.png"), image_subsample=7)
        button_forward = sg.Button(key='-FORWARD-', border_width=0, button_color=(sg.theme_background_color(
        ), sg.theme_background_color()), image_filename=os.path.join(dir_interface, "arrow_right.png"), image_subsample=7)
        view_all = sg.Text('VER MAS', font="Italic 10 bold")
    else:
        button_back = sg.Button(border_width=0, button_color=(
            sg.theme_background_color(), sg.theme_background_color()))
        button_forward = sg.Button(border_width=0, button_color=(
            sg.theme_background_color(), sg.theme_background_color()))
        view_all = sg.Text()
    button_plus = sg.Button(key='-PLUS_PROFILE-', image_filename=os.path.join(dir_interface, "button_plus.png"),
                            image_subsample=4, border_width=0, button_color=(sg.theme_background_color(), sg.theme_background_color()))

    # Carrousel
    first_profile = 0
    if len_json < 3:
        carr_win = [sg.Button(key='-PROFILE' + str(index) + '-', image_filename=list_json[index][1], image_subsample=4, border_width=0,
                              button_color=((sg.theme_background_color()), (sg.theme_background_color()))) for index in range(len_json)]
    else:
        carr_win = [sg.Button(key='-PROFILE' + str(index) + '-', image_filename=list_json[index][1], image_subsample=4,
                              border_width=0, button_color=((sg.theme_background_color()), (sg.theme_background_color()))) for index in range(3)]

    carr_win.append(button_plus)
    carr_win.append(sg.Push())
    carr_win.insert(0, sg.Push())

    # Layout
    row_space = [sg.Text('', font='Italic 30 normal')]
    row0 = [sg.Push(), sg.Text(
        'UNLPImage', font='Courier 50 italic bold'), sg.Push()]
    row1 = [sg.Push(), sg.Text('| ELEGIR PERFIL |',
                               font='Courier 15 bold'), sg.Push()]
    row2 = [carr_win]
    row3 = [[sg.Push(), button_back, view_all, button_forward, sg.Push()]]
    last_row = [sg.Push(), sg.Text(
        "UNLP Informatica - Seminario Python ©", font="Italic 7 bold"), sg.Push()]
    layout = [[row_space], [row0], [row1], [sg.VPush()], [row2], [row3], [
        sg.VPush()], last_row]
    sg.set_global_icon(path.ICON_APP)
    # Window
    window = sg.Window("UNLP Image", layout, size=(700, 500), finalize=True)
    # Main loop
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == '-PLUS_PROFILE-':
            window.close()
            window_new_profile()
        if event == '-PROFILE0-':
            window.close()
            window_main_menu(list_json[first_profile][0])
        if event == '-PROFILE1-':
            window.close()
            window_main_menu(list_json[first_profile + 1][0])
        if event == '-PROFILE2-':
            window.close()
            window_main_menu(list_json[first_profile + 2][0])
        if event == '-FORWARD-':
            if (first_profile + 2) < (len(list_json) - 1):
                first_profile += 1
                carr_win, first_profile = upgrade_carr(
                    list_json, carr_win, first_profile)
        if event == '-BACKWARD-':
            if first_profile > 0:
                first_profile -= 1
                carr_win, first_profile = upgrade_carr(
                    list_json, carr_win, first_profile)

    window.close()
