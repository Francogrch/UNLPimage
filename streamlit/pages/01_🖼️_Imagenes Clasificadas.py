import streamlit as st
from scripts.script import *
import matplotlib.pyplot as plt

# Estilo de página
st.set_page_config(
    page_title="Imagenes Clasificadas",
    page_icon="🖼️",
    layout="wide"
)


logo()
css_style()
title_md('Imagenes Clasificadas 🖼️',50)
bar('#e3b04b',3,95)
title_md('Items 🔗',30)
st.markdown("""<a style="text-align: center; padding:0rem 2rem 2rem;"> [Tipos de Imágenes](#tipos-de-im-genes) - [Dimensiones maximas](#dimensiones-m-ximas-de-las-im-genes-etiquetadas) - [Relacion alto y ancho](#relaci-n-alto-y-ancho-de-im-genes)
            - [Modificacion segun dia de la semana](#modificacion-segun-dia-de-la-semana) - [Actualizaciones a travez del tiempo](#actualizaciones-a-travez-del-tiempo) - [Tags](#tags) - [Tres tags mas utilizados](#tres-tags-mas-utilizados)
             - [Bytes promedio por usuario](#bytes-promedio-por-usuario)</a>""",unsafe_allow_html=True)
bar('#e3b04b',3,95)


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
with st.expander('DataFrames que utilizaremos para los análisis',expanded=True):
    st.markdown(md1)
    st.code(code1,language="python")

    st.write('### DataFrame de las imagenes etiquetadas:')
    st.dataframe(dF)
    st.write('### DataFrame de los perfiles: ')
    st.dataframe(dF_profile)
bar()


# Título principal
title_md('Análisis de datos 📈',35)


# Sección: Gráfico de Torta - Tipos de Imágenes
st.markdown('### Tipos de Imágenes')#

code1 = """
types = dF['Type'].reset_index()
types = types.drop('index',axis=1)
types = types.groupby(['Type']).value_counts().reset_index()
types['Type'] = types['Type'].str.slice(6)
"""
md1 = """- Creamos un DataFrame solamente con la columa llamada 'Type'.
- Luego eliminamos la fila index, ya que no nos sirve.
- Agrupamos por tipo, contando la veces que se repite, y utilizamos reset_index para que vuelva a ser un DataFrame.
- Por ultimo, retiramos la palabra 'image/', de cada fila,  ya que no nos sirve"""
md2 = """- Graficamos con la libreria matplotlib:
        Un grafico de torta, agregando sombras, porcentanjes y especificando la etiqueta de cada uno de los tipos.
"""
code2 = """plt.pie(types['count'], labels=types['Type'], autopct='%1.1f%%', shadow=True, colors =COLORS)
plt.title("Tipos de datos")
plt.show()
"""
with st.expander('Este gráfico muestra el porcentaje de cada tipo de imagen en el conjunto de datos.',expanded=True):
    st.markdown(md1)
    st.code(code1,language="python")
    st.markdown(md2)
    st.code(code2,language="python")
    c1, c2 = st.columns(2)
    c2.write('## Data Frame')
    c2.dataframe(types_images()[0])
    c1.write('## Gráfico de Torta')
    c1.pyplot(types_images()[1])

bar()


# Sección: Dimensiones Máximas de las Imágenes Etiquetadas
st.markdown('### Dimensiones Máximas de las Imágenes Etiquetadas')#
code1 = """dF['Height'] = dF['Resolution'].apply(lambda x: int(x.split(',')[0][1:]))
dF['Width'] = dF['Resolution'].apply(lambda x: int(x.split(',')[1][:-1]))
"""
md1 = """Agregamos al DataFrame dos columnas:
- Alto: tipo de dato entero.
- Ancho: tipo de dato entero.
  
Esto nos va a servir para poder hacer operaciones con estos numeros"""
md2 = """- Calculamos el maximo y el minimo, tanto de la columna alto, como ancho.

- Lo imprimimos."""
code2 = """ max_height = dF['Height'].max()
max_width = dF['Width'].max()
print('+','-'*20,'+')
print(f"| Maximo alto: {max_height}px  |\n|{' '*22}|\n| Maximo ancho: {max_width}px |")
print('+','-'*20,'+')"""
with st.expander('Calcula los valores máximos de ancho y alto de las imágenes clasificadas.',expanded=True):
    st.markdown(md1)
    st.code(code1, language="python")
    st.markdown(md2)
    st.code(code2, language="python")
    c1, c2 = st.columns(2)
    c1.dataframe(max_height_width()[2])
    c2.write(f" La altura maxima es de {max_height_width()[0]}px y el alto maximo de {max_height_width()[1]}px")

bar()


# Sección: Gráfico de Dispersión - Relación Alto y Ancho de Imágenes
st.markdown('### Relación Alto y Ancho de Imágenes')
md1 = """- Creamos una variable de tipo series con la informaciond el alto y ancho que tenes almacenada en el DataFrame 
"""
code1 = """wid_hei = pd.Series(dF['Width'].values, index=dF['Height'])
"""
md2 = """- Graficamos utilizando la libreria matplotlib
  - Cambiamos el color (c), la opacidad(alpha)
  - Agregamos las etiquetas y el titulo
  - Agregamos cuadriculas a la imagen (grid)"""
