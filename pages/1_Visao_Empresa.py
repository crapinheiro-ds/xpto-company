# Bibliotecas
import sys
sys.path.append('lib')
import lib_curry_company as lib
import pandas as pd
import streamlit as st


# ========== INICIO ============= #
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
st.header("Marketplace - Customer's Vision", anchor=None)

tab1, tab2, tab3 = st.tabs(['Visão Gerencial', 'Visão Tática', 'Visão Geográfica'])

with tab1:
    with st.container():
        # Order Metric
        st.markdown('### Pedidos Por Dia')
        cols = ['Order_Date', 'ID']
        fig = lib.order_metric( cols, df)
        st.plotly_chart( fig, use_container_width = True)
        
    with st.container():
        # Criando duas colunas
        col1, col2 =  st.columns( 2 )

        with col1:
            # Distribuição dos pedidos por tipo de tráfego
            st.markdown('### Distribuição dos pedidos por tipo de tráfego')
            cols = [ 'Road_traffic_density', 'ID' ] 
            fig = lib.traffic_orders_share( cols, df )
            st.plotly_chart( fig, use_container_width = True )
            
        with col2:
            # Comparação do volume de pedidos por cidade e tipo de tráfego.
            st.markdown('### Volume de pedidos por cidade e tipo de tráfego')
            cols = [ 'City', 'Road_traffic_density', 'ID' ]
            fig = lib.traffic_orders_by_city( cols, df)
            st.plotly_chart( fig, use_container_width = True)
            
with tab2:
    with st.container():
        st.markdown("# Orders By Week")
        cols = [ 'Order_Date', 'ID' ]
        fig = lib.orders_by_week(cols, df)
        st.plotly_chart( fig, use_container_width = True)
        
    with st.container():
        # Quantidade de pedidos por entregador por semana
        st.markdown("# Orders Share By Week")
        cols = [ 'Delivery_person_ID', 'ID' ]
        fig = lib.orders_share_by_week(cols, df)
        st.plotly_chart( fig, use_container_width = True)
    
with tab3:
    st.markdown("# Country Map")
    cols = [ 'City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude' ]
    lib.country_map( cols, df)
    

    
    
