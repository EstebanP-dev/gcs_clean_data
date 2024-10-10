from django.db import models

# Create your models here. 
class SensorData(models.Model):
    timestamp = models.DateTimeField(null=True)
    mag_x = models.FloatField(null=True)
    mag_y = models.FloatField(null=True)
    mag_z = models.FloatField(null=True)
    barometro = models.FloatField(null=True)
    ruido = models.FloatField(null=True)
    giro_x = models.FloatField(null=True)
    giro_y = models.FloatField(null=True)
    giro_z = models.FloatField(null=True)
    acel_x = models.FloatField(null=True)
    acel_y = models.FloatField(null=True)
    acel_z = models.FloatField(null=True)
    vibracion = models.FloatField(null=True)
    gps_lat = models.FloatField(null=True)
    gps_lon = models.FloatField(null=True)

    class Meta:
        db_table = 'sensor_data'  
        verbose_name = 'Sensor Data'
        verbose_name_plural = 'Sensor Data'
        ordering = ['id']  

    def __str__(self):
        return f'SensorData(id={self.id}, timestamp={self.timestamp})'