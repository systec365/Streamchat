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
    </style>
""", unsafe_allow_html=True)

# Servidor de datos compartido en memoria para usuarios externos
@st.cache_resource
def obtener_memoria_chat():
    return []

historial_global = obtener_memoria_chat()

# Control de estado interno para detectar nuevos mensajes y lanzar la alerta sonora
if "mensajes_leidos" not in st.session_state:
    st.session_state["mensajes_leidos"] = len(historial_global)

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
# 1. PANEL DE MENSAJERÍA (COLUMNA IZQUIERDA)
# ==========================================
with col_chat:
    st.markdown("### 🗪 Centro de Mensajes")
    
    usuario = st.text_input("Operador:", value="Operador_1", key="alias_usuario")
    
    contenedor_mensajes = st.container(height=420)
    
    with contenedor_mensajes:
        if not historial_global:
            st.markdown("<span style='color:#8a94a6;'>No hay registros de texto en la sesión actual.</span>", unsafe_allow_html=True)
        else:
            for i, msg in enumerate(historial_global):
                hora_actual = msg["hora"]
                # Colocamos un ID HTML únicamente al último mensaje de la lista
                id_ultimo = 'id="ultimo_msg"' if i == len(historial_global) - 1 else ""
                
                if msg["remitente"] == usuario:
                    st.markdown(f"<div {id_ultimo} style='margin-bottom: 8px;'><b style='color:#0070FF;'>[Tú]</b> <span style='color:#8a94a6; font-size:11px;'>({hora_actual}):</span> <br>{msg['texto']}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div {id_ultimo} style='margin-bottom: 8px;'><b style='color:#e1e4ea;'>[{msg['remitente']}]</b> <span style='color:#8a94a6; font-size:11px;'>({hora_actual}):</span> <br>{msg['texto']}</div>", unsafe_allow_html=True)
                st.markdown("<hr style='margin:8px 0; border:0; border-top:1px solid #283143;'>", unsafe_allow_html=True)

    # REPRODUCTOR DE AUDIO Y CONTROL DE ENFOQUE AUTOMÁTICO (JS)
    reproducir_alerta = "false"
    if len(historial_global) > st.session_state["mensajes_leidos"]:
        st.session_state["mensajes_leidos"] = len(historial_global)
        reproducir_alerta = "true"

    st.components.v1.html(f"""
        <script>
            // Forzar el scroll inferior buscando el elemento ID en la ventana principal de Streamlit
            setTimeout(() => {{
                const chatContainer = window.parent.document.getElementById('ultimo_msg');
                if (chatContainer) {{
                    chatContainer.scrollIntoView({{ behavior: 'smooth', block: 'end' }});
                }}
            }}, 50);

            // Alerta sonora industrial sin bloqueos del navegador
            if ({reproducir_alerta} === true) {{
                var audio = new Audio("https://assets.mixkit.co/active_storage/sfx/2357/2357-84.wav");
                audio.volume = 0.6;
                audio.play().catch(function(error) {{ console.log("Audio retenido hasta interacción"); }});
            }}
        </script>
    """, height=0, width=0)

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
            # Actualizamos el estado para tu propio mensaje
            st.session_state["mensajes_leidos"] = len(historial_global)
            st.rerun()

# ==========================================
# 2. PANEL DE VIDEO SEGURO (COLUMNA DERECHA)
# ==========================================
with col_video:
    st.markdown("### 📺 Video en Directo")
    
    ID_SALA_EQUIPO = "Aura19997822252"
    
    # Inyección de la API JS oficial. Captura el evento 'videoConferenceLeft' (cuando cuelgas)
    # y borra el contenedor de Jitsi reemplazándolo por un aviso oscuro integrado tipo HikCentral.
    codigo_api_jitsi = f"""
    <div id="jitsi-container" style="height: 485px; width: 100%; border: 1px solid #283143; border-radius: 4px; background-color: #171b26;"></div>
    
    <script src="https://meet.jit.si/external_api.js"></script>
    <script>
        const domain = 'meet.jit.si';
        const options = {{
            roomName: '{ID_SALA_EQUIPO}',
            width: '100%',
            height: 485,
            parentNode: document.querySelector('#jitsi-container'),
            configOverwrite: {{ 
                startWithVideoMuted: false,
                startWithAudioMuted: false,
                prejoinPageEnabled: false
            }},
            interfaceConfigOverwrite: {{
                SHOW_JITSI_WATERMARK: false,
                SHOW_BRAND_WATERMARK: false,
                DISPLAY_WELCOME_PAGE: false
            }}
        }};
        
        const api = new JitsiMeetExternalAPI(domain, options);
        
        // INTERCEPTOR DE SALIDA: Elimina la publicidad de Jitsi al colgar
        api.addEventListener('videoConferenceLeft', () => {{
            const container = document.querySelector('#jitsi-container');
            container.innerHTML = `
                <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100%; color: #8a94a6; font-family: sans-serif; background-color: #171b26; text-align: center; padding: 20px;">
                    <div style="font-size: 50px; margin-bottom: 15px; color: #3b4861;">📴</div>
                    <div style="font-size: 16px; font-weight: bold; color: #ffffff; margin-bottom: 5px;">LLAMADA FINALIZADA</div>
                    <div style="font-size: 13px; color: #8a94a6;">Canal multimedia cerrado de forma segura por el operador.</div>
                    <button onclick="window.location.reload();" style="margin-top: 20px; background-color: #0070FF; color: white; border: none; padding: 8px 16px; border-radius: 3px; cursor: pointer; font-weight: bold;">Reconectarse al canal</button>
                </div>
            `;
        }});
    </script>
    """
    
    st.components.v1.html(codigo_api_jitsi, height=490)
    st.markdown(f"<span style='color:#8a94a6; font-size:12px;'>ID de la matriz activa: <code>{ID_SALA_EQUIPO}</code></span>", unsafe_allow_html=True)

# ==========================================
# 3. MOTOR DE AUTO-REFRESCO DE CHAT
# ==========================================
time.sleep(2)
st.rerun()
