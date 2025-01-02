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
#import matplotlib.pyplot as plt


st.set_page_config(
    page_title="SIAGOV",
    page_icon="datasets/siagov.ico",
    layout="wide",
)

with open('styles.css') as fcss:
    st.markdown(f"<style>{fcss.read()}</style>", unsafe_allow_html=True)

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


# def add_logo(png_file):
#     logo_markup = build_markup_for_logo(png_file)
#     st.markdown(
#         logo_markup,
#         unsafe_allow_html=True,
#     )

# add_logo("datasets/siagovlogonovo.png")
st.image("datasets/siagovlogonovo.png", width=300)

imagemlogosidebar = "datasets/siagov.ico"
logoprincipal = "datasets/siagov.ico"
st.logo(imagemlogosidebar, icon_image = logoprincipal)
st.sidebar.image("datasets/GovPBT.png") #, width = 200)
st.sidebar.divider()

#ano = st.sidebar.selectbox('Execício:', [2023, 2024])

dataatual = date.today()
ano = 2024 #dataatual.year
mesA = 13 #dataatual.month

# if 'ano' not in st.session_state:
#     st.session_state.ano = dataatual.year
# if 'mes' not in st.session_state:
#     st.session_state.mes = dataatual.month
# mes  = st.session_state.mes
# ano = st.session_state.ano
st.sidebar.text(f'{mesA}, {ano}' )

### CARGA DE DADOS EMPENHO ORIGINAL
if dataatual.year > ano:
        mes = mesA + 1

@st.cache_resource
def load_empOri2024():
    empOrigt = []
    for i in range (1, mesA):
        arq = f"files/empenho_original{ano}mes{i}.gzip"
        if os.path.isfile(arq):
                emp = pd.read_csv(arq, sep=';', encoding='ISO-8859-1', compression={'method': 'gzip', 'compresslevel': 1, 'mtime': 1}) #, index_col=[0]
                empOrigt.append(emp)
        #else:
            #st.write(f"Arquivo **empenho_original{ano}mes{mesA}** não disponível")
    empOrigr = pd.concat(empOrigt)
    empOrigr["CODIGO_MODALIDADE_LICITACAO"] = empOrigr["CODIGO_MODALIDADE_LICITACAO"].fillna(0)
    empOrigr["CODIGO_ACAO"] = empOrigr["CODIGO_ACAO"].fillna(0)
    empOrigr["CODIGO_FONTE_RECURSO"] = empOrigr["CODIGO_FONTE_RECURSO"].fillna(0)
    empOrigr["CODIGO_ITEM_DESPESA"] = empOrigr["CODIGO_ITEM_DESPESA"].fillna(0)
    return empOrigr

@st.cache_resource
def load_empSup2024():
    empSupt = []
    for i in range (1, mesA):
        arq = f"files/empenho_suplementacao{ano}mes{i}.gzip"
        if os.path.isfile(arq):
                emp = pd.read_csv(arq, sep=';', encoding='ISO-8859-1', compression={'method': 'gzip', 'compresslevel': 1, 'mtime': 1}) #, index_col=[0]
                empSupt.append(emp)
        #else:
            #st.write(f"Arquivo **empenho_suplementacao{ano}mes{mesA}** não disponível")
    empSupr = pd.concat(empSupt)
    empSupr["CODIGO_MODALIDADE_LICITACAO"] = empSupr["CODIGO_MODALIDADE_LICITACAO"].fillna(0)
    empSupr["CODIGO_ACAO"] = empSupr["CODIGO_ACAO"].fillna(0)
    empSupr["CODIGO_FONTE_RECURSO"] = empSupr["CODIGO_FONTE_RECURSO"].fillna(0)
    empSupr["CODIGO_ITEM_DESPESA"] = empSupr["CODIGO_ITEM_DESPESA"].fillna(0)
    return empSupr

