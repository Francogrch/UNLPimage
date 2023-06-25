import streamlit as st
from scripts.script import *
import matplotlib.pyplot as plt

# Estilo de página
st.set_page_config(
    page_title="Logs del sistema",
    page_icon="📊",
    layout="wide"
)


logo()
css_style()
title_md('Logs del sistema  📊', 50)
bar('#e3b04b',3,95)
title_md('Items 🔗',30)
st.markdown("""<a style="text-align: center; padding:0rem 1rem 2rem;"> [Uso por dia de semana](#uso-por-dia-de-semana) - [Uso de la aplicacion por generos](#procentaje-de-uso-de-la-aplicacion-por-generos) - [Cantidades de operaciones realizadas](#cantidades-de-operaciones-realizadas)
            - [Operaciones por nick](#operaciones-por-nick) - [Ranking de meme y collage](#ranking-de-meme-y-collage) - [Textos de memes](#textos-de-memes) - [Textos de collages](#textos-de-collages)
             - [Operaciones por genero](#operaciones-por-genero)</a>""",unsafe_allow_html=True)
bar('#e3b04b', 3, 95)


st.subheader('Inicializaciones y DataFrames')
md1 = """- Inicializamos las librerias
- La constate colors, con los colores que usaremos
- Las variables con las direcciones de los archivos que utilizaremos
    """
code1 = """import pandas as pd
import matplotlib.pyplot as plt
import os
COLORS = [
    '#BFEFFF',  # Lightblue
    '#BDF5BD',  # Lightgreen
    '#FFCACA',  # Red
    '#FFD8A0',  # Orange
    '#DAB8D9',  # Purple
    '#FFFFC0',  # Yellow
    '#C2FFFF',  # Cyan
    '#E0E0E0',  # Black
    '#F0E68C',  # Khaki
    '#ADD8E6',  # Lightblue
    '#98FB98',  # Palegreen
    '#FFA07A',  # Lightsalmon
    '#E6E6FA',  # Lavender
    '#FFEC8B',  # Lightgoldenrodyellow
]
path_main = os.path.join(os.path.abspath('')[:-9])
path_tagger = os.path.join(path_main, 'config','data_files','tagger.csv')
path_profiles = os.path.join(path_main,'config','data_files','profiles.json')
path_logs = os.path.join(path_main,'logs','logs.csv')

"""
md2 = """- Creamos el dataFrame con los datos del logs.csv
"""
code2 = """dF_logs = pd.read_csv(path_logs)"""
with st.expander('DataFrames que utilizaremos para los análisis',expanded=True):
    st.markdown(md1)
    st.code(code1,language="python")
    st.markdown(md2)
    st.code(code2,language="python")
    st.write('### DataFrame de los logs:')
    st.dataframe(dF_logs)
    st.write('### DataFrame de los perfiles: ')
    st.dataframe(dF_profile)
    
bar()


# Título principal
title_md('Análisis de datos 📈', 35)

# Grafico de barras - Uso por dia de semana
st.subheader('Uso por dia de semana')
md1 = """- Importamos la libreria datetime
- Creamos una nueva columna con la fecha bien pareseada
- Guardamos en variable date, la agrupacion de las fechas segun el dia de la semana, y la cantidad de veces que se repite"""

code1 = """
dF_logs['date'] = dF_logs['timestamp'].apply(lambda x: datetime.fromtimestamp(x))
date = dF_logs.groupby(dF_logs['date'].dt.day_of_week).size()
"""

md2 = """- Renombramos los indices con los respectivos nombres de los dias de la semana
"""
code2 = """ date = date.rename(index={0:'Lunes',1:'Martes',2:'Miercoles',3:'Jueves',4:'Viernes',5:'Sabado',6:'Domingo'})"""

