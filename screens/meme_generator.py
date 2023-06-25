from PIL import Image, ImageTk, ImageDraw, ImageFont, ImageOps
from screens.path import get_interface_folder, get_meme_template_json, get_memes_folder, get_theme, get_fonts_folder, get_main_folder
from screens.meme_template import window_meme_template
from screens.main_menu import window_main_menu
from screens.error import window_error
from screens.tagger import resize
from screens.log import update_log
import PySimpleGUI as sg
import textwrap
import os
import json
import datetime


def window_meme_generator(nick, meme):
    """Muestra la pantalla una imagen que luego se le va a agregar una frase

    Esta funcion utiliza las siguientes funciones en screens:
    - window_main_menu(): funcion que crea y abre la ventana del menu principal.
    """
    sg.change_look_and_feel(get_theme())
    SZ_INPUT = 25
    FONT_TEXT = ('Italic 10 normal')
    select_image = ()
    font = ["bold", "bitcheese", "impact", "roboto", "coolvetica"]

    def box_size(x1, y1, x2, y2):
        """Saca el ancho y alto del espacio a escribir

        Parametros:
        - x1 (int) : Coordenadas de top_left_x
        - y1 (int) : Coordenadas de top_left_y
        - x2 (int) : Coordenadas de bottom_right_x
        - y2 (int) : Coordenadas de bottom_right_y

        Retorna:
        - (x2 - x1, y2 - y1) (int) : Una tupla con el alto y ancho
        """
        return (x2 - x1, y2 - y1)

    def enters(container, content):
        """Te dice si el alto y ancho del texto a escribir es menor al espacio que tiene disponible en el meme.json

        Parametros:
        - container :  Alto y ancho del espacio disponible en la Imagen
        - content : Alto y ancho de lo que ocupa el texto en la Imagen

        Retorna:
        - (contenido[0] <= contenedor[0] and contenido[1] <= contenedor[1]) (boolean) : verdadero si el texto entra
         en la imagen y falso sino
        """
        return content[0] <= container[0] and content[1] <= container[1]

    def calculate_font_size(draw, text, path_font, coordinates):
        """Calcula el tamaño de la fuente que se va a utilizar en la imagen

        Parametro:
        - draw (ImageDraw) : Modulo para agregar texto a las imagenes
        - text (String) : Texto a colocar
        - path_fuente (String) : Direccion de la fuente
        - coordinates (int) : Coordenadas del meme.json

        Retorna:
        - font (String) : La fuente con su tamaño para el texto
        """
        container_size = box_size(coordinates[num]["top_left_x"], coordinates[num]["top_left_y"], coordinates[num]["bottom_right_x"],
                                  coordinates[num]["bottom_right_y"])
        for size in range(100, 5, -5):
            font = ImageFont.truetype(path_font, size)
            wrapped_text = textwrap.wrap(text, width=10)
            wrapped_text = "\n".join(wrapped_text)
            box_text = draw.textbbox(
                (coordinates[num]["top_left_x"], coordinates[num]["top_left_y"]), wrapped_text, font=font)
            box_text_size = box_size(
                box_text[0], box_text[1], box_text[2], box_text[3])
            if enters(container_size, box_text_size):
                return font, wrapped_text

        return font

    def add(coordinates, def_image, texts, font):
        """Agrega al meme los textos escritos en los input

        Parametro:
        - coordinates(dict): Coordenadas de cada texto
        - def_image(str): Direccion de la imagen que va a editarse en pantalla 
        - texts(str): Textos que se escribieron en los inputs
        - path_font (String) : Nombre de la fuente

        Retorna:
        - image(Image) : Imagen editada con el texto
        """
        try:
            image = Image.open(def_image)
            draw = ImageDraw.Draw(image)
            path_fon = os.path.join(get_fonts_folder(), font)
            try:
                for num in range(len(coordinates)):
                    fontF, wrapped_text = calculate_font_size(
                        draw, texts[num], path_fon, coordinates)
                    draw.multiline_text((coordinates[num]["top_left_x"], coordinates[num]["top_left_y"], coordinates[num]["bottom_right_x"],
                                         coordinates[num]["bottom_right_y"]), wrapped_text, font=fontF, fill=(0, 0, 0))
                output = ImageOps.pad(image, (300, 300), color=(
                    sg.theme_background_color()))
                image_tk = ImageTk.PhotoImage(output)
                window["-IMAGE-"].update(data=image_tk)
            except:
                raise TypeError
            return image
        except FileNotFoundError:
            window_error(
                "No se encuentra la imagen que quiere abrir")

    def sucessfully():
        """Te avisa que la imagen fue guardada correctamente
        """
        layout2 = [[sg.Text("La imagen se a guardado correctamente", font=FONT_TEXT)],
                   [sg.Push(), sg.Button("ACEPTAR", key="-ACEPT-"), sg.Push()]]
        window = sg.Window('Guardado exitoso', layout2, finalize=True,)
        exit_var = False
        while not exit_var:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == "-ACEPT-":
                exit_var = True
                window.close()

    try:
        with open(get_meme_template_json(), "r") as file:
            data = json.load(file)
            coordinates = data[meme]["text_boxes"]
    except FileNotFoundError:
        window_error("El Archivo no se encuentra")
        window.close()
        window_main_menu()

    col1 = []
    for num in range(len(coordinates)):
        col1.append([sg.Text("Texto " + str(num+1) + ":")])
        col1.append([sg.Input(key="-TEXT" + str(num+1) + "-", font=None)])
    col1.append([sg.Text("Selecionar fuente")])
    col1.append([sg.Combo(font, default_value="bold", key="-SOURCE-", size=(SZ_INPUT-1),
                          font=FONT_TEXT, readonly=True)])
    col1.append([sg.Button("Agregar", key="-ADD-")])

    save = [sg.Push(), sg.Button("Guardar", key="-SAVE-"), sg.Push()]

    col2 = [[sg.Image(filename=select_image, key="-IMAGE-")], save
            ]

    last_raw = [sg.Push(), sg.Text(
        "UNLP Informatica-Seminario Python ©", font="Italic 7 bold"), sg.Push()]

    topcolum1 = [[sg.Button(key="-BACK-", border_width=0, button_color=(sg.theme_background_color(), sg.theme_background_color()),
                            image_filename=os.path.join(get_interface_folder(), "back.png"), image_subsample=6, tooltip='Volver')]]
    topcolum2 = [
        [sg.Push(), sg.Text("| MEME GENERATOR |", font='Courier 15 bold')]]
    raw1 = [[sg.Column(topcolum1, size=(378, 50)), sg.Column(
        topcolum2)]]

    layout = [[raw1],
              [sg.Column(col1), sg.Push(), sg.Column(col2), sg.Push()],
              [sg.VPush()],
              [last_raw]
              ]

    def_image = os.path.join(get_interface_folder(),
                             "memes", data[meme]["image"])

    window = sg.Window("UNLP Image", layout, size=(700, 500), finalize=True)
    window["-IMAGE-"].update(data=resize(
        os.path.join(def_image), (300, 300)))
    ok = False
    while True:
        event, value = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == "-BACK-":
            window.close()
            window_meme_template(nick)
            break
        if event == "-ADD-":
            try:
                texts = list([value["-TEXT" + str(elem+1) + "-"]
                              for elem in range(len(coordinates))])
                if value["-SOURCE-"] == "coolvetica":
                    font = value["-SOURCE-"] + ".otf"
                else:
                    font = value["-SOURCE-"] + ".ttf"
                image = add(coordinates, def_image, texts, font)
                ok = True
            except TypeError:
                window_error("El texto es demaciado grande")
        if event == "-SAVE-" and ok == False:
            window_error(
                "No es posible guardar la imagen, ya que no se a modificado")
        if event == "-SAVE-" and ok:
            path_meme = get_memes_folder()
            if os.path.exists(path_meme):
                now = datetime.datetime.now()
                image_path = os.path.join(
                    path_meme, nick + "_" + str(now.timestamp())[-4:] + ".png")
                image.save(image_path)  # eliminar foto en screens si se usa
                update_log(nick, "new_meme", data[meme]["image"], texts)
                sucessfully()
                window.close()
                window_meme_template(nick)
                break
            else:
                window_error(
                    'La carpeta de los memes, no es valida. Cambie la configuracion')
                window.close()
                window_main_menu(nick)
                break
    window.close()
