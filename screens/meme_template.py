import PySimpleGUI as sg
import os
import json


def window_meme_template(nick):
    """Permite crear memes eligiendo una imagen y agregando texto

    Esta funcion utiliza las siguientes funciones definidas en screens:
    - get_theme():  funcion que retorna el tema para la ventana
    - get_interface_folder(): funcion que devuelve la direccion de la carpeta interface
    - get_datafile_folder(): funcion que devuelve la direccion de la carpeta datafile
    - get_memes_folder(): funcion que devuelve la direccion de la carpeta memes
    - window_main_menu(): funcion que crea y abre la ventana del menu principal.
    - resize(): funcion que devuelve una imagen ajustada para mostrar
    - window_error(): funcion que genera una ventana de error

    Parametros:
    - nick(str): el nick del usuario
    """

    from screens.path import get_theme, get_interface_folder, get_datafile_folder, get_memes_folder
    from screens.main_menu import window_main_menu
    from screens.meme_generator import window_meme_generator
    from screens.tagger import resize
    from screens.error import window_error

    def update_rigth_side(dir):
        """ Recibe el nombre de archivo de un meme, lo ajusta y lo muestra en la mitad derecha de la ventana

        Parametros:
        - dir(str): Nombre del arhivo a mostrar
        """
        full_dir = os.path.join(get_interface_folder(), 'memes', dir)
        window["-IMAGE-"].update(data=resize(full_dir, (350, 350)))
    exist=True
    try:  # copio la data del meme.json en full_dict
        with open(os.path.join(get_datafile_folder(), 'meme.json')) as json_file:
            full_dict = json.load(json_file)
    except FileNotFoundError:
        window_error("No se encuentra el archivo meme.json")
        full_dict = {'error':{'image':'error'}}
        exist=False


    sg.change_look_and_feel(get_theme())
    FONT_BUTTON = 'Italic 12 bold'

    # copio los nombres de los memes(keys) y reemplazo los '_'
    templates = list(full_dict.keys())
    # guardo el primer meme para mostrar por defecto
    first_meme = templates[0]
    templates = [meme.replace("_", " ")for meme in templates]
    # diccionario con formato {nombre_meme_mostrado, nombre_meme_archivo}
    dict_name = dict(
        map(lambda key: (key, full_dict[key]['image']), full_dict))
    default_meme = dict_name[first_meme]

    left_column = [
                  [sg.Push(), sg.Listbox(templates, key="-FILE_LIST-", font=any, size=(18, 12), no_scrollbar=False, sbar_width=0,
                                         enable_events=True, pad=(0, (10, 70)),
                                         ), sg.Push()],
        [sg.Push(), sg.Button("  SELECCIONAR  ", font=FONT_BUTTON, key="-GENERATE-"), sg.Push()]]

    rigth_column = [
        [sg.Push(), sg.Image(key="-IMAGE-", size=(250, 250)), sg.Push()]]

    topcolum1 = [[sg.Button(key="-BACK-", border_width=0, button_color=(sg.theme_background_color(), sg.theme_background_color()),
                            image_filename=os.path.join(get_interface_folder(), "back.png"), image_subsample=6, tooltip=' Volver al menu principal ')]]
    topcolum2 = [
        [sg.Text("| Seleccionar Plantilla |", font='Courier 15 bold')]]
    row0 = [sg.Column(topcolum1), sg.Push(), sg.Column(topcolum2)]

    last_row = [sg.Push(), sg.Text(
        "UNLP Informatica-Seminario Python ©", font="Italic 7 bold"), sg.Push()]

    row1 = [sg.Push(), sg.Column(left_column, pad=((80, 80), 0)), sg.Push(),
            sg.Column(rigth_column), sg.Push()]

    layout = [row0,
              [sg.VPush()],
              row1,
              [sg.VPush()],
              last_row]

    window = sg.Window("UNLP Image", layout, size=(700, 500), finalize=True)
    # cargo la imagen por defecto
    default_dir = os.path.join(get_interface_folder(), 'memes', default_meme)
    if exist:
        window["-IMAGE-"].update(data=resize(default_dir, (350, 350)))
    window["-BACK-"].bind("<Return>", "_Enter")

    while exist:
        # "Volver" cierra la ventana y abre el menu principal manteniendo el usuario
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == '-BACK-':
            window.close()
            window_main_menu(nick)
            break
        elif event == "-FILE_LIST-":  # devuelvo los '_' a la imagen seleccionada y actualizo
            meme_name = values["-FILE_LIST-"][0].replace(" ", "_")
            update_rigth_side(dict_name[meme_name])
        elif event == "-GENERATE-":
            try:  # si seleccione una imagen le devuelvo los '_'
                meme_name = values["-FILE_LIST-"][0].replace(" ", "_")
            except IndexError:
                # si no seleccione una imagen guardo la imagen
                # por defecto
                meme_name = first_meme
            # compruebo que la imagen existe antes de llamar al meme_generator
            dir = os.path.join(get_interface_folder(),
                               'memes', dict_name[meme_name])
            if not os.path.exists(dir):
                window_error(
                    "No se puede generar un meme debido a que la imagen seleccionada no existe")
            else:  # abro la ventana meme_generator con el nombre del meme
                window.close()
                window_meme_generator(nick, meme_name)
                break
    if not exist:
        window.close()
        window_main_menu(nick)
    window.close()
