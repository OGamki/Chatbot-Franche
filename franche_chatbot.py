import streamlit as st
from woocommerce import API
import time
import random

# ---------------------------------------------------------
# 1. CONFIGURACIÓN DE LA PÁGINA
# ---------------------------------------------------------
st.set_page_config(page_title="Franche Travel Bot", page_icon="✈️")

# ---------------------------------------------------------
# 2. CONEXIÓN A WOOCOMMERCE (TU TIENDA)
# ---------------------------------------------------------
def conectar_woocommerce():
    return API(
        url="https://viajoconfranche.com",
        consumer_key="ck_TU_CLAVE_AQUI",      # <--- ¡PEGA TU CLAVE DE CLIENTE AQUÍ!
        consumer_secret="cs_TU_SECRETO_AQUI", # <--- ¡PEGA TU CLAVE SECRETA AQUÍ!
        version="wc/v3",
        timeout=20
    )

def obtener_tours_reales():
    """Consulta la tienda y trae los productos formateados"""
    try:
        wcapi = conectar_woocommerce()
        # Traemos 10 productos publicados
        response = wcapi.get("products", params={"per_page": 10, "status": "publish"})
        
        if response.status_code == 200:
            productos = response.json()
            
            if not productos:
                return "⚠️ No encontré tours publicados en la tienda en este momento."

            mensaje = "🎒 **Estos son nuestros Tours disponibles ahora mismo:**\n\n"
            for p in productos:
                nombre = p['name']
                # Formatear precio si existe
                precio = f"S/ {p['price']}" if p['price'] else "Consultar precio"
                link = p['permalink']
                
                # Diseño de la tarjeta del producto
                mensaje += f"🌟 **{nombre}**\n💰 {precio}\n🔗 [Ver detalles y reservar]({link})\n"
                mensaje += "---\n"
            
            return mensaje
        else:
            return "❌ Error de conexión con la tienda. Por favor verifica las claves API."
            
    except Exception as e:
        return f"❌ Error técnico al buscar tours: {str(e)}"

