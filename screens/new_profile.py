import PySimpleGUI as sg
import json
import datetime
import os
from PIL import Image, ImageTk, ImageOps
from screens.path import get_profile_json, get_avatar_folder, get_interface_folder, get_theme


GENRES = ['Hombre', 'Mujer', 'Otre']
FILE_TYPES = [("", "*.svg .bmp .raw .jpeg .jpg .png"),]


def set_image(image, size):
    """Establece el tamanio de la imagen para mostrarla en la ventana correctamente.

    Parametros:
    - image (str): Direccion donde se encuentra la imagen a mostrar.
    - size (tuple): Tupla con el tama;o de la imagen a mostrar

    Retorna:
    - image_tk (PhotoImage): imagen compatible con tkinter y pysimplegui
    """
    image = Image.open(image)  # Abro la imagen que me viene como parametro
    # Le aplico un resize de 120x120 para mostrar esa imagen
    image = image.resize(size)
    # Convierto la imagen en un tipo PhotoImage para que pysimplegui pueda mostrarla sin problemas
    image_tk = ImageTk.PhotoImage(image)
    return image_tk


def save_image(image, o_path, set_img=True):
    """Establece el formato de una imagen para mostrarla en la ventana (circular y 300x300) guardandola en la carpeta images/avatar.

    Parametros:
    - image (Str): Direccion donde se encuentra la imagen original que se quiere colocar.
    - o_path (Str): Direccion donde se guardara la imagen modificada, incluye el nombre de la foto.png.

    Retorna:
    - set_image(o_path) (PhotoImage): Llamada a la funcion que me devuelve la imagen que necesito para mostrarla
    """
    img = Image.open(image)  # Abro la imagen que me viene como parametro
    # Creo la ruta donde se encuentra la mascara que utilizo
    mask_path = os.path.join(get_avatar_folder(), 'mask.png')
    # Abro la mascara y la transformo en una escala de grises para no tener inconvenientes al aplicar ".putalpha"
    mask = Image.open(mask_path).convert('L')
    # Escalo y recorto la imagen original para que tenga el mismo tama;o que la mascara (300x300), y la centro en 0.5,0.5
    output = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
    # Aplico a la foto una transparencia basada en la mascara, donde lo negro es transparente y lo blanco queda tal y como estaba
    output.putalpha(mask)
    output = output.convert('RGBA')
    output.save(o_path)
    if set_img:
        return set_image(o_path, (150, 150))


