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
    initial_sidebar_state="collapsed",
    
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

#add_logo("datasets/siagovlogonovo.png")
#imagemlogosidebar = "datasets/siagovlogonovo.png"
# logoprincipal = "datasets/siagovlogonovo.png"
#st.logo(imagemlogosidebar)

#st.sidebar.image("datasets/siagovlogonovo.png")
# ano = 2023 #st.sidebar.selectbox('Execício:', [2023, 2024], index=0)
# dataatual = date.today()
# if ano == dataatual.year:
#     mes = dataatual.month
# elif ano < dataatual.year:
#     mes = 12
# st.session_state.ano = ano
# st.session_state.mes = mes
# setor = 270001
# st.sidebar.text(f'{mes}, {ano}' )

#### FOOTER SIDEBAR #####
if st.sidebar.button('Limpar Cache'):
     st.cache_data.clear()
st.sidebar.divider()
st.sidebar.markdown('Desenvolvido por [SIAGOV](https://siagov.com.br)')
st.sidebar.text('S712')

#dataatual = date.today()
#mes = 9 #dataatual.month - 1
#ano = dataatual.year

#st.header("Dados de Empenho")

#path = zipfile.Path('datasets/empenho_original_exercicio_2023_mesinicio_1_mesfim_9.zip', at='')
#c.read_text('empenho_original_exercicio_2023_mes_9.csv', encoding='ISO-8859-1')
#a = path.exists('empenho_original_exercicio_2023_mes_9.csv')


### MENU SUPERIOR
st.image("datasets/siagovlogonovo.png", width=300)
# st.subheader('', divider='blue')
# col1, col2, col3, col4, col5, col6 = st.columns([2,2,2,2,2,6])
# with col1:
#     btn1 = st.button('Ações de Governo')
# with col2:
#     btn2 = st.button('Lista de Empenhos')
# with col3:
#     btn3 = st.button('Lista de Contratos')
# with col4:
#     btn = st.button("Acessar Dados PB")
#     if btn:
#         webbrowser.open_new_tab("https://dados.pb.gov.br/")
# with col5:
#     btn4 = st.button('Sobre')
# with col6:
#     st.write('')
st.subheader('', divider='blue')

