from django.db import models

# Reference https://realpython.com/django-migrations-a-primer/
class File(models.Model):
    url = models.fields.TextField()
    org_id = models.fields.IntegerField()
    user_id = models.fields.IntegerField()

    class Meta:
        unique_together = ('url','org_id', 'user_id') #https://stackoverflow.com/a/29461922

class FileVersionInformation(models.Model):
    # One to one reference https://docs.djangoproject.com/en/4.2/topics/db/examples/one_to_one/
    file_version_id = models.OneToOneField(
        File, on_delete=models.CASCADE, db_index=True)
    version_number = models.fields.PositiveIntegerField()
    #How to populate this field with utc time https://stackoverflow.com/a/11263695 
    created_at = models.DateTimeField(auto_now_add=True) 
    details = models.fields.BinaryField()
    
    class Meta:
        unique_together = ('file_version_id','version_number') #https://stackoverflow.com/a/29461922
