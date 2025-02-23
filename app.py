import streamlit as st
import pandas as pd

st.title("❤️ MON HÔPITAL DES CŒURS - V2.0")
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSLyU2aDLFF7PnIFz3AdziYzPN5rYw3dFo2zia9jhltzcqOWnUBigMN4-oixb3vihzSSoNDQWtxc9R7/pub?gid=0&single=true&output=csv"

try:
    # Chargement des données avec cache pour meilleures performances
    @st.cache_data(ttl=60)  # Actualisation toutes les 60 secondes
    def load_data():
        return pd.read_csv(url)
    
    data = load_data()
    
    if not data.empty:
        # Interface temps réel
        st.subheader("🫀 Surveillance Cardiaque Live")
        st.metric("Dernier relevé", f"{data.iloc[-1, 0]} bpm")
        st.line_chart(data, color="#FF0000", use_container_width=True)
        
        # Système d'alerte intelligent
        st.subheader("🚨 Algorithme de Détection")
        seuil = st.slider("Seuil de tachycardie (bpm)", 70, 200, 100, 
                         help="Valeur médicale recommandée : 100 bpm au repos")
        
        valeurs_dangereuses = data[data.iloc[:, 0] > seuil]
        
        if valeurs_dangereuses.any():
            st.error(f"ALERTE : {valeurs_dangereuses.sum()} pics dangereux détectés!")
            st.write("Relevés critiques :", data[valeurs_dangereuses])
            st.audio("https://soundbible.com/mp3/Emergency_Alert-SoundBible.com-1830219066.mp3")  # Son d'alerte
        else:
            st.success("Rythme cardiaque normal ✅")
            
        # Prévention santé
        st.info(f"💡 Conseil médical : Maintenez votre rythme sous {seuil} bpm (hydration, respiration lente)")
            
    else:
        st.warning("📭 Aucune donnée reçue - Vérifiez la connexion au Google Sheets")

except Exception as e:
    st.error("⚠️ Crise technique - Contacter le support")
    st.code(f"ERREUR : {str(e)}", language="bash")
