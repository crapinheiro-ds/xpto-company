# Bibliotecas
import pandas as pd
from PIL import Image
import streamlit as st
import plotly.express as px
import folium as fl
from streamlit_folium import folium_static

def clean_code( df_raw ):
    """ Esta função tem a responsabilidade de limpar o Dataframe.
    
        Args:
        df_raw (_type_: Dataframe)->  Dataframe gerado a partir da leitura do arquivo CSV.
        
        Returns:
        _type_: Dataframe -> Dataframe limpo
    """
    # LIMPEZA DOS DADOS
    df_clean = df_raw.copy()
    #
    # Conversao de texto/categoria/strings para numeros inteiros
    col = 'Delivery_person_Age'
    criterio = df_clean[ col ] != 'NaN '
    df_clean[ col ] = df_clean.loc[criterio, col ].astype( int )
    #
    # Conversao de texto/categoria/strings para numeros decimais
    col = 'Delivery_person_Ratings'
    df_clean[ col ] = df_clean[ col ].astype( float )
    #
    # Conversao de texto para data
    col = 'Order_Date'
    df_clean[ col ] = pd.to_datetime( df_clean[ col ], format='%d-%m-%Y' )
    #
    #Retirando os espaços em branco das strings -> método strip()
    df_clean['ID'] = df_clean['ID'].str.strip()
    df_clean['Delivery_person_ID'] = df_clean['Delivery_person_ID'].str.strip()
    df_clean['Road_traffic_density'] = df_clean['Road_traffic_density'].str.strip()
    df_clean['Type_of_order'] = df_clean['Type_of_order'].str.strip()
    df_clean['Type_of_vehicle'] = df_clean['Type_of_vehicle'].str.strip()
    df_clean['City'] = df_clean['City'].str.strip()
    df_clean['Festival'] = df_clean['Festival'].str.strip()

    #RETIRANDO COLUNAS 'NaN '
    criterio = df_clean['Delivery_person_Age'] != 'NaN '
    df_clean = df_clean.loc[criterio, :]

    criterio = df_clean['Weatherconditions'] != 'conditions NaN'
    df_clean = df_clean.loc[criterio,:]

    criterio = df_clean['Road_traffic_density'] != 'NaN'
    df_clean = df_clean.loc[criterio,:]

    criterio = df_clean['Festival'] != 'NaN'
    df_clean = df_clean.loc[criterio,:]

    criterio = df_clean['City'] != 'NaN'
    df_clean = df_clean.loc[criterio,:]
    #
    #Limpando a coluna Time_taken(min) usando LAMBDA
    col = 'Time_taken(min)'
    df_clean[col] = df_clean[col].apply( lambda x: x.split( '(min) ' )[1] )
    df_clean[col] =  df_clean[col].astype( int ) 
    # df['Time_taken(min)'] 

    return df_clean

def define_sidebar( df ):
    """ Esta função tem a responsabilidade de criar a barra lateral das
        páginas geradas pelo Streamlit.
        
        Args:
        df (_type_: Dataframe)->  Dataframe usado para que os filtros fiquem dinâmicos.
    
        Returns: none
    """
    # ver referência do streamlit em 'https://docs.streamlit.io/library/get-started/'
    # ======= SIDEBAR ========= #
    image_path = 'img/logo.png'
    image = Image.open(image_path)
    st.sidebar.image( image, width = 200)
    st.sidebar.markdown('# XPTO COMPANY ')
    st.sidebar.markdown('## Fastest Delivery in Town ')
    st.sidebar.markdown("""___""")

    st.sidebar.markdown("### Selecione uma data limite")
    date_slider = st.sidebar.slider(
        'Até qual valor?',
        value = pd.datetime(2022, 4, 13),
        min_value = pd.datetime(2022, 2, 11),
        max_value = pd.datetime(2022, 4, 13),
        format='DD-MM-YYYY')

    st.sidebar.markdown("""___""")


    traffic_options = st.sidebar.multiselect(
        'Quais as condições do trânsito?',
        ['Low', 'Medium', 'High', 'Jam'],
        default = ['Low', 'Medium', 'High', 'Jam'])

    st.sidebar.markdown("""___""")

    st.sidebar.markdown("### Powered By Cláudio Pinheiro")

    # ======================================#
    #  CONECTANDO MEUS FILTROS AOS GRÁFICOS #
    # ======================================#

    # Filtro do slider
    filtro_data = df['Order_Date'] <= date_slider
    df = df.loc[ filtro_data, :]

    #Filtro do tráfego
    filtro_tipo_grafico = df['Road_traffic_density'].isin( traffic_options )  #verifica se o valor do dataframe está na lista
    df = df.loc[ filtro_tipo_grafico, :]

