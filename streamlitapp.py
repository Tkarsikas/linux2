import streamlit as st
import mysql.connector, secrets
import pandas as pd
conn = mysql.connector.connect(host=secrets.host, user=secrets.user,
password=secrets.password, database=secrets.database)
df = pd.read_sql('SELECT * FROM weather_data ORDER BY timestamp DESC LIMIT 50',
conn)
conn.close()
st.title('Säädata Helsingistä')
st.dataframe(df)
st.line_chart(df.set_index('timestamp')['temperature'])