import PySimpleGUI as sg
import os
import csv
import mimetypes
import datetime
from PIL import Image, ImageTk, ImageOps
from screens.main_menu import window_main_menu
from screens.path import get_image_folder, get_tagger_csv, get_interface_folder, get_theme
from screens.log import update_log
from screens.error import window_error


def create_tagger_csv():
    """Crea un archivo csv donde se guarda la configuracion en caso de no existir, 
    el archivo posee una primera linea donde se indica el formato a guardar.

    Esta funcion utiliza la siguiente funcion definida en screens/path:
    - get_tagger_csv(): funcion que devuelve la direccion donde se guarda el archivo csv.
    """
    if not os.path.exists(get_tagger_csv()):
        with open(get_tagger_csv(), "x", newline='') as csv_file:
            file = csv.writer(csv_file)
            head_row = ["Relative path", "Description", "Resolution",
                        "Size", "Type", "Tags", "Profile", "Last_update"]
            file.writerow(head_row)


def resize(img, size=(250, 250)):
    """Recibe la direccion de una imagen y devuelve una copia adaptada para mostrar

    Parametros:
    - img(str): direccion de la imagen a abrir
    - size(tuple): tamaño de la imagen requerido, por defecto (250,250)

    Retorna:
    - output(PIL.Image.Image): 
    """
    try:
        img = Image.open(img)
        output = ImageOps.pad(img, size, color=(
            sg.theme_background_color()))
        return ImageTk.PhotoImage(output)
    except FileNotFoundError:
        window_error(
            "No se encuentra la imagen que esta intentando abrir, Puede ser que la hayas borrado o cambiado de lugar?")