md3 = """- Graficamos utilizando matplotlib
- Le agregamos un titulo, y sus etiquetas
- Ajustamos el texto de las etiquetas para que queden rotadas, en caso que sea necesario
- Se muestra el grafico"""
code3 = """fig, ax = plt.subplots()
ax.bar(date.index, date.values,color=COLORS)

plt.title("Cantidad por fecha")
plt.xlabel("Fecha")
plt.ylabel("Cantidad")

plt.xticks(rotation=45, ha='right')

plt.show()"""

with st.expander('Realizar un gráfico comparando los días de la semana en que se realizaron operaciones usando la aplicación.',expanded=True):
    st.markdown(md1)
    st.code(code1,language="python")
    st.markdown(md2)
    st.code(code2,language="python")
    st.markdown(md3)
    st.code(code3,language="python")
    c1, c2 = st.columns(2)
    c2.write('## Data Frame')
    c2.dataframe(week_day_use()[0])
    c1.write('## Grafico de barras')
    c1.pyplot(week_day_use()[1])
    
bar()


# Grafico de Torta - Procentaje de uso de la aplicacion por generos
st.subheader('Procentaje de uso de la aplicacion por generos')
md1 = """- Creamos un dataFrame con los datos del JSON de los perfiles
- Rotamos los indices por las columnas
- Renombramos la columna index por nick"""

code1 = """dF_profile = pd.read_json(path_profiles)
dF_profile = dF_profile.transpose().reset_index()
dF_profile = dF_profile.rename(columns={'index':'nick'})
"""

md2 = """- Creamos otro data frame, quedandonos solo con la columna nick, del dataframe de los logs"""

code2 = """dF_nick_log = dF_logs['nick'].to_frame()"""

md3 = """- Como tenen el mismo nombre, podemos juntar los dos dataFrames con un merge, y quedarnos con la columna de genero"""

code3 = """dF_merge = pd.merge(dF_nick_log,dF_profile,on='nick',how='outer')['genre']"""
md4 = """- Ahora ya podemos agrupar por genero, y contar sus repeticiones
- Renombramos la columna genre, por cant, y reseteamos los indices"""

code4 = """dF_genre = dF_merge.groupby(dF_merge).size().to_frame()
dF_genre = dF_genre.rename(columns={'genre':'cant'}).reset_index()
"""

md5 = """- Creamos el grafico, pasandole los datos de del dataFrame, los colores de la constante COLORS, le agregamos sombras, formateamos los valores a procentajes, y que comienze con un angulo de 90 grados
- Nos aseguramos que el grafico quede con un aspecto redondo
- Agregamos un titulo"""

code5 = """plt.pie(dF_genre['cant'], labels=dF_genre['genre'], autopct='%1.1f%%', colors=COLORS, shadow=True, startangle=90)
plt.axis('equal')
plt.title("Uso por género")
plt.show()"""
with st.expander('Relacionando el archivo de logs con el archivo de perfiles generar un gráfico que muestre los porcentajes de uso de la aplicación por género.',expanded=True):
    st.markdown(md1)
    st.code(code1,language="python")
    st.markdown(md2)
    st.code(code2,language="python")
    st.markdown(md3)
    st.code(code3,language="python")
    st.markdown(md4)
    st.code(code4,language="python")
    st.markdown(md5)
    st.code(code5,language="python")
    c1, c2 = st.columns(2)
    c2.write('## Data Frame')
    c2.dataframe(genre_use(dF_profile)[0])
    c1.write('Grafico de Torta')
    c1.pyplot(genre_use(dF_profile)[1])
    dF_profile = genre_use(dF_profile)[2]
    
bar()


# Grafico de barras - Cantidades de operaciones realizadas
st.subheader('Cantidades de operaciones realizadas')
md1 = """- Vamos a utilizar el dataFrame de Logs
- Guardamos en cant_op la cantidad de eventos de los logs, agrupando por evento y contando las repeticiones."""
code1 = """cant_op = dF_logs['event'].groupby(dF_logs['event']).size()"""
md2 = """- Creamos el grafico de barras, utilizando los colores de la constante COLORS
- Cambiamos el fondo del grafico
- Le agregamos titulo y etiquetas
- Ajustamos el formato de las etiquetas a 45 grados
- Imprimimos"""
code2 = """fig, ax = plt.subplots()
ax.bar(cant_op.index, cant_op.values,color=COLORS)
ax.set_facecolor('whitesmoke')

plt.title("Cantidad por operacion")
plt.xlabel("Operacion")
plt.ylabel("Cantidad")

plt.xticks(rotation=45, ha='right')
plt.show()"""

