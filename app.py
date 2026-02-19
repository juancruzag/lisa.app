import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="LISA Campaign", page_icon="📸")

# --- SECRETOS & CONFIGURACIÓN ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("⚠️ Falta la API Key en los Secrets de Streamlit.")
    st.stop()

# --- INTERFAZ ---
st.title("📸 LISA - Generador de Campaña")
st.markdown("Generá la campaña con estética Bahía Blanca.")

uploaded_file = st.file_uploader("Subir foto de la prenda", type=["jpg", "png", "webp"])

col1, col2, col3 = st.columns(3)
with col1: modelo = st.selectbox("Modelo", ["Joven", "Madura", "Plus Size"])
with col2: momento = st.selectbox("Momento", ["Día", "Noche"])
with col3: vibe = st.selectbox("Vibe", ["Urbano", "Social", "Trabajo", "Relax"])

# --- CEREBRO DE LA APP ---
if st.button("GENERAR CAMPAÑA ✨", type="primary"):
    if not uploaded_file:
        st.warning("Subí una foto primero.")
    else:
        with st.spinner("1. Analizando prenda y creando Prompt..."):
            try:
                # PASO 1: CREAR EL PROMPT CON GEMINI FLASH
                image_input = Image.open(uploaded_file)
                
                # Reglas de estilo (Prompt Engineer)
                system_prompt = """
                You are a Fashion Art Director. Your task is to write a PRECISE IMAGE GENERATION PROMPT for 'Imagen 3'.
                Based on the user's garment image and parameters, write a prompt following these rules:
                1. FRAMING: Strict close-up from nose down. No eyes visible.
                2. LOCATION: Bahía Blanca, Argentina (sidewalk tiles, sycamore trees).
                3. AESTHETIC: 35mm Kodak Portra 400, film grain.
                4. MODEL: Describe the model based on the selection (Joven/Madura/Plus Size).
                5. OUTFIT: Describe the uploaded garment in extreme detail based on the image provided.
                OUTPUT ONLY THE ENGLISH PROMPT TEXT. NO INTRO.
                """
                
                request = f"Create a prompt for a {modelo} woman, at {momento}, vibe {vibe}."
                
                flash_model = genai.GenerativeModel('gemini-2.5-flash')
                response = flash_model.generate_content([system_prompt, request, image_input])
                final_prompt = response.text

                st.success("¡Prompt Creado!")
                with st.expander("Ver Prompt generado (Inglés)"):
                    st.code(final_prompt)

            except Exception as e:
                st.error(f"Error en paso 1: {e}")
                st.stop()

        with st.spinner("2. Revelando fotografía (Esto puede tardar)..."):
            try:
                # PASO 2: GENERAR LA IMAGEN REAL (INTENTO CON IMAGEN 3)
                imagen_model = genai.GenerativeModel("imagen-3.0-generate-001")
                result = imagen_model.generate_images(
                    prompt=final_prompt,
                    number_of_images=1,
                    aspect_ratio="4:5",
                    safety_filter_level="block_only_high"
                )
                
                # Mostrar la imagen
                st.image(result.images[0].image, caption="Campaña LISA Generada")
                
            except Exception as e:
                st.warning("⚠️ Tu API Key aún no tiene acceso al modelo de IMAGEN. Pero el Prompt de arriba funciona perfecto.")
                st.error(f"Detalle del error de imagen: {e}")
                st.info("💡 SOLUCIÓN TEMPORAL: Copia el texto del cuadro gris de arriba y pégalo en Midjourney o Firefly.")