def window_new_profile():
    """Muestra en pantalla la ventana para creacion de perfiles 
    Esta función utiliza las siguientes funciones definidas en el módulo screens:
    - window_start: función que crea y muestra la ventana de inicio de sesión.
    - window_main_menu: función que crea y muestra la ventana del menu principal.

    Esta función utiliza la siguiente funcion para generar una ventana emergente:
    - window_error: funcion que crea y muestra una ventana emergente dependiendo del error que ocurre.

    Exepciones:
    - FileNotFound: Si el archivo JSON no existe, crea uno. 
    """
    from screens.main_menu import window_main_menu
    from screens.start import window_start
    from screens.error import window_error
    from screens.log import update_log

    data = {}

    def generate_profile_json(data):
        try:
            with open(get_profile_json(), 'x') as json_file:
                json.dump(data, json_file)
        except IOError:
            window_error(
                "Error al crear el archivo JSON de perfiles, intente dando los permisos correctos.")
            window.close()
            window_start()

    try:
        with open(get_profile_json(), 'r') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        generate_profile_json(data)
    except IOError:
        window_error(
            "Error al crear el archivo JSON de perfiles, intente dando los permisos correctos.")
        window.close()
        window_start()

    def set_user(data, nick, name, age, genre, o_path):
        """Guarda en el archivo JSON la informacion del usuario nuevo.

        Parametros:
        - nick (Str): Recibe el nick nuevo para guardarlo
        - name (Str): Recibe el nombre nuevo para guardarlo.
        - age (Str): Recibe la edad nueva para guardarlo.
        - genre (Str): Recibe el genero nuevo para guardarlo.
        - o_path (Str): Recibe la direccion donde se encuentra la imagen nueva guardada.

        Retorna:
        - Booleano: si puedo guardar el usuario True, sino False porque el usuario con el nick recibido ya existe               
        """
        if nick not in data:
            data[nick] = {"name": name,
                          "age": age,
                          "genre": genre,
                          "image": o_path}
            success = True
        else:
            success = False
        try:
            with open(get_profile_json(), 'w') as json_file:
                json.dump(data, json_file, indent=3)
        except FileNotFoundError:
            data = {}
            generate_profile_json(data)
        except IOError:
            window_error(
                "Error al crear el archivo JSON de perfiles, intente dando los permisos correctos.")
            window.close()
            window_start()
        return success

    sg.change_look_and_feel(get_theme())
    SZ_INPUT = 25
    FONT_TEXT = ('Italic 11 normal')
    FONT_BUTTON = ('Italic 11 bold')

    now = datetime.datetime.now()  # Obtengo hora actual
    # Genero un nombre para una foto con la hora actual para que sea unico
    img_name = "avatar_" + str(now.timestamp())[-8:] + ".png"
    # Path completo donde se encuentra la nueva foto
    output_path = os.path.join(get_avatar_folder(), img_name)
    # Path de imagen por defecto
    DEF_IMAGE = os.path.join(get_avatar_folder(), "button_perfil.png")

    topcolum1 = [[sg.Button(key="-BACK-", border_width=0, button_color=(sg.theme_background_color(), sg.theme_background_color()),
                            image_filename=os.path.join(get_interface_folder(), "back.png"), image_subsample=6, tooltip='Volver')]]
    topcolum2 = [
        [sg.Push(), sg.Text("| NUEVO PERFIL |", font='Courier 15 bold')]]

    colum1 = [[sg.Text("Nick", font=FONT_TEXT, pad=((0, 0), (0, 0)))], [sg.InputText(key="-NICK-", size=(SZ_INPUT), tooltip='Apodo', font=FONT_TEXT)],
              [sg.Text("Nombre", font=FONT_TEXT, pad=((0, 0), (10, 0)))], [sg.InputText(
                  key="-REAL_NAME-", size=(SZ_INPUT), tooltip='Nombre Completo', font=FONT_TEXT)],
              [sg.Text("Edad", font=FONT_TEXT, pad=((0, 0), (10, 0)))], [sg.InputText(
                  key="-AGE-", size=(SZ_INPUT), tooltip='Edad', font=FONT_TEXT)],
              [sg.Text("Genero", font=FONT_TEXT, pad=((0, 0), (10, 0)))], [sg.Combo(GENRES, key="-GENRE-", size=(SZ_INPUT-1), font=FONT_TEXT, readonly=True)]]

    colum2 = [[sg.Push(), sg.Image(key="-IMAGE-",), sg.Push()],
              [sg.Input(key="_FILEBROWSER_", enable_events=True, visible=False)],
              [sg.Push(), sg.FileBrowse('Seleccionar avatar', target='_FILEBROWSER_',
                                        font=FONT_BUTTON, file_types=FILE_TYPES), sg.Push()],
              [sg.Push(), sg.Button("Guardar", key="-SAVE-", font='Italic 13 bold'), sg.Push()]]

    raw1 = [[sg.Column(topcolum1, size=(378, 50)), sg.Column(
        topcolum2, element_justification="Center")]]  # Boton volver

    raw2 = [[sg.Push(), sg.Column(colum1, element_justification='l'),
             sg.Push(), sg.Column(colum2, element_justification='r'), sg.Push()]]

    last_raw = [sg.Push(), sg.Text(
        "UNLP Informatica-Seminario Python ©", font="Italic 7 bold"), sg.Push()]
    raw_space = [sg.Text('', font='Italic 20 normal')]

    layout = [[raw1],
              [raw_space],
              [raw2],
              [sg.VPush()],
              [last_raw]]

    window = sg.Window("UNLP Image", layout, size=(700, 500), finalize=True)
    # Updateo la foto de la ventana con la imagen default
    window['-IMAGE-'].update(data=save_image(DEF_IMAGE, output_path))
    success = False

    while True:
        event, values = window.read()
        if event == "-BACK-":  # VOLVER A SELECCION DE PERFIL
            if os.path.exists(output_path):
                os.remove(output_path)
            window.close()
            window_start()
            break
        if event == sg.WIN_CLOSED:
            if not success and os.path.exists(output_path):
                os.remove(output_path)
            break
        if event == "_FILEBROWSER_":  # CAMBIAR LA IMAGEN DE PERFIL POR UNA NUEVA
            # Updateo la foto con la imagen que busque y llamo a set imagen para darle formato y guardarla
            window['-IMAGE-'].update(data=save_image(
                values["_FILEBROWSER_"], output_path))
        if event == "-SAVE-":  # IR A MENU PRINCIPAL
            # VERIFICO QUE NINGUN INPUT ESTE VACIO
            if values["-NICK-"] == "" or values["-REAL_NAME-"] == "" or values["-AGE-"] == "" or values["-GENRE-"] == "":
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
                # ACTUALIZO EL JSON CON LOS DATOS
                if set_user(data, values["-NICK-"], values["-REAL_NAME-"], values["-AGE-"], values["-GENRE-"], os.path.basename(output_path)):
                    success = True
                    update_log(values["-NICK-"], "profile_created")
                    window.close()
                    window_main_menu(values["-NICK-"])
                else:  # SI EL NICK YA SE ENCUENTRA EN EL JSON TIRO ERROR
                    window_error(
                        "Ocurrio un error al ingresar su nick, este ya se encuentra en uso por favor ingrese uno nuevo.")

    window.close()
