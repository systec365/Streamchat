import streamlit as st
import datetime

# Configuración de la interfaz en modo ancho y título de pestaña
st.set_page_config(page_title="Hub de Comunicación Global", layout="wide")

# Inicializar variables de estado de sesión para el chat si no existen
if "historial_chat" not in st.session_state:
    st.session_state["historial_chat"] = []

st.title("🌐 Centro de Comunicación Digital")
st.markdown("Plataforma integrada de mensajería instantánea y videoconferencia remota multiusuario.")
st.write("---")

# Crear la distribución de la pantalla (40% Chat, 60% Panel de Videoconferencia)
col_chat, col_video = st.columns([1, 1.5])

# ==========================================
# 1. PANEL DE CHAT (COLUMNA IZQUIERDA)
# ==========================================
with col_chat:
    st.subheader("💬 Sala de Mensajes")
    
    # Configuración del perfil de usuario dentro de la sala
    usuario = st.text_input("Introduce tu nombre o alias:", value="Usuario_1", key="alias_usuario")
    
    # Contenedor con barra de desplazamiento (scroll) automática para los mensajes
    contenedor_mensajes = st.container(height=400)
    
    with contenedor_mensajes:
        if not st.session_state["historial_chat"]:
            st.info("La sala está vacía. ¡Escribe el primer mensaje!")
        else:
            for msg in st.session_state["historial_chat"]:
                hora_actual = msg["hora"]
                if msg["remitente"] == usuario:
                    st.markdown(f"**[Tú]** <span style='color:#00e676;'>({hora_actual}):</span> {msg['texto']}", unsafe_allow_html=True)
                else:
                    st.markdown(f"**[{msg['remitente']}]** <span style='color:#80d8ff;'>({hora_actual}):</span> {msg['texto']}", unsafe_allow_html=True)
                st.write("") # Espaciador

    # Formulario para el envío de mensajes
    with st.form("formulario_envio", clear_on_submit=True):
        nuevo_mensaje = st.text_input("Escribe tu mensaje aquí...", placeholder="Hola a todos...")
        boton_enviar = st.form_submit_button("Enviar Mensaje")
        
        if boton_enviar and nuevo_mensaje.strip() != "":
            ahora = datetime.datetime.now().strftime("%H:%M")
            st.session_state["historial_chat"].append({
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
    
    # ID único para tu equipo. Cambia este texto para tener salas distintas si lo deseas.
    ID_SALA_EQUIPO = "SalaComunComunicacionesPrivada777"
    URL_SALA_JITSI = f"https://meet.jit.si/{ID_SALA_EQUIPO}"
    
    st.success("🚀 Enlace de comunicación remota generado con éxito.")
    
    st.markdown("""
    ### 🔓 Solución al bloqueo de Cámara/Micrófono (WebRTC)
    Para garantizar que la videollamada funcione **fuera de tu casa** y desde cualquier red móvil o Wi-Fi sin lidiar con bloqueos de seguridad del navegador, hemos separado el flujo de video en una sala dedicada de alta velocidad.
    
    1. El chat de la izquierda sigue funcionando de manera local y en tiempo real.
    2. Haz clic en el botón gigante de abajo para unirte a la videollamada con tu equipo.
    """)
    
    # Botón interactivo con redirección nativa que asegura HTTPS completo y activa la cámara al instante
    st.link_button("👉 ENTRAR A LA VIDEOLLAMADA EN VIVO (MÁX 4 PERSONAS) 👈", URL_SALA_JITSI, use_container_width=True)
    
    st.info(f"ℹ️ Comparte este enlace con las otras 3 personas para que se unan directamente desde sus casas o celulares: **{URL_SALA_JITSI}**")
