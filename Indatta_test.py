#!/usr/bin/env python
# coding: utf-8

# # Prueba técnica de Indatta

# ###### Desription
# El presente rep contiene los elementos para realizar el respectivo análisis técnico y los respectivos insight.
# ###### Glosario
# 1. NDV = Número de ventas realizadas
# 2. VPC = Ventas por canal

# ###### Insight primer grado

# In[88]:


import pandas as pd

Clientes = pd.read_csv("Tabla Clientes_indatta.csv")
Ventas = pd.read_csv("Tabla Ventas_indatta.csv")
Articulo = pd.read_csv("Tabla Articulo_indatta.csv", encoding='ISO-8859-1')


# In[101]:


# Fusiona las tablas en una nueva tabla basada en 'id_cliente' y 'Codigo Articulo'
df_combinado = pd.merge(Ventas, Clientes, left_on='Id Cliente', right_on='ID Cliente')
df_combinado_extendido = pd.merge(df_combinado, Articulo, on='Codigo Articulo', how='left')
df_1 = df_combinado_extendido.drop('ID Cliente', axis=1)


# In[102]:


# Cambiar columnas a tipo string
columnas_a_cambiar = ['Id Cliente', 'Codigo Articulo']
df_1[columnas_a_cambiar] = df_1[columnas_a_cambiar].astype(str)
df_1['Kilos'] = df_1['Kilos'].str.replace(',', '').astype(float)


# In[98]:


#Cantidad de Ventas realizadas.
NDV = len(Ventas['Nota de Venta'])
NDV


# In[128]:


#Distribución de Ventas por Canal

# Convertir 'Kilos' a numérico si no lo es
df_combinado['Kilos'] = pd.to_numeric(df_combinado['Kilos'], errors='coerce')
# Agrupar por 'Canal', contar 'ID Cliente' y sumar 'Kilos'
VPC = df_combinado.groupby('Canal').agg({'ID Cliente': 'count', 'Kilos': 'sum'}).reset_index()
# Renombrar columnas para claridad y ordenar por 'Cantidad_de_ventas' en orden descendente
VPC = VPC.rename(columns={'ID Cliente': 'Cantidad_de_ventas', 'Kilos': 'Total_Kilos'}).sort_values('Cantidad_de_ventas', ascending=False)
VPC


# In[129]:


#Top 5 de clientes que compraron más veces

# Obtener el canal más frecuente para cada cliente
canal_mas_frecuente = df_1.groupby('Id Cliente')['Canal'].agg(lambda x: x.mode()[0]).reset_index()

# Unir con la tabla de cliente_mas_compras
cliente_mas_compras_con_canal = pd.merge(cliente_mas_compras, canal_mas_frecuente, on='Id Cliente', how='left')


cliente_mas_compras_con_canal



# In[132]:


#Top 5 de clientes que compraron más kilos

# Obtener el canal más frecuente para cada cliente
canal_mas_frecuente = df_1.groupby('Id Cliente')['Canal'].agg(lambda x: x.mode()[0]).reset_index()
# Unir con la tabla de cliente_mas_kilos
cliente_mas_kilos_con_canal = pd.merge(cliente_mas_kilos, canal_mas_frecuente, on='Id Cliente', how='left')

cliente_mas_kilos_con_canal


# In[135]:


#Distribución de Ventas por mes.

# Convertir 'Fecha de Venta' a datetime con formato específico
df_1['Fecha de Venta'] = pd.to_datetime(df_1['Fecha de Venta'], format='%d/%m/%Y')

# Extraer el mes
df_1['Mes'] = df_1['Fecha de Venta'].dt.month
# Agrupar por mes y calcular las métricas deseadas
resumen_mensual = df_1.groupby('Mes').agg(Cantidad_Compras=('Id Cliente', 'size'),
                                          Total_Kilos=('Kilos', 'sum')).reset_index()
# Mostrar los resultados
print(resumen_mensual)


# In[137]:


#Coorelacion de cantidad de ventas vs kilos vendidos 
ventas_kilos_por_nota = df_1.groupby('Nota de Venta').agg(
    Cantidad_Ventas=('Nota de Venta', 'size'),
    Total_Kilos=('Kilos', 'sum')
).reset_index()
import matplotlib.pyplot as plt

plt.scatter(ventas_kilos_por_nota['Cantidad_Ventas'], ventas_kilos_por_nota['Total_Kilos'])
plt.title('Relación entre Cantidad de Ventas y Kilos Vendidos')
plt.xlabel('Cantidad de Ventas')
plt.ylabel('Total de Kilos Vendidos')
plt.show()
correlacion = ventas_kilos_por_nota['Cantidad_Ventas'].corr(ventas_kilos_por_nota['Total_Kilos'])
print("Correlación entre la cantidad de ventas y los kilos vendidos:", correlacion)


# In[140]:


#Coorelacion de cantidad de ventas vs kilos vendidos mejorada

import matplotlib.pyplot as plt
import numpy as np

# Supongamos que tenemos los siguientes datos como ejemplo (reemplazar con datos reales)
cantidad_ventas = np.ones(100)  # Todos los valores son 1
total_kilos_vendidos = np.random.exponential(scale=500, size=100)  # Ejemplo de datos

# Agregar jitter a 'cantidad_ventas'
jitter = 0.05 * np.random.randn(len(cantidad_ventas))
cantidad_ventas_jittered = cantidad_ventas + jitter

# Crear el gráfico de dispersión con jitter y transparencia
plt.figure(figsize=(10, 6))
plt.scatter(cantidad_ventas_jittered, total_kilos_vendidos, alpha=0.5)  # Alpha para transparencia
plt.title('Relación entre Cantidad de Ventas y Kilos Vendidos (con Jitter)')
plt.xlabel('Cantidad de Ventas')
plt.ylabel('Total de Kilos Vendidos')
plt.grid(True)
plt.show()


# In[141]:


# Asegúrate de que 'Fecha de Venta' es datetime
df_1['Fecha de Venta'] = pd.to_datetime(df_1['Fecha de Venta'])

# Extrae el mes de 'Fecha de Venta'
df_1['Mes'] = df_1['Fecha de Venta'].dt.month
# Agrupa por 'Canal' y 'Mes' y calcula las métricas deseadas
rendimiento_canal_mes = df_1.groupby(['Canal', 'Mes']).agg(
    Cantidad_Ventas=('Id Cliente', 'size'),
    Total_Kilos=('Kilos', 'sum')
).reset_index()
# Ordenar los resultados por 'Mes' y luego por 'Total_Kilos' descendente
rendimiento_canal_mes = rendimiento_canal_mes.sort_values(by=['Mes', 'Total_Kilos'], ascending=[True, False])
# Mostrar los resultados
print(rendimiento_canal_mes)


# ### Autor: Piero Guillén

# In[ ]:




