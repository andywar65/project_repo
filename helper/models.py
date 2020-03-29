from django.db import models

def update_streamblocks( stream_list, obj_type, obj_id ):
    #queryset of streamhelpers related to object
    helpers = StreamHelper.objects.filter(obj_type=obj_type, obj_id=obj_id)
    #we prepare a list of tuples (stream_id, stream_type)
    stream_tuples = []
    for stream in stream_list:
        if isinstance( stream['id'], list ):
            #this is to cope with as_list streamblocks
            for stream_id in stream['id']:
                stream_tuples.append(( stream_id , stream[ 'model_name' ]))
        else:
            stream_tuples.append((stream['id'], stream[ 'model_name' ]))
    #we confront tuples agains queryset
    for stream_tuple in stream_tuples:
        if helpers.filter(stream_type=stream_tuple[1],
            stream_id=stream_tuple[0]):
            #pop out existing helpers
            helpers = helpers.exclude(stream_type=stream_tuple[1],
                stream_id=stream_tuple[0])
        else:
            #create new helpers
            helper = StreamHelper.objects.create(obj_type=obj_type,
                obj_id=obj_id, stream_type=stream_tuple[1],
                stream_id=stream_tuple[0])
            helper.save()
    #delete remaining helpers
    helpers.delete()
    return

class StreamHelper(models.Model):
    obj_type = models.IntegerField( null = True, )
    obj_id = models.IntegerField( null = True, )
    stream_type = models.CharField( null = True, max_length = 50 )
    stream_id = models.IntegerField( null = True, )
