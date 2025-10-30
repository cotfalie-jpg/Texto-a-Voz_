import streamlit as st
import os
import time
import glob
from gtts import gTTS
from PIL import Image
import base64

# ===== CONFIGURACIÓN GENERAL =====
st.set_page_config(page_title="BAE | Cuento del Osito", page_icon="🧸", layout="centered")

# ===== COLORES E IDENTIDAD VISUAL BAE =====
COLOR_PRIMARIO = "#DD8E6B"   # Melocotón
COLOR_SECUNDARIO = "#FFF8EA" # Fondo cálido
COLOR_ACENTO = "#FFF2C3"     # Amarillo pastel
COLOR_SUAVE = "#C6E2E3"      # Azul agua

# ===== ESTILO CSS =====
st.markdown(f"""
    <style>
        body {{
            background-color: {COLOR_SECUNDARIO};
            color: #3C3C3C;
            font-family: 'Poppins', sans-serif;
        }}
        h1, h2, h3 {{
            color: {COLOR_PRIMARIO};
            font-weight: 700;
        }}
        .stApp {{
            background-color: {COLOR_SECUNDARIO};
        }}
        .stButton>button {{
            background-color: {COLOR_SUAVE};
            color: #3C3C3C;
            border: none;
            border-radius: 10px;
            font-weight: 600;
            padding: 0.5em 1em;
            transition: all 0.3s ease;
        }}
        .stButton>button:hover {{
            background-color: {COLOR_PRIMARIO};
            color: white;
            transform: scale(1.03);
        }}
        textarea, input {{
            border-radius: 10px !important;
            border: 1px solid {COLOR_PRIMARIO}30 !important;
            background-color: #FFFFFF !important;
        }}
        section[data-testid="stSidebar"] {{
            background-color: {COLOR_ACENTO};
            border-right: 2px solid {COLOR_PRIMARIO}20;
        }}
    </style>
""", unsafe_allow_html=True)

# ===== ENCABEZADO PRINCIPAL =====
st.title("🧸 Nube, el osito que quería abrazar el cielo")

try:
    image = Image.open('osito_bae.png')
    st.image(image, width=350)
except:
    st.image("https://via.placeholder.com/350x250.png?text=Osito+Nube", width=350)

# ===== CUENTO =====
cuento = """
En un bosque suave como el algodón vivía Nube, un osito de pelaje blanco que soñaba con tocar el cielo.  
Cada mañana miraba las nubes y pensaba: “Si tan solo pudiera abrazarlas, ¡seguro serían tan suaves como yo!” ☁️  

Un día, decidió construir una torre de hojas, flores y ramitas para alcanzarlas.  
Trepa que trepa, llegó tan alto que el viento empezó a jugar con sus orejas.  
Pero justo cuando iba a tocar una nube, esta se deshizo en una lluvia suave que lo hizo reír. 🌧️  

Mojadito y feliz, Nube entendió que no hacía falta alcanzar el cielo para sentirse cerca de él.  
Solo bastaba mirar arriba y sonreír, sabiendo que las nubes también lo miraban desde allá. 🌈  
"""

st.subheader("📖 Escucha la historia")
st.write(cuento)

# ===== SIDEBAR =====
with st.sidebar:
    st.subheader("🎧 Convierte tu cuento en audio")
    st.write("Convierte el texto del osito Nube en un cuento narrado con voz suave.")
    st.write("Ideal para antes de dormir o para calmar a tu bebé. 🌙")

# ===== FUNCIÓN DE AUDIO =====
try:
    os.mkdir("temp")
except:
    pass

st.subheader("💬 Convierte tu texto en audio")
text = st.text_area("🍼 Escribe o pega el texto que quieres escuchar:", cuento)

option_lang = st.selectbox("🌎 Selecciona el idioma", ("Español", "English"))
lg = "es" if option_lang == "Español" else "en"

def text_to_speech(text, lg):
    tts = gTTS(text, lang=lg)
    my_file_name = text[:20] if len(text) > 0 else "audio"
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name

if st.button("🎵 Convertir a Audio"):
    if text.strip():
        result = text_to_speech(text, lg)
        audio_file = open(f"temp/{result}.mp3", "rb")
        audio_bytes = audio_file.read()
        st.markdown("### 💖 Tu historia lista para escuchar:")
        st.audio(audio_bytes, format="audio/mp3", start_time=0)

        # Descargar archivo
        with open(f"temp/{result}.mp3", "rb") as f:
            data = f.read()

        def get_download_link(bin_data, filename="cuento_osito.mp3", label="📥 Descargar cuento"):
            bin_str = base64.b64encode(bin_data).decode()
            href = f'<a href="data:audio/mp3;base64,{bin_str}" download="{filename}" style="color:{COLOR_PRIMARIO};text-decoration:none;font-weight:600;">{label}</a>'
            return href

        st.markdown(get_download_link(data), unsafe_allow_html=True)
    else:
        st.warning("Por favor escribe o pega un texto antes de convertirlo a audio.")

# ===== LIMPIEZA DE ARCHIVOS TEMPORALES =====
def remove_files(n):
    mp3_files = glob.glob("temp/*.mp3")
    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)

remove_files(7)