# ---------------------------------------------------------
# 3. CEREBRO DEL BOT (TODAS TUS RESPUESTAS)
# ---------------------------------------------------------
def generar_respuesta(mensaje):
    msg = mensaje.lower().strip()

    # --- OPCIÓN 1: PASAJES Y HOTELES ---
    if any(x in msg for x in ["1", "pasaje", "vuelo", "boleto", "hotel", "reserva"]):
        return ("✈️ **Reserva de Pasajes y Hoteles**\n\n"
                "¡Genial! Para estas reservas necesitamos atención personalizada.\n"
                "Por favor escribe a nuestro WhatsApp oficial para que un asesor te atienda:\n"
                "👉 [Clic aquí para chatear con un asesor](https://wa.me/51999999999)")

    # --- OPCIÓN 2 y 5: TOURS Y PROMOCIONES (Conexión WooCommerce) ---
    if any(x in msg for x in ["2", "5", "tour", "full day", "viaje", "promocion", "oferta"]):
        return obtener_tours_reales()

    # --- OPCIÓN 3: ASESOR ---
    if any(x in msg for x in ["3", "asesor", "humano", "persona", "ayuda humana"]):
        return ("💬 **Conectando con un asesor...**\n\n"
                "Nuestros expertos están listos para ayudarte en WhatsApp para una atención más rápida:\n"
                "👉 [Hablar con Asesor en WhatsApp](https://wa.me/51999999999)")

    # --- OPCIÓN 4: REDES SOCIALES ---
    if any(x in msg for x in ["4", "redes", "facebook", "instagram", "tiktok", "social"]):
        return ("🌐 **Síguenos en nuestras redes sociales:**\n\n"
                "📘 [Facebook](https://www.facebook.com/people/Franche-Travel/61569291782697/)\n"
                "📸 [Instagram](https://www.instagram.com/franche.travel)\n"
                "🎵 [TikTok](https://www.tiktok.com/@viajaconfranche)\n"
                "💻 [Página Web](https://viajoconfranche.com)")

    # --- OPCIÓN 6: UBICACIÓN Y HORARIO ---
    if any(x in msg for x in ["6", "ubicacion", "donde estan", "direccion", "horario", "hora", "donde queda"]):
        return ("📍 **Dirección:**\n"
                "Av Los Héroes 120 | PLATAFORMA N°2 TIENDA #123\n"
                "URB. ENTEL, San Juan De Miraflores, Lima.\n\n"
                "🕒 **Horario de atención:**\n"
                "10:00 AM - 6:00 PM (Lunes a Domingo)\n\n"
                "📌 [Ver en Google Maps](https://goo.gl/maps/TU_ENLACE_AQUI)")

    # --- PAQUETE INTERNACIONAL (De tu código original) ---
    if "paquete internacional" in msg:
        return ("📦 **El Paquete Internacional incluye:**\n"
                "* Pasaje Aéreo ✈️\n"
                "* Reserva de hospedaje 🏨\n"
                "* Seguro de viaje 🛡️\n"
                "* Reserva de Tours 🎒\n\n"
                "Si deseas cotizar uno, escribe **'3'** para hablar con un asesor.")

    # --- EMPATÍA: ESTADO DE ÁNIMO ---
    if any(x in msg for x in ["triste", "mal", "estresado", "cansado", "depre", "preocupado"]):
        return ("😔 Siento que estés pasando por eso. Aquí te dejo algunos consejos:\n"
                "- Haz pausas conscientes: respira profundo o camina un rato.\n"
                "- Habla con alguien de confianza: compartir cómo te sientes ayuda.\n"
                "Si necesitas distraerte, ¿qué tal si planeamos un viaje corto para despejar la mente? 🌍")
    
    if any(x in msg for x in ["feliz", "bien", "genial", "contento", "excelente"]):
        return ("😄 ¡Qué alegría saber que estás bien!\n"
                "Esa energía es perfecta para viajar. ¿Te gustaría ver nuestros tours? Escribe **'2'**.")

    # --- AGRADECIMIENTOS ---
    if any(x in msg for x in ["gracias", "te pasaste", "ok", "listo", "vale", "chevere"]):
        return "😊 ¡De nada! Estoy aquí para ayudarte en lo que necesites."

    # --- SALUDOS GENERALES ---
    if any(x in msg for x in ["hola", "buenos dias", "buenas", "que tal", "hi", "holi"]):
        return "👋 ¡Hola! Bienvenido a Franche Travel. ¿En qué puedo ayudarte hoy?\nEscribe **'menu'** para ver las opciones."

    # --- MENÚ DE AYUDA (Opción por defecto) ---
    return """🤖 **MENÚ PRINCIPAL**
    
    1️⃣ Reservar pasajes o hoteles ✈️🏨
    2️⃣ Ver tours y full days (Tienda) 🎒
    3️⃣ Hablar con un asesor 💬
    4️⃣ Redes sociales 🌐
    5️⃣ Ver promociones 🎁
    6️⃣ Dirección y horario 📍
    
    👇 Escribe el número de la opción o tu pregunta:"""

# ---------------------------------------------------------
# 4. INTERFAZ DE USUARIO (STREAMLIT)
# ---------------------------------------------------------

# Barra lateral
with st.sidebar:
    try:
        st.image("Logo-empresa.jpg", width=150)
    except:
        st.header("✈️ Franche Travel")
    st.write("**Tu agencia de confianza.**")
    if st.button("🗑️ Borrar conversación"):
        st.session_state.messages = []
        st.rerun()

st.title("Asistente Virtual - Franche Travel")

# Inicializar historial
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant",
        "content": "¡Hola! 🤖 Soy el bot de Franche Travel.\nEscribe **'menu'** para ver las opciones o dime qué necesitas."
    })

# Mostrar chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Capturar entrada
if prompt := st.chat_input("Escribe aquí..."):
    # 1. Mostrar usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Pensar y Responder
    with st.spinner("Consultando..."):
        time.sleep(0.5) # Simular naturalidad
        respuesta_bot = generar_respuesta(prompt)

    # 3. Mostrar bot
    st.session_state.messages.append({"role": "assistant", "content": respuesta_bot})
    with st.chat_message("assistant"):
        st.markdown(respuesta_bot)