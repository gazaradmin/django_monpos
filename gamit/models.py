from django.db import models
from django.contrib.gis.db import models
from django.urls import reverse
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User
from django_resized import ResizedImageField
from django.db.models.signals import post_save
from django.dispatch import receiver

monument_material = (('Concrete', 'Бетон/арматур'),('Polar/mast', 'Төмөр/Ган'),('Etc','Бусад'),)
monument_found=(('Steel rods','Ган тулгуур'),('Concrete block','Бетон хавтан'),('Roof','Барилгын дээвэр'),('Etc','Бусад'),)
mark_desc=(('CHISELLED CROSS','Хэрээс'),('BRASS NAIL','Товгор'),('DIVOT','Цэг'),('Etc','Бусад'),)
Geologic_Characteristic=(('BEDROCK','Ул чулуу'),('CLAY','Шаварлаг'),('CONGLOMERATE','Конгломерат'),('GRAVEL','Хайрга'),('SAND','Элсэрхэг'),('Etc','Бусад'),)
Bedrock_Type=(('IGNEOUS','Галт уулын чулуулаг (IGNEOUS)'),('METAMORPHIC','Хувирсан чулуулаг (METAMORPHIC)'),('SEDIMENTARY','Тунамал чулуулаг'),)
Bedrock_Condition=(('FRESH','Шинэ/залуу'),('JOINTED','Үет'),('WEATHERED','Өгөршсөн'),)
Fracture_Spacing =(('1-10 cm','1-10 cm'),('11-50 cm','11-50 cm'),('51-200 cm','51-200 cm'),('over 200 cm','200 cm дээш'),)
Fault_zones_nearby=(('Bulnai','Булнай'),('Hangain_nuruu','Хангайн нуруу'),)

class model_system(models.Model):
	title = models.CharField(max_length=100)
	desc= models.CharField(max_length=100)
	icon= models.ImageField(upload_to='static/images', blank=True)
	def __str__(self):
		return self.title

class model_lfile(models.Model):
    id = models.AutoField(primary_key=True)
    vx = models.CharField(max_length=100, blank=True, null=True)
    vy = models.CharField(max_length=100, blank=True, null=True)
    vz = models.CharField(max_length=100, blank=True, null=True)
    epoch = models.CharField(max_length=100, blank=True, null=True)
    sigx = models.CharField(max_length=100, blank=True, null=True)
    sigy = models.CharField(max_length=100, blank=True, null=True)
    sigz = models.CharField(max_length=100, blank=True, null=True)
    sigvx = models.CharField(max_length=100, blank=True, null=True)
    sigvy = models.CharField(max_length=100, blank=True, null=True)
    sigvz = models.CharField(max_length=100, blank=True, null=True)
    note = models.CharField(max_length=100, blank=True, null=True)
    x = models.CharField(max_length=100, blank=True, null=True)
    y = models.CharField(max_length=100, blank=True, null=True)
    z = models.CharField(max_length=100, blank=True, null=True)
    site = models.CharField(max_length=4, blank=True, null=True)
    status = models.CharField(max_length=3, blank=True, null=True)
    def __str__(self):
        return '%s' % self.site

class site_identify(models.Model):
    fid = models.ForeignKey(model_lfile, on_delete=models.CASCADE)
    monument_ins=models.CharField(max_length=100, blank=True, null=True)
    iers_number=models.CharField(max_length=9, blank=True, null=True)
    cdp_number=models.CharField(max_length=4, blank=True, null=True)
    monument_desc=models.CharField(max_length=100,choices=monument_material,default='Бетон/арматур',)
    H_monumet=models.DecimalField(max_digits=5, decimal_places=5)
    monument_foundation=models.CharField(max_length=100,choices=monument_found,default='Ул чулуу',)
    H_depth=models.DecimalField(max_digits=5, decimal_places=5)
    Marker_Description=models.CharField(max_length=50,choices=mark_desc,default='Хэрээс',)
    Date_Installed=models.DateField(auto_now=False)
    Geologic_Characteristic=models.CharField(max_length=50,choices=Geologic_Characteristic,default='Ул чулуу',)
    Bedrock_Type=models.CharField(max_length=50,choices=Bedrock_Type,default='Тунамал чулуулаг')
    Bedrock_Condition=models.CharField(max_length=50,choices=Bedrock_Condition,default='Шинэ/залуу')
    Fracture_Spacing=models.CharField(max_length=50,choices=Fracture_Spacing,default='1-10 cm')
    Fault_zones_nearby=models.CharField(max_length=50,choices=Fault_zones_nearby,default='Булнай')
    def __unicode__(self):
        return self.site

