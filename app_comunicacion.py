import streamlit as st
import datetime
import time

# Configuración de la interfaz estilo centro de control HikCentral
st.set_page_config(page_title="HikCentral VMS Hub", layout="wide")

# Estilos CSS - Paleta Oficial HikCentral Professional
st.markdown("""
    <style>
        /* Fondo gris oscuro industrial y fuentes limpias */
        .stApp {
            background-color: #11141a !important;
            color: #e1e4ea !important;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        }
        
        /* Títulos e indicadores */
        h1, h2, h3, h4, label, p, span {
            color: #ffffff !important;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        }
        
        /* Cabecera estilo barra de herramientas HikCentral */
        .hik-header {
            background-color: #1c212c;
            padding: 15px;
            border-radius: 4px;
            border-left: 4px solid #0070FF;
            margin-bottom: 20px;
        }
        
        /* Contenedores de cámaras y chat (Paneles VMS) */
        .stContainer, div[data-testid="stForm"] {
            background-color: #171b26 !important;
            border: 1px solid #283143 !important;
            border-radius: 4px !important;
            padding: 12px !important;
        }
        
        /* Cajas de texto e inputs */
        input[type="text"] {
            background-color: #1f2533 !important;
            color: #ffffff !important;
            border: 1px solid #3b4861 !important;
            border-radius: 3px !important;
        }
        input[type="text"]:focus {
            border-color: #0070FF !important;
        }
        
        /* Botones estilo HikCentral (Azul comando) */
        button[data-testid="baseButton-secondaryFormSubmit"] {
            background-color: #0070FF !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 3px !important;
            font-weight: 600 !important;
            width: 100% !important;
            transition: background-color 0.2s ease;
        }
        button[data-testid="baseButton-secondaryFormSubmit"]:hover {
            background-color: #0056c7 !important;
        }
        
        /* Info boxes */
        .stAlert {
            background-color: #1c212c !important;
            border: 1px solid #0070FF !important;
            color: #e1e4ea !important;
        }
    </style>
""", unsafe_allow_html=True)

# Servidor de datos compartido en memoria para usuarios externos
@st.cache_resource
def obtener_memoria_chat():
    return []

historial_global = obtener_memoria_chat()

# Cabecera de la Aplicación
st.markdown("""
    <div class="hik-header">
        <h2 style='margin:0; font-size:22px;'>🎛️ Centro de Comunicaciones</h2>
        <p style='margin:5px 0 0 0; color:#8a94a6 !important; font-size:13px;'>SYS_STATUS: ONLINE | SECURITY: SSL_ENCRYPTED | LIVE FEED MAX 4 NODES</p>
    </div>
""", unsafe_allow_html=True)

# Distribución de pantalla (Panel de control: 35% Chat / 65% Matriz de Video Directa)
col_chat, col_video = st.columns([1, 1.8])

# ==========================================
# 1. PANEL DE MENSIDERÍA (COLUMNA IZQUIERDA)
# ==========================================
with col_chat:
    st.markdown("### 🗪 Centro de Mensajes")
    
    usuario = st.text_input("Operador:", value="Operador_1", key="alias_usuario")
    
    contenedor_mensajes = st.container(height=420)
    
    with contenedor_mensajes:
        if not historial_global:
            st.markdown("<span style='color:#8a94a6;'>No hay registros de texto en la sesión actual.</span>", unsafe_allow_html=True)
        else:
            for msg in historial_global:
                hora_actual = msg["hora"]
                if msg["remitente"] == usuario:
                    st.markdown(f"<b style='color:#0070FF;'>[Tú]</b> <span style='color:#8a94a6; font-size:11px;'>({hora_actual}):</span> <br>{msg['texto']}", unsafe_allow_html=True)
                else:
                    st.markdown(f"<b style='color:#e1e4ea;'>[{msg['remitente']}]</b> <span style='color:#8a94a6; font-size:11px;'>({hora_actual}):</span> <br>{msg['texto']}", unsafe_allow_html=True)
                st.markdown("<hr style='margin:8px 0; border:0; border-top:1px solid #283143;'>", unsafe_allow_html=True)

    with st.form("formulario_envio", clear_on_submit=True):
        nuevo_mensaje = st.text_input("Ingresar mensaje...", placeholder="Escribir mensaje...")
        boton_enviar = st.form_submit_button("Enviar Mensaje")
        
        if boton_enviar and nuevo_mensaje.strip() != "":
            ahora = datetime.datetime.now().strftime("%H:%M:%S")
            historial_global.append({
                "remitente": usuario,
                "texto": nuevo_mensaje,
                "hora": ahora
            })
            st.rerun()

# ==========================================
# 2. PANEL DE VIDEO EN DIRECTO (COLUMNA DERECHA)
# ==========================================
with col_video:
    st.markdown("### 📺 Video en Directo")
    
    ID_SALA_EQUIPO = "Aura19997822252"
    
    # MODIFICACIÓN SOLICITADA:
    # Inyectamos CSS interno codificado en la URL mediante 'config.customStyles'
    # Esto oculta selectivamente el branding de la pantalla previa (Prejoin)
    CSS_OCULTAR_TEXTOS = (
        ".prejoin-preview-title { display: none !important; } "
        ".prejoin-preview-name { display: none !important; } "
        ".prejoin-preview-header .header-logo { display: none !important; } "
        "header { display: none !important; }"
    )
    
    URL_SALA_VIDEO = (
        f"https://meet.jit.si/{ID_SALA_EQUIPO}"
        f"#config.startWithVideoMuted=false"
        f"&config.startWithAudioMuted=false"
        f"&config.prejoinPageEnabled=true"
        f"&interfaceConfigOverwrite.SHOW_JITSI_WATERMARK=false"
        f"&interfaceConfigOverwrite.DISPLAY_WELCOME_PAGE=false"
        f"&config.customStyles={CSS_OCULTAR_TEXTOS}"
    )
    
    # Código del reproductor embebido que se ejecutará nativamente gracias al HTTPS
    codigo_iframe = f"""
    <iframe 
        src="{URL_SALA_VIDEO}" 
        width="100%" 
        height="485px" 
        allow="camera; microphone; fullscreen; speaker; display-capture" 
        style="border: 1px solid #283143; border-radius: 4px; background-color: #171b26;">
    </iframe>
    """
    
    st.components.v1.html(codigo_iframe, height=490)
    st.markdown(f"<span style='color:#8a94a6; font-size:12px;'>ID de la matriz activa: <code>{ID_SALA_EQUIPO}</code></span>", unsafe_allow_html=True)

# ==========================================
# 3. MOTOR DE AUTO-REFRESCO DE CHAT
# ==========================================
time.sleep(2)
st.rerun()
