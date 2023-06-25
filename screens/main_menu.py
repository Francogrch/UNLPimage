def window_main_menu(nick):
    """Crea y muestra la ventana principal del programa para el usuario logueado.

    Parámetros:
    - nick (str): nombre de usuario logueado.

    Retorna:
    - None

    Esta función utiliza las siguientes funciones definidas en el módulo screens:
    - window_collage: función que crea y muestra la ventana para generar collages.
    - window_start: función que crea y muestra la ventana de inicio de sesión.
    - window_meme_generator: función que crea y muestra la ventana para generar memes.
    - window_edit_profile: función que crea y muestra la ventana para editar el perfil del usuario.
    - window_config: función que crea y muestra la ventana de configuración.

    La función carga los datos del perfil del usuario desde un archivo JSON y el texto de ayuda desde un archivo de texto. Luego, muestra la ventana principal con opciones para generar memes, collages, editar perfil, ver la ayuda y cerrar sesión.
    """
    from screens.collage_template import window_collage
    from screens.start import window_start
    from screens.meme_template import window_meme_template
    from screens.edit_profile import window_edit_profile
    from screens.config import window_config
    from screens.tagger import window_tagger
    from screens.error import window_error
    import PySimpleGUI as sg
    import os
    import json
    import screens.path as path

    # Style window
    sg.change_look_and_feel(path.get_theme())
    sz_button = 40
    font_button = ('Italic 15 normal')
    font_help = ("Arial", 16)
    path.valid_image()
    # Directions
    dir_json = path.get_profile_json()
    dir_help = path.get_help_txt()
    dir_interface = path.get_interface_folder()
    dir_avatar = path.get_avatar_folder()

    try:
        with open(dir_help, encoding='utf-8') as file_help:
            HELP_TEXT = file_help.read()
    except FileNotFoundError:
        HELP_TEXT = 'NO SE ENCONTRO ARCHIVO HELP.TXT'
    try:
        with open(dir_json) as file_profile:
            dic_json = json.load(file_profile)
    except FileNotFoundError or IOError:
        window_error('No encontro archivo de perfiles!')
        return False
    dir_image = os.path.join(dir_avatar, dic_json[nick]['image'])
    # Layout
    colum1 = [[sg.Push(), sg.Button(key='-PERFIL-', button_color=(sg.theme_background_color(), sg.theme_background_color()), image_filename=dir_image, image_subsample=5, border_width=0), sg.Push()],
              [sg.Push(), sg.Text(f"| {nick.upper()[:20]} |", font=('Courier 10 normal')), sg.Push()]]
    colum2 = [[sg.Button(key='-CONFIG-', button_color=(sg.theme_background_color(), sg.theme_background_color()), image_filename=(os.path.join(dir_interface, "button_config.png")), image_subsample=5, border_width=0),
               sg.Button(key='-HELP-', button_color=(sg.theme_background_color(), sg.theme_background_color()), image_filename=(os.path.join(dir_interface, "button_help.png")), image_subsample=5, border_width=0)],
              [sg.Push(), sg.Text(), sg.Push()]]
    row1 = [sg.Column(colum1, element_justification='left'),
            sg.Push(background_color=None),
            sg.Column(colum2, element_justification='right')]
    row2 = [sg.Push(), sg.Text(
        'UNLPImage', font='Courier 50 italic bold'), sg.Push()]
    row3 = [[sg.Push(), sg.Button(button_text="Etiquetar imagenes", key="-TAGGER-", size=sz_button, font=font_button), sg.Push()],
            [sg.Push(), sg.Button(button_text="Generar meme",
                                  key="-GENERATOR_M-", size=sz_button, font=font_button), sg.Push()],
            [sg.Push(), sg.Button(button_text="Generar collage",
                                  key="-GENERATOR_C-", size=sz_button, font=font_button), sg.Push()],
            [sg.Push(),
             sg.Button(button_text="Salir sesion", key="-LOG_OUT-",
                       size=(round(sz_button/2) - 1), font=font_button),
             sg.Button(button_text="Salir", key="-EXIT-",
                       size=(round(sz_button/2) - 1), font=font_button),
             sg.Push()]]
    last_row = [sg.Push(), sg.Text(
        "UNLP Informatica-Seminario Python ©", font="Italic 7 bold"), sg.Push()]

    layout = [[row1],
              [row2],
              [sg.VPush()],
              [row3],
              [sg.VPush()],
              [last_row]]

    window = sg.Window("UNLP Image", layout, size=(700, 500), finalize=True)
    # Main loop
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "-EXIT-":
            break
        if event == '-HELP-':
            sg.popup_scrolled(HELP_TEXT, title=" Ayuda ",
                              font=font_help, size=(50, 10))
        if event == '-TAGGER-':
            window.close()
            window_tagger(nick)
        if event == '-GENERATOR_M-':
            window.close()
            window_meme_template(nick)
        if event == '-GENERATOR_C-':
            window.close()
            window_collage(nick)
        if event == '-LOG_OUT-':
            window.close()
            window_start()
            break
        if event == '-PERFIL-':
            window.close()
            window_edit_profile(nick)
        if event == '-CONFIG-':
            window.close()
            window_config(nick)

    window.close()