@st.cache_resource
def load_empAnu2024():
    empAnut = []
    for i in range (1, mesA):
        arq = f"files/empenho_anulacao{ano}mes{i}.gzip"
        if os.path.isfile(arq):
                emp = pd.read_csv(arq, sep=';', encoding='ISO-8859-1', compression={'method': 'gzip', 'compresslevel': 1, 'mtime': 1}) #, index_col=[0]
                empAnut.append(emp)
        #else:
            #st.write(f"Arquivo **empenho_anulacao{ano}mes{mesA}** não disponível")
    empAnur = pd.concat(empAnut)
    empAnur["CODIGO_MODALIDADE_LICITACAO"] = empAnur["CODIGO_MODALIDADE_LICITACAO"].fillna(0)
    empAnur["CODIGO_ACAO"] = empAnur["CODIGO_ACAO"].fillna(0)
    empAnur["CODIGO_FONTE_RECURSO"] = empAnur["CODIGO_FONTE_RECURSO"].fillna(0)
    empAnur["CODIGO_ITEM_DESPESA"] = empAnur["CODIGO_ITEM_DESPESA"].fillna(0)
    empAnur['VALOR_EMPENHO'] = -empAnur['VALOR_EMPENHO']
    return empAnur

@st.cache_resource
def load_pagAnu2024():
    pagAnut = []
    for i in range (1, mesA):
        arq = f"files/pagamento_anulacao{ano}mes{i}.gzip"
        if os.path.isfile(arq):
                emp = pd.read_csv(arq, sep=';', encoding='ISO-8859-1', compression={'method': 'gzip', 'compresslevel': 1, 'mtime': 1}) #, index_col=[0]
                pagAnut.append(emp)
        #else:
            #st.write(f"Arquivo **pagamento_anulacao{ano}mes{mesA}** não disponível")
    pagAnur = pd.concat(pagAnut)
    pagAnur['VALOR_EMPENHO'] = -pagAnur['VALOR_DOCUMENTO']
    pagAnur['DATA_DOCUMENTO'] = pd.to_datetime(pagAnur['DATA_DOCUMENTO'])#, format="%B", errors='ignore') #format="ISO8601" OU mixed
    pagAnur['MES_DOCUMENTO'] = pagAnur['DATA_DOCUMENTO'].dt.month_name()
    pagAnur['NUM_MES_DOCUMENTO'] = pagAnur['DATA_DOCUMENTO'].dt.month #.dt.month_name()
    return pagAnur
###################################
### TRATAMENTO DOS EMPENHOS ###
#tab1, tab2, tab3, tab4 = st.tabs(['`Empenhos Originários`', '`Empenhos Suplementação`','`Empenhos Anulações`','`Pagamento Anulações`'])
#with tab1:
#st.subheader('`Empenhos Originários`')
totEmpOrig = load_empOri2024()
# totEmpOrig["CODIGO_MODALIDADE_LICITACAO"] = totEmpOrig["CODIGO_MODALIDADE_LICITACAO"].fillna(0)
# totEmpOrig["CODIGO_ACAO"] = totEmpOrig["CODIGO_ACAO"].fillna(0)
# totEmpOrig["CODIGO_FONTE_RECURSO"] = totEmpOrig["CODIGO_FONTE_RECURSO"].fillna(0)
# totEmpOrig["CODIGO_ITEM_DESPESA"] = totEmpOrig["CODIGO_ITEM_DESPESA"].fillna(0)
#st.dataframe(totEmpOrig)
#st.session_state["orig2024"] = totEmpOrig
#with tab2:
#st.subheader('`Empenhos Suplementação`')
totEmpSup = load_empSup2024()
# totEmpSup["CODIGO_MODALIDADE_LICITACAO"] = totEmpSup["CODIGO_MODALIDADE_LICITACAO"].fillna(0)
# totEmpSup["CODIGO_ACAO"] = totEmpSup["CODIGO_ACAO"].fillna(0)
# totEmpSup["CODIGO_FONTE_RECURSO"] = totEmpSup["CODIGO_FONTE_RECURSO"].fillna(0)
# totEmpSup["CODIGO_ITEM_DESPESA"] = totEmpSup["CODIGO_ITEM_DESPESA"].fillna(0)
#st.write(totEmpSup)
#st.session_state["sup2024"] = totEmpSup
#with tab3:
#st.subheader('`Empenhos Anulações`')
totEmpAnu = load_empAnu2024()
# totEmpAnu["CODIGO_MODALIDADE_LICITACAO"] = totEmpAnu["CODIGO_MODALIDADE_LICITACAO"].fillna(0)
# totEmpAnu["CODIGO_ACAO"] = totEmpAnu["CODIGO_ACAO"].fillna(0)
# totEmpAnu["CODIGO_FONTE_RECURSO"] = totEmpAnu["CODIGO_FONTE_RECURSO"].fillna(0)
# totEmpAnu["CODIGO_ITEM_DESPESA"] = totEmpAnu["CODIGO_ITEM_DESPESA"].fillna(0)
# totEmpAnu['VALOR_EMPENHO'] = -totEmpAnu['VALOR_EMPENHO']
#st.write(totEmpAnu)
#st.session_state["anuE2024"] = totEmpAnu
#with tab4:
#st.subheader('`Pagamento Anulações`')
totPagAnu = load_pagAnu2024()
# colunas = ['CODIGO_UNIDADE_GESTORA', 'NUMERO_EMPENHO', 'VALOR_EMPENHO','DATA_DOCUMENTO']
# totPagAnu['VALOR_EMPENHO'] = -totPagAnu['VALOR_DOCUMENTO']
# totPagAnu['DATA_DOCUMENTO'] = pd.to_datetime(totPagAnu['DATA_DOCUMENTO'])#, format="%B", errors='ignore') #format="ISO8601" OU mixed
# #totPagAnu['MES_DOCUMENTO'] = pd.DataFrame({"MES_DOCUMENTO": pd.to_datetime(totPagAnu['DATA_DOCUMENTO'])})
# #totPagAnu['MES'] = totPagAnu['MES_DOCUMENTO'].dt.month
# totPagAnu['MES_DOCUMENTO'] = totPagAnu['DATA_DOCUMENTO'].dt.month_name()
# totPagAnu['NUM_MES_DOCUMENTO'] = totPagAnu['DATA_DOCUMENTO'].dt.month #.dt.month_name()
#st.write(totPagAnu)
#st.session_state["anuP2024"] = totPagAnu

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
if modLicita == []:
     modLicita = sorted(totEmpOrig.query(f"CODIGO_UNIDADE_GESTORA == {ugs}")["CODIGO_MODALIDADE_LICITACAO"].unique())
