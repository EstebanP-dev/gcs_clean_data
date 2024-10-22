import geocoder
import random
from geopy import distance

# yourapp/gps.py

import random
from geopy import distance
import geocoder

class GPS:
    def __init__(self):
        try:
            # Obtener la posición actual del dispositivo
            g = geocoder.ip('me')  # Obtiene la ubicación basada en la IP
            if g.latlng:
                self.center_lat, self.center_lon = g.latlng  # Extrae latitud y longitud
            else:
                print("No se pudo obtener la ubicación basada en la IP.")
                # Establecer valores predeterminados o manejar el error
                self.center_lat = 0.0  # Reemplaza con una latitud predeterminada
                self.center_lon = 0.0  # Reemplaza con una longitud predeterminada
        except Exception as e:
            print(f"Error al obtener la ubicación: {e}")
            # Establecer valores predeterminados o manejar el error
            self.center_lat = 0.0
            self.center_lon = 0.0
        self.speed = 0  # Inicializa velocidad a 0 (m/s)
        self.bearing = 0  # Inicializa dirección a 0 (grados)
        self.max_distance = 100  # km, distancia máxima desde el centro

    def update_position(self):
        # Calcula el nuevo punto basado en la velocidad y dirección
        origin = (self.center_lat, self.center_lon)
        distance_meters = self.speed  # Suponiendo que la velocidad está en m/s
        destination = distance.distance(meters=distance_meters).destination(origin, self.bearing)

        new_lat, new_lon = destination.latitude, destination.longitude

        # Verifica si el nuevo punto está dentro del radio permitido
        if distance.distance(origin, (new_lat, new_lon)).km <= self.max_distance:
            self.center_lat, self.center_lon = new_lat, new_lon
        else:
            # Si está fuera del radio, genera un nuevo punto aleatorio dentro del área permitida
            angle = random.uniform(0, 360)  # Ángulo aleatorio en grados
            dist = random.uniform(0, self.max_distance * 1000)  # Distancia aleatoria en metros
            new_point = distance.distance(meters=dist).destination(origin, angle)
            self.center_lat, self.center_lon = new_point.latitude, new_point.longitude

        # Actualiza velocidad y dirección aleatoriamente con cambios más pronunciados
        self.speed += random.uniform(-1.5, 1.5)  # Cambia velocidad más agresivamente
        self.speed = max(0.5, min(self.speed, 15))  # Limita entre 0.5 y 15 m/s para evitar detenciones completas

        self.bearing += random.uniform(-30, 30)  # Cambia dirección más agresivamente
        self.bearing = self.bearing % 360  # Asegura que la dirección esté entre 0 y 360 grados

    def get_position(self, use_current_location=True):
        if use_current_location:
            try:
                g = geocoder.ip('me')
                if g.latlng:
                    return {
                        'latitude': g.latlng[0],
                        'longitude': g.latlng[1],
                        'speed': self.speed,
                        'bearing': self.bearing
                    }
                else:
                    print("No se pudo obtener la ubicación basada en la IP.")
            except Exception as e:
                print(f"Error al obtener la ubicación: {e}")
        
        # Si no se usa la ubicación actual, generar una posición aleatoria consistente
        self.update_position()
        return {
            'latitude': self.center_lat,
            'longitude': self.center_lon,
            'speed': self.speed,
            'bearing': self.bearing
        }
