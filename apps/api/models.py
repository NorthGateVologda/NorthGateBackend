from django.contrib.gis.db import models


class Username(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

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
    wkb_geometry = models.GeometryField(srid=3857)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'objects_tourism'

class BufferObjectTourism(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    street = models.CharField(max_length=255, null=True)
    house = models.CharField(max_length=255, null=True)
    post = models.CharField(max_length=255, null=True)
    x = models.FloatField()
    y = models.FloatField()
    username = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    wkb_geometry = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'buffer_objects_tourism'