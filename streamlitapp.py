import streamlit as st
import mysql.connector
import pandas as pd
import altair as alt
import my_secrets as secrets

# Yhteys tietokantaan
conn = mysql.connector.connect(
    host=secrets.host,
    user=secrets.user,
    password=secrets.password,
    database=secrets.database
)

# Hae viimeiset 50 riviä taulukosta weather_data
df = pd.read_sql('SELECT * FROM weather_data ORDER BY timestamp DESC LIMIT 50', conn)
conn.close()

# Streamlit-sisältö
st.title('Säädata Helsingistä')
st.dataframe(df)

# Line chart lämpötilalle
st.line_chart(df.set_index('timestamp')['temperature'])

# Scatter plot (pistegraafi)
scatter_chart = alt.Chart(df).mark_circle(size=60, color='red').encode(
    x='timestamp:T',
    y='temperature:Q',
    tooltip=['timestamp', 'temperature']  # Näyttää tooltipin hoverissa
).interactive()  # Mahdollistaa zoomauksen ja panauksen

st.altair_chart(scatter_chart, use_container_width=True)
