
import streamlit as st
import pandas as pd
from datetime import date
import os

# Criar pastas para armazenar dados
if not os.path.exists("data"):
    os.makedirs("data")

# Carregar dados existentes
if os.path.exists("data/vendas.csv"):
    vendas = pd.read_csv("data/vendas.csv")
else:
    vendas = pd.DataFrame(columns=["Data", "Cliente", "Produto", "Quantidade", "Valor Unitário", "Total"])

if os.path.exists("data/despesas.csv"):
    despesas = pd.read_csv("data/despesas.csv")
else:
    despesas = pd.DataFrame(columns=["Data", "Categoria", "Descrição", "Valor"])

# ----------------- REGISTRO DE VENDAS -----------------
st.title("App de Controle de Marmitex")

st.header("Registrar Venda")
with st.form("venda_form"):
    data_venda = st.date_input("Data", value=date.today())
    cliente = st.text_input("Cliente")
    produto = st.text_input("Produto")
    quantidade = st.number_input("Quantidade", min_value=1)
    valor_unit = st.number_input("Valor Unitário", min_value=0.0, format="%.2f")
    submitted_venda = st.form_submit_button("Registrar Venda")

    if submitted_venda:
        total = quantidade * valor_unit
        vendas = pd.concat([vendas, pd.DataFrame([{
            "Data": data_venda,
            "Cliente": cliente,
            "Produto": produto,
            "Quantidade": quantidade,
            "Valor Unitário": valor_unit,
            "Total": total
        }])], ignore_index=True)
        vendas.to_csv("data/vendas.csv", index=False)
        st.success(f"Venda registrada! Total: R$ {total:.2f}")

# ----------------- REGISTRO DE DESPESAS -----------------
st.header("Registrar Despesa")
categorias = ["Embalagens","Motoboy","Gás","Energia","Água","iFood","Carne","Hortifruti","Supermercado","Funcionário"]
with st.form("despesa_form"):
    data_despesa = st.date_input("Data", value=date.today(), key="data_despesa")
    categoria = st.selectbox("Categoria", categorias)
    descricao = st.text_input("Descrição")
    valor_desp = st.number_input("Valor", min_value=0.0, format="%.2f")
    submitted_despesa = st.form_submit_button("Registrar Despesa")

    if submitted_despesa:
        despesas = pd.concat([despesas, pd.DataFrame([{
            "Data": data_despesa,
            "Categoria": categoria,
            "Descrição": descricao,
            "Valor": valor_desp
        }])], ignore_index=True)
        despesas.to_csv("data/despesas.csv", index=False)
        st.success(f"Despesa registrada: {categoria} - R$ {valor_desp:.2f}")

# ----------------- RELATÓRIOS -----------------
st.header("Relatórios")
periodo = st.date_input("Período inicial", value=date.today())
periodo_fim = st.date_input("Período final", value=date.today())

# Filtrar vendas
vendas_periodo = vendas[(pd.to_datetime(vendas["Data"]) >= pd.to_datetime(periodo)) &
                        (pd.to_datetime(vendas["Data"]) <= pd.to_datetime(periodo_fim))]

despesas_periodo = despesas[(pd.to_datetime(despesas["Data"]) >= pd.to_datetime(periodo)) &
                            (pd.to_datetime(despesas["Data"]) <= pd.to_datetime(periodo_fim))]

st.subheader("Resumo de Vendas")
st.dataframe(vendas_periodo)

st.subheader("Resumo de Despesas")
st.dataframe(despesas_periodo)

st.subheader("Despesas por Categoria")
categoria_sum = despesas_periodo.groupby("Categoria")["Valor"].sum()
st.bar_chart(categoria_sum)

st.subheader("Faturamento x Despesas")
total_vendas = vendas_periodo["Total"].sum()
total_despesas = despesas_periodo["Valor"].sum()
st.write(f"Faturamento: R$ {total_vendas:.2f}")
st.write(f"Despesas: R$ {total_despesas:.2f}")
st.write(f"Lucro: R$ {total_vendas - total_despesas:.2f}")
