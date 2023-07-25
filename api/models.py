from django.contrib.gis.db import models

class Facility(models.Model):
    facility_id =  models.AutoField(primary_key=True)
    address = models.CharField(max_length=255)
    x = models.FloatField()
    y = models.FloatField()
    number_of_inhabitants = models.FloatField()
    
    def get_location(self):
        return Point(self.x, self.y)
    
    class Meta:
        managed = False
        db_table = 'facility'