import streamlit as st
from PIL import Image

st.set_page_config(
    page_title = "Visão Empresa",
    page_icon='img/target.png',
    layout="centered", 
    initial_sidebar_state="auto"
)

image_path = 'img/logo.png'
st.sidebar.image( image_path, width=200)

st.sidebar.markdown('# XPTO COMPANY ')
st.sidebar.markdown('## Fastest Delivery in Town ')
st.sidebar.markdown("""___""")

st.write("# XPTO Company Growth Dashboard")
st.markdown(
    """
    Growth Dashboard foi construído para acompanhar as méticas de crescimento  dos Entregadores e Restaurantes
    ### Como utilizar este dashboard?
    - Visão Empresa:
        - Visão Gerencial: Métricas gerais de comportamento.
        - Visão Tática: Indicadores semanais de crescimento.
        - Visão Geográfica: Insights de geolocalização.  
    - Visão Entregador:
        - Agrupamento dos indicadores semanais de crescimento.
    - Visão Restaurante:
        - Indicadores semanais de crescimento dos restaurantes.
    ### Ask for help
    - Linkedin: crapinheiro.ds
    """
)