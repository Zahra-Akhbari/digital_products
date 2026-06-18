import random
from uuid import UUID

from django.utils import timezone

from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import PermissionsMixin,AbstractBaseUser,BaseUserManager,send_mail
from django.core.mail import send_mail




class UserManager(BaseUserManager):
    use_in_migrations=True

    def create_user(self,username=None,email=None,phone_number=None,password=None,**extra_fields):
        if username is None:
            if email:
                username=email.split('@',1)[0]
            if phone_number:
                username=random.choice('abcdefghijklmnopqrstuvwxyz'+str(phone_number)[-7:])
                while User.objects.filter(username=username).exists():
                    username+=str(random.randint(10,99))
        return self.create_user(username,phone_number,email,password,False,False,**extra_fields)

    def create_superuser(self,username,email,phone_number,password,**extra_fields):
        return self.create_user(username,phone_number,email,password,True,True,**extra_fields)

    def get_by_phone_number(self,phone_number):
        return self.get(**{"phone_number":phone_number})




 # وقتی میخوایم یوزر درست کنیم که ویژگی های اضافه تر باشه
class User(AbstractBaseUser,PermissionsMixin):
    user_name=models.CharField(_('username'),max_length=100,unique=True,
                              help_text=_('Required. 100 characters or fewer. Letters, digits and '),
                              validators=[
                                        RegexValidator(regex=r'^[a-zA-Z][a-zA-Z0-9_\.]+$',
                                                        message= _('Enter a valid username.'))
                                ]
                               )

    first_name=models.CharField(_('first name'),max_length=100,blank=True,null=True)
    last_name=models.CharField(_('last name'),max_length=100,blank=True,null=True)
    email=models.EmailField(_('email'),max_length=100,blank=True,null=True,unique=True)
    phone_number=models.BigIntegerField(_('phone number'),blank=True,null=True,unique=True)
    is_staff=models.BooleanField(_('is staff user'),default=False,
                                 help_text=_('Designates whether the user can log into this admin site.')
                                 )
    is_active=models.BooleanField(_('is active user'),default=True,
                                  help_text=_('Designates whether this user should be treated as active. Unselected ')
                                  )
    date_joined=models.DateTimeField(_('date joined'),default=timezone.now)
    last_seen=models.DateTimeField(_('last seen date'),null=True,blank=True)

    objects=UserManager()

    USERNAME_FIELD='user_name'
    REQUIRED_FIELDS=['email','phone_number']

    class Meta:
        db_table='user'
        verbose_name=_('user')
        verbose_name_plural=_('users')







class UserProfile(models.Model):
    user = models.OneToOneField(User,verbose_name=_('user'),on_delete=models.CASCADE)
    nick_name=models.CharField(_('nick_name'),max_length=100,blank=True,null=True)
    avatar=models.ImageField(_('avatar'),upload_to='users/%Y/%m/%d/')
    birthday=models.DateField(_('birthday'),null=True,blank=True)
    gender=models.BooleanField(_('gender'),blank=True,null=True,
                                   help_text=_('Designates whether this user has a gender'),default=None)
    province=models.ForeignKey('province',on_delete=models.SET_NULL,null=True,blank=True)




class Device(models.Model):
    Web=1
    IOS=2
    Android=3
    DEVICE_TYPE_CHOICES=(
        (Web,_('web')),
        (IOS,_('ios')),
        (Android,_('android')),
    )

    user = models.ForeignKey(User,related_name='device',on_delete=models.CASCADE)
    device_uuid=models.UUIDField(_('device UUID'),default=UUID,editable=False)

    last_login=models.DateTimeField(_('last login'),null=True,blank=True)
    device_type=models.PositiveSmallIntegerField(choices=DEVICE_TYPE_CHOICES,default=Web)
    device_os=models.CharField(_('device OS'),max_length=100,blank=True,null=True)
    device_model=models.CharField(_('device model'),max_length=100,blank=True,null=True)
    app_version=models.CharField(_('app version'),max_length=100,blank=True,null=True)
    create_time=models.CharField(_('create time'),max_length=100,blank=True,null=True)

    class Meta:
        db_table='user_device'
        verbose_name=_('device')
        verbose_name_plural=_('devices')
        unique_together=('user','device_uuid')

class Province(models.Model):
        name=models.CharField(_('province'),max_length=100,blank=True,null=True)
        is_valid=models.BooleanField(_('is valid province'),default=True)
        modified_at=models.DateTimeField(_('modified time'),auto_now=True)
        created_at=models.DateTimeField(_('created time'),auto_now_add=True)

        def __str__(self):
            return self.name