code2 = """fig, ax = plt.subplots()
ax.scatter(wid_hei.index, wid_hei.values, c='steelblue', alpha=0.7)
ax.set_xlabel('Ancho')
ax.set_ylabel('Altura')
ax.set_title('Gráfico de dispersión de Ancho vs. Altura')
ax.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()"""
with st.expander('Este gráfico de dispersión muestra la relación entre el ancho y el alto de las imágenes.',expanded=True):
    st.markdown(md1)
    st.code(code1, language="python")
    st.markdown(md2)
    st.code(code2, language="python")
    c1, c2 = st.columns(2)
    c2.write('## Data Frame')
    c2.dataframe(dispersion()[0])
    c1.write('## Gráfico de Dispersión')
    c1.pyplot(dispersion()[1])

bar()


# Seccion: Grafico de barras - Modificacion segun dia de la semana
st.markdown('### Modificacion segun dia de la semana')
md1 = """Importamos la libreria datetime
Creamos una nueva columna con la fecha bien parseada"""
code1 = """dF['Fecha'] = dF['Last_update'].apply(lambda x: datetime.fromtimestamp(x))"""
md2 = """- Creamos una variable, donde agrupamos por dia de la semana, y guardamos la cantidad de repeticiones."""
code2 = """date = dF.groupby(dF['Fecha'].dt.day_of_week).size()"""
md3 = """- Renombramos los indices de los dias, para luego poder graficarlos con su nombre correspondiente"""
code3 = """date = date.rename(index={0:'Lunes',1:'Martes',2:'Miercoles',3:'Jueves',4:'Viernes',5:'Sabado',6:'Domingo'})"""
md4 = """- Graficamos utilizando matplotlib, pasando la constante colores para hacerlo mas agradable.
- Tambien le agregamos un texto, y sus respectivas etiquetas.
- Rotamos las etiquetas en el caso que no entren (xticks)
- Ajustamos el espacio entre las barras (tight_layout)"""
code4 = """fig, ax = plt.subplots()

ax.bar(date.index, date.values, color=COLORS)

plt.title("Cantidad de operaciones por día")
plt.xlabel("Día")
plt.ylabel("Cantidad de operaciones")

plt.xticks(rotation=45)
plt.tight_layout()

plt.show()"""
with st.expander('En base a la fecha de última actualización, cantidad de cambios realizados para cada día de la semana (posible gráfico de torta o barras).',expanded=True):
    st.markdown(md1)
    st.code(code1, language="python")
    st.markdown(md2)
    st.code(code2, language="python")
    st.markdown(md3)
    st.code(code3, language="python")
    st.markdown(md4)
    st.code(code4, language="python")
    c1, c2 = st.columns(2)
    c2.write('## Data Frame')
    c2.dataframe(week_day()[0])
    c1.write('## Grafico de barras')
    c1.pyplot(week_day()[1])

bar()


# Seccion: Grafico de lineas - Actualizaciones a travez del tiempo
st.markdown('### Actualizaciones a travez del tiempo')
md1 = """- Agrupamos segun la fecha, y su cantidad de repeticiones."""
code1 = """date_upt = dF.groupby(dF['Fecha'].dt.date).size()"""
md2 = """- Graficamos utilizando matplotlib, pasando la el valor 'blue' como color para hacerlo mas agradable.
- Tambien le agremos un texto, y sus respectivas etiquetas.
- Agregamos cuadriculas a la imagen (grid)"""
code2 = """fig, ax = plt.subplots()
ax.plot(date_upt.index, date_upt.values, marker = "o", markersize = 5,color=COLORS[0])
plt.title("Cantidad de operaciones por fecha")
plt.xlabel("FECHA")
plt.ylabel("CANT. OPERACIONES")
ax.grid(True, linestyle='--', alpha=0.5)
plt.show()"""

with st.expander('Crear un gráfico de líneas para visualizar la evolución de la cantidad de actualizaciones a lo largo del tiempo.',expanded=True):
    st.markdown(md1)
    st.code(code1, language="python")
    st.markdown(md2)
    st.code(code2, language="python")
    c1, c2 = st.columns(2)
    c2.write('## Data Frame')
    c2.dataframe(line_time()[0])
    c1.write('## Grafico de lineas')
    c1.pyplot(line_time()[1])
    
bar()


