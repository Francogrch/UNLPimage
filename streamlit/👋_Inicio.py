import streamlit as st
import os
from scripts.script import *

_main_folder = os.path.dirname(os.path.abspath('__main__'))[:-10]
with open(os.path.join(_main_folder, 'README.md'), 'r', encoding="utf-8") as file:
    readme = file.read()

st.set_page_config(layout="wide")
css_style()
logo()
title_md('Inicio 👋', 50)
bar('#e3b04b', 3, 95)
title_md('Seminario de lenguaje: Python',50)
bar()

st.write(readme)
# Información adicional
bar()
st.info("UNLP Informatica-Seminario Python ©")