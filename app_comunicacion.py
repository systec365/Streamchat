import streamlit as st
import datetime

# Configuración de la interfaz en modo ancho y título de pestaña
st.set_page_config(page_title="Hub de Comunicación Global", layout="wide")

# Servidor de datos compartido en memoria para usuarios externos
@st.cache_resource
def obtener_memoria_chat():
    return []

historial_global = obtener_memoria_chat()

st.title("🌐 Centro de Comunicación Digital")
st.markdown("Plataforma integrada de mensajería instantánea y videoconferencia remota multiusuario.")
st.write("---")

# Crear la distribución de la pantalla (40% Chat, 60% Panel de Videoconferencia)
col_chat, col_video = st.columns([1, 1.5])

# ==========================================
# 1. PANEL DE CHAT GLOBAL (COLUMNA IZQUIERDA)
# ==========================================
with col_chat:
    st.subheader("💬 Sala de Mensajes en Vivo")
    
    usuario = st.text_input("Introduce tu nombre o alias:", value="Usuario_1", key="alias_usuario")
    
    # Botón manual para actualizar nuevos mensajes de otros usuarios
    if st.button("🔄 Actualizar Chat"):
        st.rerun()
        
    contenedor_mensajes = st.container(height=400)
    
    with contenedor_mensajes:
        if not historial_global:
            st.info("La sala está vacía. ¡Escribe el primer mensaje!")
        else:
            for msg in historial_global:
                hora_actual = msg["hora"]
                if msg["remitente"] == usuario:
                    st.markdown(f"**[Tú]** <span style='color:#00e676;'>({hora_actual}):</span> {msg['texto']}", unsafe_allow_html=True)
                else:
                    st.markdown(f"**[{msg['remitente']}]** <span style='color:#80d8ff;'>({hora_actual}):</span> {msg['texto']}", unsafe_allow_html=True)
                st.write("") 

    with st.form("formulario_envio", clear_on_submit=True):
        nuevo_mensaje = st.text_input("Escribe tu mensaje aquí...", placeholder="Hola a todos...")
        boton_enviar = st.form_submit_button("Enviar Mensaje")
        
        if boton_enviar and nuevo_mensaje.strip() != "":
            ahora = datetime.datetime.now().strftime("%H:%M")
            historial_global.append({
                "remitente": usuario,
                "texto": nuevo_mensaje,
                "hora": ahora
            })
            st.rerun()

# ==========================================
# 2. PANEL DE VIDEO GLOBAL (COLUMNA DERECHA)
# ==========================================
with col_video:
    st.subheader("🎥 Sala de Videoconferencia HD (Hasta 4 personas)")
    
    ID_SALA_EQUIPO = "SalaComunComunicacionesPrivada777"
    URL_SALA_JITSI = f"https://meet.jit.si/{ID_SALA_EQUIPO}"
    
    st.success("🚀 Enlace de comunicación remota generado con éxito.")
    
    st.markdown("""
    ### 🔓 Conexión Remota Segura (HTTPS)
    Para garantizar que la videollamada funcione **fuera de tu casa** desde cualquier red móvil o Wi-Fi sin bloqueos de seguridad del navegador, iniciamos la comunicación en un canal cifrado externo de alta velocidad.
    
    1. El chat de la izquierda coordina el texto de forma global.
    2. Haz clic en el botón gigante de abajo para ingresar a la sala de video con soporte multimedia completo.
    """)
    
    st.link_button("👉 ENTRAR A LA VIDEOLLAMADA EN VIVO (MÁX 4 PERSONAS) 👈", URL_SALA_JITSI, use_container_width=True)
    st.info(f"ℹ️ Enlace directo para compartir: **{URL_SALA_JITSI}**")
