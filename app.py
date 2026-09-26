import json
import uuid
from datetime import datetime, timezone

import streamlit as st


def aplicar_estilos():
    st.markdown(
        """
        <style>
        :root {
            color-scheme: dark;
            --app-bg: #080d16;
            --surface: #0f1724;
            --surface-raised: #151f2e;
            --border: #253247;
            --text-primary: #eef3fa;
            --text-secondary: #9ba9bc;
            --accent: #60a5fa;
            --accent-strong: #2563eb;
        }

        [data-testid="stAppViewContainer"] {
            background: var(--app-bg);
            color: var(--text-primary);
        }

        [data-testid="stHeader"] {
            background: rgba(8, 13, 22, 0.88);
            border-bottom: 1px solid rgba(37, 50, 71, 0.55);
        }

        [data-testid="stSidebar"] {
            background: #0c1320;
            border-right: 1px solid var(--border);
        }

        .block-container {
            max-width: 1200px;
            padding: 2.25rem 2rem 4rem;
        }

        [data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlock"] {
            gap: 1.25rem;
        }

        h1, h2, h3 {
            color: var(--text-primary);
            letter-spacing: 0;
        }

        .page-header {
            margin: 0.25rem 0 0.35rem;
            padding: 0 0 1.35rem;
            border-bottom: 1px solid var(--border);
        }

        .page-header h1 {
            margin: 0;
            font-size: 1.8rem;
            line-height: 1.25;
            font-weight: 680;
        }

        .page-header p {
            margin: 0.55rem 0 0;
            color: var(--text-secondary);
            font-size: 0.96rem;
        }

        .section-heading {
            margin-bottom: 0.35rem;
        }

        .section-heading h2 {
            margin: 0;
            font-size: 1.18rem;
            line-height: 1.4;
            font-weight: 640;
        }

        .section-heading p {
            margin: 0.3rem 0 0;
            color: var(--text-secondary);
            font-size: 0.9rem;
        }

        [data-testid="stWidgetLabel"] p,
        [data-testid="stWidgetLabel"] label {
            color: #d4deeb;
            font-size: 0.9rem;
        }

        [data-testid="stTextInput"] input,
        [data-testid="stTextArea"] textarea,
        [data-testid="stSelectbox"] [data-baseweb="select"] > div,
        [data-testid="stDateInput"] input {
            background: var(--surface-raised);
            border-color: #35455d;
            border-radius: 10px;
            color: var(--text-primary);
        }

        [data-testid="stTextInput"] input:focus,
        [data-testid="stTextArea"] textarea:focus,
        [data-testid="stDateInput"] input:focus {
            border-color: var(--accent);
            box-shadow: 0 0 0 1px var(--accent);
        }

        [data-testid="stTextInput"] input:disabled {
            background: #0b1220;
            border-color: #263449;
            color: #8190a5;
            opacity: 0.82;
        }

        [data-testid="stTextArea"] textarea::placeholder,
        [data-testid="stTextInput"] input::placeholder {
            color: #8190a5;
        }

        [data-testid="stRadio"] [role="radiogroup"] {
            gap: 0.7rem;
            flex-wrap: wrap;
        }

        [data-testid="stRadio"] label {
            color: #d4deeb;
        }

        .criterion-question {
            min-height: 3.1rem;
            display: flex;
            align-items: center;
            color: #dce5f1;
            font-size: 0.94rem;
            line-height: 1.45;
        }

        .recommendation {
            margin-top: 0.25rem;
            padding: 0.95rem 1rem;
            border: 1px solid #24518a;
            border-left: 3px solid var(--accent);
            border-radius: 9px;
            background: rgba(37, 99, 235, 0.11);
            color: #dbeafe;
        }

        .recommendation span {
            color: #93c5fd;
        }

        .alert-note {
            padding: 0.7rem 0.85rem;
            border: 1px solid rgba(180, 139, 69, 0.35);
            border-radius: 10px;
            background: rgba(180, 139, 69, 0.07);
            color: #c9b995;
            font-size: 0.87rem;
        }

        [data-testid="stMetric"] {
            padding: 0.8rem 1rem;
            background: rgba(37, 99, 235, 0.08);
            border: 1px solid rgba(96, 165, 250, 0.22);
            border-radius: 12px;
        }

        [data-testid="stMetricLabel"] p {
            color: var(--text-secondary);
        }

        [data-testid="stMetricValue"] {
            color: #93c5fd;
        }

        [data-testid="stProgress"] > div > div {
            background: var(--accent-strong);
        }

        [data-testid="stProgress"] > div {
            background: #202c3d;
            border-radius: 999px;
        }

        [data-testid="stAlert"] {
            border-radius: 9px;
        }

        .stButton > button,
        [data-testid="stDownloadButton"] > button {
            min-height: 2.9rem;
            border-radius: 9px;
            font-weight: 620;
            transition: background-color 160ms ease, border-color 160ms ease;
        }

        .stButton > button[kind="primary"] {
            background: var(--accent-strong);
            border-color: var(--accent-strong);
            color: white;
            box-shadow: 0 6px 18px rgba(37, 99, 235, 0.2);
        }

        .stButton > button[kind="primary"]:hover {
            background: #1d4ed8;
            border-color: #3b82f6;
            transform: translateY(-1px);
        }

        [data-testid="stJson"] {
            border: 1px solid var(--border);
            border-radius: 10px;
            overflow: hidden;
        }

        @media (max-width: 640px) {
            .block-container {
                padding: 1.35rem 1rem 2.5rem;
            }

            .page-header h1 {
                font-size: 1.45rem;
            }

            .criterion-question {
                min-height: auto;
                padding-bottom: 0.35rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


st.set_page_config(
    page_title="Avaliação de Transição de Nível de Cuidado",
    layout="wide",
)
aplicar_estilos()


# =========================================================
# Constantes
# =========================================================

ESTADOS = [
    "UTI",
    "Semi-UTI",
    "Enfermaria",
    "Home Care",
]

DIRECOES = [
    "Manter",
    "Desescalonar",
    "Escalonar",
]

ORDEM_ESTADOS = {
    "Home Care": 0,
    "Enfermaria": 1,
    "Semi-UTI": 2,
    "UTI": 3,
}

ESTADOS_POR_NIVEL = {
    0: "Home Care",
    1: "Enfermaria",
    2: "Semi-UTI",
    3: "UTI",
}

CRITERIOS_SEGURANCA = {
    "estabilidade_hemodinamica":
        "O paciente apresenta estabilidade hemodinâmica?",

    "sem_suporte_ventilatorio":
        "O paciente está sem necessidade de suporte ventilatório?",

    "sem_drogas_vasoativas":
        "O paciente está sem uso de drogas vasoativas?",

    "nivel_consciencia_preservado":
        "O nível de consciência está preservado?",

    "dor_controlada_via_oral":
        "A dor está controlada com medicação por via oral?",

    "aceitacao_dieta_oral":
        "Há boa aceitação de dieta por via oral?",

    "mobilidade_compativel_proximo_nivel":
        "A mobilidade do paciente é compatível com o próximo nível de cuidado?",

    "suporte_familiar_disponivel":
        "Há suporte familiar disponível para dar continuidade ao cuidado?",
}

CRITERIOS_ALERTA = {
    "sinais_instabilidade_aguda":
        "Há sinais de instabilidade aguda?",

    "necessidade_monitorizacao_continua":
        "Há necessidade de monitorização contínua?",
}


# =========================================================
# Funções
# =========================================================

def calcular_estado_recomendado(
    estado_atual: str,
    direcao_transicao: str,
) -> str:
    nivel_atual = ORDEM_ESTADOS[estado_atual]

    if direcao_transicao == "Manter":
        novo_nivel = nivel_atual

    elif direcao_transicao == "Desescalonar":
        novo_nivel = max(0, nivel_atual - 1)

    elif direcao_transicao == "Escalonar":
        novo_nivel = min(3, nivel_atual + 1)

    else:
        novo_nivel = nivel_atual

    return ESTADOS_POR_NIVEL[novo_nivel]


def resposta_para_bool(resposta: str) -> bool | None:
    if resposta == "Sim":
        return True

    if resposta == "Não":
        return False

    return None


def calcular_pontuacao(
    criterios_seguranca: dict,
    criterios_alerta: dict,
) -> int:
    qtd_seguranca_sim = sum(
        valor is True
        for valor in criterios_seguranca.values()
    )

    qtd_alerta_sim = sum(
        valor is True
        for valor in criterios_alerta.values()
    )

    pontuacao = qtd_seguranca_sim - (2 * qtd_alerta_sim)

    return max(0, min(10, pontuacao))


def exibir_cabecalho_secao(titulo: str, descricao: str) -> None:
    st.markdown(
        f"""
        <div class="section-heading">
            <h2>{titulo}</h2>
            <p>{descricao}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# Cabeçalho
# =========================================================

st.markdown(
    """
    <header class="page-header">
        <h1>Avaliação de Transição de Nível de Cuidado</h1>
        <p>Formulário para avaliação da possibilidade de mudança do nível de cuidado do paciente.</p>
    </header>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# Identificação
# =========================================================

# Mock temporário enquanto não conectamos ao Databricks
PACIENTES_POR_INTERNACAO = {
    "INT-001": {
        "id_paciente": "paciente-001",
        "nome": "Paciente 001",
    },
    "INT-002": {
        "id_paciente": "paciente-002",
        "nome": "Paciente 002",
    },
    "INT-003": {
        "id_paciente": "paciente-003",
        "nome": "Paciente 003",
    },
}

# Mock do usuário autenticado
id_profissional = "profissional-001"
nome_profissional = "Dra. Camila Rocha"

with st.container(border=True):
    exibir_cabecalho_secao(
        "1. Identificação",
        "Selecione o contexto assistencial e confira os dados vinculados.",
    )

    col1, col2 = st.columns(2, gap="large")

    with col1:
        hospital = st.selectbox(
            "Hospital *",
            [
                "Selecione...",
                "Hospital Vida Nova",
                "Hospital Central",
                "Hospital Regional",
            ],
        )

    with col2:
        id_internacao = st.selectbox(
            "Internação ativa *",
            [
                "Selecione...",
                "INT-001",
                "INT-002",
                "INT-003",
            ],
        )

    if id_internacao != "Selecione...":
        paciente = PACIENTES_POR_INTERNACAO[id_internacao]
        col1, col2 = st.columns(2, gap="large")

        with col1:
            st.text_input(
                "ID do paciente",
                value=paciente["id_paciente"],
                disabled=True,
            )

        with col2:
            st.text_input(
                "Paciente",
                value=paciente["nome"],
                disabled=True,
            )

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.text_input(
            "ID do profissional",
            value=id_profissional,
            disabled=True,
        )

    with col2:
        st.text_input(
            "Profissional",
            value=nome_profissional,
            disabled=True,
        )


# =========================================================
# Estado atual e transição
# =========================================================

with st.container(border=True):
    exibir_cabecalho_secao(
        "2. Estado atual e direção da transição",
        "Informe o nível vigente e a conduta considerada para a continuidade do cuidado.",
    )

    col1, col2 = st.columns(2, gap="large")

    with col1:
        estado_atual = st.selectbox("Estado atual *", ESTADOS)

    with col2:
        direcao_transicao = st.radio(
            "Direção da transição *",
            DIRECOES,
            horizontal=True,
        )

    estado_recomendado = calcular_estado_recomendado(
        estado_atual,
        direcao_transicao,
    )

    st.markdown(
        f"""
        <div class="recommendation">
            <span>Estado recomendado</span><br>
            <strong>{estado_recomendado}</strong>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# Critérios de segurança
# =========================================================

respostas_seguranca = {}

with st.container(border=True):
    exibir_cabecalho_secao(
        "3. Critérios de segurança",
        "Todos os critérios abaixo são obrigatórios.",
    )

    for campo, pergunta in CRITERIOS_SEGURANCA.items():
        col_pergunta, col_resposta = st.columns([2.2, 1], gap="large")

        with col_pergunta:
            st.markdown(
                f'<div class="criterion-question">{pergunta}</div>',
                unsafe_allow_html=True,
            )

        with col_resposta:
            resposta = st.radio(
                pergunta,
                ["Selecione...", "Sim", "Não"],
                key=campo,
                horizontal=True,
                label_visibility="collapsed",
            )

        respostas_seguranca[campo] = resposta_para_bool(resposta)


# =========================================================
# Critérios de alerta
# =========================================================

respostas_alerta = {}

with st.container(border=True):
    exibir_cabecalho_secao(
        "4. Critérios de alerta",
        "Sinais que exigem atenção adicional na decisão de transição.",
    )

    st.markdown(
        '<div class="alert-note">Cada resposta “Sim” reduz a pontuação de segurança.</div>',
        unsafe_allow_html=True,
    )

    for campo, pergunta in CRITERIOS_ALERTA.items():
        col_pergunta, col_resposta = st.columns([2.2, 1], gap="large")

        with col_pergunta:
            st.markdown(
                f'<div class="criterion-question">{pergunta}</div>',
                unsafe_allow_html=True,
            )

        with col_resposta:
            resposta = st.radio(
                pergunta,
                ["Selecione...", "Sim", "Não"],
                key=campo,
                horizontal=True,
                label_visibility="collapsed",
            )

        respostas_alerta[campo] = resposta_para_bool(resposta)


# =========================================================
# Pontuação
# =========================================================

pontuacao_seguranca = calcular_pontuacao(
    respostas_seguranca,
    respostas_alerta,
)

with st.container(border=True):
    exibir_cabecalho_secao(
        "5. Pontuação de segurança",
        "Resultado automático calculado a partir dos critérios informados.",
    )

    col1, col2 = st.columns([1, 3], gap="large", vertical_alignment="center")

    with col1:
        st.metric("Pontuação", f"{pontuacao_seguranca} / 10")

    with col2:
        st.progress(pontuacao_seguranca / 10)


# =========================================================
# Justificativa
# =========================================================

with st.container(border=True):
    exibir_cabecalho_secao(
        "6. Justificativa clínica",
        "Documente o raciocínio clínico que sustenta a conduta selecionada.",
    )

    justificativa = st.text_area(
        "Justificativa *",
        placeholder=(
            "Registre o raciocínio clínico que fundamenta "
            "a direção de transição escolhida."
        ),
        height=180,
    )

    data_prevista_transicao = None

    if direcao_transicao in ["Desescalonar", "Escalonar"]:
        st.markdown("#### Data prevista da transição")
        data_prevista_transicao = st.date_input(
            "Data prevista para transição *"
        )

    st.markdown("#### Observações")
    observacoes = st.text_area(
        "Observações",
        placeholder="Informações adicionais...",
        height=120,
    )


# =========================================================
# Envio
# =========================================================

enviar = st.button(
    "Registrar avaliação",
    type="primary",
    use_container_width=True,
)


if enviar:
    erros = []

    # -----------------------------------------------------
    # Validações
    # -----------------------------------------------------

    if hospital == "Selecione...":
        erros.append(
            "Selecione o hospital."
        )

    if id_internacao == "Selecione...":
        erros.append(
            "Selecione uma internação ativa."
        )

    if any(
        valor is None
        for valor in respostas_seguranca.values()
    ):
        erros.append(
            "Responda todos os critérios de segurança."
        )

    if any(
        valor is None
        for valor in respostas_alerta.values()
    ):
        erros.append(
            "Responda todos os critérios de alerta."
        )

    if not justificativa.strip():
        erros.append(
            "Informe a justificativa clínica."
        )

    if (
        direcao_transicao in [
            "Desescalonar",
            "Escalonar",
        ]
        and data_prevista_transicao is None
    ):
        erros.append(
            "Informe a data prevista para transição."
        )


    # -----------------------------------------------------
    # Resultado
    # -----------------------------------------------------

    if erros:
        st.error(
            "Não foi possível registrar a avaliação."
        )

        for erro in erros:
            st.warning(erro)

    else:
        id_formulario = str(uuid.uuid4())

        paciente = PACIENTES_POR_INTERNACAO[
            id_internacao
        ]

        data_avaliacao = (
            datetime
            .now(timezone.utc)
            .replace(microsecond=0)
            .isoformat()
            .replace("+00:00", "Z")
        )

        criterios_avaliados = {
            **respostas_seguranca,
            **respostas_alerta,
        }

        registro = {
            "id_formulario": id_formulario,
            "id_internacao": id_internacao,
            "id_paciente": paciente["id_paciente"],
            "id_profissional": id_profissional,
            "nome_profissional": nome_profissional,
            "data_avaliacao": data_avaliacao,
            "hospital": hospital,

            "estado_atual": estado_atual,
            "estado_recomendado": estado_recomendado,
            "direcao_transicao": direcao_transicao,

            "criterios_avaliados": criterios_avaliados,

            "pontuacao_seguranca": pontuacao_seguranca,

            "justificativa": justificativa.strip(),

            "data_prevista_transicao": (
                data_prevista_transicao.isoformat()
                if data_prevista_transicao
                else None
            ),

            "observacoes": observacoes.strip(),
        }

        st.success(
            "Avaliação registrada com sucesso."
        )

        st.subheader("JSON gerado")

        st.json(registro)

        nome_arquivo = (
            f"{data_avaliacao[:10]}_"
            f"{id_formulario}.json"
        )

        st.download_button(
            label="Baixar JSON",
            data=json.dumps(
                registro,
                indent=2,
                ensure_ascii=False,
            ),
            file_name=nome_arquivo,
            mime="application/json",
        )
