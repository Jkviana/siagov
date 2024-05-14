import streamlit as st
import pandas as pd
import os
import plotly.express as px
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

df = pd.read_pickle("files/consolidado.pkl.compress", compression="gzip")
#st.write(df)
df_ugs = pd.read_csv("files/unidade_gestora_2023.gzip", sep=';', encoding='ISO-8859-1', compression={'method': 'gzip', 'compresslevel': 1, 'mtime': 1})

#st.selectbox("Unidade",df["CODIGO_UNIDADE_GESTORA"].unique())
colunas = list(df_ugs)
df_ugs[colunas] = df_ugs[colunas].astype('category')

if 'ugsKey' not in st.session_state:
    st.session_state['ugsKey'] = '270001'

unid = df_ugs[df_ugs['CODIGO_UNIDADE_GESTORA'] == int(st.session_state.ugsKey)].iloc[0]
#texto = str(unid['NOME_UNIDADE_GESTORA'])#.iloc[0]
#unid
st.subheader(f"{unid['CODIGO_UNIDADE_GESTORA']} - {unid['SIGLA_UNIDADE_GESTORA']}")
st.header(f"{unid['NOME_UNIDADE_GESTORA']}", divider='blue')


colunas.remove('EXERCICIO')
col1, col2 = st.columns(2)

with col2:
    with st.expander("Consultar Códigos e Siglas das Unidades Gestoras"):
        st.write(df_ugs[colunas].set_index('CODIGO_UNIDADE_GESTORA'))
with col1:
    with st.expander("Selecionar Unidade Gestora"):
        ugss = st.selectbox("Unidade Gestora Selecionada",sorted(df["CODIGO_UNIDADE_GESTORA"].unique()),label_visibility="collapsed")
        ### INICIALIZAR UNIDADE GESTORA ###
        if st.button("Alterar"):
            st.session_state.ugsKey = ugss
            st.rerun()

ugs = df[df['CODIGO_UNIDADE_GESTORA'] == int(st.session_state.ugsKey)].query('CODIGO_MODALIDADE_LICITACAO == 4') #CODIGO_MOTIVO_DISPENSA_LICITACAO
#ugs

tabela = pd.pivot_table(ugs, values='VALOR_EMPENHO', index=['NOME_ITEM_DESPESA'], columns=['NUM_MES_DOCUMENTO'], aggfunc='sum')
tabela['TOTAL'] = tabela.sum(axis=1)

st.dataframe(tabela.sort_values('TOTAL', ascending=False), use_container_width=True,column_config={"1":st.column_config.NumberColumn("Janeiro",format="%.2f"),
                                                                                                   "2":st.column_config.NumberColumn("Fevereiro",format="%.2f"),
                                                                                                   "3":st.column_config.NumberColumn("Março",format="%.2f"),
                                                                                                   "4":st.column_config.NumberColumn("Abril",format="%.2f"),
                                                                                                   "TOTAL":st.column_config.NumberColumn("TOTAL",format="%.2f")})

item_con = st.selectbox('Detalhar Item de Despesa', sorted(ugs['NOME_ITEM_DESPESA'].unique()))
con_item = ugs[ugs['NOME_ITEM_DESPESA'] == item_con]
st.dataframe(con_item.sort_values('NUMERO_EMPENHO_ORIGEM'), hide_index=True, use_container_width=True, column_config={"VALOR_EMPENHO":st.column_config.NumberColumn(format="%.2f")})

def formatar(valor):
     return "R$ {:,.2f}".format(float(valor)).replace(",", "X").replace(".", ",").replace("X", ".")

st.divider()
st.subheader('Fornecedores')
fornecedores = con_item[["NOME_CREDOR", "CPFCNPJ_CREDOR" , "VALOR_EMPENHO"]]#.groupby(["NOME_MUNICIPIO"] , as_index=True).sum('VALOR_EMPENHO')
fornec = pd.DataFrame(fornecedores.groupby(["NOME_CREDOR", "CPFCNPJ_CREDOR"] , as_index=True).sum('VALOR_EMPENHO').sort_values('VALOR_EMPENHO', ascending=False))
forneccht = fornec
fornec['VALOR_EMPENHO'] = fornec['VALOR_EMPENHO'].apply(formatar)
st.dataframe(fornec, use_container_width=True)
fig1 = con_item.groupby('NOME_CREDOR').sum('VALOR_EMPENHO').reset_index()
fig1 = fig1.sort_values('VALOR_EMPENHO', ignore_index=True, ascending=False)
chtforn = px.bar(fig1, x="NOME_CREDOR" , y='VALOR_EMPENHO', text_auto='.2f', orientation='v')
st.plotly_chart(chtforn, theme="streamlit",use_container_width=True)

st.divider()

st.subheader('Municipios Atendidos')
chart_municip = pd.DataFrame(con_item.groupby(["NOME_MUNICIPIO"] , as_index=True).sum('VALOR_EMPENHO').sort_values('VALOR_EMPENHO', ascending=False))
chart_municip['VALOR_EMPENHO'] = chart_municip['VALOR_EMPENHO'].apply(formatar)
st.dataframe(chart_municip)

#chart = pd.DataFrame(con_item.groupby(["NOME_MUNICIPIO"], as_index=True).sum('VALOR_EMPENHO'))
#st.bar_chart(chart.sort_values('VALOR_EMPENHO', ascending=False)["VALOR_EMPENHO"])#.plot.bar())
fig2 = con_item.groupby('NOME_MUNICIPIO').sum('VALOR_EMPENHO').reset_index()
cht = px.bar(fig2, x="NOME_MUNICIPIO" , y='VALOR_EMPENHO')
st.plotly_chart(cht, theme="streamlit", use_container_width=True)

arq = f"files/regiao_municipio.csv"
if os.path.isfile(arq):
        regiaoMunicipio = pd.read_csv(arq, sep=';', encoding='UTF-8')

municipiosN = pd.merge(con_item, regiaoMunicipio, on="NOME_MUNICIPIO", how="outer")
municipiosN["VALOR_EMPENHO"] = municipiosN["VALOR_EMPENHO"].fillna(0)
municipiosN["CONTAR"] = 1

st.divider()
st.subheader('Municípios Não Atendidos')
municpN = (municipiosN[municipiosN["VALOR_EMPENHO"] == 0])
st.dataframe(municpN[['NOME_MUNICIPIO','REGIAO','SEDE_REGIAO','IDH']], hide_index=True, use_container_width=True)

#st.bar_chart(municpN, x="REGIAO", y=["CONTAR"], )
municcht = municpN.groupby('REGIAO').sum('CONTAR').reset_index()
fig = px.bar(municcht, x="REGIAO", y="CONTAR", title = "Municípios não atendidos por região")
st.plotly_chart(fig, theme="streamlit", use_container_width=True)
