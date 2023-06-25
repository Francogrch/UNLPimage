import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime
from wordcloud import WordCloud
import streamlit as st
import base64
from pathlib import Path
path_main = os.path.join(os.path.abspath('')[:-10])


def bar(color='#e6be70', height=1, width=85):
    return st.markdown(f"""<hr style="background-color: {color};height: {height}px; width: {width}%;">""", unsafe_allow_html=True)


def logo():
    logo_url = os.path.join(path_main, 'logo.png')
    logo = f"url(data:image/png;base64,{base64.b64encode(Path(logo_url).read_bytes()).decode()})"
    return st.markdown(
        f"""
            <style>
                [data-testid="stSidebarNav"] {{
                    background-image: {logo};
                    background-repeat: no-repeat;
                    background-size: 110px;
                    padding-top: 60px;
                    background-position: 100px 30px;
                }}

            </style>
            """,
        unsafe_allow_html=True,
    )


def css_style():
    return st.markdown(
        f"""
            <style>
                hr {{
                    border: none;
                    border-radius: 5px;
                    margin-left: auto;
                    margin-right: auto;
                }}
                [data-testid="stExpander"] {{
                    font-style: italic;
                    color: red;
                }}
                .css-z5fcl4{{
                    padding: 0rem 10rem 10rem;
                }}
                @media screen and (max-width: 1000px) {{
                .css-z5fcl4{{
                    padding: 0rem 1rem 10rem;
                    }}
                }}
                .css-25i2ip{{
                    font-size: 0px;
                }}
            </style>
            """,
        unsafe_allow_html=True,
    )


def title_md(title, size):
    return st.markdown(f"""
                       <h1 style="text-align: center; font-size: {size}px;color: #F0F0F0;">{title}</h1>
                       """, unsafe_allow_html=True)


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


path_tagger = os.path.join(path_main, 'config', 'data_files', 'tagger.csv')
path_profiles = os.path.join(
    path_main, 'config', 'data_files', 'profiles.json')
path_logs = os.path.join(path_main, 'logs', 'logs.csv')


dF = pd.read_csv(path_tagger)
dF_logs = pd.read_csv(path_logs)
dF_profile = pd.read_json(path_profiles)


# Grafico de torta - Tipos de imagenes
def types_images():
    types = dF['Type'].reset_index()
    types = types.drop('index', axis=1)
    types = types.groupby(['Type']).value_counts().reset_index()
    types['Type'] = types['Type'].str.slice(6)
    plt.pie(types['count'], labels=types['Type'],
            autopct='%1.1f%%', shadow=True, colors=COLORS)
    plt.title("Tipos de datos")
    return types, plt


# Alto y ancho maximos de las imagenes etiquetadas
def max_height_width():
    dF['Height'] = dF['Resolution'].apply(lambda x: int(x.split(',')[0][1:]))
    dF['Width'] = dF['Resolution'].apply(lambda x: int(x.split(',')[1][:-1]))
    max_height = dF['Height'].max()
    max_width = dF['Width'].max()
    return max_height, max_width, dF[['Height', 'Width']]


# Grafico dispersion - Relacion alto y ancho de imagenes
def dispersion():
    wid_hei = pd.Series(dF['Width'].values, index=dF['Height'])
    fig, ax = plt.subplots()
    ax.scatter(wid_hei.index, wid_hei.values, c='steelblue', alpha=0.7)
    ax.set_xlabel('Ancho')
    ax.set_ylabel('Altura')
    ax.set_title('Gráfico de dispersión de Ancho vs. Altura')
    ax.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    return wid_hei, fig


# Grafico de barras - Modificacion segun dia de la semana
def week_day():
    dF['Fecha'] = dF['Last_update'].apply(lambda x: datetime.fromtimestamp(x))
    date = dF.groupby(dF['Fecha'].dt.day_of_week).size()
    date = date.rename(index={0: 'Lunes', 1: 'Martes', 2: 'Miercoles',
                              3: 'Jueves', 4: 'Viernes', 5: 'Sabado', 6: 'Domingo'})

    fig, ax = plt.subplots()
    ax.bar(date.index, date.values, color=COLORS)
    plt.title("Cantidad de operaciones por día")
    plt.xlabel("Día")
    plt.ylabel("Cantidad de operaciones")
    plt.xticks(rotation=45)
    plt.tight_layout()
    return date, plt


# Grafico de lineas - Actualizaciones a travez del tiempo
def line_time():
    date_upt = dF.groupby(dF['Fecha'].dt.date).size()
    fig, ax = plt.subplots()
    ax.plot(date_upt.index, date_upt.values,
            marker="o", markersize=5, color=COLORS[0])
    plt.title("Cantidad de operaciones por fecha")
    plt.xlabel("FECHA")
    plt.ylabel("CANT. OPERACIONES")
    ax.grid(True, linestyle='--', alpha=0.5)
    return date_upt, plt


