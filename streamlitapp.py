import streamlit as st
import mysql.connector
import pandas as pd
import my_secrets as secrets

st.set_page_config(
    page_title="🌡️ Temperature Analysis",
    page_icon="🌡️",
    layout="wide"
)

conn = mysql.connector.connect(
    host=secrets.host,
    user=secrets.user,
    password=secrets.password,
    database=secrets.database
)
df = pd.read_sql('SELECT * FROM weather_data ORDER BY timestamp desc', conn)
conn.close()

st.title('🌡️ Temperature Analysis - Helsinki')
st.markdown("---")

if not df.empty:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        avg_temp = df['temperature'].mean()
        st.metric(label="📊 Average Temperature", value=f"{avg_temp:.1f}°C")
    
    with col2:
        max_temp = df['temperature'].max()
        st.metric(label="🔥 Highest Temperature", value=f"{max_temp:.1f}°C")
    
    with col3:
        min_temp = df['temperature'].min()
        st.metric(label="❄️ Lowest Temperature", value=f"{min_temp:.1f}°C")
    
    st.markdown("---")
    
    st.subheader("📈 Temperature Trend")
    st.line_chart(df.set_index('timestamp')['temperature'], color='#FF6B6B')
    
    st.subheader("📋 Weather Data Details")
    st.dataframe(df, use_container_width=True)
else:
    st.warning("No weather data available. Please check the data collection.")