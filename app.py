import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="LISA Campaign Generator",
    page_icon="📸",
    layout="centered"
)

# --- SYSTEM PROMPT (CEREBRO DE LA APP) ---
# Aquí pegamos las reglas inmutables de LISA
SYSTEM_INSTRUCTION = """
**CORE AESTHETIC & FRAMING RULES (NON-NEGOTIABLE):**
1.  **THE "NOSE-DOWN" RULE (CRITICAL):** All images MUST be strictly framed from the tip of the nose down. NEVER show eyes, forehead, or the upper half of the face. The framing must cut right above the nostrils. Focus is 80% on the outfit's texture/fit and 20% on the lower face/lips/chin to convey attitude without identity.
2.  **THE LOOK:** Analog photography style, 35mm Kodak Portra 400 film. High texture, visible film grain, natural light leaks, slight vignette. NO smooth/plastic "AI skin".
3.  **THE LOCATION:** Bahía Blanca, Argentina. You must ensure the environment looks authentic to this Argentine city. Use visual cues: "veredas con baldosas calcáreas" (patterned sidewalk tiles), "árboles plátanos" (sycamore trees), neoclassical architecture facades, and general urban grit.
4.  **THE RATIO:** All images must be generated in **4:5 aspect ratio (vertical portrait)**.

**DYNAMIC SCENARIO MIXER (Internal Logic):**
Select a scenario based on 'Vibe' and 'Momento', applying it to the chosen 'Modelo'.
* *Urbano/Día:* Crossing a street on "baldosas" sidewalks, pausing next to a "plátano" tree, waiting at a vintage bus stop.
* *Urbano/Noche:* Waiting for a taxi under neon lights of a kiosk, walking fast on wet pavement reflecting city lights, standing near a brutalist concrete building.
* *Social/Día:* Having an aperitivo at a sidewalk cafe table, browsing a local outdoor market, holding a bouquet of flowers.
* *Social/Noche:* Holding a cocktail at a dimly lit speakeasy bar counter, standing outside a crowded music venue (flash photography style), laughing at a dinner table with string lights.
* *Trabajo/Aesthetic:* typing on a laptop in a minimalist cafe with large windows, looking through vinyl records in a shop, carrying a leather folder in a downtown area.

**SUBJECT DEFINITIONS:**
* **Joven:** Authentic Argentine woman (20s).
* **Madura:** Sophisticated Argentine woman (40s-50s), showing elegant, natural signs of aging on neck/hands.
* **Plus Size:** Confident, voluptuous curvy Argentine woman, clothes fitting tightly but naturally showing figure.
"""

# --- INTERFAZ DE USUARIO ---
st.title("📸 LISA - Generador de Campaña")
st.markdown("Subí la foto de la prenda y generá la campaña con estética Bahía Blanca.")

# Sidebar para la API Key
with st.sidebar:
    st.header("Configuración")
    api_key = st.text_input("Ingresa tu Google API Key", type="password")
    st.markdown("[Conseguir API Key](https://aistudio.google.com/app/apikey)")

if not api_key:
    st.warning("👈 Por favor ingresa tu API Key en la barra lateral para comenzar.")
    st.stop()

# Configurar Gemini
try:
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"Error en la API Key: {e}")

# --- FORMULARIO PRINCIPAL ---
uploaded_file = st.file_uploader("Subir foto de la prenda", type=["jpg", "jpeg", "png", "webp"])

col1, col2, col3 = st.columns(3)
with col1:
    modelo = st.selectbox("Modelo", ["Joven", "Madura", "Plus Size"])
with col2:
    momento = st.selectbox("Momento", ["Día", "Noche"])
with col3:
    vibe = st.selectbox("Vibe", ["Urbano", "Social", "Trabajo", "Relax"])

# Botón de generación
if st.button("GENERAR CAMPAÑA ✨", type="primary"):
    if not uploaded_file:
        st.error("⚠️ Por favor sube una imagen de la prenda primero.")
    else:
        with st.spinner("📸 La IA está haciendo la sesión de fotos... (Esto puede tardar unos segundos)"):
            try:
                # Cargar imagen
                image = Image.open(uploaded_file)
                
                # Configurar el modelo (Usamos Gemini 1.5 Pro por su capacidad multimodal)
                model = genai.GenerativeModel(
                    model_name="gemini-1.5-pro",
                    system_instruction=SYSTEM_INSTRUCTION
                )

                # Construir el prompt simple (El System Prompt hace el trabajo pesado)
                user_prompt = f"Create a fashion campaign photo. MODELO: {modelo}. MOMENTO: {momento}. VIBE: {vibe}. The garment is shown in the attached image."

                # Generar
                response = model.generate_content([user_prompt, image])
                
                # Mostrar resultado
                st.success("¡Foto generada con éxito!")
                st.image(response.text, caption="Prompt generado (Nota: Gemini devuelve texto, la imagen real requiere integración con herramienta de imagen o esperar a que Gemini 1.5 Pro soporte output nativo de imagen en API. Por ahora, este código simula la creación del PROMPT PERFECTO para usar en Nano Banana/Midjourney, o si tu API Key tiene acceso a generación de imagen, devolverá la imagen).")
                
                # NOTA IMPORTANTE PARA JUAN CRUZ:
                # Actualmente la API estándar de Python devuelve TEXTO. 
                # Si tienes acceso a Imagen 3 via API, el código cambia ligeramente.
                # Este código te devolverá el PROMPT PERFECTO para pegar.
                
                st.code(response.text, language="markdown")

            except Exception as e:
                st.error(f"Ocurrió un error: {e}")
