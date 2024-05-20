from flask import Blueprint, render_template, request, redirect, url_for, session, flash, send_file
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
import geopandas as gpd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from class_firebase_database import FirebaseDB
from config import firebase_config
import folium
import os

# Inicializar FirebaseDB
credentials_path = "Esto lo encontraras en tu base de datos firebase"
database_url = "Esto tambien"
firebase_db = FirebaseDB(credentials_path, database_url)

events_blueprint = Blueprint('events', __name__)

@events_blueprint.route('/mi_perfil')
def mi_perfil():
    """Renderiza la página del perfil del usuario."""
    if 'user' in session:
        try:
            user_email = session['user_email']
            events = firebase_db.read_record('events')
            user_events = [event for event in events.values() if event['created_by'] == user_email]
            return render_template('mi_perfil.html', events=user_events)
        except Exception as e:
            flash('Failed to retrieve events. Please try again.', 'error')
            print(e)
            return redirect(url_for('home'))
    else:
        return redirect(url_for('login.login'))

@events_blueprint.route('/create_event', methods=['POST'])
def create_event():
    """Maneja la creación de eventos por parte del usuario."""
    if 'user' in session:
        if request.method == 'POST':
            event_name = request.form['event_name']
            event_date = request.form['event_date']
            department = request.form['department']
            municipality = request.form['municipality']
            address = request.form['address']
            event_type = request.form['event_type']
            num_participants = request.form['num_participants']
            event_duration = request.form['event_duration']
            event_description = request.form['event_description']
            user_email = session['user_email']
            
            event_data = {
                'name': event_name,
                'date': event_date,
                'department': department,
                'municipality': municipality,
                'address': address,
                'type': event_type,
                'participants': num_participants,
                'duration': event_duration,
                'description': event_description,
                'created_by': user_email
            }
            
            try:
                firebase_db.write_record(f'events/{event_name}', event_data)
                flash('Event created successfully!', 'success')
                return redirect(url_for('events.mi_perfil'))
            except Exception as e:
                flash('Failed to create event. Please try again.', 'error')
                print(e)
                return redirect(url_for('events.mi_perfil'))
        return render_template('create_event.html')
    else:
        return redirect(url_for('login.login'))

@events_blueprint.route('/edit_event', methods=['POST'])
def edit_event():
    """Edita los datos de un evento existente."""
    if 'user' in session:
        event_name = request.form['event_name']
        event_date = request.form['event_date']
        department = request.form['department']
        municipality = request.form['municipality']
        address = request.form['address']
        event_type = request.form['event_type']
        num_participants = request.form['num_participants']
        event_duration = request.form['event_duration']
        event_description = request.form['event_description']
        
        event_data = {
            'date': event_date,
            'department': department,
            'municipality': municipality,
            'address': address,
            'type': event_type,
            'participants': num_participants,
            'duration': event_duration,
            'description': event_description,
        }
        
        try:
            firebase_db.update_record(f'events/{event_name}', event_data)
            flash('Event updated successfully!', 'success')
            return redirect(url_for('events.mi_perfil'))
        except Exception as e:
            flash('Failed to update event. Please try again.', 'error')
            print(e)
            return redirect(url_for('events.mi_perfil'))
    else:
        return redirect(url_for('login.login'))

@events_blueprint.route('/delete_event', methods=['POST'])
def delete_event():
    """Elimina un evento existente."""
    if 'user' in session:
        event_name = request.form['event_name']
        try:
            firebase_db.delete_record(f'events/{event_name}')
            flash('Event deleted successfully!', 'success')
            return redirect(url_for('events.mi_perfil'))
        except Exception as e:
            flash('Failed to delete event. Please try again.', 'error')
            print(e)
            return redirect(url_for('events.mi_perfil'))
    else:
        return redirect(url_for('login.login'))

@events_blueprint.route('/view_event_map/<event_name>')
def view_event_map(event_name):
    """Renderiza el mapa de un evento específico."""
    if 'user' in session:
        try:
            event = firebase_db.read_record(f'events/{event_name}')
            
            if not event:
                flash('Event not found.', 'error')
                return redirect(url_for('events.mi_perfil'))
            
            # Crear un GeoDataFrame para el evento
            df = pd.DataFrame([event])
            
            # Geocodificar la dirección del evento
            geocoded_df = geocode_addresses(df)
            
            if geocoded_df['latitude'].isnull().any() or geocoded_df['longitude'].isnull().any():
                flash('Failed to geocode the event address. Please try again.', 'error')
                return redirect(url_for('events.mi_perfil'))
            
            gdf = gpd.GeoDataFrame(
                geocoded_df, geometry=gpd.points_from_xy(geocoded_df.longitude, geocoded_df.latitude)
            )
            
            # Crear un mapa de Folium
            event_map = folium.Map(location=[geocoded_df.latitude[0], geocoded_df.longitude[0]], zoom_start=15)
            folium.Marker([geocoded_df.latitude[0], geocoded_df.longitude[0]], popup=event_name).add_to(event_map)
            
            # Guardar el mapa en un archivo HTML
            map_path = os.path.join('static', 'maps', f'event_map_{event_name}.html')
            if not os.path.exists('static/maps'):
                os.makedirs('static/maps')
            event_map.save(map_path)
            
            return redirect(url_for('static', filename=f'maps/event_map_{event_name}.html'))
        except Exception as e:
            flash('Failed to generate event map. Please try again.', 'error')
            print(e)
            return redirect(url_for('events.mi_perfil'))
    else:
        return redirect(url_for('login.login'))


def geocode_addresses(df):
    """Geocodifica las direcciones de los eventos.

    Args:
        df (DataFrame): DataFrame con las ubicaciones de los eventos.

    Returns:
        DataFrame: DataFrame con las coordenadas geográficas de las ubicaciones.
    """
    geolocator = Nominatim(user_agent="sports_connect")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

    latitudes = []
    longitudes = []

    for index, row in df.iterrows():
        address = f"{row['address']}, {row['municipality']}, {row['department']}, Colombia"
        location = geocode(address)
        if location:
            latitudes.append(location.latitude)
            longitudes.append(location.longitude)
        else:
            latitudes.append(None)
            longitudes.append(None)

    df['latitude'] = latitudes
    df['longitude'] = longitudes

    return df
