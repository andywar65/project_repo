from django.db import models

class StreamHelper(models.Model):
    obj_type = models.IntegerField( null = True, )
    obj_id = models.IntegerField( null = True, )
    stream_type = models.CharField( null = True, max_length = 50 )
    stream_id = models.IntegerField( null = True, )
