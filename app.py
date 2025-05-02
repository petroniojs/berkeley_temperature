import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(
    page_title="Evolução da Temperatura Global", layout="centered")
st.title("🌍 Evolução das Anomalias de Temperatura (1850 - 2024)")

# Carregar os dados
df = pd.read_csv("berkeley_temperature_cleaned.csv")

# Filtros laterais
st.sidebar.header("Filtros")

# Slider para definir intervalo de anos
año_inicio = st.sidebar.slider("Ano inicial", int(
    df["Year"].min()), int(df["Year"].max()), 1900)
año_fim = st.sidebar.slider("Ano final", int(
    df["Year"].min()), int(df["Year"].max()), 2024)

st.write('A temperatura média global está subindo — mas quanto, onde e com que consequências?”

Apesar de sabermos que o planeta está esquentando, muitas pessoas ainda não têm a real dimensão do problema ou não sabem como esse aumento se comporta ao longo do tempo e em diferentes regiões. Como conversar com as pessoas sobre o tema?')


# Seleção do tipo de média
tipo_media = st.sidebar.selectbox(
    "Tipo de média",
    ("Mensal", "Anual", "5 anos", "10 anos", "20 anos")
)

# Aplicar o filtro de anos
df_filtered = df[(df["Year"] >= año_inicio) & (df["Year"] <= año_fim)]

# Mapeamento de colunas conforme seleção do usuário
colunas = {
    "Mensal": ("Monthly_Anomaly", "Monthly_Unc"),
    "Anual": ("Annual_Anomaly", "Annual_Unc"),
    "5 anos": ("FiveYear_Anomaly", "FiveYear_Unc"),
    "10 anos": ("TenYear_Anomaly", "TenYear_Unc"),
    "20 anos": ("TwentyYear_Anomaly", "TwentyYear_Unc")
}
col_anomalia, col_incerteza = colunas[tipo_media]

# Criar uma coluna de data para facilitar visualização
# Usamos o mês também para melhor resolução nos dados mensais
df_filtered["Date"] = pd.to_datetime(df_filtered["Year"].astype(
    str) + '-' + df_filtered["Month"].astype(str), errors='coerce')
df_filtered = df_filtered.dropna(subset=[col_anomalia])

# ============================
# GRÁFICO PRINCIPAL DE LINHA
# ============================
st.subheader(f"Gráfico de Linha: Anomalia de Temperatura ({tipo_media})")

fig_line = px.line(
    df_filtered,
    x="Date",
    y=col_anomalia,
    labels={"Date": "Ano", col_anomalia: "Anomalia (°C)"},
    title=f"Evolução da Anomalia de Temperatura ({tipo_media})"
)

# Adicionando limites de incerteza como pontos transparentes
fig_line.add_scatter(
    x=df_filtered["Date"],
    y=df_filtered[col_anomalia] + df_filtered[col_incerteza],
    mode="lines",
    line=dict(width=0),
    fill=None,
    name="Limite Superior"
)
fig_line.add_scatter(
    x=df_filtered["Date"],
    y=df_filtered[col_anomalia] - df_filtered[col_incerteza],
    mode="lines",
    line=dict(width=0),
    fill='tonexty',
    fillcolor='rgba(0,100,200,0.2)',
    name="Faixa de Incerteza"
)

st.plotly_chart(fig_line, use_container_width=True)

# =============================
# GRÁFICO DE DISPERSÃO POR ANO
# =============================
st.subheader("Dispersão de Anomalias por Ano")
fig_scatter = px.scatter(
    df_filtered,
    x="Year",
    y=col_anomalia,
    color=col_anomalia,
    color_continuous_scale="RdBu_r",
    labels={"Year": "Ano", col_anomalia: "Anomalia (°C)"},
    title="Variação das Anomalias Ano a Ano"
)
st.plotly_chart(fig_scatter, use_container_width=True)

# ============================
# HISTOGRAMA DAS ANOMALIAS
# ============================
st.subheader("Distribuição das Anomalias")
fig_hist = px.histogram(
    df_filtered,
    x=col_anomalia,
    nbins=50,
    labels={col_anomalia: "Anomalia (°C)"},
    title="Distribuição Frequente das Anomalias de Temperatura"
)
st.plotly_chart(fig_hist, use_container_width=True)

# ============================
# CONCLUSÃO INTERPRETATIVA
# ============================
st.markdown("""
### 🔍 Conclusão
Os gráficos acima mostram:
- Uma tendência clara de **aumento das anomalias** de temperatura desde o século XX;
- **Faixas de incerteza** que se mantêm relativamente estáveis ao longo do tempo;
- **Distribuição** com predomínio de valores positivos recentes, reforçando o aquecimento global.

Essas análises são fundamentais para embasar decisões sobre políticas ambientais, planejamento urbano e ações sustentáveis.
""")
