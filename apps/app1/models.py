from django.db import models
from datetime import date, datetime, timedelta
import re

# Create your models here.


class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}

        if len(postData['firstnameHTML'])<2:
            errors['firstnameHTML'] = "El nombre debe tener al menos de 2 caracteres"

        if len(postData['lastnameHTML'])<2:
            errors['lastnameHTML'] = "El apellido debe tener al menos de 2 caracteres"

        # valida el password
        if len(postData['passwordHTML'])<8:
            errors['passwordHTML'] = "la contraseña debe contener al menos 8 caracteres"

        if postData['passwordHTML'] != postData['password_confirmHTML']:
            errors['passwordHTML'] = "la contraseña no coincide con la de confirmación"

        if  postData['birth_dateHTML'] > str(date.today()):
            errors['birth_dateHTML'] = "La fecha no puede estar en el futuro"

        # valida el email
        EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
        if not EMAIL_REGEX.match(postData['emailHTML']):          
            errors['emailHTML'] = "Correo Invalido"
      
        
        for s in User.objects.all():
            # se usa .lower() para ovbiar las mayúsculas en la comparación de palabras
            if postData['emailHTML'].lower() == s.email.lower(): 
                errors['emailHTML'] = "Este email ya existe"
        return errors



class User(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    birth_date = models.DateField()
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=225)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()