def window_tagger(nick):
    """Permite selecionar, visualizar y editar los tags y descripciones de imagenes.

    Esta funcion utiliza las siguientes funciones definidas en screens:
    - get_image_folder(): funcion que devuelve la direccion donde se guardan las imagenes.
    - window_main_menu(): funcion que crea y abre la ventana del menu principal.

    Excepciones:
    - UnboundLocalError: si no se selecciona una imagen antes de agregar un tag/descripcion o intentan guardar.
    - IndexError: si el directorio donde se buscan las imagenes no posee ninguna imagen seleccionable.
    """

    def search_metadata(img_dir):
        """Recibe la direcion de una imagen y devuelve una lista con los metadatos de la imagen.

        Esta funcion utiliza: 
        - create_new_row(): genera los metadatos de una imagen y los devuelve en una lista.
        - create_tagger_csv(): funcion que crea un csv en caso de no existir

        Parametros:
        - img_dir(str): direccion de la imagen que quiero buscar.

        Retorna:
        - metadata(list): lista con los metadatos de la imagen recibida.
        """
        try:
            with open(get_tagger_csv()) as csv_file:  # carga el csv en data
                reader = csv.reader(csv_file)
                data = [row for row in reader]
        except FileNotFoundError:
            create_tagger_csv()
        found = False
        pos = -1
        for elem in data:  # Busco en data si la imagen existe
            pos += 1
            if elem[0] == img_dir:
                found = True
                break
        if (found):  # Si la encontre devuelve la lista guardada
            metadata = data[pos]
            # corrigue errores al pasar de lista a str debido al formato csv
            delete_car = "[' ]"
            translate_table = str.maketrans("", "", delete_car)
            metadata[5] = metadata[5].translate(translate_table)
            metadata[5] = [elem.strip() for elem in metadata[5].split(",")]
        else:
            # Sino devuelve una lista con todos los metadatos
            metadata = create_newrow(os.path.join(get_image_folder(), img_dir))
        return metadata

    def update_rigth_side(name):
        """Recibe el nombre de la imagen seleccionada en ["-FILE_LIST-"] y muestra sus datos en el lado derecho de la ventana.

        Esta funcion utiliza:
        - resize(): devuelve la imagen que se muestra.
        - search_metadata(): devuelve la metadata que se muestra.

        Retorna:
        - metadata(list): lista con la metadata de la imagen recibida.
        """
        window["-IMAGE-"].update(data=resize(os.path.join(get_image_folder(), name))
                                 )  # Ajusta el tamaño de la imagen a mostrar
        metadata = search_metadata(name)
        # Busca y devuelve la metadata relacionada a la imagen en el csv
        if type(metadata[2]) is str:
            # corrige errores al pasar de tuplas a str debido al formato csv
            size = metadata[2].replace('(', '').replace(')', '').split(',')
            img_data = f"| {metadata[4]} | {metadata[3]} Bytes | {size[0]}x{size[1]} |"
        else:
            img_data = f"| {metadata[4]} | {metadata[3]} Bytes | {metadata[2][0]}x{metadata[2][1]} |"
        # guarda tipo,tamaño,dimencion
        window["-METADATA-"].update(img_data)
        window["-SHOW_DESCRIPTION-"].update(metadata[1])
        window["-IMG_NAME-"].update(name)
        # Carga los datos para visualizarlos
        return metadata

    def create_newrow(name):
        """Recibe la direccion de una imagen y devuelve una nueva lista con formato: ["Relative path","Description","Resolution","Size","Type","Tags","Profile","Last_update"].

        Esta funcion utiliza la siguiente funcion definidas en screens:
        - window_error(): funcion que genera una ventana de error

        Parametros:
        - dir(str): direccion de la imagen a la que generar la metadata.

        Retorna:
        - row(list): metadata de la imagen recibida.
        """
        try:
            img = Image.open(name)
            description = ""
            width, heigth = img.size
            resolution = (width, heigth)  # Guarda la resolucion de la imagen
            size = os.path.getsize(name)  # Guarda el tamaño en bytes
            mt = mimetypes.guess_type(name)  # Guarda el tipo de imagen (png)
            tags = []
            now = datetime.datetime.now()
            # Guarda el momento actual en que se modifico
            last_update = int(now.timestamp())
            row = [os.path.basename(name), description, resolution,
                   size, mt[0], tags, nick, last_update]
            return row
        except FileNotFoundError:
            window_error("No se encuentra la imagen que esta buscando")

    def update_csv(row):
        """"Recibe una lista con metadatos de una imagen, la busca en un csv y agrega o actualiza sus datos

        Esta funcion utiliza las siguientes funciones definidas en screens:
        - get_tagger_csv(): funcion que retorna la direccion donde se guarda el archivo csv.
        - update_log(): funcion que agrega eventos al log.csv
        - create_tagger_csv(): funcion que crea un csv en caso de no existir
        - window_error(): funcion que genera una ventana de error

        Parametros:
        - row(list): lista con metadatos.

        Esta funcion no retorna sino que actualiza un archivo csv.
        """
        found = False
        pos = -1
        data = []
        try:
            with open(get_tagger_csv()) as csv_file:  # copio los datos del csv en data
                reader = csv.reader(csv_file)
                data = [row for row in reader]
        except FileNotFoundError:
            create_tagger_csv()
        for elem in data:  # busco en data si la imagen existe
            pos += 1
            if elem[0] == row[0]:  # pregunto por la direccion de la imagen guardada en row[0]
                found = True
                break
        if (found):  # si la encontre la actualizo con los datos recibidos
            # si la imagen esta guardada y row[tags] es diferentes a los tags en data
            if str(row[5]) != data[pos][5]:
                update_log(nick, "change_tags", row[0], row[5])
            # si la imagen esta guardada y row[description] es diferentes a la description en data
            if row[1] != data[pos][1]:
                update_log(nick, "change_description", row[0], row[1])
            row[5] = list(filter(lambda x: x != "", row[5]))
            row[6] = nick
            now = datetime.datetime.now()
            row[7] = int(now.timestamp())
            data[pos] = row
        else:  # si no existe agrego la lista que recibi
            if row[5] != "":  # si no esta guardada y row[tags] no esta vacio
                update_log(nick, "new_image_classified", row[0])
                if row[5] != []:
                    update_log(nick, "change_tags", row[0], row[5])
            data.append(row)
        # copio los datos modificados de vuelta al csv
        try:
            with open(get_tagger_csv(), "w", newline='') as csv_file:
                writer = csv.writer(csv_file, lineterminator='\n')
                writer.writerows(data)
        except FileNotFoundError:
            window_error(
                "El archivo que intenta acceder fue movido o eliminado")

    def update_tags_buttons(tag_list, ini, tag_table):
        """Recibe una lista de tags, un indice y una tabla con botones, habilita/deshabilita los botones (hasta un maximo de 3) segun la cantidad de tags
        que contenga la lista.

        Parametros:
        - tag_list(list): lista con tags(str).
        - ini(int): puntero para manejar tag_table.
        - tag_table(list): lista con botones donde se muestran los tags.

        Retorna:
        - tag_list(list): valor actualizado del puntero 
        """
        tag_list = list(filter(lambda x: x != "", tag_list)
                        )  # filtra cualquier elemento vacio que pueda generarse
        COLOR_BUTTON = '#d98880'
        # si hay al menos 1 tag en la lista habilita el boton 1
        if len(tag_list) >= 1 and ini < len(tag_list):
            tag_table[0].update(
                tag_list[ini][:8], disabled=False, button_color=COLOR_BUTTON)
        else:  # sino lo desabilitada
            tag_table[0].update("", disabled=True, button_color=(
                (sg.theme_background_color()), (sg.theme_background_color())))
        # si hay al menos 2 tag en la lista habilita el boton 2
        if len(tag_list) >= 2 and ini+1 < len(tag_list):
            tag_table[2].update(
                tag_list[ini+1][:8], disabled=False, button_color=COLOR_BUTTON)
        else:  # sino lo desabilitada
            tag_table[2].update("", disabled=True, button_color=(
                (sg.theme_background_color()), (sg.theme_background_color())))
        # si hay al menos 3 tag en la lista habilita el boton 3
        if len(tag_list) >= 3 and ini+2 < len(tag_list):
            tag_table[4].update(
                tag_list[ini+2][:8], disabled=False, button_color=COLOR_BUTTON)
        else:  # sino lo desabilitada
            tag_table[4].update("", disabled=True, button_color=(
                (sg.theme_background_color()), (sg.theme_background_color())))
        return tag_list

    def window_delete():
        """Crea una nueva ventana con los botones cancelar/eliminar y retorna un booleano segun que boton se seleccione 

        Retorna:
        - True/False(boolean): devuelve "True" se se eliguio el boton "eliminar" o "False" para "cancelar"
        """
        DELETE = " Quiere eliminar el tag seleccionado? "
        layout_delete = [[sg.Push(), sg.Text(DELETE, font=6), sg.Push()],
                         [[sg.Push(), sg.Button(" Cancelar ", key=("-CANCEL-")), sg.Button(" Eliminar ", key=("-DELETE-")), sg.Push()]]]
        win_delete = sg.Window("UNLP Image", layout_delete, size=(340, 80))
        exit_var = False
        while not (exit_var):
            event, values = win_delete.read()
            if event == sg.WIN_CLOSED:
                exit_var = True
                win_delete.close()
            if event == "-CANCEL-":
                exit_var = True
                win_delete.close()
                return False
            if event == "-DELETE-":
                exit_var = True
                win_delete.close()
                return True

    sg.change_look_and_feel(get_theme())
    FONT_GENERAL = 'Italic 15 normal'
    FONT_TEXT = 'Italic 11 normal'
    FONT_BUTTON = 'Italic 12 normal'
    FONT_TAG = ('Italic 12 bold')
    TOOLTIP_ADD_TAG = " Agregar tags a la imagen seleccionada "
    TOOLTIP_ADD_DESCRIPTION = " Agregar una descripcion de la imagen seleccionada "
    TOOLTIP_BACK = " Volver al menu principal "
    TOOLTIP_SAVE = " Guardar los cambios las descripciones/tags "
    TOOLTIP_DELETE = " Eliminar tag "

    file_list = list(filter(lambda file: file.endswith(
        (".png", ".jpg", ".jpeg", ".svg", ".bmp", ".row")), os.listdir(get_image_folder())))

    tag_table = [sg.Button("", disabled=True, border_width=0, font=FONT_TAG, button_color=((sg.theme_background_color()), (sg.theme_background_color())), key="-TAG1-", tooltip=TOOLTIP_DELETE),
                 sg.Push(),
                 sg.Button("", disabled=True, border_width=0, font=FONT_TAG, button_color=((sg.theme_background_color(
                 )), (sg.theme_background_color())), key="-TAG2-", tooltip=TOOLTIP_DELETE),
                 sg.Push(),
                 sg.Button("", disabled=True, border_width=0, font=FONT_TAG, button_color=((sg.theme_background_color(
                 )), (sg.theme_background_color())), key="-TAG3-", tooltip=TOOLTIP_DELETE),
                 ]

    last_row = [sg.Push(), sg.Text(
        "UNLP Informatica-Seminario Python ©", font="Italic 7 bold"), sg.Push()]

    buttons_left = [sg.Push(), sg.Button('Volver', key="-BACK-", tooltip=TOOLTIP_BACK, font=FONT_GENERAL),
                    sg.Button('Guardar', key="-SAVE-", tooltip=TOOLTIP_SAVE, font=FONT_GENERAL), sg.Push()]

    buttons_right = [sg.Button('', key="-BACKWARD-", border_width=0, button_color=(sg.theme_background_color(), sg.theme_background_color()), image_filename=os.path.join(get_interface_folder(), "arrow_left.png"), image_subsample=10), sg.Push(),
                     sg.Button('', key="-FORWARD-", border_width=0, button_color=(sg.theme_background_color(), sg.theme_background_color()), image_filename=os.path.join(get_interface_folder(), "arrow_right.png"), image_subsample=10)]

    colum_left = [[sg.Text('| ETIQUETAR IMAGENES |', font='Courier 15 bold')],
                  [sg.Listbox(values=file_list, enable_events=True,
                              key="-FILE_LIST-", size=(40, 12))],
                  [sg.Text('Tags', font=FONT_TEXT)],
                  [sg.InputText(size=20, key="-INPUT_TAGS-", font=FONT_GENERAL, do_not_clear=False, tooltip="*PROCURA AGREGAR ANTES DE REALIZAR OTRA ACCION*"),
                   sg.Button('Agregar', key="-ADD_TAGS-", font=FONT_BUTTON, tooltip=TOOLTIP_ADD_TAG)],
                  [sg.Text('Descripcion', font=FONT_TEXT)],
                  [sg.InputText(size=20, key="-INPUT_DESCRIPTION-", font=FONT_GENERAL, do_not_clear=False, tooltip="*PROCURA AGREGAR ANTES DE REALIZAR OTRA ACCION*"),
                   sg.Button('Agregar', tooltip=TOOLTIP_ADD_DESCRIPTION, key="-ADD_DESCRIPTION-", font=FONT_BUTTON)],
                  buttons_left]
    colum_right = [
        [sg.Push(), sg.Image(
            key='-IMAGE-', size=(250, 250),), sg.Push()],
        [sg.Push(), sg.Text("", key="-IMG_NAME-", font=FONT_GENERAL), sg.Push()],
        [sg.Push(), sg.Text("", key="-METADATA-",
                            font='Courier-Bold 11 normal'), sg.Push()],
        tag_table, buttons_right,
        [sg.Text('Descripcion: ', font=FONT_GENERAL)],
        [sg.Push(), sg.Text("", font='Italic 12 italic',
                            key="-SHOW_DESCRIPTION-", auto_size_text=False), sg.Push()]
    ]
    row1 = [sg.Column(colum_left), sg.Push(),
            sg.Column(colum_right), sg.VPush()]
    row2 = [last_row]

    layout = [row1, [sg.VPush()], row2]

    window = sg.Window("UNLP Image", layout,
                       size=(700, 500), finalize=True)
    window["-INPUT_TAGS-"].bind("<Return>", "_Enter")
    window["-INPUT_DESCRIPTION-"].bind("<Return>", "_Enter")

    tag_ini = 0
    row = []
    while True:
        # "Volver" cierra la ventana y abre el menu principal manteniendo el usuario
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break

        elif event == '-BACK-':
            window.close()
            window_main_menu(nick)
            break

        # boton "agregar" guarda los tags en la lista local de metadatos
        elif event == "-INPUT_TAGS-" + "_Enter" or event == "-ADD_TAGS-":
            try:
                if row != []:  # row[5] es la posicion donde se guardan los tags
                    row[5] = list(row[5])
                    if len(values["-INPUT_TAGS-"]) != 0:
                        row[5].append(values["-INPUT_TAGS-"])
                        change = True
                    else:
                        window_error(
                            " Ingrese un tag antes de intentar agregarlo ")
                    # se envia la lista con tags y se actualizan los botones segun la cantidad de elementos
                    row[5] = update_tags_buttons(row[5], tag_ini, tag_table)
                else:
                    window_error(" Seleccione una imagen para modificar ")
            except UnboundLocalError:
                # error al intentar agregar un tag sin seleccionar imagen
                window_error(
                    " Por favor seleccione una imagen a la cual modificar ")

        # Boton "agregar" guarda la descripcion en la lista local de metadatos
        elif event == "-INPUT_DESCRIPTION-" + '_Enter' or event == "-ADD_DESCRIPTION-":
            try:
                if row != []:
                    if (len(values["-INPUT_DESCRIPTION-"])) != 0:
                        # copia los valores del input en la lista
                        row[1] = values["-INPUT_DESCRIPTION-"]
                        # actualiza el texto en pantalla con la nueva descripcion
                        window["-SHOW_DESCRIPTION-"].update(row[1])
                        change = True
                    else:
                        window_error(
                            " Ingrese una descripcion antes de intentar agregarla ")
                else:
                    window_error(" Seleccione una imagen para modificar ")
            except UnboundLocalError:
                # error al intentar agregar una descripcion sin seleccionar imagen
                window_error(
                    " Por favor seleccione una imagen a la cual modificar ")

        elif event == "-SAVE-":     # boton "guardar" prepara la lista de metadatos y lo guarda en el csv
            try:
                try:
                    if (change):    # chance = true si se genero cualquier cambio en la metadata
                        # se envia la lista de metadatos local actualizada para guardar los cambios en el csv
                        update_csv(row)
                        change = False
                except UnboundLocalError:
                    window_error(" Realize algun cambio antes de guardalo ")
            except UnboundLocalError:
                # error al intentar guardar sin seleccionar imagen
                window_error(
                    " Por favor seleccione una imagen a la cual modificar ")

        elif event == "-FILE_LIST-":         # toma el nombre de la imagen seleccionada en el buscador, le acomoda el tamaño, actualiza el lado derecho
            try:                            # y setea "row" con los metadatos de la imagen
                # tomo los datos de la imagen seleccionada desde el csv y guardo en una lista local
                row = update_rigth_side(values["-FILE_LIST-"][0])
                # formato csv guarda todo como str por lo que hay que volver a convertir row[5] a una lista
                row[5] = list(row[5])
                tag_ini = 0
                row[5] = update_tags_buttons(row[5], tag_ini, tag_table)
            except IndexError:
                # En caso de intentar seleccionar un elemento vacio salta mensaje de error
                window_error(
                    " El directorio que eligio no tiene ninguna imagen .png para mostrar, por favor vuelva a configuracion y selecione una carpeta con imagenes dentro ")

        elif event == "-BACKWARD-":
            # retrocede el "carrucel" con los tags
            if tag_ini > 0:
                tag_ini -= 1
                row[5] = update_tags_buttons(row[5], tag_ini, tag_table)

        elif event == "-FORWARD-":
            # avanza el "carrusel" con los tags
            if (row != []) and (tag_ini + 2) < len(row[5])-1:
                tag_ini += 1
                row[5] = update_tags_buttons(row[5], tag_ini, tag_table)

        elif event == "-TAG1-" or event == "-TAG2-" or event == "-TAG3-":
            # ini siempre apunta al elemento en el boton mas izquierdo y pos es la diferencia hasta el boton selecionado
            if event == "-TAG1-":
                pos = 0
            elif event == "-TAG2-":
                pos = 1
            elif event == "-TAG3-":
                pos = 2
            if window_delete():  # ventana para eliminar tags
                if row[5] != []:
                    row[5].pop(tag_ini+pos)
                    if len(row[5]) <= 3 and tag_ini > 0:
                        tag_ini -= 1
                    row[5] = update_tags_buttons(row[5], tag_ini, tag_table)
                    change = True
    window.close()
