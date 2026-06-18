import uuid
from django.utils import timezone
from django.core.validators import RegexValidator

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import PermissionsMixin,AbstractBaseUser,BaseUserManager,send_mail
from django.core.mail import send_mail
from pygments.lexers import web



class Category(models.Model):
    parent = models.ForeignKey('self',verbose_name=_('parent'),on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(_('Name'),max_length=100)
    description = models.TextField(_("description"),blank=True)
    avatar= models.ImageField(_('avatar'),blank=True,upload_to='categories')
    is_enable=models.BooleanField(_('is enable'),default=True)
    created_time=models.DateTimeField(_('created time'),auto_now_add=True)
    updated_time=models.DateTimeField(_('updated time'),auto_now=True)

    class Meta:
        db_table='categories'
        verbose_name=_('category')
        verbose_name_plural=_('categories')

    def __str__(self):
        return self.title



class Product(models.Model):
    title = models.CharField(_('Name'), max_length=100)
    description = models.TextField(_("description"),blank=True)
    avatar = models.ImageField(_('avatar'), upload_to='Products')
    is_enable=models.BooleanField(_('is enable'),default=True)
    categories= models.ManyToManyField('Category',verbose_name=_('category'),blank=True)
    created_time=models.DateTimeField(_('created time'),auto_now_add=True)
    updated_time=models.DateTimeField(_('updated time'),auto_now=True)
    def __str__(self):
        return self.title

class File(models.Model):
    # اضافه کردن تایپ
    FILE_AUDIO=1
    FILE_VIDEO=2
    FILE_PDF=3
    FILE_TYPES=(
    (FILE_AUDIO,_('audio file')),
    (FILE_VIDEO,_('video file')),
    (FILE_PDF,_('pdf file')),
    )



    product = models.ForeignKey(Product,verbose_name=_('product'),on_delete=models.CASCADE,related_name='files')
    title = models.CharField(_('title'),max_length=100)

    file_type= models.IntegerField(_('file type'),choices=FILE_TYPES,default=FILE_AUDIO)
    file=models.FileField(_('file'),upload_to='files/%Y/%m/%d/')
    is_enable=models.BooleanField(_('is enable'),default=True)
    created_time=models.DateTimeField(_('created time'),auto_now_add=True)
    updated_time=models.DateTimeField(_('updated time'),auto_now=True)


    class Meta:
        db_table='files'
        verbose_name=_('file')
        verbose_name_plural=_('files')

    def __str__(self):
        return self.title




























