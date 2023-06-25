from screens.main_menu import window_main_menu
from screens.path import get_interface_folder, get_theme
import PySimpleGUI as sg
import os
from screens.collage_generator import window_collage_generator


def window_collage(nick):
    """Crea y muestra la ventana para seleccionar una plantilla de collage.

    Parámetros:
    - nick (str): nombre de usuario logueado.

    Esta función utiliza la siguientes funciones definidas en el módulo screens:
    - window_main_menu: función que crea y muestra la ventana del menu principal.
    - window_collage_generator: función que crea y muestra la ventana para generar un collage.

    La funcion muestra en pantalla una serie de plantillas para luego utilizar a la hora de generar un collage."""
    
    sg.change_look_and_feel(get_theme())
    TEMPLATE_KEYS = ["-SPLIT_VERTICAL-", "-DOUBLE_SQUARE_RIGHT-", "-DOUBLE_SQUARE_UP-",
                     "-SPLIT_HORIZONTAL-", "-DOUBLE_SQUARE_LEFT-", "-DOUBLE_SQUARE_DOWN-"]

    topcolum1 = [[sg.Button(key="-BACK-", border_width=0, button_color=(sg.theme_background_color(), sg.theme_background_color()),
                            image_filename=os.path.join(get_interface_folder(), "back.png"), image_subsample=6, tooltip='Volver')]]
    topcolum2 = [[sg.Text("| Diseño de collage |", font='Courier 15 bold')]]
    row1 = [[sg.Column(topcolum1), sg.Push(), sg.Column(
        topcolum2, element_justification="Center")]]

    row2 = [sg.Push(), sg.Button(key="-SPLIT_VERTICAL-", border_width=0, button_color=(sg.theme_background_color(), sg.theme_background_color()),
                                 image_filename=os.path.join(get_interface_folder(), "split_vertical.png"), image_subsample=1),
            sg.Push(), sg.Button(key="-DOUBLE_SQUARE_RIGHT-", border_width=0, button_color=(sg.theme_background_color(), sg.theme_background_color()),
                                 image_filename=os.path.join(get_interface_folder(), "double_square_right.png"), image_subsample=1),
            sg.Push(), sg.Button(key="-DOUBLE_SQUARE_UP-", border_width=0, button_color=(sg.theme_background_color(), sg.theme_background_color()),
                                 image_filename=os.path.join(get_interface_folder(), "double_square_up.png"), image_subsample=1), sg.Push()]

    row3 = [sg.Push(), sg.Button(key="-SPLIT_HORIZONTAL-", border_width=0, button_color=(sg.theme_background_color(), sg.theme_background_color()),
                                 image_filename=os.path.join(get_interface_folder(), "split_horizontal.png"), image_subsample=1),
            sg.Push(), sg.Button(key="-DOUBLE_SQUARE_LEFT-", border_width=0, button_color=(sg.theme_background_color(), sg.theme_background_color()),
                                 image_filename=os.path.join(get_interface_folder(), "double_square_left.png"), image_subsample=1),
            sg.Push(), sg.Button(key="-DOUBLE_SQUARE_DOWN-", border_width=0, button_color=(sg.theme_background_color(), sg.theme_background_color()),
                                 image_filename=os.path.join(get_interface_folder(), "double_square_down.png"), image_subsample=1), sg.Push()]

    last_row = [sg.Push(), sg.Text(
        "UNLP Informatica-Seminario Python ©", font="Italic 7 bold"), sg.Push()]

    layout = [[row1], [sg.VPush()],
              [row2], [sg.VPush()],
              [row3],
              [sg.VPush()],
              [last_row]]

    window = sg.Window("UNLP Image", layout, size=(700, 500))

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == "-BACK-":
            window.close()
            window_main_menu(nick)
            break
        if event in TEMPLATE_KEYS:
            window.close()
            window_collage_generator(nick, event[1:-1].lower())
    window.close()
