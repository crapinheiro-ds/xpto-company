# Bibliotecas
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from haversine import haversine
import streamlit as st
import folium as fl
from streamlit_folium import folium_static
import lib_curry_company as lib
import numpy as np

# Import CSV
df_raw = pd.read_csv('data/train.csv')

# Limpa Dataframe
df = lib.clean_code(df_raw)

# =====================================#
#        LAYOUT NO STREAMLIT           #
# =====================================#
st.set_page_config(layout="wide")
lib.define_sidebar( df )

# ======= CORPO DA PÁGINA ========= #
st.header("Marketplace - Visão Restaurantes", anchor=None)

with st.container():
    col1, col2, col3, col4, col5, col6 =  st.columns( 6 )
    
    with col1:
        # Entregadores únicos
        entregadores_unicos = df['Delivery_person_ID'].nunique()
        col1.metric( label='Nº Entregadores', value = entregadores_unicos, help = 'Quantidade de entregadores únicos')
    with col2:
        # Distância média
        cols = ['Restaurant_latitude','Restaurant_longitude', 'Delivery_location_latitude','Delivery_location_longitude']
        df['distancia'] = df.loc[:,cols].apply( lambda x: haversine( (x['Restaurant_latitude'], x['Restaurant_longitude']),(x['Delivery_location_latitude'], x['Delivery_location_latitude'])), axis=1 )
        distancia_media = np.round( df.loc[ :,[ 'distancia' ]].mean()/1000, 2)
        col2.metric( label = 'Distância Média', value = distancia_media, help = 'Distância média entre restaurantes e locais de entrega')
    with col3:
        # Tempo de entrega médio com festival
        filtro = df['Festival'] == 'Yes'
        avarage_time_festival = df.loc[filtro,['Festival','Time_taken(min)']].groupby(['Festival']).mean().reset_index()
        avarage_time_festival = np.round( avarage_time_festival['Time_taken(min)'], 2)
        col3.metric( label = 'Tempo Médio Com Festival', value = avarage_time_festival, help = 'Tempo de entrega médio com festival')
        
    with col4:
        # Desvio padrao de Tempo de entrega médio com festival
        filtro = df['Festival'] == 'Yes'
        avarage_time_festival = df.loc[filtro,['Festival','Time_taken(min)']].groupby(['Festival']).std().reset_index()
        avarage_time_festival = np.round( avarage_time_festival['Time_taken(min)'], 2)
        col4.metric( label = 'Desv.Pardão Com Festival', value = avarage_time_festival, help = 'Desvio Padrão de tempo de entrega médio com festival')
    with col5:
        # Tempo de entrega médio sem festival
        filtro = df['Festival'] == 'No'
        avarage_time_festival = df.loc[filtro,['Festival','Time_taken(min)']].groupby(['Festival']).mean().reset_index()
        avarage_time_festival = np.round( avarage_time_festival['Time_taken(min)'], 2)
        col5.metric( label = 'Tempo Médio Sem Festival', value = avarage_time_festival, help = 'Tempo de entrega médio sem festival')
    with col6:
        # Desvio padrao de Tempo de entrega médio sem festival
        filtro = df['Festival'] == 'No'
        avarage_time_festival = df.loc[filtro,['Festival','Time_taken(min)']].groupby(['Festival']).std().reset_index()
        avarage_time_festival = np.round( avarage_time_festival['Time_taken(min)'], 2)
        col6.metric( label = 'Desv.Pardão Sem Festival', value = avarage_time_festival, help = 'Desvio Padrão de tempo de entrega médio sem festival')

st.markdown("""___""")

with st.container():
    
    col1,col2 = st.columns([1.5,1])  
            
    with col1:
        # O tempo médio e o desvio padrão de entrega por cidade.
        st.markdown("##### Distribuição do Tempo")
        cols = [ 'Time_taken(min)', 'City' ]
        df_aux = (df.loc[ :, cols]
                    .groupby( 'City' )
                    .agg( { 'Time_taken(min)' : [ 'mean', 'std' ] } ))
        df_aux.columns = ['Avg_Time','Std_Time']
        df_aux = df_aux.reset_index()
        fig = go.Figure()
        fig.add_trace( go.Bar( name = 'Control', 
                                x = df_aux['City'], 
                                y = df_aux['Avg_Time'], 
                                error_y = dict( 
                                        type = 'data', 
                                        array=df_aux['Std_Time'])))
        st.plotly_chart( fig )
    with col2:
        st.markdown('##### Tempo Médio Por Tipo de Entrega')
        st.markdown(' ')
        df_aux = ( df.loc[ :, ['Time_taken(min)', 'City', 'Type_of_order']]
                .groupby([ 'City', 'Type_of_order' ])
                .agg({ 'Time_taken(min)': [ 'mean', 'std' ]})
                )
        df_aux.columns = [ 'mean','std' ]
        df_aux = df_aux.reset_index()
        st.dataframe(df_aux)
        
st.markdown("""___""")

with st.container():
    col1, col2 =  st.columns( [1.5,2] )
    with col1:
        #distribuição da distancia média por cidade
        st.markdown('##### Tempo de Entrega Médio Por Cidade')
        cols = ['Delivery_location_latitude','Delivery_location_longitude','Restaurant_latitude','Restaurant_longitude']
        df['distancia'] = (df.loc[:, cols]
                        .apply( lambda x: haversine( 
                            (x['Restaurant_latitude'], x['Restaurant_longitude']),
                            (x['Delivery_location_latitude'], x['Delivery_location_latitude'])), 
                                axis=1 ))
        avg_distance = (df.loc[:, ['City','distancia']].
                        groupby('City').
                        mean().
                        reset_index())
        fig = go.Figure( data = [go.Pie( labels=avg_distance['City'], 
                                        values = avg_distance['distancia'], 
                                        pull = [0, 0.1, 0])])
        st.plotly_chart( fig, use_container_width = True)
    
    with col2:
        # Tempo médio por tipo de entrega
        st.markdown('##### Distribuição de Tempo Por Cidade e Tipo de Tráfego')
        df_aux = ( df.loc[ :, ['Time_taken(min)','City','Road_traffic_density']]
                    .groupby( ['City', 'Road_traffic_density'])
                    .agg( {'Time_taken(min)' : ['mean','std']})
                )
        df_aux.columns = ['Avg_time','Std_time']
        df_aux = df_aux.reset_index()
        fig = ( px.sunburst( df_aux, path = ['City', 'Road_traffic_density'],
                                     values = 'Avg_time',
                                     color = 'Std_time',
                                     color_continuous_scale = 'RdBu',
                                     color_continuous_midpoint = np.average(df_aux[ 'Std_time' ])
                            )
        )
        st.plotly_chart( fig )
        


       