# Nube de palabras - Tags
def cloud_tags():
    s_cloud = dF['Tags'].str[1:-1].str.split(', ')
    s_cloud = s_cloud.explode()
    s_cloud = s_cloud.str.replace("'", "")
    s_cloud = s_cloud.groupby(s_cloud.values).count()

    wordcloud = WordCloud(background_color="black",
                          contour_color='steelblue', colormap='Pastel1')
    wordcloud.generate_from_frequencies(s_cloud)
    plt.title("Cloud")
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    return s_cloud, plt


# DataFrame - Tres tags mas utilizados
def tags_tops():
    s_cloud = dF['Tags'].str[1:-1].str.split(', ')
    s_cloud = s_cloud.explode()
    s_cloud = s_cloud.str.replace("'", "")
    s_cloud = s_cloud.groupby(s_cloud.values).count()
    tags_max = s_cloud.sort_values(ascending=False).head(3)
    tags_max = tags_max.to_frame().reset_index()
    tags_max = tags_max.rename(columns={'index': 'Tags', 'Tags': 'Usos'})
    return tags_max


# DataFrame - Bytes promedio por usuario
def bytes_promedio():
    dF_json = pd.read_json(path_profiles)
    dF_json = dF_json.keys()
    dF_json = dF_json.to_frame().reset_index().drop(0, axis=1)
    dF_json = dF_json.rename(columns={"index": "Profile"})
    prom = pd.merge(dF, dF_json, on='Profile', how='outer')
    dF_profiles = prom[['Profile', 'Size']]
    dF_profiles = dF_profiles.groupby(
        dF_profiles['Profile']).value_counts(dropna=False).reset_index()
    dF_profiles = dF_profiles.groupby(
        dF_profiles['Profile']).sum().reset_index()
    dF_profiles['Average'] = (dF_profiles['Size'] / dF_profiles['count'])
    dF_profiles['Average_MB'] = round(dF_profiles['Average'] / (1024*1024), 2)
    dF_profiles['Average_MB'] = dF_profiles['Average_MB'].astype(str)
    dF_profiles['Average_MB'] = dF_profiles['Average_MB'] + ' MB'
    dF_final = dF_profiles[['Profile', 'Average_MB']]
    dF_final = dF_final.rename(
        columns={'Profile': 'Perfil', 'Average_MB': 'Tamaño promedio'})
    return dF_final


# Analisis de datos de log del sistema

# Grafico de barras - Uso por dia de semana
def week_day_use():
    dF_logs['date'] = dF_logs['timestamp'].apply(
        lambda x: datetime.fromtimestamp(x))
    date = dF_logs.groupby(dF_logs['date'].dt.day_of_week).size()
    date = date.rename(index={0: 'Lunes', 1: 'Martes', 2: 'Miercoles',
                       3: 'Jueves', 4: 'Viernes', 5: 'Sabado', 6: 'Domingo'})
    fig, ax = plt.subplots()
    ax.bar(date.index, date.values, color=COLORS)
    plt.title("Cantidad por fecha")
    plt.xlabel("Fecha")
    plt.ylabel("Cantidad")
    plt.xticks(rotation=45, ha='right')
    return date, fig

# Grafico de Torta - Procentaje de uso de la aplicacion por generos


def genre_use(dF_profile):
    dF_profile = dF_profile.transpose().reset_index()
    dF_profile = dF_profile.rename(columns={'index': 'nick'})
    dF_nick_log = dF_logs['nick'].to_frame()
    dF_merge = pd.merge(dF_nick_log, dF_profile,
                        on='nick', how='outer')['genre']
    dF_genre = dF_merge.groupby(dF_merge).size().to_frame()
    dF_genre = dF_genre.rename(columns={'genre': 'cant'}).reset_index()
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(dF_genre['cant'], labels=dF_genre['genre'],
           autopct='%1.1f%%', colors=COLORS, shadow=True, startangle=90)
    ax.axis('equal')
    ax.set_title("Uso por género")
    return dF_genre, fig, dF_profile


# Grafico de barras - Cantidades de operaciones realizadas
def cant_ope():
    cant_op = dF_logs['event'].groupby(dF_logs['event']).size()
    fig, ax = plt.subplots()
    ax.bar(cant_op.index, cant_op.values, color=COLORS)
    ax.set_facecolor('whitesmoke')
    plt.title("Cantidad por operacion")
    plt.xlabel("Operacion")
    plt.ylabel("Cantidad")
    plt.xticks(rotation=45, ha='right')
    return cant_op, fig

