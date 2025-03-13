# st.title('Echo bot')

# if 'messages' not in st.session_state:
#     st.session_state.messages = []

# for message in st.session_state.messages:
#     with st.chat_message(message['role']):
#         st.markdown(message['content'])

# if prompt := st.chat_input('what is up?'):

#     with st.chat_message('user'):
#         st.markdown(prompt)

#     st.session_state.messages.append({'role':'user', 'content':prompt})

#     response = f'Echo: {prompt}'

#     with st.chat_message('assistant'):
#         st.markdown(response)

#     st.session_state.messages.append({'role':'assistant', 'content':response})

import openai
import streamlit as st
from streamlit import runtime
runtime.exists()

avatar = {
    'user': 'lorelei',
    'assistant': 'pixel-art'
}

system_message = '''
Analiza cada solicitud de crédito de acuerdo con la normativa "Arca Lisim - Libre Inversión" y proporciona un análisis detallado basado en las siguientes variables. El modelo debe aprender de las evaluaciones previas hechas por analistas humanos y ajustar su análisis progresivamente ten presente que si se incumple un solo criterio entonces el crédito debe ser negado.

Datos de Entrada requeridos:
Tipo de crédito solicitado: (Libre Inversión(Consumo), Compra de Cartera, Retanqueo).
Monto solicitado: Verificar si está dentro de los límites permitidos.
Plazo solicitado: Comparar con los plazos permitidos.
Forma de pago solicitada: Descuento por nómina o pago por caja.
Nivel de riesgo del solicitante: Bajo, Medio Bajo, Medio, Medio Alto, Alto.
Endeudamiento global: Calcular la relación entre deudas y el ingreso mensual del solicitante (deudas/ingresos mensuales).
Porcentaje de descuento por nómina proyectado: No debe exceder el 50% del ingreso mensual.
Flujo de caja proyectado: Debe ser positivo para aprobar el crédito.
Solvencia del solicitante: Activo Total / Pasivo Total, el ratio debe estar entre 0.5 y 1.5.
Aporte social y ahorro permanente: Confirmar que esté cancelado.
Historial de pagos y moras: Revisar si existen moras en Buró Externo y Buró Interno.
Antigüedad laboral del solicitante: Indicar la cantidad de tiempo (años o meses).
Cuentas en mal manejo o embargadas: Confirmar si el solicitante tiene cuentas en esta situación (Sí o No).
Información Financiera y Socioeconómica del Solicitante:
Ingresos mensuales del solicitante: Especificar el valor exacto de los ingresos netos.
Gastos mensuales: Especificar el total de gastos recurrentes.
Deudas activas: Detallar las deudas actuales (monto y tipo de cada una).
Puntaje de crédito del solicitante: Scoring crediticio.
Edad del solicitante: En años.
Estado civil: (Soltero, Casado, Unión Libre, etc.).
Sector laboral: (Público, Privado, Independiente, etc.).
Ahorro programado: Confirmar si el solicitante tiene ahorro programado y especificar el monto.
Número de cuotas pagas del crédito (solo aplica para retanqueo)
% pago del crédito (solo aplica para retanqueo)
Tener presente que 1 S.M.M.L.V. equivale a 1423500 COP (pesos colombianos)

Criterios Específicos por Tipo de Crédito:

Libre Inversión(Consumo):

Monto máximo: 346 S.M.M.L.V.
Plazo: Hasta 84 meses (nómina)
Endeudamiento global ≤ 20 veces el ingreso mensual.
tasa 1.85%
Solvencia entre 0.5 y 1.5.
Descuento por nómina ≤ 50%.
Flujo de caja positivo.
Nivel de riesgo: Bajo, Medio bajo, Medio, Medio Alto (Nomina) y Bajo, Medio bajo, Medio (Caja)
Antiguedad laboral: mayor a 12 meses (Caja) mayor a 6 meses (nómina)
Edad: Entre 18 años y 74 años 11 meses (Nómina) y entre 24 y 74 años 11 meses (Caja)
Ingresos: mayor a 1 S.M.M.L.V (nómina) y 1.5 S.M.M.L.V (caja)
Mora Buró externo: No presentar ni un solo día de mora.
Mora Muró Interno: Se permite máximo 45 días para pago por nómina y 0 para pago por caja

Compra de Cartera:

Consolidación de deudas.
Monto máximo: 346 S.M.M.L.V.
Plazo: Hasta 84 meses (nómina)
Endeudamiento global ≤ 20 veces el ingreso mensual.
Solvencia entre 0.5 y 1.5.
Descuento por nómina ≤ 50%.
Flujo de caja positivo.
Nivel de riesgo: Bajo, Medio bajo, Medio (Nomina) y Bajo(Caja)
Antiguedad laboral: mayor a 12 meses (Caja) mayor a 6 meses (nómina)
Edad: Entre 18 años y 74 años 11 meses (Nómina) y entre 24 y 74 años 11 meses (Caja)
Ingresos: mayor a 1 S.M.M.L.V (nómina) y 1.5 S.M.M.L.V (caja)
Mora Buró externo: No presentar ni un solo día de mora.
Mora Muró Interno: No presentar ni un solo día de mora

Retanqueo:

Verificar obligaciones vigentes.
Mínimo 7 cuotas pagadas
mínimo 30% de crédito pago
tasa : 1.7% (caja) y  1.6%(nómina)
Edad: Entre 24 y 64 años.
nivel de riesgo: bajo, medio bajo (Nómina) y bajo(caja)
Mora buró externo: máximo 59 días de mora.
Mora buró interno: 0 días (caja) y máximo 45 (nómina)
No se permiten reestructuraciones activas, Castigadas o dudoso cobro.
Endeudamiento global ≤ 15 veces el ingreso mensual.
'''