with st.expander('Generar un gráfico que refleje las cantidades de cada operación realizada.',expanded=True):
    st.markdown(md1)
    st.code(code1,language="python")
    st.markdown(md2)
    st.code(code2,language="python")
    c1, c2 = st.columns(2)
    c2.write('## Data Frame')
    c2.dataframe(cant_ope()[0])
    c1.write('## Grafico de barras')
    c1.pyplot(cant_ope()[1])
    
bar()


# Grafico de barra apilado horizontal - Operaciones por nick
st.subheader('Operaciones por nick')
md1 = """- Vamos a utlizar el dataFrame de logs
- Nos quedamos con las columnas nick y event del dataframe
- Agrupamos por nick y event, contamos repeticiones, lo volvemos dataframe y reseteamos los indices
- Renombramos las columnas"""
code1 = """cant_op_nick = dF_logs[['nick','event']]
cant_op_nick = cant_op_nick.groupby(['nick','event']).size().to_frame().reset_index()
cant_op_nick = cant_op_nick.rename(columns={0:'cant','nick':'Nick','event':'Operacion'})
"""
md2 = """- Utilizamos el metodo pivot, para rotar el dataframe, poniendo como indice la columna Nick, y como columna el indice Operacion, los valores de DF seran los que estan en la columna cant. Luego reemplazamos los NaN por 0"""
code2 = """df_pivot = cant_op_nick.pivot(index='Nick',columns='Operacion', values='cant').fillna(0)"""
md3 = """- Graficamos, poniendo titulo, especificando que hay que stackear los valores, y usando los colores de la constante COLORS."""
code3 = """df_pivot.plot.barh(stacked=True, title='Operaciones por nick', color=COLORS)
plt.show()"""
with st.expander('Generar un gráfico de barra apilado que muestre las cantidades de operaciones por nick.',expanded=True):
    st.markdown(md1)
    st.code(code1,language="python")
    st.markdown(md2)
    st.code(code2,language="python")
    st.markdown(md3)
    st.code(code3,language="python")
    c1, c2 = st.columns(2)
    c2.write('## Data Frame')
    c2.dataframe(op_nick()[0])
    c1.write('## rafico de barra apilado horizontal')
    c1.pyplot(op_nick()[1])

bar()


# DataFrame - Ranking de meme y collage
st.subheader('Ranking de meme y collage')
md1 = """- Nos quedamos con las columnas de event y value del DataFrame de logs
- Guardamos en new_meme, solo las filas que tengan en evento new_meme
- Agrupamos los eventos y contamos las repeticiones
- Ordenamos de manera descendente, y lo transformamos en DataFrame
- Renombramos la columna value, reseteamos los indices y remobramos la otra columna value
- Nos quedamos con los 5 primeros"""
code1 = """logs_events = dF_logs[['event','value']]
new_meme = logs_events.loc[logs_events['event'] == 'new_meme', 'value']
new_meme = new_meme.groupby(new_meme).count()
new_meme = new_meme.sort_values(ascending=False).to_frame()
new_meme = new_meme.rename(columns={'value': 'Usos'}).reset_index().rename(columns={'value': 'Imagen'})
new_meme = new_meme.head(5)
"""

