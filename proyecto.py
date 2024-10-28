import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

def cargar_datos():
    data = pd.read_excel('InternetFijo.xlsx', sheet_name='internet')
    return data

df = cargar_datos()

# Título de la aplicación
st.title("Dashboard de Accesos Fijos en el Eje Cafetero")

 # Sidebar para filtros
st.sidebar.header("Filtros")

# Filtro por ciudad
municipio_seleccionado = st.sidebar.multiselect(
    "Selecciona una Ciudad",
    options=df['Municipio'].unique(),
    default=None  # Sin filtro al inicio
)

# Filtro por año
ano_seleccionado = st.sidebar.multiselect(
    "Selecciona el año",
    options=df['ano'].unique(),
    default=None  # Sin filtro al inicio
)

# Filtro por trimestre
trimestre_seleccionado = st.sidebar.multiselect(
    "Selecciona el trimestre",
    options=df['Trimestre'].unique(),
    default=None  # Sin filtro al inicio
)

# Filtrar los datos según las selecciones
df_filtered = df[
    (df['ano'].isin(ano_seleccionado)) &
    (df['Trimestre'].isin(trimestre_seleccionado)) &
    (df['Municipio'].isin(municipio_seleccionado))
]

# Mostrar los datos filtrados
st.write(f"Datos filtrados para el año {ano_seleccionado}, trimestre {trimestre_seleccionado}, municipio {municipio_seleccionado} y municipio {municipio_seleccionado}:")
st.dataframe(df_filtered)

# === PESTAÑAS PARA ORGANIZAR LOS GRÁFICOS ===
tabs = st.tabs(["Gráfico de Líneas", "Gráfico de Barras", "Histograma", "Gráfico Circular - Ciudades", "Grafico de barras - Ciudades"])

# Gráfico de Líneas
with tabs[0]:
    st.write("## Evolución de los accesos fijos por trimestre")
    line_data = df_filtered.groupby(['ano', 'Trimestre'])['Num_accesos fijos'].sum().reset_index()
    line_data['Periodo'] = line_data['ano'].astype(str) + " - T" + line_data['Trimestre'].astype(str)
    st.line_chart(line_data.set_index('Periodo')['Num_accesos fijos'])

# Gráfico de Barras
with tabs[1]:
    st.write("## Accesos fijos por trimestre")
    bar_data = df_filtered.groupby(['ano', 'Trimestre'])['Num_accesos fijos'].sum().reset_index()
    bar_data['Periodo'] = bar_data['ano'].astype(str) + " - T" + bar_data['Trimestre'].astype(str)
    st.bar_chart(bar_data.set_index('Periodo')['Num_accesos fijos'])

# Histograma
with tabs[2]:
    st.write("## Distribución de accesos fijos")
    plt.hist(df_filtered['Num_accesos fijos'], bins=10, color='skyblue', edgecolor='black')
    plt.title('Histograma de accesos fijos')
    plt.xlabel('Número de accesos fijos')
    plt.ylabel('Frecuencia')
    st.pyplot(plt)

# Tab 4: Gráfico Circular (Evolución por trimestre)
with tabs[3]:
    st.write("## Gráfico circular: Proporción de accesos fijos por trimestre")
    # Agrupamos por trimestre y sumamos los accesos fijos
    pie_data = df_filtered.groupby('Departamento')['Num_accesos fijos'].sum()
    plt.figure(figsize=(8, 8))
    plt.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
    plt.axis('equal')  # Asegura que el gráfico sea un círculo
    plt.title('Proporción de accesos fijos por trimestre')
    st.pyplot(plt)

# Gráfico de Barras por Ciudad
with tabs[4]:
    st.write("## Accesos fijos por ciudad")
    city_data = df_filtered.groupby('Municipio')['Num_accesos fijos'].sum().reset_index()
    st.bar_chart(city_data.set_index('Municipio')['Num_accesos fijos'])


# Gráfico de cambios en accesos fijos (aumento o disminución)
st.write("Cambio en el número de accesos fijos a lo largo del tiempo")

# Agrupar por año, trimestre y sumar accesos fijos
df_change = df_filtered.groupby(['ano', 'Trimestre'])['Num_accesos fijos'].sum().reset_index()

# Ordenar los datos por año y trimestre
df_change = df_change.sort_values(by=['ano', 'Trimestre'])

# Calcular la diferencia de accesos fijos entre trimestres consecutivos
df_change['Cambio_accesos'] = df_change['Num_accesos fijos'].diff()

# Mostrar la tabla de cambios
st.write("Tabla de cambios en los accesos fijos:")
st.dataframe(df_change)


