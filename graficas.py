import matplotlib
matplotlib.use('Agg')  # Usar el backend 'Agg' para evitar errores de GUI
import pandas as pd
import matplotlib.pyplot as plt
import io


def generate_charts():
    """Genera un gráfico de barras horizontales para escenarios deportivos.

    Carga los datos desde un archivo CSV, filtra los escenarios deportivos y 
    crea un gráfico de barras horizontales que muestra la cantidad de 
    escenarios por departamento. El gráfico se guarda en un objeto BytesIO 
    y se devuelve.

    Returns:
        BytesIO: El gráfico de barras en formato PNG.
    """
    # Cargar el archivo CSV
    ruta = (
        "https://raw.githubusercontent.com/Yolian007/Informacion/main/Datos%20"
        "ppi/Datos%20app%20web%20deportes/Consolidado_Escenarios_20240518.csv"
    )
    data = pd.read_csv(ruta)

    # Filtrar datos para escenarios deportivos
    escenarios = data[data['tipo'] == 'ESCENARIO']

    # Contar escenarios por departamento
    escenarios_por_departamento = escenarios['departamento'].value_counts()

    # Crear el gráfico de barras horizontales
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.barh(
        escenarios_por_departamento.index, 
        escenarios_por_departamento.values, 
        color='skyblue'
    )
    ax.set_xlabel('Número de Escenarios', fontsize=14)
    ax.set_ylabel('Departamento', fontsize=14)
    ax.tick_params(axis='x', labelsize=12)
    ax.tick_params(axis='y', labelsize=12)
    # Invertir el eje Y para mostrar el depto. con más escenarios arriba
    ax.invert_yaxis()

    # Guardar el gráfico en un objeto BytesIO
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    return img


def generate_bar_chart(department):
    """Genera un gráfico de barras horizontales para ligas deportivas.

    Carga los datos desde un archivo CSV, filtra las ligas deportivas según 
    el departamento especificado y crea un gráfico de barras horizontales 
    que muestra la cantidad de ligas por departamento. El gráfico se guarda 
    en un objeto BytesIO y se devuelve.

    Args:
        department (str): El nombre del departamento para filtrar las ligas.

    Returns:
        BytesIO: El gráfico de barras en formato PNG.
    """
    # Cargar el archivo CSV
    file_path = (
        'https://raw.githubusercontent.com/Yolian007/Informacion/main/Datos%'
        '20ppi/Datos%20app%20web%20deportes/Consolidado_Escenarios_20240518.'
        'csv'
    )
    data = pd.read_csv(file_path)

    # Filtrar datos para ligas deportivas y por depto. si no es 'all'
    if department != 'all':
        ligas = data[
            (data['tipo'] == 'LIGAS') & 
            (data['departamento'] == department)
        ]
    else:
        ligas = data[data['tipo'] == 'LIGAS']

    # Contar ligas por departamento
    ligas_por_departamento = ligas['departamento'].value_counts()

    # Crear el gráfico de barras horizontales
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.barh(
        ligas_por_departamento.index, 
        ligas_por_departamento.values, 
        color='skyblue'
    )
    ax.set_xlabel('Cantidad de Ligas', fontsize=14)
    ax.set_ylabel('Departamento', fontsize=14)
    ax.set_title(
        f'Distribución de Ligas Deportivas por Departamento - {department}',
        fontsize=16
    )
    ax.tick_params(axis='x', labelsize=12)
    ax.tick_params(axis='y', labelsize=12)
    # Invertir el eje Y para mostrar el depto. con más ligas arriba
    ax.invert_yaxis()

    # Guardar el gráfico en un objeto BytesIO
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    return img


