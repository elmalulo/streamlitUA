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

st.markdown("<span style=“background-color:#ffffff>",unsafe_allow_html=True)

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








st.markdown("""
<style>
    [data-testid=stSidebar] {
        background-color: #B3DAFF;
    }
  
    [st-bt.]{
    color: #B3DAFF;
    }
    .st-bu {
    background-color: #009C8E;
    }   
  .st-ar {
    background: linear-gradient(to right, rgba(151, 166, 195, 0.25) 0%, rgba(151, 166, 195, 0.25) 0%, rgb(82 124 255) 0%, rgb(255 233 23) 100%, rgba(151, 166, 195, 0.25) 100%, rgba(151, 166, 195, 0.25) 100%)
    }  


</style>
""", unsafe_allow_html=True)

with st.sidebar:
    
   # Selector de rango de años
    mes_inicio, mes_fin = st.sidebar.slider(
    'Range month', 
     df['Date'].dt.month.min(), 
     df['Date'].dt.month.max(), 
    (1, 12)
)
    # Selector de componentes del PIB (solo para el gráfico de área)
    filter_city = st.sidebar.multiselect(
        'City', 
        options= df.groupby('City')
    ,    default=df.groupby('City'),
        help="Selecciona los componentes para visualizar en el gráfico de área"
    )

    filter_product = st.sidebar.multiselect(
        'Product line', 
        options= df.groupby('Product line')
    ,    default=df.groupby('Product line'),
        help="Selecciona los componentes para visualizar en el gráfico de área"
    )

# ##################################################
# # FILTRADO DE DATOS
# ##################################################
    df_filtrado = df[df['City'].isin(filter_city)]
    df_filtrado = df[df['Product line'].isin(filter_product)]

#TITULO###
st.title("Analisis de venta")
st.header(" Identificación y justificación de variables relevan")
st.markdown("+ CustomerID: Permite identificar a los clientes y sus compras.\n\
+ Product: Identifica los productos permitiendo conocer los más populares o rentables.\n\
+ Quantity: Ayuda a entender el volumen de venta.\n\
+ Price: Permite calcular ingresos.\n\
+ PurchaseDate: Es clave para detectar patrones de venta por fecha.\n\
+ Region: Facilita el análisis regional de ventas.")

st.header("Reflexión sobre la importancia de las variables")
st.markdown("+ CustomerID: Permite identificar a los clientes y sus compras.\n+ Product: Identifica los productos permitiendo conocer los más populares o rentables.\n+ Quantity: Ayuda a entender el volumen de venta.\n+ Price: Permite calcular ingresos.\n+ PurchaseDate: Es clave para detectar patrones de venta por fecha.\n+ Region: Facilita el análisis regional de ventas.")



# #########################################################
# # SECCIÓN DE GRÁFICOS 
# #########################################################


# # Sección: Composición del PIB
st.subheader('COMPORTAMIENTO DE VENTAS EN EL TIEMPO')


# Dividimos la pantalla en dos columnas (proporción 5:5)
c1_f1, c2_f1 = st.columns((5,5))

with c1_f1:
    if filter_city:

        fig, ax = plt.subplots(figsize=(10, 3))
        sales_over_time = df_filtrado.groupby('Date')['Total'].sum().reset_index()
        sns.lineplot(data=sales_over_time, x='Date', y='Total')
     
        # Etiquetas y cuadrícula
        ax.set_ylabel("Ventas totales $")
        ax.set_xlabel("Fecha calendario")
        ax.set_title("Evolución de las ventas totales")
        ax.grid(True, alpha=0.5)

    
    
        st.pyplot(fig)
        st.write("*El gráfico muestra las ventas diarias, permitiendo identificar temporadas altas y posibles caídas en las ventas. Resulta útil para detectar patrones y para apoyar la toma de decisiones , mejorando posibles estrategias de ventas e inventario.*")
    else:
        st.info("Selecciona al menos una ciudad del filtro")


c1_fx, c2_fx = st.columns((5,5))
with c1_fx:
        # 8. Composición del Ingreso Bruto por Sucursal y Línea de Producto
        fig = plt.figure(figsize=(6, 5))
        # Creamos un gráfico de barras que muestra la suma del ingreso bruto por sucursal (agrupado), muestra ademas el desglose por línea de producto.
        sns.barplot(data=df_filtrado, x='Branch', y='gross income', hue='Product line', estimator=sum)
        plt.title('Ingreso bruto por sucursal y línea de producto')
        plt.xlabel('Sucursal')
        plt.ylabel('Ingreso bruto')
        plt.legend(title='Línea de producto', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
    
        # Mostramos el gráfico
        st.pyplot(fig)
        st.write("*El gráfico muestrea el ingreso bruto por sucursal, desglosado por línea de producto. Ayuda a comparar el rendimiento entre sucursales y entender qué productos generan mayores ingresos en cada una. Útil para optimizar la estrategia de venta de los productos.*")
with c2_fx:
    ""

with c2_f1:
    if filter_product:
        fig  = plt.figure(figsize=(10, 4))
        sns.barplot(data=df_filtrado, x='Product line', y='Total', estimator=sum)
        plt.title('Ingresos por linea de producto')
        plt.ylabel('Total ingresos')
        plt.tight_layout()
       
        # # Mostramos el gráfico en Streamlit
        st.pyplot(fig)
        st.write("*El siguiente gráfico presenta los ingresos totales por línea de producto, mostrandonos el desempeño por categoría de producto. Permite identificar cuáles productos generan mayores ventas y a la toma de decisiones sobre el inventario o promociones.*")
    else:
        st.info("Selecciona al menos un producto del filtro")



# ###################################################
# # 2da Fila
# ###################################################




st.subheader('COMPORTAMIENTO CLIENTES')
st.write('Buscamos clasificar los tipos de clientes que se presentan acorde a la distribución de atributos relacionados')

c1_f2, c2_f2 = st.columns((5,5))

with c1_f2:
    fig = plt.figure(figsize=(8, 6))
    # Creamos un histograma de la columna 'Rating'
    sns.histplot(df_filtrado['Rating'], bins=20, kde=True)
    plt.title('Distribución de la Calificación de Clientes')
    plt.xlabel('Rating')
    plt.ylabel('Frecuencia')
    plt.tight_layout()
    plt.show()
  
    # Mostramos el gráfico
    st.pyplot(fig)
    st.write("*Se denota la distribución de calificaciones (rating) entregadas por los clientes, nos ayuda a conocer la percepción del servicio. Lo cual se traduce en posibles mejoras en la experiencia del cliente, clave para fortalecer la fidelización y la calidad del servicio.*")


with c2_f2:
    # 4. Comparación del Gasto por Tipo de Cliente
    fig = plt.figure(figsize=(8, 6))
    # Creamos un boxplot que compara la distribución del gasto total segun el tipo de cliente.
    sns.boxplot(data=df_filtrado, x='Customer type', y='Total')
    plt.title('Comparación del Gasto por Tipo de Cliente')
    plt.xlabel('Tipo de Cliente')
    plt.ylabel('Total Gastado')
    plt.tight_layout()
    
    
    # Mostramos el gráfico
    st.pyplot(fig)
    st.write("*El gráfico nos brinda la distribución del gasto total según el tipo de cliente. Permite identificar diferencias de consumo y qué tipo de cliente gasta más dinero en las sucursales. Es útil para investigar estrategias de ventas.*")




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
    st.write("*El gráfico muestra la frecuencia de uso de los método de pago. Facilita la identificación de los medios más utilizados, lo cual es clave para mejorar las opciones de pago, mejorar la experiencia de compra y tomar decisiones comerciales o que involucren la operacion de la sucursal.*")


with c2_f3:
  # 5. Relación entre Costo y Ganancia Bruta
    fig = plt.figure(figsize=(8, 6))
    # Creamos un gráfico de dispersión que muestra la relación entre el costo de bienes vendidos (COGS) y el ingreso bruto
    sns.scatterplot(data=df_filtrado, x='cogs', y='gross income')
    plt.title('Relación entre costo y ganancia bruta')
    plt.xlabel('Costo de bienes vendidos (COGS)')
    plt.ylabel('Ingreso bruto')
    plt.tight_layout()
  
    # Mostramos el gráfico
    st.pyplot(fig)
    st.write("*El siguiente gráfico muestra la relación entre el costo de los productos vendidos y la ganancia bruta. Permite observar cómo varía el ingreso bruto en función del costo de los productos. Es útil para analizar los márgenes de ganacia en las ventas.*")



# ###################################################
# # 4ta Fila
# ###################################################


st.subheader('OBSERVAVILIDAD DE VARIABLES')
st.write('simple correlacion de parametros')

c1_f4, c2_f4 = st.columns((5,5))

with c1_f4:
    # 7. Análisis de Correlación Numérica
    fig = plt.figure(figsize=(8, 6))
    # Seleccionamos las columnas numéricas relevantes para el análisis.
    numerical_cols = ['Unit price', 'Quantity', 'Tax 5%', 'Total', 'cogs', 'gross income', 'Rating']
    # Calculamos la matriz de correlación entre las variables numéricas seleccionadas
    correlation_matrix = df_filtrado[numerical_cols].corr()
    # Generamos un mapa de calor para visualizar las correlaciones (coolwarm)
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Matriz de correlación de variables numéricas')

    # Mostramos el gráfico
    st.pyplot(fig)
    st.write("*El gráfico muestra la correlación entre variables numéricas importantes del negocio. Permite identificar relaciones entre indicadores como precio, cantidad, ingresos y calificaciones. Es útil para entender patrones de comportamiento, apoyar decisiones analíticas y detectar variables influyentes en el desempeño comercial.*")


with c2_f4:
   ""

# # Pie de página simple
st.markdown("---")
st.caption("Dashboard Analisis de venta grupo 17 | Datos: data.csv")

# Asegurar ejecución correcta en el entorno

