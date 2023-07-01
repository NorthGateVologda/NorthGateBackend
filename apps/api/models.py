from django.contrib.gis.db import models


class Username(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'usernames'

class ObjectTourism(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    house = models.CharField(max_length=255)
    post = models.CharField(max_length=255)
    x = models.FloatField()
    y = models.FloatField()
    wkb_geometry = models.GeometryField()

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'objects_tourism'

class BufferObjectTourism(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    house = models.CharField(max_length=255)
    post = models.CharField(max_length=255)
    x = models.FloatField()
    y = models.FloatField()
    username = models.CharField(max_length=255)
    wkb_geometry = models.GeometryField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'buffer_objects_tourism'