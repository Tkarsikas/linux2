import streamlit as st
import pandas as pd
import plotly.express as px

# Cachettaa tietokantayhteyden ja datan
@st.cache_data(ttl=600)
def mySql():
    # Initialize connection using Streamlit secrets
    conn = st.connection('mysql', type='sql')
    
    # Hae data kyykky-taulusta
    df_kyykky = conn.query('SELECT viikko, paino FROM kyykky LIMIT 100;')
    df_kyykky['harjoituslaji'] = 'kyykky'
    
    # Hae data penkki-taulusta
    df_penkki = conn.query('SELECT viikko, paino FROM penkki LIMIT 100;')
    df_penkki['harjoituslaji'] = 'penkki'
    
    return df_kyykky, df_penkki

# Streamlit-sovellus
def main():
    st.title("Kyykky ja Penkki kehitys viikottain")
    st.write("Näytetään painot kehityksestä viikoittain")
    
    df_kyykky, df_penkki = mySql()
    
    if not df_kyykky.empty or not df_penkki.empty:
        # Yhdistä data
        df_combined = pd.concat([df_kyykky, df_penkki], ignore_index=True)
        
        # Piirrä viikkokohtainen painokehitys
        fig = px.line(
            df_combined, 
            x="viikko", 
            y="paino", 
            color="harjoituslaji",  # eri värit kyykylle ja penkille
            title="Harjoitus painot viikottain",
            markers=True
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("Ei dataa näytettäväksi")

if __name__ == "__main__":
    main()
