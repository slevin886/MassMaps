from django.db import models


class Origins(models.Model):
    name = models.CharField(max_length=75)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __repr__(self):
        return f"{self.name}"


class Commute(models.Model):
    MODE_CHOICES = (
        ('transit', 'Public Transportation'),
        ('driving', 'Driving')
    )
    origin = models.ForeignKey(Origins, on_delete=models.CASCADE, db_index=True)
    distance = models.IntegerField()
    duration = models.IntegerField()
    in_traffic = models.IntegerField(null=True)
    date = models.DateTimeField(db_index=True)
    mode = models.CharField(choices=MODE_CHOICES, max_length=8, db_index=True)

    def __repr__(self):
        return f"{self.origin}, {self.date}"
