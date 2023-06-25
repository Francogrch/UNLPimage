import os
import PySimpleGUI as sg
import json
import csv
import datetime
import string
from PIL import Image, ImageTk, ImageOps, ImageDraw, ImageFont


def window_collage_generator(nick, template):
    """Crea y muestra la ventana para seleccionar imagenes y generar un collage.

    Parámetros:
    - nick (str): nombre de usuario logueado.
    - template (str): nombre del template a utilizar.

    Esta función utiliza la siguientes funciones definidas en el módulo screens:
    - window_main_menu: función que crea y muestra la ventana del menu principal.
    - window_collage: función que crea y muestra la ventana para seleccionar una plantilla de collage.
    - window_error: funcion que genera una ventana emergente con un error dependiendo que haya sucedido.

    La funcion permite seleccionar una serie de imagenes que se utilizaran para generar un collage con el titulo que se le ingrese."""
    from screens.path import get_interface_folder, get_image_folder, get_collage_folder, get_theme, get_collage_json, get_tagger_csv, get_fonts_folder, get_main_folder
    from screens.main_menu import window_main_menu
    from screens.collage_template import window_collage
    from screens.error import window_error
    from screens.log import update_log

    def is_valid_filename(title):
        """Verifica si un titulo es valido segun S.O para utilizar.

        Parámetros:
        - title (str): titulo del collage.

        Retorna:
        - Boolean: Si es valido el titulo o no.

        La funcion comprueba si el titulo es valido respecto a letras, numeros, espacios o guiones."""
        # PATTERN = r'^[a-zA-Z0-9- -_--]+$'  # expresion regular
        PATTERN = string.ascii_letters + string.digits + " " + '_' + '-'
        for letter in title:
            if letter not in PATTERN:
                return False
                break
        return True

    def apply_mask(image, mask_path):
        """Aplica una mascara a una imagen.

        Parámetros:
        - image (Image): imagen a aplicar mascara.
        - mask_path (str): direccion donde se encuentra la mascara.

        Retorna:
        - image (Image): Imagen con mascara aplicada.

        La funcion abre y aplica una mascara a la imagen que se le pasa por parametro."""
        tmp_mask = Image.open(mask_path).convert('L')
        image.putalpha(tmp_mask)
        return image

    def update_title(image, text, mask_path):
        """Coloca un texto a la imagen.

        Parámetros:
            image (Image): imagen a colocar texto.
            text (str): texto a colocar.
            mask_path (Str): direccion de la mascara.

        Retorna:
            image (Image): Imagen con texto colocado.

        La funcion coloca un texto pasado como parametro, dependiendo de la cantidad de caracteres ingresados disminuye el tamaño de la fuente, generando un rectangulo con
        esquinas redondeadas del mismo tamaño que el texto para aplicarlo en la imagen."""
        if len(text) > 13:
            size = round(1700*(1/len(text)))
        else:
            size = 120
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(os.path.join(
            get_fonts_folder(), 'roboto.ttf'), size)
        w, h = font.getsize(text)
        left_top_x = (1080-w)//2
        left_top_y = 850
        if text != "":
            draw.rounded_rectangle(
                [((left_top_x-30), left_top_y-30), (left_top_x+30+w, left_top_y+30+h)], radius=30, fill='#1D1D1B')

        draw.text((left_top_x, left_top_y), text,
                  font=font, fill=(255, 255, 255, 255))

        image = apply_mask(image, mask_path)
        return image

    def update_image(dic_box, name_image, image):
        """Actualiza la imagen colocandola donde corresponda.

        Parámetros:
            dic_box (Dic): diccionario con las coordenadas donde colocar la imagen.
            name_image (Str): nombre de la imagen.
            image (Image): imagen a la que se le coloca las nuevas imagenes .
            title (Str): titulo.

        Retorna:
            image (Image): imagen con todo colocado.
        """
        path_image = os.path.join(IMG_PATH, name_image)
        tmp_image = Image.open(path_image)
        tmp_image = ImageOps.fit(tmp_image, ((dic_box['bottom_right_x'] - dic_box['top_left_x']), (
            dic_box['bottom_right_y'] - dic_box['top_left_y'])), centering=(0.5, 0.5))
        image.paste(
            tmp_image, (dic_box['top_left_x'], dic_box['top_left_y']))
        image = apply_mask(image, MASK_PATH)
        return image

    def save_collage(title, image, img1, img2, img3=None):
        """Guarda el collage en la direccion especificada en configuracion.

        Parámetros:
            title (Str): Titulo del collage.
            image (Image): Imagen que se muestra en pantalla.
            img1 (Str): Nombre de la primer imagen.
            img2 (Str): Nombre de la segunda imagen.
            img3 (Str, optional): Nombre de la tercer imagen. Defaults en None.
        """
        path_collage = get_collage_folder()
        if os.path.exists(path_collage):
            if os.path.exists(os.path.join(path_collage, f"{title}.png")):
                title = f"{title}-{str(now.timestamp())[-4:]}"
            if img3 != None:
                images = [img1, img2, img3]
            else:
                images = [img1, img2]
            update_log(nick, "new_collage", images, title)
            image.save(os.path.join(path_collage, f"{title}.png"))
        else:
            window_error(
                'La carpeta de los collages, no es valida. Cambie la configuracion')

    sg.change_look_and_feel(get_theme())
    IMG_SIZE = (340, 340)
    IMG_PATH = get_image_folder()
    MASK_PATH = os.path.join(get_interface_folder(),
                             'mask_collage.png')
    BGROUND_PATH = os.path.join(get_interface_folder(), 'img_original.png')
    SIZE_BUTTON = 10
    now = datetime.datetime.now()
    try:
        with open(get_collage_json()) as archive:
            template_json = json.loads(archive.read())
    except:
        template_json = {}
    try:
        with open(get_tagger_csv()) as archive:
            csv_tagger = csv.reader(archive)
            header, list_tagger = next(csv_tagger), list(csv_tagger)
    except:
        list_tagger = []
        header = []

    list_images = [n[0]
                   for n in list_tagger if n[5] != '[]']  # Sin etiqueta no van

    # Lista con imagenes tageadas que se encuentran solo en la carpeta seleccionada en configuracion
    list_images = list(filter(lambda x: os.path.exists(
        os.path.join(get_image_folder(), x)), list_images))

    # variables del json de los templates
    list_boxes = template_json[template]['images_boxes']
    cant_image = len(template_json[template]['images_boxes'])

    img_ori = Image.open(BGROUND_PATH)
    img_copy = Image.new(mode='RGBA', size=img_ori.size)
    img_window = ImageTk.PhotoImage(img_ori.resize(IMG_SIZE))

    # layout

    first_row = [sg.Button(key="-BACK-", border_width=0, button_color=(sg.theme_background_color(), sg.theme_background_color()), image_filename=os.path.join(
        get_interface_folder(), "back.png"), image_subsample=6, tooltip='Volver'), sg.Push(), sg.Text("| GENERAR COLLAGE |", font='Courier 15 bold')]
    column_left = [[sg.Combo(list_images, key=f"-IMAGE{i}-", size=30, readonly=True, enable_events=True)]
                   for i, combo in enumerate(range(cant_image))]
    column_left.insert(0, [sg.Text("Elegir imagenes")])
    column_left.append([sg.Text('Titulo: ', size=30)])
    column_left.append(
        [sg.Input(key='-TITLE-', size=30, disabled=True, enable_events=True)])
    column_right = [[
        sg.Image(key='-IMAGE_WINDOW-')], [sg.VPush()], [sg.Push(), sg.Button('GUARDAR', key='-SAVE-', size=SIZE_BUTTON, font='Italic 13 bold'), sg.Push()]]

    row1 = [[sg.VPush()], [sg.VPush(), sg.Column(column_left),
                           sg.Push(), sg.Column(column_right)], [sg.VPush()]]
    last_row = [[sg.VPush()], [sg.Push(), sg.Text(
        "UNLP Informatica-Seminario Python ©", font="Italic 7 bold"), sg.Push()]]

    layout = [[first_row, row1, last_row]]
    window = sg.Window("UNLP Image", layout, size=(700, 500), finalize=True)
    window["-IMAGE_WINDOW-"].update(data=img_window)
    while True:
        event, value = window.read()
        if event == '-BACK-':
            window.close()
            window_collage(nick)
            break
        if event == sg.WIN_CLOSED:
            break
        if event == '-SAVE-':
            if value["-TITLE-"] != "" and (is_valid_filename(value["-TITLE-"])):
                if cant_image == 2:
                    save_collage(value['-TITLE-'], img_copy,
                                 value['-IMAGE0-'], value['-IMAGE1-'])
                elif cant_image > 2:
                    save_collage(
                        value['-TITLE-'], img_copy, value['-IMAGE0-'], value['-IMAGE1-'], value['-IMAGE2-'])
                window.close()
                window_main_menu(nick)
                break
            else:
                window_error(
                    "Ingrese un titulo alfanmumerico antes de guardar el collage.")

        if event == '-IMAGE0-':
            img_ori = update_image(
                list_boxes[0], value['-IMAGE0-'], img_ori)
            img_copy = update_title(
                img_ori.copy(), value['-TITLE-'], MASK_PATH)
            window["-IMAGE_WINDOW-"].update(
                data=ImageTk.PhotoImage(img_copy.resize(IMG_SIZE)))
        if event == '-IMAGE1-':
            img_ori = update_image(
                list_boxes[1], value['-IMAGE1-'], img_ori)
            img_copy = update_title(
                img_ori.copy(), value['-TITLE-'], MASK_PATH)
            window["-IMAGE_WINDOW-"].update(
                data=ImageTk.PhotoImage(img_copy.resize(IMG_SIZE)))
        if event == '-IMAGE2-':
            img_ori = update_image(
                list_boxes[2], value['-IMAGE2-'], img_ori)
            img_copy = update_title(
                img_ori.copy(), value['-TITLE-'], MASK_PATH)
            window["-IMAGE_WINDOW-"].update(
                data=ImageTk.PhotoImage(img_copy.resize(IMG_SIZE)))
        if value['-IMAGE0-'] != "" and value['-IMAGE1-'] != "":
            if cant_image == 2:
                column_left[cant_image+2][0].update(disabled=False)
            elif cant_image > 2 and value['-IMAGE2-'] != "":
                column_left[cant_image+2][0].update(disabled=False)

        if event == '-TITLE-':
            img_copy = img_ori.copy()
            img_copy = update_title(
                img_copy, value['-TITLE-'], MASK_PATH)
            window["-IMAGE_WINDOW-"].update(
                data=ImageTk.PhotoImage(img_copy.resize(IMG_SIZE)))

    window.close()
