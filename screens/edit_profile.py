def window_edit_profile(nick):
    """Crea y muestra la ventana para editar un perfil logeado.

    Parámetros:
    - nick (str): nombre de usuario logueado.

    Esta función utiliza la siguiente funcion definida en el módulo screens:
    - window_main_menu: función que crea y muestra la ventana del menu principal.

    Esta función utiliza la siguiente funcion definida en el modulo de new_profile:
    - window_error: funcion que crea y muestra una ventana emergente dependiendo del error que ocurre.

    La funcion muestra los datos del usuario logeado, permitiendo editarlos (salvo por el Nick), para luego actualizar sus datos y guardarlos nuevamente.
    """
    import os
    import PySimpleGUI as sg
    from screens.main_menu import window_main_menu
    import json
    from screens.path import get_profile_json, get_interface_folder, get_avatar_folder, get_theme, valid_image
    from screens.new_profile import save_image, set_image, GENRES, FILE_TYPES
    from screens.error import window_error
    from screens.log import update_log

    def update_profile(data, name, age, genre):
        """Actualiza la informacion del perfil, y lo guarda en el JSON.

           Parámetros:
           - data (list(dict())): json con informacion del perfil.
           - nick (str): nombre del usuario.
           - age (str): edad del usuario.
           - genre (str): genero del usuario.

           La funcion recibe los datos del perfil que va actualizar, abre el archivo JSON y pisa la informacion que habia con la nueva. 
        """
        data[nick]["name"] = name
        data[nick]["age"] = age
        data[nick]["genre"] = genre
        try:
            with open(get_profile_json(), 'w') as json_file:
                json.dump(data, json_file, indent=3)
        except FileNotFoundError:
            window_error(
                "Error al acceder al archivo JSON de perfiles, POR QUE LO ELIMINASTE??!?!?!?!?.")
            window.close()
            window_main_menu(nick)
        except IOError:
            window_error(
                "Error al acceder al archivo archivo JSON de perfiles, intente dando los permisos correctos.")
            window.close()
            window_main_menu(nick)

    sg.change_look_and_feel(get_theme())
    SZ_INPUT = 25
    FONT_TEXT = ('Italic 11 normal')
    FONT_BUTTON = ('Italic 11 bold')
    valid_image()
    # Guardo la informacion del JSON en data para actualizarlo
    try:
        with open(get_profile_json(), 'r') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        window_error(
            "Error al acceder al archivo JSON de perfiles, POR QUE LO ELIMINASTE??!?!?!?!?.")
        window.close()
        window_main_menu(nick)
    except IOError:
        window_error(
            "Error al crear el archivo JSON de perfiles, intente dando los permisos correctos.")
        window.close()
        window_main_menu(nick)
    # Guardo los datos del perfil ingresado
    def_image = data[nick]["image"]
    name = data[nick]["name"]
    age = data[nick]["age"]
    genre = data[nick]["genre"]

    topcolum1 = [[sg.Button(key="-BACK-", border_width=0, button_color=(sg.theme_background_color(), sg.theme_background_color()),
                            image_filename=os.path.join(get_interface_folder(), "back.png"), image_subsample=6, tooltip='Volver')]]
    topcolum2 = [
        [sg.Push(), sg.Text("| EDITAR PERFIL |", font='Courier 15 bold')]]

    colum1 = [[sg.Text("Nick", font=FONT_TEXT, pad=((0, 0), (0, 0)))], [sg.InputText(key="-NICK-", size=(SZ_INPUT), tooltip='Apodo', font=FONT_TEXT, disabled=True, default_text=nick)],
              [sg.Text("Nombre", font=FONT_TEXT, pad=((0, 0), (10, 0)))], [sg.InputText(
                  key="-REAL_NAME-", size=(SZ_INPUT), tooltip='Nombre Completo', font=FONT_TEXT, default_text=name)],
              [sg.Text("Edad", font=FONT_TEXT, pad=((0, 0), (10, 0)))], [sg.InputText(
                  key="-AGE-", size=(SZ_INPUT), tooltip='Edad', font=FONT_TEXT, default_text=age)],
              [sg.Text("Genero", font=FONT_TEXT, pad=((0, 0), (10, 0)))], [sg.Combo(GENRES, key="-GENRE-", size=(SZ_INPUT - 1), font=FONT_TEXT, default_value=genre, readonly=True)]]

    colum2 = [[sg.Push(), sg.Image(key="-IMAGE-"), sg.Push()],
              [sg.Input(key="_FILEBROWSER_", enable_events=True, visible=False)],
              [sg.Push(), sg.FileBrowse('Seleccionar avatar', font=FONT_BUTTON,
                                        target='_FILEBROWSER_', file_types=FILE_TYPES), sg.Push()],
              [sg.Push(), sg.Button("Guardar", key="-SAVE-", font=FONT_BUTTON), sg.Push(),]]

    row1 = [[sg.Column(topcolum1, size=(378, 50)), sg.Column(
        topcolum2, element_justification="Center")]]

    row2 = [[sg.Push(), sg.Column(colum1, element_justification='l'),
             sg.Push(), sg.Column(colum2, element_justification='r'), sg.Push()],]

    last_row = [sg.Push(), sg.Text(
        "UNLP Informatica-Seminario Python ©", font="Italic 7 bold"), sg.Push()]
    row_space = [sg.Text('', font='Italic 20 normal')]
    layout = [[row1],
              [row_space],
              [row2],
              [sg.VPush()],
              [last_row]]

    window = sg.Window("UNLP Image", layout, size=(700, 500), finalize=True)
    # UPDATEO LA FOTO CON LA IMAGEN DEFAULT
    dir_avatar = get_avatar_folder()

    window['-IMAGE-'].update(data=set_image(os.path.join(dir_avatar,
                             def_image), (150, 150)))

    while True:
        event, values = window.read()
        if event == "-BACK-":  # VOLVER MAIN MENU SIN EDITAR NADA
            window.close()
            window_main_menu(nick)
            break
        if event == sg.WIN_CLOSED:
            break
        if event == '_FILEBROWSER_':  # CAMBIAR LA IMAGEN DE PERFIL POR UNA NUEVA
            # Updateo la imagen de perfil con la imagen que busque, dandole nuevo formato y guardandola con el mismo nombre que tenia
            window['-IMAGE-'].update(data=save_image(
                values['_FILEBROWSER_'], os.path.join(dir_avatar, data[nick]["image"])))
        if event == "-SAVE-":  # IR AL MENU PRINCIPAL
            # VERIFICO QUE NINGUN INPUT ESTE VACIO
            if values["-REAL_NAME-"] == "" or values["-AGE-"] == "" or values["-GENRE-"] == "":
                window_error(
                    "Ocurrio un error al ingresar sus datos, por favor verifique que haya completado todos los campos.")
            elif not values["-AGE-"].isdigit():  # VERIFICO QUE LA EDAD NO TENGA NUMEROS
                window_error(
                    "Ocurrio un error al ingresar su edad, por favor intente colocando solo numeros.")
            elif int(values["-AGE-"]) > 123:  # VERIFICO QUE LA EDAD SEA MENOR A 123 A;OS
                window_error(
                    "Ocurrio un error al ingresar su edad, por favor ingrese una edad real.")
            # VERIFICO QUE EL NOMBRE TENGA SOLO LETRAS
            elif not values["-REAL_NAME-"].isalpha():
                window_error(
                    "Ocurrio un error al ingresar su nombre, por favor ingrese solo letras.")
            else:
                # ACTUALIZO EL JSON CON LOS DATOS NUEVOS
                update_profile(data, values["-REAL_NAME-"],
                               values["-AGE-"], values["-GENRE-"])
                update_log(nick, "profile_modified")
                window.close()
                window_main_menu(nick)  # VOY AL MAIN MENU
    window.close()