md2 = """- Creamos un DataFrame con las columans de event y value de dF_logs
- Solo guardamos los eventos que sean new_collage, lo transformamos a data frame
- Spliteamos los valores por comnas, le sacamos las corchetes de inicio y final
- Transformamos esa lista str, a una fila individual por elemento"""
code2 = """logs_events = dF_logs[['event','value']]
new_collage = logs_events.loc[logs_events['event'] == 'new_collage', 'value'].to_frame()
new_collage = new_collage['value'].str[1:-1].str.split(', ')
new_collage = new_collage.explode()"""
md3 = """- Agrupamos por los mismo valores, y contamos sus repeticiones
- Ordenamos de manera descendete, y lo convertimos en DataFrame
- Renombramos las columas value
- Nos quedamos con los primeros 5"""
code3 = """new_collage = new_collage.groupby(new_collage).count()
new_collage = new_collage.sort_values(ascending=False).to_frame()
new_collage = new_collage.rename(columns={'value': 'Usos'}).reset_index().rename(columns={'value': 'Imagen'})
new_collage = new_collage.head(5)"""
with st.expander('Generar un ranking de las 5 imágenes más usadas para generar memes y otro para generar collages.',expanded=True):
    st.markdown(md1)
    st.code(code1,language="python")
    st.markdown(md2)
    st.code(code2,language="python")
    st.markdown(md3)
    st.code(code3,language="python")
    c1, c2 = st.columns(2)
    c2.write('## Data Frame de meme')
    c2.dataframe(ranking_meme())
    c1.write('## Data Frame de collage')
    c1.dataframe(ranking_collage())
    
bar()


# Nubes de palabras - Textos de memes y collages
st.subheader('Textos de memes')
md1 = """
- Utilizaremos las columnas de event y text del dataFrame dF_logs
- Nos quedamos solo con los eventos que sean 'new_meme', y lo convertimos en dataframe"""
code1 = """meme_text = dF_logs[['event','text']].loc[logs_events['event'] == 'new_meme', 'text'].to_frame()
"""
md2 = """- Hacemos un slicing, eliminando los corchetes, y eliminamos las comillas simples y comas, y lo dividimos en una lista de acuerdo a los espacios
- Luego, transformamos esos elementos de la lista, a filas del dataframe, y los guardamos en la columna text"""
code2 = """meme_text['text'] = meme_text['text'].str[1:-1].str.replace("'","").str.replace(",","").str.split(' ')
meme_text = meme_text.explode(column='text')"""
md3 = """- Agrupamos estas palabras, y contamos la cantidad de repeticiones """
code3 = """meme_text = meme_text.groupby(['text']).size()"""
md4 = """- Por ultimo, utilizamos la libreria wordcloud para graficar, usando los parametros del color de fondo, el color del contorno, y un mapeo de color a la nube."""
code4 = """from wordcloud import WordCloud
wordcloud = WordCloud(background_color="black", contour_color='steelblue', colormap='Pastel1')
wordcloud.generate_from_frequencies(meme_text)

plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()"""
with st.expander('Generar una nube de palabras de los textos agregados en los collages y otra con los textos agregados en los memes',expanded=True):
    st.markdown(md1)
    st.code(code1,language="python")
    st.markdown(md2)
    st.code(code2,language="python")
    st.markdown(md3)
    st.code(code3,language="python")
    st.markdown(md4)
    st.code(code4,language="python")
    c1, c2 = st.columns(2)
    c2.write('## Data Frame')
    c2.dataframe(cloud_text_meme()[0])
    c1.write('## Nube de palabras')
    c1.pyplot(cloud_text_meme()[1])
    
bar()