################# Style Metrics ###############3
#@extra
def style_metric_cards(
    background_color: str = "#F1F1F1",#FFE
    border_size_px: int = 0,
    border_color: str = "#CCC",
    border_radius_px: int = 5,
    border_left_color: str = "#1E69AD",
    box_shadow: bool = True,
) -> None:
    """
    Applies a custom style to st.metrics in the page

    Args:
        background_color (str, optional): Background color. Defaults to "#FFF".
        border_size_px (int, optional): Border size in pixels. Defaults to 1.
        border_color (str, optional): Border color. Defaults to "#CCC".
        border_radius_px (int, optional): Border radius in pixels. Defaults to 5.
        border_left_color (str, optional): Borfer left color. Defaults to "#9AD8E1".
        box_shadow (bool, optional): Whether a box shadow is applied. Defaults to True.
    """

    box_shadow_str = (
        "box-shadow: 0 0.15rem 1.75rem 0 rgba(58, 59, 69, 0.0) !important;"
        if box_shadow
        else "box-shadow: none !important;"
    )
    st.markdown(
        f"""
        <style>
            div[data-testid="stMetric"],
            div[data-testid="metric-container"] {{
                background-color: {background_color};
                border: {border_size_px}px solid {border_color};
                padding: 5% 5% 5% 10%;
                border-radius: {border_radius_px}px;
                border-left: 0.5rem solid {border_left_color} !important;
                {box_shadow_str}
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

############## 2024 ###############
    
ano = 2024
mes = date.today().month

### Carga de dados ###
@st.cache_data
def load_empOri2024():
    empOrigt = []
    for i in range (1, mes):
        arq = f"files/empenho_original{ano}mes{i}.gzip"
        if os.path.isfile(arq):
                emp = pd.read_csv(arq, sep=';', encoding='ISO-8859-1', compression={'method': 'gzip', 'compresslevel': 1, 'mtime': 1}) #, index_col=[0]
                empOrigt.append(emp)
        #else:
            #st.write(f"Arquivo **empenho_original{ano}mes{mes}** não disponível")
    empOrigr = pd.concat(empOrigt)
    return empOrigr

@st.cache_data
def load_empSup2024():
    empSupt = []
    for i in range (1, mes):
        arq = f"files/empenho_suplementacao{ano}mes{i}.gzip"
        if os.path.isfile(arq):
                emp = pd.read_csv(arq, sep=';', encoding='ISO-8859-1', compression={'method': 'gzip', 'compresslevel': 1, 'mtime': 1}) #, index_col=[0]
                empSupt.append(emp)
        #else:
            #st.write(f"Arquivo **empenho_suplementacao{ano}mes{mes}** não disponível")
    empSupr = pd.concat(empSupt)
    return empSupr

@st.cache_data
def load_empAnu2024():
    empAnut = []
    for i in range (1, mes):
        arq = f"files/empenho_anulacao{ano}mes{i}.gzip"
        if os.path.isfile(arq):
                emp = pd.read_csv(arq, sep=';', encoding='ISO-8859-1', compression={'method': 'gzip', 'compresslevel': 1, 'mtime': 1}) #, index_col=[0]
                empAnut.append(emp)
        #else:
            #st.write(f"Arquivo **empenho_anulacao{ano}mes{mes}** não disponível")
    empAnur = pd.concat(empAnut)
    return empAnur

@st.cache_data
def load_pagAnu2024():
    pagAnut = []
    for i in range (1, mes):
        arq = f"files/pagamento_anulacao{ano}mes{i}.gzip"
        if os.path.isfile(arq):
                emp = pd.read_csv(arq, sep=';', encoding='ISO-8859-1', compression={'method': 'gzip', 'compresslevel': 1, 'mtime': 1}) #, index_col=[0]
                pagAnut.append(emp)
        #else:
            #st.write(f"Arquivo **pagamento_anulacao{ano}mes{mes}** não disponível")
    pagAnur = pd.concat(pagAnut)
    return pagAnur
### Fim da carga de dados ###

### Totlização de empenhos ###
totEmpOrig = load_empOri2024()
totalOriginal = totEmpOrig.sum(numeric_only=True)[["VALOR_EMPENHO"]]
valor_realText = "{:,.2f}".format(float(totalOriginal)).replace(",", "X").replace(".", ",").replace("X", ".")
valor_real = "R${:,.2f}".format(float(totalOriginal/1000)).replace(",", "X").replace(".", ",").replace("X", ".")
contOriginal = totEmpOrig.count(numeric_only=True)[["VALOR_EMPENHO"]]
contagemOriginal = "{:,.0f} Lançamentos".format(float(contOriginal)).replace(",", "X").replace(".", ",").replace("X", ".")

totEmpSup = load_empSup2024()
totalSuplement = totEmpSup.sum(numeric_only=True)[["VALOR_EMPENHO"]]
valor_realSupText = "{:,.2f}".format(float(totalSuplement)).replace(",", "X").replace(".", ",").replace("X", ".")
valor_realSup = "R${:,.2f}".format(float(totalSuplement/1000)).replace(",", "X").replace(".", ",").replace("X", ".")
contSup = totEmpSup.count(numeric_only=True)[["VALOR_EMPENHO"]]
contagemSuplement = "{:,.0f} Lançamentos".format(float(contSup)).replace(",", "X").replace(".", ",").replace("X", ".")

totEmpAnu = load_empAnu2024()
totalEmpAnu = totEmpAnu.sum(numeric_only=True)[["VALOR_EMPENHO"]]
valor_realEmpAnuText = "{:,.2f}".format(float(totalEmpAnu)).replace(",", "X").replace(".", ",").replace("X", ".")
valor_realEmpAnu = "R${:,.2f}".format(float(totalEmpAnu/1000)).replace(",", "X").replace(".", ",").replace("X", ".")
contEmpAnu = totEmpAnu.count(numeric_only=True)[["VALOR_EMPENHO"]]
contagemEmpAnu = "{:,.0f} Lançamentos".format(float(contEmpAnu)*-1).replace(",", "X").replace(".", ",").replace("X", ".")

totPagAnu = load_pagAnu2024()
totalPagAnu = totPagAnu.sum(numeric_only=True)[["VALOR_DOCUMENTO"]]
valor_realPagAnuText = "{:,.2f}".format(float(totalPagAnu)).replace(",", "X").replace(".", ",").replace("X", ".")
valor_realPagAnu = "R${:,.2f}".format(float(totalPagAnu/1000)).replace(",", "X").replace(".", ",").replace("X", ".")
contPagAnu = totPagAnu.count(numeric_only=True)[["VALOR_DOCUMENTO"]]
contagemPagAnu = "{:,.0f} Lançamentos".format(float(contPagAnu)*-1).replace(",", "X").replace(".", ",").replace("X", ".")

### Fim da totlização de empenhos ###
totalEmpenhado = sum(totalOriginal, totalSuplement)
valorTotalEmpenhado = "{:,.2f}".format(float(totalEmpenhado)).replace(",", "X").replace(".", ",").replace("X", ".")
totalAnulado = sum(totalEmpAnu, totalPagAnu)
valorTotalAnulado = "{:,.2f}".format(float(totalAnulado)).replace(",", "X").replace(".", ",").replace("X", ".")
contTotalEmp = sum(contOriginal,contSup)
contTotalEmpText = "{:,.0f}".format(float(contTotalEmp)).replace(",", "X").replace(".", ",").replace("X", ".")
contTotalAnu = sum(contEmpAnu,contPagAnu)
contTotalAnuText = "{:,.0f}".format(float(contTotalAnu)).replace(",", "X").replace(".", ",").replace("X", ".")

mes = mes-1
if mes == 1:
    mesText = "janeiro"
elif mes == 2:
    mesText = "fevereiro"
elif mes == 3:
    mesText = "março"
elif mes == 4:
    mesText = "abril"
elif mes == 5:
    mesText = "maio"
elif mes == 6:
    mesText = "junho"
elif mes == 7:
    mesText = "julho"
elif mes == 8:
    mesText = "agosto"
elif mes == 9:
    mesText = "setembro"
elif mes == 10:
    mesText = "outubro"
elif mes == 11:
    mesText = "novembro"
elif mes == 12:
    mesText = "dezembro"

st.subheader(f'Consolidação dos Empenhos do Governo da Paraíba em {ano}') # , divider='violet') #blue, green, orange, red, violet, gray, grey, rainbow   
st.write(f'Até {mesText} de {ano} foram empenhados mais de __RS {valorTotalEmpenhado}__ com a efetivação de *{contTotalEmpText}* lançamentos de empenhos e suplementações.\
    No mesmo período foram cancelados __RS{valorTotalAnulado}__ em *{contTotalAnuText}* registros de anulação de empenhos e anulação de autorização de pagamentos. \
')

style_metric_cards()
col1, col2, col3, col4 = st.columns(4)

col1.metric(label="Empenhos (em milhões)", value=f"{valor_real}", delta=f"{contagemOriginal}")
col2.metric(label="Suplementação (em milhões)", value=f"{valor_realSup}", delta=f"{contagemSuplement}")
col3.metric(label="Anulação de Empenhos (em milhões)", value=f"{valor_realEmpAnu}", delta=f"{contagemEmpAnu}", help="Totais de Empenhos Anulados")
col4.metric(label="Anulação de Pagamentos (em milhões)", value=f"{valor_realPagAnu}", delta=f"{contagemPagAnu}", help="Totais de Pagamentos Anulados")

st.subheader('', divider='blue')
################  2023  ############

ano = 2023
mes = 13
### Carga de dados ###
@st.cache_data
def load_empOri1():
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

@st.cache_data
def load_empSup1():
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

@st.cache_data
def load_empAnu1():
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

@st.cache_data
def load_pagAnu1():
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
### Fim da carga de dados ###

### Totlização de empenhos ###
totEmpOrig = load_empOri1()
totalOriginal = totEmpOrig.sum(numeric_only=True)[["VALOR_EMPENHO"]]
valor_real = "R${:,.2f}".format(float(totalOriginal/1000)).replace(",", "X").replace(".", ",").replace("X", ".")
contOriginal = totEmpOrig.count(numeric_only=True)[["VALOR_EMPENHO"]]
contagemOriginal = "{:,.0f} Lançamentos".format(float(contOriginal)).replace(",", "X").replace(".", ",").replace("X", ".")

totEmpSup = load_empSup1()
totalSuplement = totEmpSup.sum(numeric_only=True)[["VALOR_EMPENHO"]]
valor_realSup = "R${:,.2f}".format(float(totalSuplement/1000)).replace(",", "X").replace(".", ",").replace("X", ".")
contSup = totEmpSup.count(numeric_only=True)[["VALOR_EMPENHO"]]
contagemSuplement = "{:,.0f} Lançamentos".format(float(contSup)).replace(",", "X").replace(".", ",").replace("X", ".")

totEmpAnu = load_empAnu1()
totalEmpAnu = totEmpAnu.sum(numeric_only=True)[["VALOR_EMPENHO"]]
valor_realEmpAnu = "R${:,.2f}".format(float(totalEmpAnu/1000)).replace(",", "X").replace(".", ",").replace("X", ".")
contEmpAnu = totEmpAnu.count(numeric_only=True)[["VALOR_EMPENHO"]]
contagemEmpAnu = "{:,.0f} Lançamentos".format(float(contEmpAnu)*-1).replace(",", "X").replace(".", ",").replace("X", ".")

totPagAnu = load_pagAnu1()
totalPagAnu = totPagAnu.sum(numeric_only=True)[["VALOR_DOCUMENTO"]]
valor_realPagAnu = "R${:,.2f}".format(float(totalPagAnu/1000)).replace(",", "X").replace(".", ",").replace("X", ".")
contPagAnu = totPagAnu.count(numeric_only=True)[["VALOR_DOCUMENTO"]]
contagemPagAnu = "{:,.0f} Lançamentos".format(float(contPagAnu)*-1).replace(",", "X").replace(".", ",").replace("X", ".")

### Fim da totlização de empenhos ###

totalEmpenhado = sum(totalOriginal, totalSuplement)
valorTotalEmpenhado = "{:,.2f}".format(float(totalEmpenhado)).replace(",", "X").replace(".", ",").replace("X", ".")
totalAnulado = sum(totalEmpAnu, totalPagAnu)
valorTotalAnulado = "{:,.2f}".format(float(totalAnulado)).replace(",", "X").replace(".", ",").replace("X", ".")
contTotalEmp = sum(contOriginal,contSup)
contTotalEmpText = "{:,.0f}".format(float(contTotalEmp)).replace(",", "X").replace(".", ",").replace("X", ".")
contTotalAnu = sum(contEmpAnu,contPagAnu)
contTotalAnuText = "{:,.0f}".format(float(contTotalAnu)).replace(",", "X").replace(".", ",").replace("X", ".")

st.subheader(f'Consolidação dos Empenhos do Governo da Paraíba em {ano}') # , divider='violet') #blue, green, orange, red, violet, gray, grey, rainbow   
st.write(f'De janeiro a dezembro de {ano} foram empenhados de __RS {valorTotalEmpenhado}__ com a efetivação de *{contTotalEmpText}* lançamentos de empenhos e suplementações.\
    No mesmo período foram cancelados __RS{valorTotalAnulado}__ em *{contTotalAnuText}* registros de anulação de empenhos e anulação de autorização de pagamentos. \
')

style_metric_cards()
col1, col2, col3, col4 = st.columns(4)

col1.metric(label="Empenhos (em milhões)", value=f"{valor_real}", delta=f"{contagemOriginal}")
col2.metric(label="Suplementação (em milhões)", value=f"{valor_realSup}", delta=f"{contagemSuplement}")
col3.metric(label="Anulação de Empenhos (em milhões)", value=f"{valor_realEmpAnu}", delta=f"{contagemEmpAnu}", help="Totais de Empenhos Anulados")
col4.metric(label="Anulação de Pagamentos (em milhões)", value=f"{valor_realPagAnu}", delta=f"{contagemPagAnu}", help="Totais de Pagamentos Anulados")

st.subheader('', divider='blue')

###### PARA A CARGA DOS ARQUIVOS ########
# anoB = 2024
# mesB = 10
# arquivo = "empenho_suplementacao" # "empenho_suplementacao"  "empenho_original" "empenho_anulacao" "pagamento_anulacao"
# col1, col2 = st.columns([0.5, 4])
# with col2:
#     for i in range (1, mesB):
#         arqbaixado = f"files/{arquivo}{anoB}mes{i}.gzip"
#         if os.path.isfile(arqbaixado):
#             st.info(f"Arquivo **{arquivo}{anoB}mes{i}** disponível")
#         else:
#             st.warning(f"Arquivo **{arquivo}{anoB}mes{i}** não disponível")
#             if st.button(f'Baixar arquivos do mês {i}'):
#                 resposta = rq.get(f"https://dados.pb.gov.br:443/getcsv?nome={arquivo}&exercicio={anoB}&mes={i}")
#                 if resposta.status_code == rq.codes.OK:
#                     df = pd.read_csv(f'https://dados.pb.gov.br:443/getcsv?nome={arquivo}&exercicio={anoB}&mes={i}', sep=';', encoding='ISO-8859-1')
#                     df.to_csv(f"files/{arquivo}{anoB}mes{i}.gzip", sep=';', encoding='ISO-8859-1', index=False, compression={'method': 'gzip', 'compresslevel': 1, 'mtime': 1})
#                     st.success(f"Arquivos de {arquivo} do ano {anoB} mês {i} baixados com sucesso")
#                 else:
#                     if i == 13:
#                         st.success(f"Todos arquivos do {anoB} disponíveis")
#                     else:
#                         st.error(f"Arquivos de {arquivo} do ano {anoB} mês {i} não disponível")
# with col1:
#     st.write(i)