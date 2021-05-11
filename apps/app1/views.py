from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
import bcrypt
# from django.http import JsonResponse

# Create your views here.
def login_register(request):
    return  render(request,'login_register.html')




def register(request):
    # si no existe la sesion, primera vez ingresando
    if 'firstname' not in request.session:
        request.session['firstname'] = {}
    
    # obtiene datos del formulario
    firstname = request.POST["firstnameHTML"]
    lastname = request.POST["lastnameHTML"]
    birth_date = request.POST["birth_dateHTML"]
    email = request.POST["emailHTML"]
    password = request.POST["passwordHTML"]
    password_confirm = request.POST["password_confirmHTML"]

    errors = User.objects.validator(request.POST)
    print(errors)

    # verifica si hay errores en el ingreso del formulario
    if len(errors) >0:
        for key, value in errors.items():
             messages.error(request, value)
        return redirect('/')
    else: 
        # encripta el pass
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(firstname=firstname, lastname=lastname, birth_date=birth_date , email=email, password=pw_hash )
        
        request.session['firstname'] = firstname
        request.session['lastname'] = lastname
        request.session['email'] = email
        request.session['birth_dateHTML'] = birth_date
        return redirect('/success')
     

def login(request):
    # si se ingresaron ambos datos(email y pass) en el form
    if request.POST['emailHTML'] and request.POST['passwordHTML']:
        # busca un objeto en la base de datos que tenga el email ingresado en el form
        user = User.objects.filter(email = request.POST['emailHTML'])
        # si encuentra un usuario
        if user:
            # guarda el objeto user encontrado segun su email
            logged_user = user[0] # user[0] es el primer objeto encontrado (deberia ser el unico!)#
            # obtiene el password del usuario encriptado desde la base de datos
            pwd_on_bd = logged_user.password
            # compara si el pass ingresado en el form(encriptado) coincide con el pass de la BD(tambien encriptado)
            if bcrypt.checkpw(request.POST['passwordHTML'].encode(), pwd_on_bd.encode()):
                request.session['firstname'] = logged_user.firstname
                request.session['lastname'] = logged_user.lastname
                request.session['email'] = logged_user.email
                request.session['birth_date'] = str(logged_user.birth_date)
                return redirect('/success')
            
        # si NO encuentra un usuario
        print('pass incorrecto')
    return redirect('/')

def success(request):
    return render(request,'success.html')

def logout(request):
    request.session.delete()
    return redirect('/')