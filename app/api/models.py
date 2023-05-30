from django.db import models

class Pump(models.Model):
    date = models.DateTimeField(primary_key=True)
    state = models.BooleanField()    

class Sensors(models.Model):
    date = models.DateTimeField(primary_key=True)
    ph = models.DecimalField(max_digits = 5, decimal_places = 2)
    water_level = models.DecimalField(max_digits = 5, decimal_places = 2)
    salinity = models.DecimalField(max_digits = 5, decimal_places = 2)
    pressure = models.DecimalField(max_digits = 5, decimal_places = 2)
    flow = models.DecimalField(max_digits = 5, decimal_places = 2)

class Fertilizers(models.Model):
    class Meta:
        unique_together = (('date', 'idx'),)    
    date = models.DateTimeField(primary_key=True)
    idx = models.IntegerField()
    state = models.BooleanField()
    running_time = models.BigIntegerField()

class Breakers(models.Model):
    class Meta:
        unique_together = (('date', 'idx'),)        
    date = models.DateTimeField(primary_key=True)
    idx = models.IntegerField()
    state = models.BooleanField()

class Valves(models.Model):
    class Meta:
        unique_together = (('date', 'idx'),)             
    date = models.DateTimeField(primary_key=True)
    idx = models.IntegerField()
    state = models.BooleanField()