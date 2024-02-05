import streamlit as st
import pandas as pd
import zipfile
from zipfile import ZipFile
from zipfile import Path
import requests as rq
from io import StringIO
from datetime import date
import webbrowser
import os
import base64

st.set_page_config(
    page_title="SIAGOV",
    page_icon="datasets/siagov.ico",
    layout="wide",
)

#@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(png_file):
    with open(png_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


def build_markup_for_logo(
    png_file,
    background_position="50% 10%",
    margin_top="10%",
    image_width="60%",
    image_height="",
):
    binary_string = get_base64_of_bin_file(png_file)
    return """
            <style>
                [data-testid="stSidebarNav"] {
                    background-image: url("data:image/png;base64,%s");
                    background-repeat: no-repeat;
                    background-position: %s;
                    margin-top: %s;
                    background-size: %s %s;
                }
            </style>
            """ % (
        binary_string,
        background_position,
        margin_top,
        image_width,
        image_height,
    )


def add_logo(png_file):
    logo_markup = build_markup_for_logo(png_file)
    st.markdown(
        logo_markup,
        unsafe_allow_html=True,
    )

add_logo("datasets/siagovlogonovo.png")

st.sidebar.image("datasets/GovPBT.png") #, width = 200)
st.sidebar.divider()

#ano = st.sidebar.selectbox('Execício:', [2023, 2024])

dataatual = date.today()
ano = dataatual.year - 1
mes = 12 #dataatual.month

# if 'ano' not in st.session_state:
#     st.session_state.ano = dataatual.year
# if 'mes' not in st.session_state:
#     st.session_state.mes = dataatual.month
# mes  = st.session_state.mes
# ano = st.session_state.ano
st.sidebar.text(f'{mes}, {ano}' )

### CARGA DE DADOS EMPENHO ORIGINAL
if dataatual.year > ano:
        mes = mes+1
@st.cache_resource
def load_empOri():
    empOrigt = []
    for i in range (1, mes):
        arq = f"files/empenho_original{ano}mes{i}.gzip"
        if os.path.isfile(arq):
                emp = pd.read_csv(arq, sep=';', encoding='ISO-8859-1', compression={'method': 'gzip', 'compresslevel': 1, 'mtime': 1}) #, index_col=[0]
                empOrigt.append(emp)
        else:
            st.write(f"Arquivo **empenho_original{ano}mes{mes}** não disponível")
    empOrigr = pd.concat(empOrigt)
    return empOrigr

@st.cache_resource
def load_empSup():
    empSupt = []
    for i in range (1, mes):
        arq = f"files/empenho_suplementacao{ano}mes{i}.gzip"
        if os.path.isfile(arq):
                emp = pd.read_csv(arq, sep=';', encoding='ISO-8859-1', compression={'method': 'gzip', 'compresslevel': 1, 'mtime': 1}) #, index_col=[0]
                empSupt.append(emp)
        else:
            st.write(f"Arquivo **empenho_suplementacao{ano}mes{mes}** não disponível")
    empSupr = pd.concat(empSupt)
    return empSupr

@st.cache_resource
def load_empAnu():
    empAnut = []
    for i in range (1, mes):
        arq = f"files/empenho_anulacao{ano}mes{i}.gzip"
        if os.path.isfile(arq):
                emp = pd.read_csv(arq, sep=';', encoding='ISO-8859-1', compression={'method': 'gzip', 'compresslevel': 1, 'mtime': 1}) #, index_col=[0]
                empAnut.append(emp)
        else:
            st.write(f"Arquivo **empenho_anulacao{ano}mes{mes}** não disponível")
    empAnur = pd.concat(empAnut)
    return empAnur

@st.cache_resource
def load_pagAnu():
    pagAnut = []
    for i in range (1, mes):
        arq = f"files/pagamento_anulacao{ano}mes{i}.gzip"
        if os.path.isfile(arq):
                emp = pd.read_csv(arq, sep=';', encoding='ISO-8859-1', compression={'method': 'gzip', 'compresslevel': 1, 'mtime': 1}) #, index_col=[0]
                pagAnut.append(emp)
        else:
            st.write(f"Arquivo **pagamento_anulacao{ano}mes{mes}** não disponível")
    pagAnur = pd.concat(pagAnut)
    return pagAnur
###################################
### TRATAMENTO DOS EMPENHOS ###
#tab1, tab2, tab3, tab4 = st.tabs(['`Empenhos Originários`', '`Empenhos Suplementação`','`Empenhos Anulações`','`Pagamento Anulações`'])
#with tab1:
#st.subheader('`Empenhos Originários`')
totEmpOrig = load_empOri()
totEmpOrig["CODIGO_MODALIDADE_LICITACAO"] = totEmpOrig["CODIGO_MODALIDADE_LICITACAO"].fillna(0)
#st.dataframe(totEmpOrig)
st.session_state["orig"] = totEmpOrig
#with tab2:
#st.subheader('`Empenhos Suplementação`')
totEmpSup = load_empSup()
#st.write(totEmpSup)
st.session_state["sup"] = totEmpSup
#with tab3:
#st.subheader('`Empenhos Anulações`')
totEmpAnu = load_empAnu()
totEmpAnu['VALOR_EMPENHO'] = -totEmpAnu['VALOR_EMPENHO']
#st.write(totEmpAnu)
st.session_state["anuE"] = totEmpAnu
#with tab4:
#st.subheader('`Pagamento Anulações`')
totPagAnu = load_pagAnu()
colunas = ['CODIGO_UNIDADE_GESTORA', 'NUMERO_EMPENHO', 'VALOR_EMPENHO','DATA_DOCUMENTO']
totPagAnu['VALOR_EMPENHO'] = -totPagAnu['VALOR_DOCUMENTO']
totPagAnu['DATA_DOCUMENTO'] = pd.to_datetime(totPagAnu['DATA_DOCUMENTO'])#, format="%B", errors='ignore') #format="ISO8601" OU mixed
#totPagAnu['MES_DOCUMENTO'] = pd.DataFrame({"MES_DOCUMENTO": pd.to_datetime(totPagAnu['DATA_DOCUMENTO'])})
#totPagAnu['MES'] = totPagAnu['MES_DOCUMENTO'].dt.month
totPagAnu['MES_DOCUMENTO'] = totPagAnu['DATA_DOCUMENTO'].dt.month_name()
totPagAnu['NUM_MES_DOCUMENTO'] = totPagAnu['DATA_DOCUMENTO'].dt.month #.dt.month_name()
#st.write(totPagAnu)
st.session_state["anuP"] = totPagAnu

##############################

####### ENCONTRAR O INDEX DA UNID GESTORA 270001 ##############
df = pd.DataFrame(totEmpOrig["CODIGO_UNIDADE_GESTORA"].unique())
df.reset_index(inplace=True)
df.rename(columns={0:'nome'}, inplace=True)
#st.dataframe(df)
dfnome = df.query(f"nome == 270001")
dfnometx = format(int(dfnome.sum(numeric_only=True)['index']))
#st.write(dfnometx)
ugs = st.sidebar.selectbox("Código da Unidade Gestora", totEmpOrig["CODIGO_UNIDADE_GESTORA"].unique(), index=int(dfnometx), help="Unidade Gestora", placeholder="Selecione Unidade Gestora")

licita = sorted(totEmpOrig.query(f"CODIGO_UNIDADE_GESTORA == {ugs}")["CODIGO_MODALIDADE_LICITACAO"].unique())
modLicita = st.sidebar.multiselect("Código Modalidade Licitação", licita, default=licita, help="Escolha a modalidade de licitação disponível")
st.sidebar.divider()
codAcao = st.sidebar.multiselect("Código da Ação", sorted(totEmpOrig.query(f"CODIGO_UNIDADE_GESTORA == {ugs} & CODIGO_MODALIDADE_LICITACAO == {modLicita}")["CODIGO_ACAO"].unique()), placeholder="Seleção Opcional")
codFonte = st.sidebar.multiselect("Código Fonte de Recurso", sorted(totEmpOrig.query(f"CODIGO_UNIDADE_GESTORA == {ugs} & CODIGO_MODALIDADE_LICITACAO == {modLicita}")["CODIGO_FONTE_RECURSO"].unique()), placeholder="Seleção Opcional")
codNatDesp = st.sidebar.multiselect("Código Natureza da Despesa", sorted(totEmpOrig.query(f"CODIGO_UNIDADE_GESTORA == {ugs} & CODIGO_MODALIDADE_LICITACAO == {modLicita}")["CODIGO_NATUREZA_DESPESA"].unique()), placeholder="Seleção Opcional")
codItemDesp = st.sidebar.multiselect("Código Item da Despesa", sorted(totEmpOrig.query(f"CODIGO_UNIDADE_GESTORA == {ugs} & CODIGO_MODALIDADE_LICITACAO == {modLicita}")["CODIGO_ITEM_DESPESA"].unique()), placeholder="Seleção Opcional")
# st.write(codAcao)
# st.write(codNatDesp)
# st.write(codItemDesp)
if codAcao == [] and codFonte == [] and codNatDesp == [] and codItemDesp == []:
     consulta = totEmpOrig.query(f"CODIGO_UNIDADE_GESTORA == {ugs} & CODIGO_MODALIDADE_LICITACAO == {modLicita}")
else:
     consulta = totEmpOrig.query(f"CODIGO_UNIDADE_GESTORA == {ugs} & CODIGO_MODALIDADE_LICITACAO == {modLicita} & (CODIGO_ACAO in {codAcao} | CODIGO_FONTE_RECURSO in {codFonte} | CODIGO_NATUREZA_DESPESA in {codNatDesp} | CODIGO_ITEM_DESPESA in {codItemDesp})")

if st.sidebar.button('Limpar Cache'):
     st.cache_resource.clear()

arq = f"files/unidade_gestora_2023.gzip"
if os.path.isfile(arq):
        unidGestora = pd.read_csv(arq, sep=';', encoding='ISO-8859-1', compression={'method': 'gzip', 'compresslevel': 1, 'mtime': 1})

elementoFiltro = unidGestora[unidGestora["CODIGO_UNIDADE_GESTORA"] == ugs].iloc[0]
st.subheader(f"{elementoFiltro['CODIGO_UNIDADE_GESTORA']} - {elementoFiltro['SIGLA_UNIDADE_GESTORA']}")
st.header(f"{elementoFiltro['NOME_UNIDADE_GESTORA']}", divider='blue')
st.caption(f'Dados de janeiro a dezembro de {ano}')
#st.write(st.session_state["orig"].query((f"CODIGO_UNIDADE_GESTORA == {ugs}")))

st.dataframe(consulta)

col1, col2, col3, col4 = st.columns(4)
with col1:
    with st.expander("Código da Ação selecionadas"):
        st.write(consulta["CODIGO_ACAO"].unique())
with col2:
    with st.expander("Código Fonte de Recurso selecionadas"):
        st.write(consulta["CODIGO_FONTE_RECURSO"].unique())
with col3:
    with st.expander("Natureza da Despesa selecionadas"):
        st.write(consulta["CODIGO_NATUREZA_DESPESA"].unique())
with col4:
    with st.expander("Item da Despesa selecionadas"):
        st.write(consulta["CODIGO_ITEM_DESPESA"].unique())

st.divider()


#### FOOTER SIDEBAR #####
st.sidebar.divider()
st.sidebar.markdown('Desenvolvido por [SIAGOV](https://siagov.com.br)')
st.sidebar.text('S712')