import streamlit as st
import pandas as pd
import plotly.express as px
@st.cache_resource
def mySql():
    # Initialize connection.
    conn = st.connection('mysql', type='sql')
    # Perform query.
    df_kyykky = conn.query('SELECT viikko, nimi, toistot, paino from kyykky LIMIT 100;', ttl=600)
    df_penkki = conn.query('SELECT viikko, nimi, toistot, paino from penkki LIMIT 100;', ttl=600)
    df_kyykky['harjoituslaji'] = 'kyykky'
    df_penkki['harjoituslaji'] = 'penkki'
    
    return df_kyykky, df_penkki
    # Streamlit
def main():
    st.title("dataa mysql tietokannasta")
    st.write("kyykky ja penkki kehitys viikottain")
    df_kyykky, df_penkki = mySql()
    #plot data
    if not df_kyykky.empty or not df_penkki.empty:
        df_combined = pd.concat([df_kyykky, df_penkki], ignore_index=True)
        fig = px.line(df_combined, x="viikko", y="paino", color="nimi",
                      line_dash="harjoituslaji",
                      title='harjoitus painot viikottain', markers=True)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("Ei dataa näytettäväksi")
if __name__ == "__main__":
    main()