st.title("Chatea con el FincoAnalítico 💬🧑‍💻")

with st.sidebar:
    st.title('Configuraciones')
    # st.sidebar.info('por EvoAcademy: https://www.evoacademy.cl/', icon='ℹ️')
    # if ('APIKEY' in st.secrets) and ('IDMODEL' in st.secrets):
    #     st.success('Credenciales secretas cargadas!', icon='✅')
    #     api_key = st.secrets['APIKEY']
    #     id_model = st.secrets['IDMODEL']
    
    # else:
    placeholder = st.empty()
    api_key = st.text_input('API Key:', placeholder='Aquí tu API Key de OpenAI', type='password')
    id_model = st.text_input('Id Modelo:', placeholder='Id de tu modelo de fine-tuning', type='password')
    with placeholder.container():
        if not (api_key and id_model):
            st.warning('Por favor, ingresa tus credenciales!', icon='⚠️')
        else:
            st.success('Procede a ingresar los mensajes!', icon='👉')
            
    # system_message = st.text_area(label='Mensaje de sistema:',
    #                             height=180,
    #                             placeholder='Instrucciones que complementan el comportamiento de tu modelo de fine-tuning. Ej: Responde siempre alegre.')
    memory = st.slider(label='Memoria conversación (num. mensajes):',value=4, min_value=1)
    temp = st.slider(label='Creatividad (temperatura):',value=0.5, min_value=0.0, max_value=2.0, step=0.1)
    openai.api_key = api_key


if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": system_message},
        ]

for message in st.session_state.messages:
    if message['role']=='system': continue
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = st.session_state.messages = [
        {"role": "system", "content": system_message},
        ]
st.sidebar.button('Limpiar chat', on_click=clear_chat_history)

def generate_response(model):
    history = [st.session_state.messages[0]]+st.session_state.messages[-memory:] if len(st.session_state.messages)>5 else st.session_state.messages
    response = openai.chat.completions.create(
                        model=model,
                        messages=history,
                        temperature = temp,
                        max_tokens=400
                        )
    msg = response.choices[0].message.content
    return msg

if prompt := st.chat_input(disabled=not (api_key and id_model), placeholder='Tú mensaje...'):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

if st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            response = generate_response(id_model) 
            st.write(response) 
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)