def order_metric(cols, df):
    """Retorna o gráfico de Média de Pedidos

    Args:
        cols (_type_: lista ) -> lista com as colunas do dataframe que farão parte do gráfico
        df (_type_: Dataframe) -> dataframe utilizado no gráfico

    Returns:
        _type_: plotly.express -> gráfico de barras usado pelo streamlit 
    """
    x_axys = cols[0]
    y_axys = cols[1]
    df = ( df.loc[ :, cols ]
            .groupby([ x_axys ])
            .count()
            .reset_index()
    ) 

    return px.bar(df, x = x_axys, y = y_axys)

def traffic_orders_share( cols, df):
    group = cols[0]
    metric = cols[1]
    df = ( df.loc[ :, cols ]
                .groupby(group)
                .count()
                .reset_index()
    )
    df['entregas_perc'] = df[metric]/df[metric].sum()
    return px.pie( df, values = 'entregas_perc', names = group)

def traffic_orders_by_city( cols, df): 
    group1 = cols[0]
    group2 = cols[1]
    metric = cols[2]
    df = (df.loc[ :, ]
            .groupby([ group1, group2])
            .count()
            .reset_index()
    )
    
    return px.scatter(df, group1, group2, size = metric, color = group1)

def orders_by_week( cols, df):
    # Quantidade de pedidos por Semana
    group = cols[ 0 ]
    metric = cols[ 1 ]
    df[ 'week_number' ] = df [ group ].dt.strftime( '%U' )
    df = ( df.loc[ :, [ metric, 'week_number'] ]
             .groupby( 'week_number' )
             .count()
             .reset_index()
            )
    
    return px.line( df, 'week_number', metric)

def orders_share_by_week( cols, df):
    group = cols[ 0 ]
    metric = cols[ 1 ]
    df_aux1 = ( df.loc[ :, [ metric, 'week_number' ] ]
                    .groupby([ 'week_number' ])
                    .count()
                    .reset_index()
                )
    df_aux2 = ( df.loc[ :, [ group, 'week_number' ]]
                    .groupby([ 'week_number' ])
                    .nunique()
                    .reset_index()
                )

    #JUNTANDO DOIS DATA FRAMES
    df_aux3 = pd.merge(df_aux1,df_aux2,how='inner') #Equivale a um inner join no SQL
    df_aux3[ 'order_by_deliver' ] = df_aux3[ metric ]/df_aux3[ group ]

    return px.line( df_aux3, 'week_number', 'order_by_deliver' )

def country_map( cols, df):
    group1 = cols[ 0 ]
    group2 = cols[ 1 ]
    lat = cols[ 2 ]
    lgt = cols[ 3 ]
    coordenadas = ( df.loc[ :, cols ]
                        .groupby( [ group1, group2 ] )
                        .median()
                        .reset_index()
                    )
    mapa = fl.Map()        
    for index, location_info in coordenadas.iterrows(): 
        fl.Marker( [ location_info[ lat ], 
                location_info[ lgt ]],
                popup=location_info[ [ group1, group2 ] ] ).add_to( mapa )
    folium_static( mapa, width = 700, height = 400)    
    