# Nubes de palabras - Textos de memes y collages
st.subheader('Textos de collages')
md1 = """
- Nos quedamos solo con los eventos que sean 'new_collage', y lo convertimos en dataframe
"""
code1 = """collage_text = dF_logs[['event','text']].loc[logs_events['event'] == 'new_collage', 'text'].to_frame()"""
md2 = """- Dividimos las palabras en una lista de acuerdo a los espacios
- Luego, transformamos esos elementos de la lista, a filas del dataframe, y los guardamos en la columna text"""
code2 = """collage_text['text'] = collage_text['text'].str.split(' ')
collage_text = collage_text.explode(column='text')"""
md3 = """- Agrupamos estas palabras, y contamos la cantidad de repeticiones """
code3 = """collage_text = collage_text.groupby(['text']).size()"""
md4 = """- Por ultimo, utilizamos la libreria wordcloud para graficar, usando los parametros del color de fondo, el color del contorno, y un mapeo de color a la nube."""
code4 = """from wordcloud import WordCloud
wordcloud = WordCloud(background_color="black", contour_color='steelblue', colormap='Pastel1')
wordcloud.generate_from_frequencies(collage_text)

plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()"""
with st.expander('Generar una nube de palabras de los textos agregados en los collages y otra con los textos agregados en los memes',expanded=True):
    st.markdown(md1)
    st.code(code1,language="python")
    st.markdown(md2)
    st.code(code2,language="python")
    st.markdown(md3)
    st.code(code3,language="python")
    st.markdown(md4)
    st.code(code4,language="python")
    c1, c2 = st.columns(2)
    c2.write('## Data Frame')
    c2.dataframe(cloud_text_collage()[0])
    c1.write('## Nube de palabras')
    c1.pyplot(cloud_text_collage()[1])
    
bar()


# Grafico de torta - Operaciones por genero
st.subheader('Operaciones por genero')
md1 = """- Nos quedamos con las columans de nick y event
- Renombramos la columna nick por Nick"""
code1 = """cant_op_nick = dF_logs[['nick','event']]
cant_op_nick = cant_op_nick.rename(columns={'Nick':'nick'})"""
md2 = """- Vamos a utilizar el dataframe de los perfiles
- Realizamos un merge de acuerdo a la columna nick, agregando la columna gerne al dataframe cant_op_nick y realizamos slicing por columnas genre y event
- Dejamos solamente en la columna event, los eventos que sean change_tags, ne_image_classified, y change_description
- Quitamos las filas que contengan NaN
- Agrupamos segun genero y luego evento, contamos las repeticiones, lo transformamos a dataframe y reseteamos los indices
- Concadenamos los valores de las columnas a una sola columna
- Eliminamos la columna event
- Renombramos la columna genre y la columna 0"""
code2 = """op_gen = pd.merge(cant_op_nick,dF_profile,on='nick',how='left')[['genre','event']]
op_gen['event'] = op_gen.loc[(op_gen['event'] == 'change_tags') | (op_gen['event'] == 'new_image_classified') | (op_gen['event'] == 'change_description'), 'event']
op_gen = op_gen.dropna()
op_gen = op_gen.groupby(['genre','event']).size().to_frame().reset_index()
op_gen['genre'] = op_gen['genre'] + " " + op_gen['event'] 
op_gen = op_gen.drop('event',axis=1)
op_gen = op_gen.rename(columns={'genre':'genre+op',0:'cant'})
"""
md3 = """- Creamos el grafico de torta, le agregamos las etiquetas, transformamos los valores a porcentaje, usamos los colores de la constante COLORS, habilitamos las sombras, y que comienze el grafico en un angilo de 90 grados
- Hacemos que sea si o si, un circulo
- Le agregamos un titulo"""
code3 = """plt.pie(op_gen['cant'], labels=op_gen['genre+op'], autopct='%1.1f%%', colors=COLORS, shadow=True, startangle=90)

plt.axis('equal')
plt.title("Uso por género")

plt.show()"""
with st.expander('Con los datos del archivo de perfiles generar un gráfico de torta con los porcentajes según género de las personas que realizaron las operaciones: nueva imagen clasificada, modificación de imagen previamente clasificada.',expanded=True):
    st.markdown(md1)
    st.code(code1,language="python")
    st.markdown(md2)
    st.code(code2,language="python")
    st.markdown(md3)
    st.code(code3,language="python")
    c1, c2 = st.columns(2)
    c2.write('## Data Frame')
    c2.dataframe(pie_op_gen(dF_profile)[0])
    c1.write('## Grafico de torta')
    c1.pyplot(pie_op_gen(dF_profile)[1])
    
bar()


# Información adicional
st.info("UNLP Informatica-Seminario Python ©")
