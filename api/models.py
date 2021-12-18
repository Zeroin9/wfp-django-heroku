from datetime import datetime
from django.db import models

# Model of parcel with track-code
class Parcel(models.Model):
    track_code = models.CharField(max_length=250, unique=True)
    created_date = models.DateTimeField(default=datetime.now)
    updated_date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return str(self.track_code)

# Model of operation which can be getting from tracking API
class Operation(models.Model):
    date = models.DateTimeField(default=datetime.now)
    postOfficeIndex = models.CharField(max_length=6)
    postOfficeName = models.CharField(max_length=250)
    name = models.CharField(max_length=250)
    parcel = models.ForeignKey(Parcel, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)

# Model of token to identificate users
class Token(models.Model):
    # it will be UUID string
    token = models.CharField(max_length=36, unique=True)

    def __str__(self):
        return 'token ' + str(self.token)

# Model for Many-to-Many relationship between Token and Parcel
class ParcelTokenLink(models.Model):
    parcel = models.ForeignKey(Parcel, on_delete=models.CASCADE)
    token = models.ForeignKey(Token, on_delete=models.CASCADE)

    def __str__(self):
        return 'relate ' + str(self.parcel) + ' and ' + str(self.token)