# Grafico de barra apilado horizontal - Operaciones por nick


def op_nick():
    cant_op_nick = dF_logs[['nick', 'event']]
    cant_op_nick = cant_op_nick.groupby(
        ['nick', 'event']).size().to_frame().reset_index()
    cant_op_nick = cant_op_nick.rename(
        columns={0: 'cant', 'nick': 'Nick', 'event': 'Operacion'})
    df_pivot = cant_op_nick.pivot(
        index='Nick', columns='Operacion', values='cant').fillna(0)
    df_pivot.plot.barh(
        stacked=True, title='Operaciones por nick', color=COLORS)
    return df_pivot, plt

# DataFrame - Ranking de meme y collage


def ranking_meme():
    logs_events = dF_logs[['event', 'value']]
    new_meme = logs_events.loc[logs_events['event'] == 'new_meme', 'value']
    new_meme = new_meme.groupby(new_meme).count()
    new_meme = new_meme.sort_values(ascending=False).to_frame()
    new_meme = new_meme.rename(columns={'value': 'Usos'}).reset_index().rename(
        columns={'value': 'Imagen'})
    new_meme = new_meme.head(5)
    return new_meme


def ranking_collage():
    logs_events = dF_logs[['event', 'value']]
    new_collage = logs_events.loc[logs_events['event']
                                  == 'new_collage', 'value'].to_frame()
    new_collage = new_collage['value'].str[1:-1].str.split(', ')
    new_collage = new_collage.explode()
    new_collage = new_collage.groupby(new_collage).count()
    new_collage = new_collage.sort_values(ascending=False).to_frame()
    new_collage = new_collage.rename(
        columns={'value': 'Usos'}).reset_index().rename(columns={'value': 'Imagen'})
    new_collage = new_collage.head(5)
    return new_collage

# Nubes de palabras - Textos de memes y collages


def cloud_text_meme():
    meme_text = dF_logs[['event', 'text']
                        ].loc[dF_logs['event'] == 'new_meme', 'text'].to_frame()
    meme_text['text'] = meme_text['text'].str[1:-
                                              1].str.replace("'", "").str.replace(",", "").str.split(' ')
    meme_text = meme_text.explode(column='text')
    meme_text = meme_text.groupby(['text']).size()
    wordcloud = WordCloud(background_color="black",
                          contour_color='steelblue', colormap='Pastel1')
    wordcloud.generate_from_frequencies(meme_text)

    # Crear figura y ejes
    fig, ax = plt.subplots(figsize=(8, 8))

    # Mostrar nube de palabras en los ejes
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')

    return meme_text.to_frame(), fig

# Nubes de palabras - Texto de Collages


def cloud_text_collage():
    collage_text = dF_logs[['event', 'text']
                           ].loc[dF_logs['event'] == 'new_collage', 'text'].to_frame()
    collage_text['text'] = collage_text['text'].str.split(' ')
    collage_text = collage_text.explode(column='text')
    collage_text = collage_text.groupby(['text']).size()
    wordcloud = WordCloud(background_color="black",
                          contour_color='steelblue', colormap='Pastel1')
    wordcloud.generate_from_frequencies(collage_text)

    # Crear figura y ejes
    fig, ax = plt.subplots(figsize=(8, 8))

    # Mostrar nube de palabras en los ejes
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')

    return collage_text.to_frame(), fig

# Grafico de torta - Operaciones por genero


def pie_op_gen(dF_profile):
    cant_op_nick = dF_logs[['nick', 'event']]
    cant_op_nick = cant_op_nick.rename(columns={'Nick': 'nick'})
    op_gen = pd.merge(cant_op_nick, dF_profile, on='nick',
                      how='left')[['genre', 'event']]
    op_gen['event'] = op_gen.loc[(op_gen['event'] == 'change_tags') | (
        op_gen['event'] == 'new_image_classified') | (op_gen['event'] == 'change_description'), 'event']
    op_gen = op_gen.dropna()
    op_gen = op_gen.groupby(['genre', 'event']).size().to_frame().reset_index()
    op_gen['genre'] = op_gen['genre'] + " " + op_gen['event']
    op_gen = op_gen.drop('event', axis=1)
    op_gen = op_gen.rename(columns={'genre': 'genre+op', 0: 'cant'})

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(op_gen['cant'], labels=op_gen['genre+op'],
           autopct='%1.1f%%', colors=COLORS, shadow=True, startangle=90)
    ax.axis('equal')
    ax.set_title("Uso por género")
    return op_gen, fig