st.sidebar.divider()
#st.sidebar.caption('Filtros de Seleção')
codAcaoE = st.sidebar.selectbox("Código da Ação", sorted(totEmpOrig.query(f"CODIGO_UNIDADE_GESTORA == {ugs} & CODIGO_MODALIDADE_LICITACAO == {modLicita}")["CODIGO_ACAO"].unique()), placeholder="Seleção Opcional")
codFonteE = st.sidebar.multiselect("Código Fonte de Recurso", sorted(totEmpOrig.query(f"CODIGO_UNIDADE_GESTORA == {ugs} & CODIGO_MODALIDADE_LICITACAO == {modLicita} & CODIGO_ACAO == {codAcaoE} ")["CODIGO_FONTE_RECURSO"].unique()), placeholder="Seleção Opcional")
codNatDespE = st.sidebar.multiselect("Código Natureza da Despesa", sorted(totEmpOrig.query(f"CODIGO_UNIDADE_GESTORA == {ugs} & CODIGO_MODALIDADE_LICITACAO == {modLicita} & CODIGO_ACAO == {codAcaoE} & CODIGO_FONTE_RECURSO == {codFonteE}")["CODIGO_NATUREZA_DESPESA"].unique()), placeholder="Seleção Opcional")
codItemDespE = st.sidebar.multiselect("Código Item da Despesa", sorted(totEmpOrig.query(f"CODIGO_UNIDADE_GESTORA == {ugs} & CODIGO_MODALIDADE_LICITACAO == {modLicita} & CODIGO_ACAO == {codAcaoE} & CODIGO_FONTE_RECURSO == {codFonteE} & CODIGO_NATUREZA_DESPESA == {codNatDespE}")["CODIGO_ITEM_DESPESA"].unique()), placeholder="Seleção Opcional")

st.sidebar.divider()

