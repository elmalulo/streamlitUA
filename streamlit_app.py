# Importamos las bibliotecas necesarias
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
##########################################################
# CONFIGURACIÓN DEL DASHBOARD
##########################################################

# Configuración básica de la página
st.set_page_config(layout='wide', initial_sidebar_state='expanded')

# Configuración simple para los gráficos
sns.set_style("whitegrid")


##################################################
# CARGA DE DATOS
##################################################

# Función para cargar datos con cache para mejorar rendimiento
@st.cache_data
def cargar_datos():
    # Carga el archivo CSV con datos macroeconómicos
    df = pd.read_csv("data.csv")
    # Usamos solo el año como referencia temporal
    
    return df

if __name__ == "__main__":
    # Cargamos los datos
    df = cargar_datos()
    print(df.head())
    ##############################################
    # CONFIGURACIÓN DE LA BARRA LATERAL
    ##############################################

    # Simplificamos la barra lateral con solo lo esencial
    st.sidebar.header('Filtros del Dashboard')

    # normalizar informacion 

    df['Date'] = pd.to_datetime(df['Date'])
    # df['Date'] = df['Date'].str.replace('/', '-')
  
    # # Convertir la columna a tipo datetime
    # df2['fecha'] = pd.to_datetime(df2['fecha'], format='%d-%m-%Y', errors='coerce')

    # # Extraer solo el año
    df['Year'] = df['Date'].dt.year





# Selector de rango de años
anio_inicio, anio_fin = st.sidebar.slider(
    'Range years', 
     df['Date'].dt.year.min(), 
     df['Date'].dt.year.max(), 
    (2018, 2019)
)

# Selector de componentes del PIB (solo para el gráfico de área)
componentes_filter = st.sidebar.multiselect(
    'City', 
    options= df.groupby('City')
,    default=['Yangon'],
    help="Selecciona los componentes para visualizar en el gráfico de área"
)

# ##################################################
# # FILTRADO DE DATOS
# ##################################################

# #########################################################
# # SECCIÓN DE GRÁFICOS 
# #########################################################


# # Sección: Composición del PIB
st.subheader('1. Ventas y tipos de ventas totales')
st.write('blablablabl')

# Dividimos la pantalla en dos columnas (proporción 5:5)
c1_f1, c2_f1 = st.columns((5,5))

with c1_f1:
    if componentes_filter:

        fig, ax = plt.subplots(figsize=(10, 3))
        sales_over_time = df.groupby('Date')['Total'].sum().reset_index()
        sns.lineplot(data=sales_over_time, x='Date', y='Total')
     
        # Etiquetas y cuadrícula
        ax.set_ylabel("Ventas totales $")
        ax.set_xlabel("Fecha calendario")
        ax.set_title("Evolución de las ventas totales")
        ax.grid(True, alpha=0.5)

    
    
        st.pyplot(fig)
        st.write("*Explicacion del grafico.*")
    else:
        st.info("Selecciona al menos un componente del PIB")


with c2_f1:
    if componentes_filter:
        fig  = plt.figure(figsize=(10, 4))
        sns.barplot(data=df, x='Product line', y='Total', estimator=sum)
        plt.title('Ingresos por linea de producto')
        plt.ylabel('Total ingresos')
        plt.tight_layout()
       
        # # Mostramos el gráfico en Streamlit
        st.pyplot(fig)
        st.write("*Explicacion del grafico.*")
    else:
        st.info("Selecciona al menos un componente del PIB")

# ###################################################
# # 2da Fila
# ###################################################




st.subheader('SUBTITULOS')
st.write('blablablabl')

c1_f2, c2_f2 = st.columns((5,5))

with c1_f2:
    fig = plt.figure(figsize=(8, 6))
    # Creamos un histograma de la columna 'Rating'
    sns.histplot(df['Rating'], bins=20, kde=True)
    plt.title('Distribución de la Calificación de Clientes')
    plt.xlabel('Rating')
    plt.ylabel('Frecuencia')
    plt.tight_layout()
    plt.show()
  
    # Mostramos el gráfico
    st.pyplot(fig)
    st.write("*Explicacion del grafico.*")


