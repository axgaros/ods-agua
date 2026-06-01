"""
Dashboard ODS 6 - Cobertura de Agua Potable en México
Ejecutar: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ─── CONFIGURACIÓN DE PÁGINA ───────────────────────────────
st.set_page_config(
    page_title="ODS 6 - Agua en México",
    page_icon="💧",
    layout="wide"
)

st.title("💧 ODS 6: Agua Limpia y Saneamiento en México")
st.markdown("Dashboard de cobertura de agua potable por entidad federativa — Camino al 2030")

st.divider()

# ─── DATOS DEMO ────────────────────────────────────────────
# Datos realistas de cobertura de agua por estado (última década)
# Fuente simulada: INEGI / CONAGUA
# Reemplazar con CSV real: pd.read_csv("data/datos.csv")

@st.cache_data
def cargar_datos():
    cobertura_historica = {
        "Aguascalientes":   [98.2, 98.4, 98.5, 98.7, 98.8],
        "Baja California":  [96.5, 96.8, 97.0, 97.2, 97.3],
        "Baja California Sur": [94.0, 94.5, 95.0, 95.3, 95.8],
        "Campeche":         [90.5, 91.0, 91.5, 92.0, 92.5],
        "Coahuila":         [97.0, 97.2, 97.5, 97.8, 98.0],
        "Colima":           [97.5, 97.8, 98.0, 98.2, 98.5],
        "Chiapas":          [68.0, 69.5, 71.0, 72.5, 74.0],
        "Chihuahua":        [95.0, 95.5, 96.0, 96.3, 96.5],
        "CDMX":             [99.0, 99.1, 99.2, 99.3, 99.4],
        "Durango":          [93.0, 93.5, 94.0, 94.5, 95.0],
        "Guanajuato":       [93.5, 94.0, 94.5, 95.0, 95.5],
        "Guerrero":         [72.0, 73.0, 74.5, 76.0, 77.5],
        "Hidalgo":          [89.0, 90.0, 90.8, 91.5, 92.0],
        "Jalisco":          [95.5, 96.0, 96.3, 96.6, 97.0],
        "Estado de México": [94.0, 94.8, 95.2, 95.5, 96.0],
        "Michoacán":        [89.5, 90.5, 91.5, 92.5, 93.0],
        "Morelos":          [92.0, 92.8, 93.5, 94.0, 94.5],
        "Nayarit":          [93.0, 93.8, 94.5, 95.0, 95.3],
        "Nuevo León":       [98.5, 98.7, 98.8, 98.9, 99.0],
        "Oaxaca":           [65.0, 66.5, 68.0, 70.0, 72.0],
        "Puebla":           [85.0, 86.0, 87.5, 88.5, 89.5],
        "Querétaro":        [95.5, 96.0, 96.5, 97.0, 97.2],
        "Quintana Roo":     [96.0, 96.3, 96.5, 96.7, 97.0],
        "San Luis Potosí":  [90.0, 91.0, 92.0, 93.0, 93.5],
        "Sinaloa":          [94.0, 94.5, 95.0, 95.5, 96.0],
        "Sonora":           [96.5, 96.8, 97.0, 97.2, 97.5],
        "Tabasco":          [80.0, 81.0, 82.5, 84.0, 85.5],
        "Tamaulipas":       [95.5, 95.8, 96.2, 96.5, 96.8],
        "Tlaxcala":         [94.0, 94.8, 95.5, 96.0, 96.5],
        "Veracruz":         [78.0, 79.0, 80.5, 82.0, 83.5],
        "Yucatán":          [96.0, 96.5, 96.8, 97.0, 97.3],
        "Zacatecas":        [93.0, 93.8, 94.5, 95.0, 95.5],
    }

    anios = [2020, 2021, 2022, 2023, 2024]

    filas = []
    for estado, valores in cobertura_historica.items():
        for i, anio in enumerate(anios):
            filas.append({
                "Estado": estado,
                "Año": anio,
                "Cobertura_Agua_Potable": valores[i],
                "Sin_Acceso": round(100 - valores[i], 1)
            })

    df = pd.DataFrame(filas)

    # Datos por zona (urbano vs rural) — solo año más reciente
    zona = {
        "Aguascalientes":    (99.1, 89.0),
        "Baja California":   (98.5, 88.0),
        "Baja California Sur": (97.2, 86.0),
        "Campeche":          (94.0, 78.0),
        "Coahuila":          (98.8, 90.0),
        "Colima":            (99.2, 89.5),
        "Chiapas":           (85.0, 55.0),
        "Chihuahua":         (98.0, 87.0),
        "CDMX":              (99.8, 97.0),
        "Durango":           (96.5, 84.0),
        "Guanajuato":        (97.0, 86.0),
        "Guerrero":          (88.0, 58.0),
        "Hidalgo":           (93.5, 78.0),
        "Jalisco":           (98.2, 88.0),
        "Estado de México":  (97.5, 85.0),
        "Michoacán":         (94.5, 81.0),
        "Morelos":           (96.0, 84.0),
        "Nayarit":           (96.8, 85.0),
        "Nuevo León":        (99.5, 93.0),
        "Oaxaca":            (84.0, 52.0),
        "Puebla":            (91.0, 75.0),
        "Querétaro":         (98.0, 87.0),
        "Quintana Roo":      (98.5, 89.0),
        "San Luis Potosí":   (95.0, 79.0),
        "Sinaloa":           (97.5, 87.0),
        "Sonora":            (98.5, 90.0),
        "Tabasco":           (88.0, 70.0),
        "Tamaulipas":        (98.0, 88.0),
        "Tlaxcala":          (97.8, 88.0),
        "Veracruz":          (90.0, 68.0),
        "Yucatán":           (98.2, 90.0),
        "Zacatecas":         (96.8, 86.0),
    }

    df_zona = pd.DataFrame([
        {"Estado": e, "Urbano": v[0], "Rural": v[1]}
        for e, v in zona.items()
    ])

    return df, df_zona, anios

df, df_zona, anios = cargar_datos()

# ─── SIDEBAR ───────────────────────────────────────────────
with st.sidebar:
    st.header("🔍 Filtros")
    anio_sel = st.selectbox("Año", anios, index=len(anios)-1)
    zona_sel = st.radio("Zona", ["Todo", "Urbano", "Rural"])
    st.divider()
    st.markdown("### 📥 Datos reales")
    st.markdown("Reemplaza el CSV en `data/datos.csv` con datos del INEGI o CONAGUA")
    st.markdown("[inegi.org.mx/temas/agua](https://www.inegi.org.mx/temas/agua)")
    st.divider()
    st.caption("Dashboard ODS 6 — Proyecto escolar")

# ─── FILTRAR DATOS ─────────────────────────────────────────
df_filtrado = df[df["Año"] == anio_sel].copy()

# ─── MÉTRICAS PRINCIPALES ──────────────────────────────────
promedio = df_filtrado["Cobertura_Agua_Potable"].mean()
mejor = df_filtrado.loc[df_filtrado["Cobertura_Agua_Potable"].idxmax()]
peor = df_filtrado.loc[df_filtrado["Cobertura_Agua_Potable"].idxmin()]
brecha = mejor["Cobertura_Agua_Potable"] - peor["Cobertura_Agua_Potable"]

col1, col2, col3, col4 = st.columns(4)
col1.metric("📊 Cobertura Nacional", f"{promedio:.1f}%")
col2.metric("🏆 Mejor Estado", mejor["Estado"], f"{mejor['Cobertura_Agua_Potable']}%")
col3.metric("⚠️ Peor Estado", peor["Estado"], f"{peor['Cobertura_Agua_Potable']}%")
col4.metric("📉 Brecha", f"{brecha:.1f}%")

st.divider()

# ─── MAPA DE MÉXICO ────────────────────────────────────────
st.subheader("🗺️ Mapa de Cobertura por Estado")

fig_mapa = px.choropleth(
    df_filtrado,
    locations="Estado",
    locationmode="geojson-id",
    color="Cobertura_Agua_Potable",
    color_continuous_scale="Blues",
    range_color=(60, 100),
    labels={"Cobertura_Agua_Potable": "Cobertura (%)"},
    title=f"Cobertura de Agua Potable — {anio_sel}"
)

fig_mapa.update_geos(
    visible=False,
    scope="north america",
    projection_scale=4,
    center={"lat": 23.6, "lon": -102.5},
)
fig_mapa.update_layout(
    height=500,
    margin={"r": 0, "t": 30, "l": 0, "b": 0},
    geo=dict(
        showframe=False,
        showcoastlines=True,
        coastlinecolor="gray",
        showland=True,
        landcolor="lightgray",
        showcountries=True,
        countrycolor="gray"
    )
)

st.plotly_chart(fig_mapa, use_container_width=True)

# ─── GRÁFICAS ──────────────────────────────────────────────
col_izq, col_der = st.columns(2)

with col_izq:
    st.subheader("🏆 Top 10 Estados con Mejor Cobertura")
    top10 = df_filtrado.nlargest(10, "Cobertura_Agua_Potable").sort_values("Cobertura_Agua_Potable")
    fig_bar = px.bar(
        top10,
        x="Cobertura_Agua_Potable",
        y="Estado",
        orientation="h",
        color="Cobertura_Agua_Potable",
        color_continuous_scale="greens",
        text="Cobertura_Agua_Potable"
    )
    fig_bar.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig_bar.update_layout(
        xaxis_range=[85, 100],
        yaxis=dict(autorange="reversed"),
        height=400
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with col_der:
    st.subheader("⚠️ Top 10 Estados con Menor Cobertura")
    bot10 = df_filtrado.nsmallest(10, "Cobertura_Agua_Potable").sort_values("Cobertura_Agua_Potable", ascending=False)
    fig_bar2 = px.bar(
        bot10,
        x="Cobertura_Agua_Potable",
        y="Estado",
orientation="h",
        color="Cobertura_Agua_Potable",
        color_continuous_scale="reds",
        text="Cobertura_Agua_Potable"
    )
    fig_bar2.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig_bar2.update_layout(
        xaxis_range=[50, 85],
        yaxis=dict(autorange="reversed"),
        height=400
    )
    st.plotly_chart(fig_bar2, use_container_width=True)

# ─── EVOLUCIÓN EN EL TIEMPO ────────────────────────────────
st.subheader("📈 Evolución de Cobertura 2020-2024")
st.markdown("Selecciona los estados que quieras comparar")

estados_todos = sorted(df["Estado"].unique())
default_estados = ["Nuevo León", "CDMX", "Oaxaca", "Chiapas", "Guerrero", "Promedio Nacional"]
estados_sel = st.multiselect("Estados", estados_todos, default=[e for e in default_estados if e in estados_todos or e == "Promedio Nacional"])

df_evol = df.groupby("Año")["Cobertura_Agua_Potable"].mean().reset_index()
df_evol["Estado"] = "Promedio Nacional"

dfs_comparar = [df_evol]
for estado in estados_sel:
    if estado != "Promedio Nacional":
        dfs_comparar.append(df[df["Estado"] == estado][["Año", "Cobertura_Agua_Potable"]].assign(Estado=estado))

df_linea = pd.concat(dfs_comparar)

fig_linea = px.line(
    df_linea,
    x="Año",
    y="Cobertura_Agua_Potable",
    color="Estado",
    markers=True,
    labels={"Cobertura_Agua_Potable": "Cobertura (%)"}
)
fig_linea.update_layout(
    height=450,
    yaxis_range=[60, 100],
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0)
)
st.plotly_chart(fig_linea, use_container_width=True)

# ─── BRECHA URBANO vs RURAL ────────────────────────────────
st.subheader("🏙️ vs 🌾 Brecha Urbano-Rural")

df_zona_melt = df_zona.melt(id_vars="Estado", var_name="Zona", value_name="Cobertura")
df_zona_melt["Brecha"] = df_zona_melt.groupby("Estado")["Cobertura"].transform(lambda x: x.max() - x.min())
df_zona_top_brecha = df_zona_melt.drop_duplicates("Estado").nlargest(10, "Brecha")

fig_dot = px.strip(
    df_zona_melt[df_zona_melt["Estado"].isin(df_zona_top_brecha["Estado"])],
    x="Cobertura",
    y="Estado",
    color="Zona",
    color_discrete_map={"Urbano": "#2196F3", "Rural": "#FF9800"},
    labels={"Cobertura": "Cobertura (%)"}
)
fig_dot.update_layout(height=400, yaxis=dict(autorange="reversed"))
st.plotly_chart(fig_dot, use_container_width=True)

# ─── TABLA COMPLETA ────────────────────────────────────────
st.subheader("📋 Datos Completos")

tabla = df_filtrado[["Estado", "Cobertura_Agua_Potable", "Sin_Acceso"]].sort_values("Cobertura_Agua_Potable", ascending=False)
tabla.columns = ["Estado", "Cobertura (%)", "Sin Acceso (%)"]
st.dataframe(
    tabla.style.background_gradient(subset=["Cobertura (%)"], cmap="Blues"),
    use_container_width=True,
    hide_index=True,
    height=600
)

csv = tabla.to_csv(index=False).encode("utf-8")
st.download_button("📥 Descargar datos (CSV)", csv, f"cobertura_agua_{anio_sel}.csv", "text/csv")

# ─── FOOTER ────────────────────────────────────────────────
st.divider()
st.caption("📌 Datos demo con fines académicos. Reemplazar con datos oficiales de INEGI/CONAGUA para versión final.")
