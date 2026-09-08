import streamlit as st
import streamlit.components.v1 as components

# Configuración inicial
st.set_page_config(page_title="Shark Tank Interactivo", layout="wide", page_icon="🦈")

# --- BASE DE DATOS EN MEMORIA ---
@st.cache_resource
def get_game_state():
    return {
        "wacc": 12.0,
        "tir": 15.0,
        "solicitud": 50000,
        "equity": 15,
        "preguntas": [],
        "ofertas": {},
        "deal_closed": False,
        "ganador": ""
    }

state = get_game_state()

# --- SELECCIÓN DE ROL ---
st.sidebar.title("🦈 Shark Tank: Módulo 1705")
rol = st.sidebar.radio("Selecciona tu rol para entrar:", ["Pizarra Principal (Docente/Equipo)", "Tiburón (Inversor - Móvil)"])

# ==========================================
# ROL 1: PIZARRA PRINCIPAL (Pantalla Grande)
# ==========================================
if rol == "Pizarra Principal (Docente/Equipo)":
    st.title("📊 Pizarra Principal - Proyecto en Evaluación")
    
    # PANTALLA DE VICTORIA (Suena Automático al pulsar "Aceptar oferta")
    if state["deal_closed"]:
        st.balloons()
        st.success(f"🎉 ¡LO CONSEGUISTE! ESTÁS DENTRO 🎉\n\nAcuerdo cerrado con el inversor: **{state['ganador']}**.")
        
        # Reproducción automática e inmediata de la música de victoria
        components.html(
            """
            <audio autoplay style="display:none;">
              <source src="./app/static/Ganar.mp3" type="audio/mpeg">
            </audio>
            """,
            height=0
        )
        
        if st.button("Reiniciar Simulador para otro equipo"):
            state["deal_closed"] = False
            state["preguntas"] = []
            state["ofertas"] = {}
            st.rerun()
            
    # PANTALLA NORMAL DE EXPOSICIÓN (Requiere Play manual para el discurso)
    else:
        components.html(
            """
            <div style="background: #0E2A35; padding: 10px; border-radius: 8px; text-align: center; border: 1px solid #1E4652; margin-bottom: 10px;">
                <p style="color: #9FBAC2; font-family: sans-serif; margin: 0 0 6px 0; font-size: 13px;">🎶 Ambiente de Tensión (Haz clic en Play para activar el pitch)</p>
                <audio controls loop style="width: 80%; height: 35px;">
                  <source src="./app/static/Suspenso.mp3" type="audio/mpeg">
                </audio>
            </div>
            """,
            height=85
        )
            
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("1. Datos de la Propuesta")
            state["wacc"] = st.number_input("WACC Estimado (%)", value=state["wacc"], step=0.5)
            state["tir"] = st.number_input("TIR Proyectada (%)", value=state["tir"], step=0.5)
            state["solicitud"] = st.number_input("Inversión Solicitada (€)", value=state["solicitud"], step=1000)
            state["equity"] = st.number_input("Equity Ofrecido (%)", value=state["equity"], step=1)
            
            st.markdown("---")
            st.subheader("3. Ofertas de los Tiburones")
            if not state["ofertas"]:
                st.info("Esperando ofertas de los inversores...")
            
            for inversor, oferta in state["ofertas"].items():
                st.success(f"🦈 **{inversor}** ofrece: **{oferta['monto']}€** por el **{oferta['pct']}%**")
                if st.button(f"🤝 Aceptar oferta de {inversor}", key=f"btn_{inversor}"):
                    state["deal_closed"] = True
                    state["ganador"] = inversor
                    st.rerun()

        with col2:
            st.subheader("2. Preguntas en Vivo (Tipo Kahoot)")
            if st.button("🔄 Sincronizar Pizarra (Ver nuevas preguntas)"):
                st.rerun()
                
            if len(state["preguntas"]) == 0:
                st.info("Los inversores aún no han lanzado preguntas.")
            else:
                for idx, p in enumerate(reversed(state["preguntas"])):
                    st.warning(f"💬 {p}")

# ==========================================
# ROL 2: TIBURÓN INVERSOR (Para los móviles)
# ==========================================
elif rol == "Tiburón (Inversor - Móvil)":
    st.title("📱 Panel de Inversor")
    
    if state["deal_closed"]:
        if state["ganador"] == st.session_state.get("mi_nombre", ""):
            st.snow()
            st.success("¡Felicidades! Tu oferta fue la ganadora. Eres socio del proyecto.")
        else:
            st.error(f"El proyecto se lo llevó {state['ganador']}. ¡Más suerte en la próxima inversión!")
    else:
        nombre = st.text_input("Ingresa tu Nombre / Apodo de Tiburón:", key="mi_nombre")
        
        if nombre:
            st.markdown("---")
            st.subheader("A. Lanza una pregunta a la pizarra")
            pregunta_pre = st.selectbox("Elige una pregunta técnica rápida:", [
                "", 
                "¿Cómo has calculado exactamente tu WACC?", 
                "Tu TIR me parece muy optimista, ¿qué pasa si las ventas caen un 20%?", 
                "¿Por qué estás valorando la empresa tan alto con tan pocas ventas?"
            ])
            pregunta_libre = st.text_input("O escribe tu propia pregunta libre:")
            
            if st.button("Enviar Pregunta"):
                preg_final = pregunta_libre if pregunta_libre else pregunta_pre
                if preg_final:
                    state["preguntas"].append(f"{nombre}: {preg_final}")
                    st.success("Pregunta enviada. Pide a la pizarra que sincronice.")

            st.markdown("---")
            st.subheader("B. Asistente de Decisión Automático")
            if state["tir"] >= state["wacc"] + 5:
                    st.success("🤖 **RECOMENDACIÓN: INVERTIR.** La TIR supera ampliamente el WACC.")
            elif state["tir"] >= state["wacc"]:
                st.warning("🤖 **RECOMENDACIÓN: PRECAUCIÓN.** La TIR cubre el WACC, pero el margen es mínimo.")
            else:
                st.error("🤖 **RECOMENDACIÓN: NO INVERTIR.** La TIR es menor al WACC. Riesgo altísimo.")

            st.markdown("---")
            st.subheader("C. Hacer Contraoferta")
            st.write(f"*El equipo pide {state['solicitud']}€ por el {state['equity']}%*")
            monto_of = st.number_input("Dinero que ofreces (€):", value=state["solicitud"])
            pct_of = st.number_input("Equity que exiges (%):", value=state["equity"])
            
            if st.button("¡Lanzar Oferta!"):
                state["ofertas"][nombre] = {"monto": monto_of, "pct": pct_of}
                st.success("Oferta enviada al equipo. ¡Espera su decisión en la pizarra!")
