# Bibliotecas
import pandas as pd
import plotly.express as px
from haversine import haversine
import streamlit as st
import folium as fl
from streamlit_folium import folium_static
import lib_curry_company as lib

# Import CSV
df_raw = pd.read_csv('data/train.csv')

# Limpa Dataframe
df = lib.clean_code(df_raw)

# =====================================#
#        LAYOUT NO STREAMLIT           #
# =====================================#
st.set_page_config(layout="centered")
lib.define_sidebar( df )

# ======= CORPO DA PÁGINA ========= #

st.header("Marketplace - Visão Entregadores", anchor=None)

with st.container():  
    st.markdown('### Métricas Gerais')

    # Criando duas colunas
    col1, col2, col3, col4 =  st.columns( 4, gap = 'large' )

    with col1:
        # A maior idade dos entregadores
        maior_idade = int(df['Delivery_person_Age'].max())
        st.metric( label='Maior Idade', value = maior_idade, help = 'Idade do entregador mais velho')
    with col2:
        # A menor idade dos entregadores
        menor_idade = int(df['Delivery_person_Age'].min())
        st.metric( label='Menor Idade', value = menor_idade, help = 'Idade do entregador mais novo')
    with col3:
        # A melhor condição de veículos.
        melhor_condicao = df['Vehicle_condition'].max()
        st.metric( label='Melhor Condição', value = melhor_condicao, help = 'Melhor condição dos veículos')
    with col4:
        # A pior condição de veículos.
        pior_condicao = df['Vehicle_condition'].min()
        st.metric( label='Pior Condição', value = pior_condicao, help = 'Pior condição dos veículos')

st.markdown("""___""")

with st.container():
    st.markdown('### Avaliações')
    col1, col2 =  st.columns( 2, gap = 'large' )

    with col1:
        # A avaliação média por entregador.
        st.markdown('###### Avaliação Média Por Entregador')
        df_aux = df.loc[:,['Delivery_person_ID','Delivery_person_Ratings']].groupby('Delivery_person_ID').mean().sort_values('Delivery_person_Ratings', ascending=False).reset_index()
        media_entregador = df_aux.rename( columns = {'Delivery_person_ID' : 'ID', 'Delivery_person_Ratings' : 'Avaliação Média'})
        st.dataframe(media_entregador, width = 300, height = 485)
        
    with col2:
        with st.container():
            st.markdown('###### Avaliação Média Por Trânsito')
            df_aux = ( df.loc[:,['Road_traffic_density','Delivery_person_Ratings']]
                      .groupby('Road_traffic_density')
                      .agg({'Delivery_person_Ratings': ['mean','std']}))
            df_aux.columns = ['mean','std']
            media_transito = df_aux.reset_index()
            st.dataframe(media_transito)
            
        with st.container():
            st.markdown('###### Avaliação Média Por Clima')
            df_aux = (df.loc[:,['Weatherconditions','Delivery_person_Ratings']]
                      .groupby('Weatherconditions')
                      .agg({'Delivery_person_Ratings': ['mean','median','std','var']}))
            df_aux.columns = ['mean','median','std','var']
            media_transito = df_aux.reset_index()
            st.dataframe(media_transito)
            
st.markdown("""___""")

with st.container(): 
    st.markdown('### Velocidade De Entrega')
    col1, col2 =  st.columns( 2 )

    with col1:
        st.markdown('###### Top 10 Entregadores Mais Rápidos Por Cidade')
        df_aux = (df.loc[:,['City','Delivery_person_ID','Time_taken(min)']]
                  .groupby(['City','Delivery_person_ID'])
                  .mean()
                  .sort_values(['City','Time_taken(min)'],ascending=True)
                  .reset_index())
        df_city1 = df_aux.loc[df_aux['City']=='Metropolitian',:].head(10)
        df_city2 = df_aux.loc[df_aux['City']=='Urban',:].head(10)
        df_city3 = df_aux.loc[df_aux['City']=='Semi-Urban',:].head(10)
        df_city_total = pd.concat([df_city1,df_city2,df_city3]) # método concat() é usado para concatenar dataframes. Recebe uma lista de dataframes como parâmetro
        top_rapidos = df_city_total.reset_index()
        st.dataframe(top_rapidos, width = 350, height = 485)
    with col2:
        st.markdown('###### Top 10 Entregadores Mais Lentos Por Cidade')
        df_aux = (df.loc[:,['City','Delivery_person_ID','Time_taken(min)']]
                  .groupby(['City','Delivery_person_ID'])
                  .mean()
                  .sort_values(['City','Time_taken(min)'],ascending=False)
                  .reset_index())
        df_city1 = df_aux.loc[df_aux['City']=='Metropolitian',:].head(10)
        df_city2 = df_aux.loc[df_aux['City']=='Urban',:].head(10)
        df_city3 = df_aux.loc[df_aux['City']=='Semi-Urban',:].head(10)
        df_city_total = pd.concat([df_city1,df_city2,df_city3]) # método concat() é usado para concatenar dataframes. Recebe uma lista de dataframes como parâmetro
        top_lentos = df_city_total.reset_index()
        st.dataframe(top_lentos, width = 350, height = 485)

    