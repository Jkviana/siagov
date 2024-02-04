import streamlit as st
import pandas as pd
import zipfile
from zipfile import ZipFile
from zipfile import Path
import requests as rq
from io import StringIO
from datetime import date
import webbrowser
#import altair as alt
#import plotly_express as px
import base64

st.set_page_config(
    page_title="SIAGOV",
    page_icon="datasets/siagov.ico",
    layout="wide",
    #base="light",
    #initial_sidebar_state="collapsed"
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

#st.sidebar.image("datasets/siagovlogonovo.png")


setor = 270001
dataatual = date.today()
mes = 9 #dataatual.month - 1
ano = dataatual.year

#st.header("Dados de Empenho")

#path = zipfile.Path('datasets/empenho_original_exercicio_2023_mesinicio_1_mesfim_9.zip', at='')
#c.read_text('empenho_original_exercicio_2023_mes_9.csv', encoding='ISO-8859-1')
#a = path.exists('empenho_original_exercicio_2023_mes_9.csv')
if "data" not in st.session_state:
    with zipfile.ZipFile('files/empenho_original_exercicio_2023_mesinicio_1_mesfim_9.zip') as z:
        try:
            with z.open(f'empenho_original_exercicio_2023_mes_{mes}.csv') as f:
                empenhosOriginal = pd.read_csv(f, sep=';', encoding = 'ISO-8859-1')
        except:
            st.write('arquivo não localizado')
        else:
            empenhosOriginal = pd.read_csv('files/empenho_original_exercicio_2023_mes_9.csv', sep=';', encoding = 'ISO-8859-1') #empenhosOriginal = empenhosOriginal[empenhosOriginal["CODIGO_UNIDADE_GESTORA"] == setor]
            empenhosOriginal = empenhosOriginal.sort_values(by="NUMERO_EMPENHO_ORIGEM", ascending=False)
            empenhosOriginal["EXERCICIO"] = empenhosOriginal["EXERCICIO"].astype("string")
            st.session_state["data"] = empenhosOriginal

st.subheader(f'DADOS DE EMPENHO {ano}', divider='violet') #blue, green, orange, red, violet, gray, grey, rainbow   
st.sidebar.markdown('Desenvolvido por [SIAGOV](https://siagov.com.br)')

btn = st.button("Acessar Dados PB")
if btn:
    webbrowser.open_new_tab("https://dados.pb.gov.br/")

st.markdown(
    """
    O conjunto de dados de empenho ...

    Com __*mais de 130.000 registros*__, os dados __tratados__ ...
    """
)
#st.divider()

# try:
#     urlOrig = f'https://dados.pb.gov.br:443/getcsv?nome=empenho_original&exercicio={ano}&mes={mes}'
#     dadosOrig = rq.get(urlOrig)
#     empOrig = dadosOrig.content
#     empOrigConv = str(empOrig)[2:-1]
#     empenhos = empOrigConv.replace('\\n', '\n')
#     empOriginarios = StringIO(empenhos)
#     empOriginariosDef = pd.read_csv(empOriginarios, sep=";", lineterminator='\n', encoding='latin-1')
#     empOriginariosDef
# except:
#     st.write(f'mês {mes} ainda não disponível')


