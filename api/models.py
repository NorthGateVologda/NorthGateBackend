from django.contrib.gis.db import models
from django.contrib.gis.geos import Point


class Facility(models.Model):
    facility_id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=255)
    x = models.FloatField()
    y = models.FloatField()
    number_of_inhabitants = models.FloatField()

    def get_location(self):
        return Point(self.x, self.y)

    class Meta:
        managed = False
        db_table = 'facility'


class ObjectTourism(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    house = models.CharField(max_length=255)
    post = models.CharField(max_length=255)
    x = models.FloatField()
    y = models.FloatField()
    wkb_geometry = models.GeometryField(srid=3857)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'objects_tourism'