Constellation_list = (('G', 'G'),('GR', 'G/R'),('GRE','G/R/E'),('GREC','G/R/E/C'),('GREZ','G/R/E/Z'),('GRC','G/R/C'))
class site_hardware(models.Model):
	fid = models.ForeignKey(model_lfile, on_delete=models.CASCADE)
	Receiver=models.CharField(max_length=100, blank=False, null=True)
	Receiver_SN=models.CharField(max_length=100, blank=False, null=True)
	Antenna=models.CharField(max_length=100, blank=False, null=True)
	Antenna_Radome=models.CharField(max_length=100, blank=False, null=True)
	Last_Data_Available=models.CharField(max_length=100, blank=True, null=True)
	Constellation=models.CharField(max_length=50,choices=Constellation_list,default='G/R')
	Data_Center=models.CharField(max_length=100, blank=True, null=True, default='Monpos')
	Station_Log=models.FileField(upload_to='static/site_log', blank=True,validators=[FileExtensionValidator(allowed_extensions=['log'])])
	left=ResizedImageField(size=[180,200],quality=100, upload_to='static/site_log', blank=True)
	right=ResizedImageField(size=[180,200],quality=100, upload_to='static/site_log', blank=True)
	north=ResizedImageField(size=[180,200],quality=100, upload_to='static/site_log', blank=True)
	south=ResizedImageField(size=[180,200],quality=100, upload_to='static/site_log', blank=True)
	def __str__(self):
		return '%s' % self.fid
def defaultsystem():
    return 4326

class Convert(models.Model):
    sys = (
    ('4326', 'WGS84'),
    ('4978', 'Cartesian'),    
    ('32645', 'UTM/45'),
    ('32646', 'UTM/46'),
    ('32647', 'UTM/47'),
    ('32648', 'UTM/48'),
    ('32649', 'UTM/49'),
    ('32650', 'UTM/50'),
    ('115', 'TM/45'),
    ('116', 'TM/46'),
    ('117', 'TM/47'),
    ('118', 'TM/48'),
    ('119', 'TM/49'),
    ('120', 'TM/50'),)
    dec=(
        ('0','0'),
        ('1','1'),
        ('2','2'),
        ('3','3')
    )
    dms=(
        ('0','dms'),
        ('1','ddd'),
    )
    x_in = models.CharField(max_length=50, null=True)
    y_in = models.CharField(max_length=50, null=True)
    z_in = models.CharField(max_length=50, null=True)
    sys_in = models.CharField(max_length=50,choices=sys,default='WGS84')
    wgs_in =models.CharField(max_length=50,choices=dms,default='dms')
    x_out = models.CharField(max_length=50, blank=True, null=True)
    y_out = models.CharField(max_length=50, blank=True,null=True)
    z_out = models.CharField(max_length=50, blank=True,null=True)
    sys_out = models.CharField(max_length=50,choices=sys,default='WGS84')
    out_dec = models.CharField(max_length=5, blank=True,null=True)
    wgs_out=models.CharField(max_length=50,choices=dms,default='dms')
    dec_out=models.CharField(max_length=50,choices=dec,default='3')
    conv_date = models.DateTimeField('date published',blank=True, null=True)
    ip = models.CharField(max_length=50, blank=True,null=True)

class Question(models.Model):
	system = models.ForeignKey(model_system, on_delete=models.CASCADE)
	name = models.CharField(max_length=100, blank=False,default="Зочин")
	email= models.EmailField(max_length=100, blank=False)
	phone= models.CharField(max_length=100,blank=True) 
	asuult= models.TextField(max_length=1000)
	answered = models.BooleanField(default=False)
	created=models.DateTimeField(auto_now_add=True)
	userip=models.GenericIPAddressField(null=True) 
	def __str__(self):
		return self.asuult

class Answer(models.Model):
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE, blank=False, null=True)
    answer = models.TextField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    userip=models.GenericIPAddressField(null=True) 
    class Meta:
        ordering = ['created']
    def __str__(self):
        return self.answer

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    org = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=150)
    signup_confirmation = models.BooleanField(default=False)
    def __str__(self):
        return self.user.username
class Statistic(models.Model):
    user = models.CharField(max_length=100, blank=True)
    file = models.CharField(max_length=100, blank=True)
    created=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user
@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()