from django.db import models

# Create your models here.
class Wallet(models.Model):
    name = models.CharField(max_length=20)
    wallet_id = models.BigIntegerField()
    text = models.TextField()
    class Meta:
        db_table = 'wallets'

class Reklama(models.Model):
    text = models.TextField()
    class Meta:
        db_table = 'reklama'

class Vipbot(models.Model):
    price = models.IntegerField()
    price_type = models.CharField(max_length=15)
    expiry_date = models.IntegerField()
    class Meta:
        db_table = 'vip'
class Admins(models.Model):
    telegram_chat_id = models.BigIntegerField(unique=True)
    class Meta:
        db_table = 'admins'
class UserBot(models.Model):
    telegram_chat_id = models.BigIntegerField(unique=True)
    balans = models.IntegerField(default=0)
    is_vip = models.BooleanField(default=False)
    vip_expiry_date = models.DateTimeField(null=True, blank=True)
    is_ban = models.BooleanField(default=False)
    class Meta:
        db_table = 'users'

class Channelforforced(models.Model):
    channel_id = models.BigIntegerField(unique=True)
    class Meta:
        db_table = 'forced_channel'
class ChannelforBot(models.Model):
    channel_id = models.BigIntegerField(unique=True)
    class Meta:
        db_table = 'channel_for_receive'

class Movie(models.Model):
    image = models.TextField()
    title = models.CharField(max_length=100)    
    ganre = models.CharField(max_length=50)
    year = models.IntegerField()
    tili = models.CharField(max_length=30)
    country = models.CharField(max_length=40)
    film = models.TextField(blank=True, null=True)
    code = models.IntegerField(unique=True)
    class Meta:
        db_table = 'movie'

class Serial(models.Model):
    image = models.TextField()
    count_series = models.IntegerField()
    title = models.CharField(max_length=100)    
    ganre = models.CharField(max_length=50)
    year = models.IntegerField()
    tili = models.CharField(max_length=30)
    country = models.CharField(max_length=40)
    code = models.IntegerField(unique=True)
    class Meta:
        db_table = 'serial'

class Series(models.Model):
    serial = models.ForeignKey(Serial, null=False, on_delete=models.CASCADE)
    seria = models.IntegerField()
    part = models.TextField()
    class Meta:
        db_table = 'series'

