import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io

def cargar_datos(ruta):
    """Carga los datos desde un archivo CSV.

    Args:
        ruta (str): Ruta al archivo CSV.

    Returns:
        DataFrame: Datos cargados en un DataFrame.
    """
    return pd.read_csv(ruta)

def filtrar_datos(data, tipo):
    """Filtra los datos por tipo y cuenta por departamento.

    Args:
        data (DataFrame): Datos a filtrar.
        tipo (str): Tipo de escenario o liga.

    Returns:
        ndarray: Conteo de escenarios o ligas por departamento.
    """
    return data[data['tipo'] == tipo]['departamento'].value_counts().values

def calcular_estadisticas(valores):
    """Calcula estadísticas básicas usando NumPy.

    Args:
        valores (ndarray): Array de valores.

    Returns:
        dict: Diccionario con media, mediana, desviación estándar y total.
    """
    return {
        'media': np.mean(valores),
        'mediana': np.median(valores),
        'desviacion': np.std(valores),
        'total': np.sum(valores)
    }

def graficar_estadisticas(estadisticas, titulo, ax):
    """Genera un gráfico de barras con estadísticas calculadas.

    Args:
        estadisticas (dict): Diccionario con estadísticas.
        titulo (str): Título del gráfico.
        ax (Axes): Eje de Matplotlib para graficar.
    """
    categorias = ['Media', 'Mediana', 'Desviación Estándar']
    valores = [estadisticas['media'], estadisticas['mediana'],
               estadisticas['desviacion']]
    colores = ['blue', 'green', 'red']
    
    ax.bar(categorias, valores, color=colores)
    ax.set_title(titulo)
    ax.set_ylabel('Valores')
    ax.set_ylim(0, max(valores) * 1.2)

    for i, v in enumerate(valores):
        ax.text(i, v + 0.1, f'{v:.2f}', ha='center', va='bottom')

    ax.text(1, max(valores) * 1.1, f'Total: {estadisticas["total"]}',
            ha='center', va='bottom', fontsize=12)

def generar_graficos_estadisticas():
    """Genera gráficos de estadísticas y los guarda en un objeto BytesIO.

    Returns:
        BytesIO: Imagen del gráfico en formato PNG.
    """
    ruta = (
        'https://raw.githubusercontent.com/Yolian007/Informacion/main/'
        'Datos%20ppi/Datos%20app%20web%20deportes/Consolidado_Escenarios_'
        '20240518.csv'
    )
    data = cargar_datos(ruta)
    escenarios = filtrar_datos(data, 'ESCENARIO')
    ligas = filtrar_datos(data, 'LIGAS')

    stats_escenarios = calcular_estadisticas(escenarios)
    stats_ligas = calcular_estadisticas(ligas)

    fig, axs = plt.subplots(1, 2, figsize=(14, 6))
    graficar_estadisticas(stats_escenarios,
                          'Estadísticas de Escenarios por Departamento',
                          axs[0])
    graficar_estadisticas(stats_ligas,
                          'Estadísticas de Ligas por Departamento',
                          axs[1])

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    return img