#st.sidebar.caption('Filtros de Combinação')
#codAcao = st.sidebar.multiselect("Código da Ação", sorted(totEmpOrig.query(f"CODIGO_UNIDADE_GESTORA == {ugs} & CODIGO_MODALIDADE_LICITACAO == {modLicita}")["CODIGO_ACAO"].unique()), placeholder="Seleção Opcional")
#codFonte = st.sidebar.multiselect("Código Fonte de Recurso", sorted(totEmpOrig.query(f"CODIGO_UNIDADE_GESTORA == {ugs} & CODIGO_MODALIDADE_LICITACAO == {modLicita}")["CODIGO_FONTE_RECURSO"].unique()), placeholder="Seleção Opcional")
#codNatDesp = st.sidebar.multiselect("Código Natureza da Despesa", sorted(totEmpOrig.query(f"CODIGO_UNIDADE_GESTORA == {ugs} & CODIGO_MODALIDADE_LICITACAO == {modLicita}")["CODIGO_NATUREZA_DESPESA"].unique()), placeholder="Seleção Opcional")
#codItemDesp = st.sidebar.multiselect("Código Item da Despesa", sorted(totEmpOrig.query(f"CODIGO_UNIDADE_GESTORA == {ugs} & CODIGO_MODALIDADE_LICITACAO == {modLicita}")["CODIGO_ITEM_DESPESA"].unique()), placeholder="Seleção Opcional")
# st.write(codAcao)
# st.write(codNatDesp)
# st.write(codItemDesp)
if codAcaoE != "" and codFonteE != [] and codNatDespE != [] and codItemDespE != []:
     consulta = totEmpOrig.query(f"CODIGO_UNIDADE_GESTORA == {ugs} & CODIGO_MODALIDADE_LICITACAO == {modLicita} & CODIGO_ACAO == {codAcaoE} & CODIGO_FONTE_RECURSO == {codFonteE} & CODIGO_NATUREZA_DESPESA == {codNatDespE} & CODIGO_ITEM_DESPESA == {codItemDespE}")
     consultaSupl = totEmpSup.query(f"CODIGO_UNIDADE_GESTORA == {ugs} & CODIGO_MODALIDADE_LICITACAO == {modLicita} & CODIGO_ACAO == {codAcaoE} & CODIGO_FONTE_RECURSO == {codFonteE} & CODIGO_NATUREZA_DESPESA == {codNatDespE} & CODIGO_ITEM_DESPESA == {codItemDespE}")
     consultaEmpAnu = totEmpAnu.query(f"CODIGO_UNIDADE_GESTORA == {ugs} & CODIGO_MODALIDADE_LICITACAO == {modLicita} & CODIGO_ACAO == {codAcaoE} & CODIGO_FONTE_RECURSO == {codFonteE} & CODIGO_NATUREZA_DESPESA == {codNatDespE} & CODIGO_ITEM_DESPESA == {codItemDespE}")
     consultaPagAnu = totPagAnu.query(f"CODIGO_UNIDADE_GESTORA == {ugs}")
elif codAcaoE != "" and codFonteE != [] and codNatDespE != []:
     consulta = totEmpOrig.query(f"CODIGO_UNIDADE_GESTORA == {ugs} & CODIGO_MODALIDADE_LICITACAO == {modLicita} & CODIGO_ACAO == {codAcaoE} & CODIGO_FONTE_RECURSO == {codFonteE} & CODIGO_NATUREZA_DESPESA == {codNatDespE}")
     consultaSupl = totEmpSup.query(f"CODIGO_UNIDADE_GESTORA == {ugs} & CODIGO_MODALIDADE_LICITACAO == {modLicita} & CODIGO_ACAO == {codAcaoE} & CODIGO_FONTE_RECURSO == {codFonteE} & CODIGO_NATUREZA_DESPESA == {codNatDespE}")
     consultaEmpAnu = totEmpAnu.query(f"CODIGO_UNIDADE_GESTORA == {ugs} & CODIGO_MODALIDADE_LICITACAO == {modLicita} & CODIGO_ACAO == {codAcaoE} & CODIGO_FONTE_RECURSO == {codFonteE} & CODIGO_NATUREZA_DESPESA == {codNatDespE}")
     consultaPagAnu = totPagAnu.query(f"CODIGO_UNIDADE_GESTORA == {ugs}")
elif codAcaoE != "" and codFonteE != []:
     consulta = totEmpOrig.query(f"CODIGO_UNIDADE_GESTORA == {ugs} & CODIGO_MODALIDADE_LICITACAO == {modLicita} & CODIGO_ACAO == {codAcaoE} & CODIGO_FONTE_RECURSO == {codFonteE}")
     consultaSupl = totEmpSup.query(f"CODIGO_UNIDADE_GESTORA == {ugs} & CODIGO_MODALIDADE_LICITACAO == {modLicita} & CODIGO_ACAO == {codAcaoE} & CODIGO_FONTE_RECURSO == {codFonteE}")
     consultaEmpAnu = totEmpAnu.query(f"CODIGO_UNIDADE_GESTORA == {ugs} & CODIGO_MODALIDADE_LICITACAO == {modLicita} & CODIGO_ACAO == {codAcaoE} & CODIGO_FONTE_RECURSO == {codFonteE}")
     consultaPagAnu = totPagAnu.query(f"CODIGO_UNIDADE_GESTORA == {ugs}")
elif codAcaoE != "":
     consulta = totEmpOrig.query(f"CODIGO_UNIDADE_GESTORA == {ugs} & CODIGO_MODALIDADE_LICITACAO == {modLicita} & CODIGO_ACAO == {codAcaoE}")
     consultaSupl = totEmpSup.query(f"CODIGO_UNIDADE_GESTORA == {ugs} & CODIGO_MODALIDADE_LICITACAO == {modLicita} & CODIGO_ACAO == {codAcaoE}")
     consultaEmpAnu = totEmpAnu.query(f"CODIGO_UNIDADE_GESTORA == {ugs} & CODIGO_MODALIDADE_LICITACAO == {modLicita} & CODIGO_ACAO == {codAcaoE}")
     consultaPagAnu = totPagAnu.query(f"CODIGO_UNIDADE_GESTORA == {ugs}")
else:
     consulta = totEmpOrig.query(f"CODIGO_UNIDADE_GESTORA == {ugs} & CODIGO_MODALIDADE_LICITACAO == {modLicita}")
     consultaSupl = totEmpSup.query(f"CODIGO_UNIDADE_GESTORA == {ugs} & CODIGO_MODALIDADE_LICITACAO == {modLicita}")
     consultaEmpAnu = totEmpAnu.query(f"CODIGO_UNIDADE_GESTORA == {ugs} & CODIGO_MODALIDADE_LICITACAO == {modLicita}")
     consultaPagAnu = totPagAnu.query(f"CODIGO_UNIDADE_GESTORA == {ugs}")

if st.sidebar.button('Limpar Cache'):
     st.cache_resource.clear()

################## CABECALHO #####################
arq = f"files/unidade_gestora_2023.gzip"
if os.path.isfile(arq):
        unidGestora = pd.read_csv(arq, sep=';', encoding='ISO-8859-1', compression={'method': 'gzip', 'compresslevel': 1, 'mtime': 1})
mesA = mesA - 1
if mesA == 1:
    mesText = "janeiro"
elif mesA == 2:
    mesText = "fevereiro"
elif mesA == 3:
    mesText = "março"
elif mesA == 4:
    mesText = "abril"
elif mesA == 5:
    mesText = "maio"
elif mesA == 6:
    mesText = "junho"
elif mesA == 7:
    mesText = "julho"
elif mesA == 8:
    mesText = "agosto"
elif mesA == 9:
    mesText = "setembro"
elif mesA == 10:
    mesText = "outubro"
elif mesA == 11:
    mesText = "novembro"
elif mesA == 12:
    mesText = "dezembro"

elementoFiltro = unidGestora[unidGestora["CODIGO_UNIDADE_GESTORA"] == ugs].iloc[0]
st.subheader(f"{elementoFiltro['CODIGO_UNIDADE_GESTORA']} - {elementoFiltro['SIGLA_UNIDADE_GESTORA']}")
st.header(f"{elementoFiltro['NOME_UNIDADE_GESTORA']}", divider='blue')
arqAcao = f"files/acao_exercicio_2024.csv"
if os.path.isfile(arqAcao):
        nomeAcao = pd.read_csv(arqAcao, sep=';', encoding='ISO-8859-1')
nomeAcaoE = nomeAcao.query(f"CODIGO_ACAO == {codAcaoE}")
#st.write(nomeAcaoE)
elementoFiltroAcao = nomeAcaoE[nomeAcaoE["CODIGO_ACAO"] == codAcaoE].iloc[0]
st.subheader(f"{elementoFiltroAcao['NOME_ACAO']} - {elementoFiltroAcao['CODIGO_ACAO']}")
st.caption(f'Dados de janeiro a {mesText} de {ano}')
#st.write(st.session_state["orig"].query((f"CODIGO_UNIDADE_GESTORA == {ugs}")))

