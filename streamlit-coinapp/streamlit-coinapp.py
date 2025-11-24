import streamlit as st
import mysql.connector
import pandas as pd
import my_secrets as secrets

st.set_page_config(
    page_title="💰 Coin Analysis",
    page_icon="💰",
    layout="wide"
)

conn = mysql.connector.connect(
    host=secrets.host,
    user=secrets.user,
    password=secrets.password,
    database=secrets.database
)
df = pd.read_sql('SELECT * FROM ethereum_data ORDER BY timestamp desc', conn)
conn.close()

st.title('💰 Ethereum (ETH) Price Analysis')
st.markdown("---")

if not df.empty:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        current_price = df['price'].iloc[0]
        st.metric(label="💵 Current Price", value=f"€{current_price:.2f}")
    
    with col2:
        avg_price = df['price'].mean()
        st.metric(label="📊 Average Price", value=f"€{avg_price:.2f}")
    
    with col3:
        max_price = df['price'].max()
        st.metric(label="📈 Highest Price", value=f"€{max_price:.2f}")
    
    st.markdown("---")
    
    st.subheader("📊 Price Trend (EUR)")
    st.line_chart(df.set_index('timestamp')['price'], color='#FFB700')
    
    st.subheader("💎 Price History")
    st.dataframe(df, use_container_width=True)
else:
    st.warning("No Ethereum price data available. Please check the data collection.")