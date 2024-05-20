from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import pyrebase
import requests
from config import firebase_config

# Inicializar Firebase
firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

login_blueprint = Blueprint('login', __name__)

@login_blueprint.route('/signin', methods=['GET', 'POST'])
def login():
    """Maneja el inicio de sesión del usuario."""
    if request.method == 'POST':
        email = request.form['username']
        password = request.form['password']
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = user['idToken']
            session['user_email'] = email
            flash('¡Inicio de sesión exitosamente!', 'success')
            return redirect(url_for('home'))
        except Exception as e:
            flash('Credenciales no válidas. Inténtalo de nuevo.', 'error')
            return redirect(url_for('login.login'))
    return render_template('login.html')

@login_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    """Maneja el registro de un nuevo usuario."""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            auth.create_user_with_email_and_password(email, password)
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = user['idToken']
            session['user_email'] = email
            flash('¡Registro exitoso! Ahora está conectado.', 'success')
            return redirect(url_for('home'))
        except Exception as e:
            flash('Registro fallido. Inténtalo de nuevo.', 'error')
            return redirect(url_for('login.signup'))
    return render_template('login.html')

@login_blueprint.route('/logout')
def logout():
    """Cierra la sesión del usuario."""
    session.pop('user', None)
    session.pop('user_email', None)
    flash('Cerró sesión exitosamente.', 'success')
    return redirect(url_for('login.login'))

@login_blueprint.route('/home')
def home():
    """Renderiza la página de inicio después de iniciar sesión o registrarse."""
    if 'user' in session:
        user_email = session['user_email']
        return render_template('home.html', user_email=user_email)
    else:
        return redirect(url_for('login.login'))

@login_blueprint.route('/settings')
def settings():
    """Renderiza la página de configuración."""
    if 'user' in session:
        return render_template('settings.html')
    else:
        return redirect(url_for('login.login'))

@login_blueprint.route('/update_password', methods=['POST'])
def update_password():
    """Actualiza la contraseña del usuario."""
    if 'user' in session:
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        email = session['user_email']
        
        try:
            # Re-autenticar al usuario
            user = auth.sign_in_with_email_and_password(email, current_password)
            
            # Actualizar la contraseña usando la REST API de Firebase
            id_token = user['idToken']
            firebase_api_key = firebase_config['apiKey']
            url = f"https://identitytoolkit.googleapis.com/v1/accounts:update?key={firebase_api_key}"
            
            payload = {
                'idToken': id_token,
                'password': new_password,
                'returnSecureToken': True
            }
            
            response = requests.post(url, json=payload)
            response_data = response.json()
            
            if response.status_code == 200:
                flash('¡Contraseña actualizada exitosamente!', 'success')
                return redirect(url_for('login.settings'))
            else:
                flash('No se pudo actualizar la contraseña. Inténtalo de nuevo.', 'error')
                print(response_data)
                return redirect(url_for('login.settings'))
        except Exception as e:
            flash('No se pudo actualizar la contraseña. Inténtalo de nuevo.', 'error')
            print(e)
            return redirect(url_for('login.settings'))
    else:
        return redirect(url_for('login.login'))
