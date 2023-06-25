import PySimpleGUI as sg
import os


def window_error(error, title='ERROR'):
    """Genera una ventana emergente con un error dependiendo que haya sucedido.

    Parametros:
    - error (Str): Texto de la ventana de error.
    """
    from screens.path import get_interface_folder, get_theme, get_fonts_folder
    from screens.new_profile import set_image
    IMAGE = os.path.join(get_interface_folder(), "error.png")
    sg.change_look_and_feel(get_theme())

    row1 = [[sg.Push(), sg.Image(key='-IMAGE-'), sg.Push()]]
    row2 = [[sg.Push(), sg.Text(error.upper(), size=(40, None),
                                font='calibri 13 bold', justification='center'), sg.Push()]]
    row3 = [[sg.Push(), sg.Button(" Aceptar ".upper(), key="-ACEPT-",
                                  font='arial 10 bold'), sg.Push()]]
    layout_error = [row1, [sg.VPush()], row2, [sg.VPush()], row3, [sg.VPush()]]
    window = sg.Window(title, layout_error, finalize=True, size=(400, 350))
    window['-IMAGE-'].update(data=set_image(IMAGE, (200, 200)))
    exit_var = False  # Variable para generar un bucle hasta que se aprete el boton -ACEPT-

    while not exit_var:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "-ACEPT-":
            exit_var = True
            window.close()
