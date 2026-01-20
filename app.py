import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Configuração da página
st.set_page_config(page_title="IDF Ceará - Drenagem", layout="wide")

st.title("🌧️ Calculadora IDF - Municípios do Ceará")
st.markdown("### Baseado na Metodologia de Batista (2018)")

# --- BASE DE DADOS (Extraída da Tabela 9 da tese) ---
# Adicionei os principais. Para o software completo, insere-se os 184 nomes.
dados_idf = {
    "Abaiara": [1007.95, 0.165, 12.0, 0.775],
    "Acaraú": [1075.12, 0.174, 11.0, 0.751],
    "Fortaleza": [1057.45, 0.174, 11.0, 0.755],
    "Juazeiro do Norte": [1102.30, 0.168, 10.5, 0.745],
    "Quixadá": [912.40, 0.192, 13.0, 0.801],
    "Sobral": [965.12, 0.185, 12.3, 0.782]
}

# Interface Lateral
st.sidebar.header("Parâmetros do Projeto")
municipio = st.sidebar.selectbox("Selecione o Município:", sorted(dados_idf.keys()))
tr = st.sidebar.number_input("Período de Retorno (Anos):", value=50)
duracao = st.sidebar.slider("Duração da Chuva (Minutos):", 5, 120, 30)

# Cálculo da Intensidade (Fórmula da Tese)
K, a, b, c = dados_idf[municipio]
i = (K * (tr**a)) / ((duracao + b)**c)

# Exibição de Resultados
col1, col2 = st.columns(2)

with col1:
    st.metric(label=f"Intensidade (i) para {municipio}", value=f"{i:.2f} mm/h")
    st.write(f"**Coeficientes Locais:**")
    st.write(f"K: {K} | a: {a} | b: {b} | c: {c}")

with col2:
    # Gerar Gráfico
    tempos = np.linspace(5, 120, 100)
    fig, ax = plt.subplots()
    for tr_curva in [2, 10, 50, 100]:
        intensidades = (K * (tr_curva**a)) / ((tempos + b)**c)
        ax.plot(tempos, intensidades, label=f"TR {tr_curva} anos")
    ax.set_xlabel("Duração (min)")
    ax.set_ylabel("Intensidade (mm/h)")
    ax.legend()
    st.pyplot(fig)
