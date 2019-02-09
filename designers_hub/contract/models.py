from django.db import models
from designers_hub import settings

from user_profile.models import Designer


class Contract(models.Model):
    title = models.CharField(max_length=100)
    date_created = models.DateField(auto_now_add=True, auto_now=False)
    description = models.TextField()
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    designer = models.ForeignKey(Designer, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=10, default="active")

    def __str__(self):
      return self.title

class ContractFile(models.Model):
    description = models.TextField(verbose_name="File Description")
    file_path = models.FileField(upload_to="contract_files/", verbose_name="Attach file")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)

    def __str__(self):
        return self.description
      
      
class Rating(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.DO_NOTHING)
    designer = models.ForeignKey(Designer, on_delete=models.CASCADE)
    rating = models.IntegerField(default=3)
