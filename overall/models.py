from django.db import models
from djangotoolbox.fields import DictField, ListField
from usermgmt.models import CAUsers

import json

# Create your models here.

class FileUpload(models.Model):
    initial_file_name       = models.CharField(max_length=200)
    final_file_name         = models.CharField(max_length=200)
    file_path               = models.CharField(max_length=200)
    uploaded_at             = models.DateTimeField()
    file_type               = models.CharField(max_length=200)
    created_by              = models.ForeignKey(CAUsers,
                                on_delete=models.SET_NULL,
                                null=True)
    def __str__(self):
        return json.dumps({'id':self.id,'file_path':self.file_path})
