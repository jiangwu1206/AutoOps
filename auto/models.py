from django.db import models

# Create your models here.
class HostInfo(models.Model):
    ip = models.CharField(max_length=255)
    user = models.CharField(max_length=255)
    #password = models.CharField(max_length=255)
    server_name = models.CharField(max_length=255)
    port = models.IntegerField(default=80)
    cmd = models.CharField(max_length=255)
    host_date = models.DateTimeField()
    isDelete = models.BooleanField(default=False)

    def __str__(self):
        return "%s %s" %(self.ip,self.server_name)

class StatusInfo(models.Model):
    ip = models.CharField(max_length=255)
    port = models.IntegerField(default=80)
    status = models.CharField(max_length=255)
    status_date = models.DateTimeField()
    isDelete = models.BooleanField(default=False)

    def __str__(self):
        return "%s %s" %(self.ip, self.status)