tab1, tab2, tab3, tab4 = st.tabs(['`Empenhos Originais`', '`Empenhos Suplementares`', '`Anulação de Empenhos`', '`Anulação de Autorização de Pagamento`'])
with tab1:
     st.dataframe(consulta)
with tab2:
     st.dataframe(consultaSupl)
with tab3:
     st.dataframe(consultaEmpAnu)
with tab4:
     st.dataframe(consultaPagAnu)

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
# arqAcao = f"files/acao_exercicio_2024.csv"
# if os.path.isfile(arqAcao):
#         nomeAcao = pd.read_csv(arqAcao, sep=';', encoding='ISO-8859-1')
# st.write(codAcaoE)
# st.write(codFonteE)
# nomeAcaoE = nomeAcao.query(f"CODIGO_ACAO == {codAcaoE}")
# #st.write(nomeAcaoE)
# elementoFiltroAcao = nomeAcaoE[nomeAcaoE["CODIGO_ACAO"] == codAcaoE].iloc[0]
# st.subheader(f"{elementoFiltroAcao['NOME_ACAO']} - {elementoFiltroAcao['CODIGO_ACAO']}")

# st.divider()
st.subheader('Municípios Atendidos')
st.caption('Inclui apenas Empenhos Originais')
arq = f"files/regiao_municipio.csv"
if os.path.isfile(arq):
        regiaoMunicipio = pd.read_csv(arq, sep=';', encoding='UTF-8')#, compression={'method': 'gzip', 'compresslevel': 1, 'mtime': 1})

colm1, colm2 = st.columns([1,3])
municipios = consulta[["NOME_MUNICIPIO", "VALOR_EMPENHO"]]#.groupby(["NOME_MUNICIPIO"] , as_index=True).sum('VALOR_EMPENHO')
#"{:,.0f} Lançamentos".format(float(contOriginal)).replace(",", "X").replace(".", ",").replace("X", ".")
def formatar(valor):
     return "R$ {:,.2f}".format(float(valor)).replace(",", "X").replace(".", ",").replace("X", ".")

municipiosN = pd.merge(municipios, regiaoMunicipio, on="NOME_MUNICIPIO", how="outer")
municipiosN["VALOR_EMPENHO"] = municipiosN["VALOR_EMPENHO"].fillna(0)

with colm1:
    chart_municip = pd.DataFrame(municipios.groupby(["NOME_MUNICIPIO"] , as_index=True).sum('VALOR_EMPENHO').sort_values('VALOR_EMPENHO', ascending=False))
    chart_municip['VALOR_EMPENHO'] = chart_municip['VALOR_EMPENHO'].apply(formatar)
    st.dataframe(chart_municip)
chart = pd.DataFrame(municipios.groupby(["NOME_MUNICIPIO"], as_index=True).sum('VALOR_EMPENHO'))
#cht = chart.plot.barh(x="NOME_MUNICIPIO" , y='VALOR_EMPENHO')
with colm2:
    st.bar_chart(chart.sort_values('VALOR_EMPENHO', ascending=False)["VALOR_EMPENHO"])#.plot.bar())

st.divider()
st.subheader('Municípios Não Atendidos')
st.dataframe(municipiosN[municipiosN["VALOR_EMPENHO"] == 0])
st.divider()

st.subheader('Fornecedores')
fornecedores = consulta[["NOME_CREDOR", "CPFCNPJ_CREDOR" , "VALOR_EMPENHO"]]#.groupby(["NOME_MUNICIPIO"] , as_index=True).sum('VALOR_EMPENHO')
fornec = pd.DataFrame(fornecedores.groupby(["NOME_CREDOR", "CPFCNPJ_CREDOR"] , as_index=True).sum('VALOR_EMPENHO').sort_values('VALOR_EMPENHO', ascending=False))
fornec['VALOR_EMPENHO'] = fornec['VALOR_EMPENHO'].apply(formatar)
st.dataframe(fornec)

#### FOOTER SIDEBAR #####
st.sidebar.divider()
st.sidebar.markdown('Desenvolvido por [SIAGOV](https://siagov.com.br)')
st.sidebar.text('S712')