with c2_f2:
    # 4. Comparación del Gasto por Tipo de Cliente
    fig = plt.figure(figsize=(8, 6))
    # Creamos un boxplot que compara la distribución del gasto total segun el tipo de cliente.
    sns.boxplot(data=df, x='Customer type', y='Total')
    plt.title('Comparación del Gasto por Tipo de Cliente')
    plt.xlabel('Tipo de Cliente')
    plt.ylabel('Total Gastado')
    plt.tight_layout()
    
    
    # Mostramos el gráfico
    st.pyplot(fig)
    st.write("*Explicacion del grafico.*")




# ###################################################
# # 3ra Fila
# ###################################################



st.subheader('SUBTITULOS')
st.write('blablablabl')


c1_f3, c2_f3 = st.columns((5,5))


with c1_f3:
    # 6. Métodos de Pago Preferidos
    fig = plt.figure(figsize=(8, 6))
    # Creamos un gráfico de barras que muestra la cantidad de transacciones por cada método de pago, el grafico esta ordenado de mayor a menor frecuencia
    sns.countplot(data=df, x='Payment', order=df['Payment'].value_counts().index)
    plt.title('Métodos de pago preferidos')
    plt.xlabel('Método de pago')
    plt.ylabel('Frecuencia')
    plt.tight_layout()

    # Mostramos el gráfico
    st.pyplot(fig)
    st.write("*Explicacion del grafico.*")


with c2_f3:
  # 5. Relación entre Costo y Ganancia Bruta
    fig = plt.figure(figsize=(8, 6))
    # Creamos un gráfico de dispersión que muestra la relación entre el costo de bienes vendidos (COGS) y el ingreso bruto
    sns.scatterplot(data=df, x='cogs', y='gross income')
    plt.title('Relación entre costo y ganancia bruta')
    plt.xlabel('Costo de bienes vendidos (COGS)')
    plt.ylabel('Ingreso bruto')
    plt.tight_layout()
  
    # Mostramos el gráfico
    st.pyplot(fig)
    st.write("*Explicacion del grafico.*")



# ###################################################
# # 4ta Fila
# ###################################################


st.subheader('SUBTITULOS')
st.write('blablablabl')

c1_f4, c2_f4 = st.columns((5,5))

with c1_f4:
    # 7. Análisis de Correlación Numérica
    fig = plt.figure(figsize=(8, 6))
    # Seleccionamos las columnas numéricas relevantes para el análisis.
    numerical_cols = ['Unit price', 'Quantity', 'Tax 5%', 'Total', 'cogs', 'gross income', 'Rating']
    # Calculamos la matriz de correlación entre las variables numéricas seleccionadas
    correlation_matrix = df[numerical_cols].corr()
    # Generamos un mapa de calor para visualizar las correlaciones (coolwarm)
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Matriz de correlación de variables numéricas')

    # Mostramos el gráfico
    st.pyplot(fig)
    st.write("*Explicacion del grafico.*")


with c2_f4:
    # 8. Composición del Ingreso Bruto por Sucursal y Línea de Producto
    fig = plt.figure(figsize=(6, 5))
    # Creamos un gráfico de barras que muestra la suma del ingreso bruto por sucursal (agrupado), muestra ademas el desglose por línea de producto.
    sns.barplot(data=df, x='Branch', y='gross income', hue='Product line', estimator=sum)
    plt.title('Ingreso bruto por sucursal y línea de producto')
    plt.xlabel('Sucursal')
    plt.ylabel('Ingreso bruto')
    plt.legend(title='Línea de producto', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
  
    # Mostramos el gráfico
    st.pyplot(fig)
    st.write("*Explicacion del grafico.*")


# # Pie de página simple
st.markdown("---")
st.caption("Dashboard FALTA TITULO XXX | Datos: data.csv")

# Asegurar ejecución correcta en el entorno

