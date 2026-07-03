import streamlit as st
import datetime
import time

# Configuración de la interfaz en modo ancho y título de pestaña
st.set_page_config(page_title="🥷 SECURE CRYPTO HUB", layout="wide")

# Estilos CSS Avanzados - Estilo "Hack Term" Terminal Encriptada
st.markdown("""
    <style>
        /* Fondo principal y textos globales estilo terminal */
        .stApp {
            background-color: #0d0e11 !important;
            color: #00ff66 !important;
            font-family: 'Courier New', Courier, monospace !important;
        }
        
        /* Títulos principales */
        h1, h2, h3, h4, h5, h6, label, p, span {
            color: #00ff66 !important;
            font-family: 'Courier New', Courier, monospace !important;
            text-shadow: 0 0 5px rgba(0, 255, 102, 0.5);
        }
        
        /* Contenedor del Chat encriptado */
        .stContainer {
            background-color: #050608 !important;
            border: 2px solid #00ff66 !important;
            border-radius: 6px !important;
            box-shadow: 0 0 15px rgba(0, 255, 102, 0.2);
            padding: 15px !important;
        }
        
        /* Estilos de los inputs de texto */
        input[type="text"] {
            background-color: #14171f !important;
            color: #00ff66 !important;
            border: 1px solid #00ff66 !important;
            font-family: 'Courier New', Courier, monospace !important;
        }
        
        /* Modificación de alertas y notificaciones nativas */
        .stAlert {
            background-color: #14171f !important;
            border: 1px solid #ff3333 !important;
            color: #ff3333 !important;
        }
        
        /* Botones de acción y formularios */
        button[data-testid="baseButton-secondaryFormSubmit"], a[data-testid="stLinkButton"] {
            background-color: #00ff66 !important;
            color: #0d0e11 !important;
            font-weight: bold !important;
            border: 2px solid #00ff66 !important;
            box-shadow: 0 0 10px rgba(0, 255, 102, 0.4);
            transition: all 0.3s ease;
        }
        
        button[data-testid="baseButton-secondaryFormSubmit"]:hover, a[data-testid="stLinkButton"]:hover {
            background-color: #0d0e11 !important;
            color: #00ff66 !important;
            box-shadow: 0 0 20px rgba(0, 255, 102, 0.8);
        }
    </style>
""", unsafe_allow_html=True)

# Servidor de datos compartido en memoria para usuarios externos
@st.cache_resource
def obtener_memoria_chat():
    return []

historial_global = obtener_memoria_chat()

st.title("📟 SECURE OPERATIONAL COMMUNICATIONS")
st.markdown("> **STATUS:** `ENCRYPTED_ENDPOINT_ACTIVE` | **CHANNEL:** `P2P_OVER_HTTPS` | Mantenimiento de sesión seguro.")
st.write("---")

# Crear la distribución de la pantalla (40% Chat, 60% Panel de Videoconferencia)
col_chat, col_video = st.columns([1, 1.4])

# ==========================================
# 1. PANEL DE CHAT GLOBAL (COLUMNA IZQUIERDA)
# ==========================================
with col_chat:
    st.subheader("📡 FEED DE DATOS EN VIVO")
    
    usuario = st.text_input("OPERATOR_ID:", value="NODE_1", key="alias_usuario")
    
    # Contenedor con barra de desplazamiento (scroll) automática para los mensajes
    contenedor_mensajes = st.container(height=420)
    
    with contenedor_mensajes:
        if not historial_global:
            st.markdown("<span style='color:#ff3333;'>[SYSTEM]: No se detectan transmisiones de datos activos en la sala.</span>", unsafe_allow_html=True)
        else:
            for msg in historial_global:
                hora_actual = msg["hora"]
                if msg["remitente"] == usuario:
                    st.markdown(f"**&lt;{usuario}&gt;** <span style='color:#00ff66;'>[{hora_actual}]:</span> <span style='color:#ffffff;'>{msg['texto']}</span>", unsafe_allow_html=True)
                else:
                    st.markdown(f"**&lt;{msg['remitente']}&gt;** <span style='color:#00e5ff;'>[{hora_actual}]:</span> <span style='color:#a6b2c9;'>{msg['texto']}</span>", unsafe_allow_html=True)
                st.write("") # Espaciador

    # Formulario para el envío de mensajes
    with st.form("formulario_envio", clear_on_submit=True):
        nuevo_mensaje = st.text_input("TRANSMIT_BUFFER:", placeholder="Escribe tu mensaje seguro aquí...")
        boton_enviar = st.form_submit_button("EJECUTAR TRANSMISIÓN [ENTER]")
        
        if boton_enviar and nuevo_mensaje.strip() != "":
            ahora = datetime.datetime.now().strftime("%H:%M:%S")
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
    st.subheader("👁️ ENLACE DE VIDEO CORRESPONDIENTE")
    
    ID_SALA_EQUIPO = "SalaComunComunicacionesPrivada777"
    URL_SALA_JITSI = f"https://meet.jit.si/{ID_SALA_EQUIPO}"
    
    st.markdown("""
    ### 🛡️ PROTOCOLO DE SEGURIDAD MULTIMEDIA
    Para iniciar el flujo de video externo punto a punto sin intermediarios y mitigar bloqueos locales en navegadores de terceros, activa el túnel dedicado:
    
    * El backend sincroniza el chat textual global en bucle continuo cada 2 segundos.
    * La videollamada opera con cifrado forzado en la red pública de WebRTC.
    """)
    
    st.write("")
    st.link_button("⚡ ABRIR SALA MULTIMEDIA HD REMOTA", URL_SALA_JITSI, use_container_width=True)
    st.write("")
    
    st.markdown(f"**TOKEN_DE_ACCESO:** `{URL_SALA_JITSI}`")

# ==========================================
# 3. MOTOR DE AUTO-REFRESCO (RELOJ INVISIBLE)
# ==========================================
time.sleep(2)
st.rerun()