# Seccion: Nube de palabras - Tags
st.markdown('### Tags')
md1 = """- Guardamos todos los tags, en una variable, spliteando por ', ', para separarlos por palabras.
- Luego creamos una lista estos valores, utilizando el metodo explode().
- Por ultimo reemplazamos las ', por la nada misma, para borrarlas"""
code1 = """s_cloud = dF['Tags'].str[1:-1].str.split(', ')
s_cloud = s_cloud.explode()
s_cloud = s_cloud.str.replace("'","")"""
md2 = """- Luego, agrupamos las palabras, contando sus repeticiones."""
code2 = """s_cloud = s_cloud.groupby(s_cloud.values).count()"""
md3 = """- Por ultimo, utilizamos la libreria wordcloud para graficar, usando los parametros del color de fondo, el color del contorno, y un mapeo de color a la nube."""
code3 = """from wordcloud import WordCloud
wordcloud = WordCloud(background_color="black", contour_color='steelblue', colormap='Pastel1')
wordcloud.generate_from_frequencies(s_cloud)

plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()"""
with st.expander('Con la lista de tags generar una nube de palabras.',expanded=True):
    st.markdown(md1)
    st.code(code1, language="python")
    st.markdown(md2)
    st.code(code2, language="python")
    st.markdown(md3)
    c1, c2 = st.columns(2)
    c2.write('## Data Frame')
    c2.dataframe(cloud_tags()[0])
    c1.write('## Nube de palabras')
    c1.pyplot(cloud_tags()[1])

bar()

# Seccion: DataFrame - Tres tags mas utilizados
st.markdown('### Tres tags mas utilizados')
md1 = """- Ordenamos los tags que tenemos del grafico anterior, nos quedamos con los 3 mas utilizados
- Lo pasamos a un data frame, reseteamos los indices
- Renombramos las columnas"""
code1 = """tags_max = s_cloud.sort_values(ascending=False).head(3)
tags_max = tags_max.to_frame().reset_index()
tags_max = tags_max.rename(columns = {'index':'Tags','Tags':'Usos'})
tags_max
"""
with st.expander('Informar cuáles son los 3 tags más utilizados.',expanded=True):
    st.markdown(md1)
    st.code(code1, language="python")
    st.dataframe(tags_tops())
    
bar()

# Seccion: DataFrame - Bytes promedio por usuario 
st.markdown('### Bytes promedio por usuario')
md1 = """- Creamos DataFrame con datos de los perfiles
- Solo nos quedamos con las llaves, osea los nicks de los perfiles
- Lo volvemos un dataframe, reiniciamos los indices y eliminamos la columna llamada 0, que genera el reset_index
- renombramos la columna index por Profile"""
code1 = """dF_json = pd.read_json(path_profiles) 
dF_json = dF_json.keys()
dF_json = dF_json.to_frame().reset_index().drop(0,axis=1) 
dF_json = dF_json.rename(columns={"index": "Profile"})
"""
md2 = """- Una vez que tenemos el mismo nombre de la columna donde almacenamos los nicks, podemos hacer un merge, con el dataFrame de los tags"""
code2 = """prom= pd.merge(dF,dF_json, on='Profile', how='outer')"""
md3 = """- Creamos otro dataFrame con solamente los nicks y el espacio utilizado
- Agrupamos por perfiles, y contamos las aparicionbes del perfil, sin eliminar las filas que tengan NaN, y resetiamos los indices
- Por ultimo, volvemos a agrupar por perfil, sumamos las columnas, y reseteamos los indices."""
code3 = """dF_profiles = prom[['Profile','Size']]
dF_profiles = dF_profiles.groupby(dF_profiles['Profile']).value_counts(dropna=False).reset_index()
dF_profiles = dF_profiles.groupby(dF_profiles['Profile']).sum().reset_index()
"""
md4 = """- Creamos una columna Averange donde se guarda el promedio del espacio utilizado en bytes
- Creamos una columna Averange_MB donde pasamos el valor de la columna Average a MB
- Luego ese valor lo pasamos a string, y le sumamos la palbara 'MB'"""
code4 = """dF_profiles['Average'] = (dF_profiles['Size'] / dF_profiles['count'])
dF_profiles['Average_MB'] = round(dF_profiles['Average'] / (1024*1024), 2)
dF_profiles['Average_MB'] = dF_profiles['Average_MB'].astype(str)
dF_profiles['Average_MB'] = dF_profiles['Average_MB'] + ' MB'"""
md5 = """- Por ultimo creamos un dataFrame, con las columnas Profile y Averange_MB
- Renombramos las columnas, y mostramos"""
code5 = """dF_final = dF_profiles[['Profile','Average_MB']]
dF_final = dF_final.rename(columns={'Profile':'Perfil','Average_MB':'Tamaño promedio'})
dF_final"""
with st.expander('Calcular el tamaño en bytes promedio de las imágenes actualizadas por cada perfil, incluir los perfiles que no hayan realizado actualizaciones.',expanded=True):
    st.markdown(md1)
    st.code(code1, language="python")
    st.markdown(md2)
    st.code(code2, language="python")
    st.markdown(md3)
    st.code(code3, language="python")
    st.markdown(md4)
    st.code(code4, language="python")
    st.markdown(md5)
    st.code(code5, language="python")
    st.dataframe(bytes_promedio())
    
bar()


# Información adicional
st.info("UNLP Informatica-Seminario Python ©")



