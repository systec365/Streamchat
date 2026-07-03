import streamlit as st
import datetime
import time

# Configuración de la interfaz estilo centro de control HikCentral
st.set_page_config(page_title="HikCentral VMS Hub", layout="wide")

# Estilos CSS - Paleta Oficial HikCentral Professional
st.markdown("""
    <style>
        .stApp {
            background-color: #11141a !important;
            color: #e1e4ea !important;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        }
        h1, h2, h3, h4, label, p, span {
            color: #ffffff !important;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        }
        .hik-header {
            background-color: #1c212c;
            padding: 15px;
            border-radius: 4px;
            border-left: 4px solid #0070FF;
            margin-bottom: 20px;
        }
        /* Ajuste de estilo para el chat nativo */
        div[data-testid="stChatMessageContainer"] {
            background-color: #171b26 !important;
            border: 1px solid #283143 !important;
            border-radius: 4px !important;
        }
        iframe {
            overflow: hidden !important;
        }
    </style>
""", unsafe_allow_html=True)

# Sonido "Ping" de Notificación Corto en Base64 para saltar políticas estrictas de autoplay
AUDIO_BASE64 = "UklGRigAAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAZGF0YQQAAAAAAA=="

def reproducir_sonido_js():
    st.components.v1.html(f"""
        <script>
            var audio = new Audio("data:audio/wav;base64,{AUDIO_BASE64}");
            audio.volume = 0.7;
            audio.play().catch(function(e){{ console.log("Audio retenido por el navegador"); }});
        </script>
    """, height=0, width=0)

# ==========================================
# GESTIÓN DE MEMORIA GLOBAL Y LIMPIEZA HORARIA
# ==========================================
@st.cache_resource
def obtener_servidor_datos():
    return {
        "mensajes": [],
        "ultima_limpieza": time.time()
    }

servidor_datos = obtener_servidor_datos()

if time.time() - servidor_datos["ultima_limpieza"] >= 3600:
    servidor_datos["mensajes"] = []  
    servidor_datos["ultima_limpieza"] = time.time()  

historial_global = servidor_datos["mensajes"]

if "mensajes_vistos" not in st.session_state:
    st.session_state["mensajes_vistos"] = len(historial_global)

# Cabecera de la Aplicación
st.markdown("""
    <div class="hik-header">
        <h2 style='margin:0; font-size:22px;'>🎛️ Centro de Comunicaciones</h2>
        <p style='margin:5px 0 0 0; color:#8a94a6 !important; font-size:13px;'>SYS_STATUS: ONLINE | SECURITY: SSL_ENCRYPTED | AUTO-CLEAR: 60 MIN</p>
    </div>
""", unsafe_allow_html=True)

col_chat, col_video = st.columns([1, 1.8])

# ==========================================
# 1. PANEL DE MENSAJERÍA REAL-TIME (NATIVO AUTOMÁTICO)
# ==========================================
with col_chat:
    st.markdown("### 🗪 Centro de Mensajes")
    usuario = st.text_input("Operador:", value="Operador_1", key="alias_usuario")
    
    @st.fragment(run_every=2)
    def renderizar_chat_reactivo():
        with st.container(height=420):
            if not historial_global:
                st.markdown("<span style='color:#8a94a6;'>No hay registros de texto en la sesión actual.</span>", unsafe_allow_html=True)
            else:
                for msg in historial_global:
                    avatar = "user" if msg["remitente"] == usuario else "assistant"
                    with st.chat_message(avatar):
                        st.markdown(f"<span style='color:#8a94a6; font-size:11px;'>{msg['hora']} - <b>{msg['remitente']}</b></span>", unsafe_allow_html=True)
                        st.write(msg['texto'])

        # Comprobación si ingresaron nuevos mensajes de otros operadores
        if len(historial_global) > st.session_state["mensajes_vistos"]:
            st.session_state["mensajes_vistos"] = len(historial_global)
            reproducir_sonido_js()

        # Entrada de chat con enfoque nativo automatizado
        nuevo_mensaje = st.chat_input("Escribir mensaje...")
        if nuevo_mensaje:
            ahora = datetime.datetime.now().strftime("%H:%M:%S")
            historial_global.append({
                "remitente": usuario,
                "texto": nuevo_mensaje,
                "hora": ahora
            })
            st.session_state["mensajes_vistos"] = len(historial_global)
            reproducir_sonido_js()
            st.rerun()

    renderizar_chat_reactivo()

# ==========================================
# 2. PANEL DE VIDEO SEGURO (MANTENIENDO REGLAS DE LOGOS OCULTOS)
# ==========================================
with col_video:
    st.markdown("### 📺 Video en Directo")
    
    ID_SALA_EQUIPO = "Aura19997822252"
    
    codigo_api_jitsi = f"""
    <div id="jitsi-container" style="height: 485px; width: 100%; border: 1px solid #283143; border-radius: 4px; background-color: #171b26;"></div>
    
    <script src="https://meet.jit.si/external_api.js"></script>
    <script>
        const domain = 'meet.jit.si';
        const options = {{
            roomName: '{ID_SALA_EQUIPO}#config.prejoinPageEnabled=false&config.startWithVideoMuted=false&config.startWithAudioMuted=false',
            width: '100%',
            height: 485,
            parentNode: document.querySelector('#jitsi-container'),
            userInfo: {{
                displayName: '{usuario}'
            }},
            configOverwrite: {{ 
                startWithVideoMuted: false,
                startWithAudioMuted: false,
                prejoinPageEnabled: false,
                disableDeepLinking: true
            }},
            interfaceConfigOverwrite: {{
                SHOW_JITSI_WATERMARK: false,
                SHOW_BRAND_WATERMARK: false,
                DISPLAY_WELCOME_PAGE: false,
                JITSI_WATERMARK_LINK: ''
            }}
        }};
        
        let api = new JitsiMeetExternalAPI(domain, options);
        
        api.addEventListener('videoConferenceLeft', () => {{
            // 1. Destruimos por completo la instancia activa de Jitsi para limpiar recursos e imágenes basura
            api.dispose();
            
            // 2. Redibujamos la interfaz limpia sobre el contenedor
            const container = document.querySelector('#jitsi-container');
            if (container) {{
                container.innerHTML = `
                    <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100%; color: #8a94a6; font-family: sans-serif; background-color: #171b26; text-align: center; padding: 20px;">
                        <div style="font-size: 50px; margin-bottom: 15px; color: #3b4861;">📴</div>
                        <div style="font-size: 16px; font-weight: bold; color: #ffffff; margin-bottom: 5px;">LLAMADA FINALIZADA</div>
                        <div style="font-size: 13px; color: #8a94a6;">Canal de comunicación multimedia cerrado.</div>
                        <button onclick="window.location.reload();" style="margin-top: 20px; background-color: #0070FF; color: white; border: none; padding: 8px 16px; border-radius: 3px; cursor: pointer; font-weight: bold;">Reconectar Matriz</button>
                    </div>
                `;
            }}
        }});
    </script>
    """
    
    st.components.v1.html(codigo_api_jitsi, height=490, scrolling=False)
    st.markdown(f"<span style='color:#8a94a6; font-size:12px;'>ID de la matriz activa: <code>{ID_SALA_EQUIPO}</code></span>", unsafe_allow_html=True)
