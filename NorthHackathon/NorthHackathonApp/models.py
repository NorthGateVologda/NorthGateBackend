# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ArhangelskayaOblast(models.Model):
    ogc_fid = models.AutoField(primary_key=True)
    region = models.CharField(blank=True, null=True)
    id_full = models.IntegerField(blank=True, null=True)
    level = models.IntegerField(blank=True, null=True)
    type = models.CharField(blank=True, null=True)
    name = models.CharField(blank=True, null=True)
    wkb_geometry = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'arhangelskaya_oblast'


class AutoFootGraphArhObl(models.Model):
    ogc_fid = models.AutoField(primary_key=True)
    objectid = models.IntegerField(blank=True, null=True)
    fclass = models.CharField(blank=True, null=True)
    name = models.CharField(blank=True, null=True)
    ref = models.CharField(blank=True, null=True)
    oneway = models.CharField(blank=True, null=True)
    maxspeed = models.IntegerField(blank=True, null=True)
    layer = models.FloatField(blank=True, null=True)
    bridge = models.CharField(blank=True, null=True)
    tunnel = models.CharField(blank=True, null=True)
    auto = models.CharField(blank=True, null=True)
    foot = models.CharField(blank=True, null=True)
    meters = models.FloatField(blank=True, null=True)
    minutes = models.FloatField(blank=True, null=True)
    minutes_foot = models.FloatField(blank=True, null=True)
    wkb_geometry = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'auto_foot_graph_arh_obl'


class BaseOblPeople(models.Model):
    name = models.CharField(blank=True, null=True)
    type = models.CharField(blank=True, null=True)
    gicity = models.CharField(blank=True, null=True)
    okrug = models.CharField(blank=True, null=True)
    district = models.CharField(blank=True, null=True)
    okato = models.CharField(blank=True, null=True)
    oktmo = models.CharField(blank=True, null=True)
    wkb_geometry = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'base_obl_people'


class BaseOblPeople3000(models.Model):
    name = models.CharField(blank=True, null=True)
    type = models.CharField(blank=True, null=True)
    gicity = models.CharField(blank=True, null=True)
    okrug = models.CharField(blank=True, null=True)
    district = models.CharField(blank=True, null=True)
    people = models.IntegerField(blank=True, null=True)
    okato = models.CharField(blank=True, null=True)
    oktmo = models.CharField(blank=True, null=True)
    wkb_geometry = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'base_obl_people_3000'


class Buildings(models.Model):
    city = models.CharField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    wkb_geometry = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'buildings'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class MunObrAllBad(models.Model):
    name = models.CharField(blank=True, null=True)
    type = models.CharField(blank=True, null=True)
    level = models.IntegerField(blank=True, null=True)
    sub = models.IntegerField(blank=True, null=True)
    region = models.CharField(blank=True, null=True)
    people = models.IntegerField(blank=True, null=True)
    sum_bad = models.FloatField(blank=True, null=True)
    percent = models.FloatField(blank=True, null=True)
    road_density = models.FloatField(blank=True, null=True)
    road_demand = models.IntegerField(blank=True, null=True)
    id_full = models.IntegerField(blank=True, null=True)
    count_bad = models.IntegerField(blank=True, null=True)
    avg_free_speed_to_limit = models.FloatField(blank=True, null=True)
    sum_all = models.FloatField(blank=True, null=True)
    sum_all_signal = models.FloatField(blank=True, null=True)
    wkb_geometry = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'mun_obr_all_bad'


class MunObrArctic(models.Model):
    name = models.CharField(blank=True, null=True)
    type = models.CharField(blank=True, null=True)
    level_field = models.IntegerField(db_column='level_', blank=True, null=True)  # Field renamed because it ended with '_'.
    sub = models.IntegerField(blank=True, null=True)
    id_full = models.IntegerField(blank=True, null=True)
    region = models.CharField(blank=True, null=True)
    district = models.CharField(blank=True, null=True)
    okrug = models.CharField(blank=True, null=True)
    people = models.IntegerField(blank=True, null=True)
    oktmo = models.CharField(blank=True, null=True)
    okato = models.CharField(blank=True, null=True)
    wkb_geometry = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'mun_obr_arctic'


class ObjectsEducation(models.Model):
    name = models.CharField(blank=True, null=True)
    city = models.CharField(blank=True, null=True)
    street = models.CharField(blank=True, null=True)
    house = models.CharField(blank=True, null=True)
    post = models.CharField(blank=True, null=True)
    x = models.FloatField(blank=True, null=True)
    y = models.FloatField(blank=True, null=True)
    wkb_geometry = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'objects_education'


class ObjectsTourism(models.Model):
    name = models.CharField(blank=True, null=True)
    city = models.CharField(blank=True, null=True)
    street = models.CharField(blank=True, null=True)
    house = models.CharField(blank=True, null=True)
    post = models.CharField(blank=True, null=True)
    x = models.FloatField(blank=True, null=True)
    y = models.FloatField(blank=True, null=True)
    wkb_geometry = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'objects_tourism'


class ObjectsZdrav(models.Model):
    name = models.CharField(blank=True, null=True)
    city = models.CharField(blank=True, null=True)
    street = models.CharField(blank=True, null=True)
    house = models.CharField(blank=True, null=True)
    post = models.CharField(blank=True, null=True)
    x = models.FloatField(blank=True, null=True)
    y = models.FloatField(blank=True, null=True)
    cpi_id = models.IntegerField(blank=True, null=True)
    wkb_geometry = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'objects_zdrav'


class SlowRoadsLines(models.Model):
    category = models.IntegerField(blank=True, null=True)
    category_name = models.CharField(blank=True, null=True)
    dates = models.CharField(blank=True, null=True)
    free_speed_to_limit = models.FloatField(blank=True, null=True)
    length = models.IntegerField(blank=True, null=True)
    region = models.CharField(blank=True, null=True)
    geom_length = models.FloatField(blank=True, null=True)
    wkb_geometry = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'slow_roads_lines'


class SpatialRefSys(models.Model):
    srid = models.IntegerField(primary_key=True)
    auth_name = models.CharField(max_length=256, blank=True, null=True)
    auth_srid = models.IntegerField(blank=True, null=True)
    srtext = models.CharField(max_length=2048, blank=True, null=True)
    proj4text = models.CharField(max_length=2048, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'spatial_ref_sys'
