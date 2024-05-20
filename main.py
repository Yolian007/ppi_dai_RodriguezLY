from flask import Flask, redirect, render_template, request, send_file, session, url_for
import pandas as pd
from login import login_blueprint  # Importa el Blueprint de login.py
from graficas import generate_charts, generate_bar_chart
from estadisticas import generar_graficos_estadisticas
from eventos import events_blueprint  # Importa el Blueprint de events.py

app = Flask(__name__)
app.secret_key = "Aqui va la key que encontraras en firebase"

# Registra el Blueprint
app.register_blueprint(login_blueprint, url_prefix='/auth')
app.register_blueprint(events_blueprint, url_prefix='/events')

@app.route('/')
def index():
    """Renderiza la página principal."""
    departamentos = get_departamentos()
    return render_template('Index.html', departamentos=departamentos, title="Home")

@app.route('/home')
def home():
    """Renderiza la página de inicio."""
    if 'user' in session:
        user_email = session['user_email']
        return render_template('home.html', user_email=user_email)
    else:
        return redirect(url_for('login.login'))

@app.route('/update_chart')
def update_chart():
    """Actualiza el gráfico según el departamento seleccionado."""
    department = request.args.get('department')
    img = generate_bar_chart(department)
    return send_file(img, mimetype='image/png')

@app.route('/chart')
def chart():
    """Muestra el gráfico actual según el departamento seleccionado."""
    department = request.args.get('department', 'all')
    img = generate_bar_chart(department)
    return send_file(img, mimetype='image/png')

@app.route('/escenarios_chart')
def escenarios_chart():
    """Muestra el gráfico de escenarios deportivos."""
    img = generate_charts()
    return send_file(img, mimetype='image/png')

@app.route('/estadisticas')
def estadisticas():
    """Genera gráficos de estadísticas de escenarios y ligas."""
    img = generar_graficos_estadisticas()
    return send_file(img, mimetype='image/png')

def get_departamentos():
    """Obtiene la lista de departamentos desde el archivo CSV."""
    file_path = (
        'https://raw.githubusercontent.com/Yolian007/Informacion/main/'
        'Datos%20ppi/Datos%20app%20web%20deportes/Consolidado_Escenarios_'
        '20240518.csv'
    )
    data = pd.read_csv(file_path)
    return data['departamento'].unique()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
