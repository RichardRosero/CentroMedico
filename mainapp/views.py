from pyexpat.errors import messages
from django.shortcuts import render, redirect
#from pandas import isnull
from mainapp.forms import RegisterForm, UserChangeForm,PacienteForm, CitaForm, SignoVitalForm, ConsultaForm, LaboratorioForm, RecetaForm, FichaForm,ConsultaGeneForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from mainapp.models import Usuario,Opciones,Paciente, CatalogoDetalle, Agendar_cita, Signos_vitales, Consulta, Laboratorio,Receta, Ficha
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.core import serializers
#from pyquery import PyQuery as pq
from PIL import Image
import cv2
import base64
from matplotlib import pyplot as plt
from mtcnn.mtcnn import MTCNN #deteccion de rostro
import tensorflow as tf
from numpy import asarray
import json 
 
import datetime
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.views import View
from django.conf import settings

# Create your views here.

@login_required(login_url='login')
def index(request):

    opciones_perfil = Opciones.objects.raw("SELECT  mainapp_opciones.id_opciones, mainapp_opciones.descripcion,mainapp_opciones.url  FROM mainapp_opciones_perfil inner join mainapp_opciones  on mainapp_opciones.id_opciones=mainapp_opciones_perfil.id_opcion where mainapp_opciones_perfil.id_perfil = "+ str(request.user.id_perfil))
    
    print(opciones_perfil)
    print(request.user.id_perfil)
    return render(request,'mainapp/index.html',{
        'title':'Inicio',
        'opciones_perfil':opciones_perfil
    })

@login_required(login_url='login')
def registro_usuario(request):
    register_form= RegisterForm
    opciones_perfil = Opciones.objects.raw("SELECT  mainapp_opciones.id_opciones, mainapp_opciones.descripcion,mainapp_opciones.url  FROM mainapp_opciones_perfil inner join mainapp_opciones  on mainapp_opciones.id_opciones=mainapp_opciones_perfil.id_opcion where mainapp_opciones_perfil.id_perfil = "+ str(request.user.id_perfil))
    print('metodo')
    if request.method=='POST':
        print('formulario POST')
        print(request.POST)
        
        register_form=RegisterForm(request.POST)
        #data_form=register_form.cleaned_data
        
        print (register_form)
        if register_form.is_valid():
            print('formulario valido')
            
            register_form.save()
            return redirect('consultar_usuarios')


    return render (request, 'users/register.html',{
        'register_form':register_form,
        'accion':'CRE',
        'opciones_perfil':opciones_perfil

    })


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username,password=password)
        print(user)
        if user is not None:
            print ('usuario es no none')
            login(request,user)
            return redirect('inicio')
        else:
            messages.warning(request, 'No te has identificado correctamente')
    return render(request,"users/login.html")

def logout_user(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def consultar_usuarios(request):
    #Personas = persona.objects.all()
    opciones_perfil = Opciones.objects.raw("SELECT  mainapp_opciones.id_opciones, mainapp_opciones.descripcion,mainapp_opciones.url  FROM mainapp_opciones_perfil inner join mainapp_opciones  on mainapp_opciones.id_opciones=mainapp_opciones_perfil.id_opcion where mainapp_opciones_perfil.id_perfil = "+ str(request.user.id_perfil))
    usuario = Usuario.objects.raw("SELECT * FROM mainapp_usuario  where mainapp_usuario.is_active =1 ")
    return render(request,"users/consulta_usuarios.html",{'listUsuarios':usuario,
        'opciones_perfil':opciones_perfil})

@login_required(login_url='login')
def consulta_usuario_id(request,id):
    opciones_perfil = Opciones.objects.raw("SELECT  mainapp_opciones.id_opciones, mainapp_opciones.descripcion,mainapp_opciones.url  FROM mainapp_opciones_perfil inner join mainapp_opciones  on mainapp_opciones.id_opciones=mainapp_opciones_perfil.id_opcion where mainapp_opciones_perfil.id_perfil = "+ str(request.user.id_perfil))
    
    usuario=Usuario.objects.get(pk=id)
    print(usuario)
    form = UserChangeForm(instance=usuario)
    print(form)
    if request.method=='POST':
        print('formulario POST')
        print(request.POST)
        
        form=UserChangeForm(request.POST)
                
        if form.is_valid(): 
            print('formulario valido')     
            v_numero_identificacion=form.cleaned_data.get("numero_identificacion")
            v_nombres= form.cleaned_data.get('nombres')            
            v_apellidos= form.cleaned_data.get('apellidos')            
            v_domicilio= form.cleaned_data.get('domicilio')
            v_correo_contacto= form.cleaned_data.get('correo_contacto')
            v_id_perfil= form.cleaned_data.get('id_perfil')
            #v_username= form.cleaned_data.get('username')
            
            usuario.numero_identificacion=v_numero_identificacion
            usuario.nombres= v_nombres            
            usuario.apellidos= v_apellidos           
            usuario.domicilio= v_domicilio
            usuario.correo_contacto= v_correo_contacto
            usuario.id_perfil= v_id_perfil
            #usuario.username= v_username

            usuario.save()
            return redirect('consultar_usuarios')
    
    return render(request,"users/register.html",{'register_form':form,'id':id,'accion':'UDP','opciones_perfil':opciones_perfil}) 

@login_required(login_url='login')
def eliminar_usuario(request, id):
    usuario = Usuario.objects.get(pk=id)
    usuario.delete()
    return redirect('consultar_usuarios')

def biometria(request,id):
    paciente=Paciente.objects.get(pk=id) 
    nombre=paciente.nombre1 +''+paciente.apellido_paterno
    return render(request,"paciente/biometria.html",{
        'id':id,'nombre':nombre})

def subir_foto(request):   
        
    imgbase64 = request.POST.get("image","")
    id = request.POST.get("idPaciente","")
    paciente=Paciente.objects.get(pk=id)
    print(id)
    paciente.imagen=bytes(imgbase64,'utf-8')               
    
    instance = paciente.save()
    print(instance)
            # serialize in new friend object in json        
            # send to client side."""
    return JsonResponse({"instance": instance}, status=200)

def consultar_imagen(request, id,idcita):
    print(idcita)
    opciones_perfil = Opciones.objects.raw("SELECT  mainapp_opciones.id_opciones, mainapp_opciones.descripcion,mainapp_opciones.url  FROM mainapp_opciones_perfil inner join mainapp_opciones  on mainapp_opciones.id_opciones=mainapp_opciones_perfil.id_opcion where mainapp_opciones_perfil.id_perfil = "+ str(request.user.id_perfil))
   
    paciente_foto = Paciente.objects.raw("SELECT id_paciente, imagen, nombre1, apellido_paterno FROM mainapp_paciente where id_paciente = "+ str(id)) 
   
    for p in paciente_foto:
        imagen=bytes.decode(p.imagen)
        nombre=p.nombre1+ p.apellido_paterno
       
        
    return render(request,"paciente/consultar_imagen.html",{
    'imagen':imagen,
    'id_paciente':id,
    'opciones_perfil':opciones_perfil,
    'nombre': nombre,
    'idcita':idcita
    })
        
def verificar_imagen(request):
    print("imgresa ")
    id = request.POST.get("idPaciente","") 
    idcita = request.POST.get("idCita","") 
    print(idcita) 
    paciente_foto = Paciente.objects.raw("SELECT id_paciente, numero_identificacion, imagen FROM mainapp_paciente where id_paciente = "+ str(id)) 
    print (paciente_foto)
    for p in paciente_foto:
        imagenByte =bytes.decode(p.imagen,'UTF-8')        
        imagenByte = imagenByte.split(',')[1];             
        imagen64= base64.b64decode(imagenByte)        
        numero_identificacion= p.numero_identificacion                        
        filename = numero_identificacion+'.jpg'  # I assume you have a way of picking unique filenames
    with open(filename, "wb") as fh:
        fh.write(imagen64)
        
    filename_bio = numero_identificacion+'_login.jpg'
    strImage = request.POST.get("image","")    
    strImage = strImage.split(',')[1];  
    imagen64= base64.b64decode(strImage)  
    with open(filename_bio, "wb") as fh:
        fh.write(imagen64)
    comp= recorte_imagen(filename,filename_bio)
    
    
    print(comp)
    if comp >= 0.90:
        cita=Agendar_cita.objects.get(pk=idcita)
        cita.admitido= 1
        cita.save()
        
    mensaje="Compatibilidad del {:.1%}".format(float(comp))
    return JsonResponse({"mensaje": mensaje,'comp':comp}, status=200)

def compatibility(img1, img2):
    orb = cv2.ORB_create()

    kpa, dac1 = orb.detectAndCompute(img1, None)
    kpa, dac2 = orb.detectAndCompute(img2, None)

    comp = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    matches = comp.match(dac1, dac2)

    similar = [x for x in matches if x.distance < 70]
    if len(matches) == 0:
        return 0
    return len(similar)/len(matches)

def face(img, faces):
    data = plt.imread(img)
    print("antes for faces")
    for i in range(len(faces)):
        x1, y1, ancho, alto = faces[i]["box"]
        x2, y2 = x1 + ancho, y1 + alto
        plt.subplot(1,len(faces), i + 1)
        plt.axis("off")
        face = cv2.resize(data[y1:y2, x1:x2],(150,200), interpolation=cv2.INTER_CUBIC)
        cv2.imwrite(img, 255*face)
        plt.imshow(data[y1:y2, x1:x2])

def recorte_imagen(user, user_login ):
    img = user_login
    img_user = user    
    image2 = Image.open(img)
    image2 = image2.convert('RGB') # revisar quita colores
    pixels = asarray(image2)
    detector = MTCNN()
    faces = detector.detect_faces(pixels)    
    face(img, faces)
    
    ###
    image2 = Image.open(img_user)
    image2 = image2.convert('RGB') # revisar quita colores
    pixels = asarray(image2)
    
    faces = MTCNN().detect_faces(pixels)

    face(img_user, faces)
    
    ###
    
    face_reg = cv2.imread(img_user, 0)
    face_log = cv2.imread(img, 0)

    comp = compatibility(face_reg, face_log)
            
    if comp >= 0.90:
        print("Compatibilidad del {:.1%}".format(float(comp)))
        
    else:
        print("Compatibilidad del {:.1%}".format(float(comp)))
        
        #os.remove(img_user)
        
    return comp

@login_required(login_url='login')
def consultar_pacientes(request):
    opciones_perfil = Opciones.objects.raw("SELECT  mainapp_opciones.id_opciones, mainapp_opciones.descripcion,mainapp_opciones.url  FROM mainapp_opciones_perfil inner join mainapp_opciones  on mainapp_opciones.id_opciones=mainapp_opciones_perfil.id_opcion where mainapp_opciones_perfil.id_perfil = "+ str(request.user.id_perfil))
    pacientes = Paciente.objects.raw("SELECT * FROM mainapp_paciente where mainapp_paciente.estado =1 ")
    
    return render(request,"paciente/consultar_paciente.html",{'listPacientes':pacientes,
        'opciones_perfil':opciones_perfil})


def consultar_signos_vitales(request):
    return HttpResponse('consultar_signos_vitales')

@login_required(login_url='login')
def registro_paciente(request):
    pacienteForm= PacienteForm
    opciones_perfil = Opciones.objects.raw("SELECT  mainapp_opciones.id_opciones, mainapp_opciones.descripcion,mainapp_opciones.url  FROM mainapp_opciones_perfil inner join mainapp_opciones  on mainapp_opciones.id_opciones=mainapp_opciones_perfil.id_opcion where mainapp_opciones_perfil.id_perfil = "+ str(request.user.id_perfil))
    print('metodo')
    if request.method=='POST':
        print('formulario POST')
        print(request.POST)
        
        pacienteForm=pacienteForm(request.POST)
        #data_form=register_form.cleaned_data
        
        print (pacienteForm)
        if pacienteForm.is_valid():
            print('formulario valido')
            
            pacienteForm.save()
            return redirect('/consultar_pacientes/')


    return render (request, 'paciente/registro_paciente.html',{
        'pacienteForm':pacienteForm,
        'accion':'CRE',
        'opciones_perfil':opciones_perfil

    })
    
def eliminar_paciente(request, id):
    paciente = Paciente.objects.get(pk=id)
    paciente.delete()
    return redirect('consultar_pacientes')

@login_required(login_url='login')
def consulta_paciente_id(request,id):
    opciones_perfil = Opciones.objects.raw("SELECT  mainapp_opciones.id_opciones, mainapp_opciones.descripcion,mainapp_opciones.url  FROM mainapp_opciones_perfil inner join mainapp_opciones  on mainapp_opciones.id_opciones=mainapp_opciones_perfil.id_opcion where mainapp_opciones_perfil.id_perfil = "+ str(request.user.id_perfil))
    
    paciente=Paciente.objects.get(pk=id)
    
    form = PacienteForm(instance=paciente)
    paciente_foto = Paciente.objects.raw("SELECT id_paciente, imagen FROM mainapp_paciente where id_paciente = "+ str(id))
     
    imagen=''
    for p in paciente_foto:
        imagen=p.imagen
        
        if imagen != None:
            imagen=bytes.decode(p.imagen)
    
    if request.method=='POST':
        print('formulario POST')       
        
        form=PacienteForm(request.POST)
                
        if form.is_valid(): 
            print('formulario valido')     
            v_numero_identificacion=form.cleaned_data.get("numero_identificacion")
            v_nombre1= form.cleaned_data.get('nombre1')  
            v_nombre2= form.cleaned_data.get('nombre2')           
            v_apellido_paterno= form.cleaned_data.get('apellido_paterno')            
            v_apellido_materno= form.cleaned_data.get('apellido_materno')            
            v_domicilio= form.cleaned_data.get('domicilio')
            v_correo_contacto= form.cleaned_data.get('correo_contacto')           
            v_id_provincia= form.cleaned_data.get('id_provincia')
            v_id_ciudad = form.cleaned_data.get('id_ciudad')
            v_id_tipo_sangre = form.cleaned_data.get('id_tipo_sangre')
            v_id_estado_civil = form.cleaned_data.get('id_estado_civil')
            v_id_sexo = form.cleaned_data.get('id_sexo')
            v_telefono_contacto = form.cleaned_data.get('telefono_contacto')
            v_fecha_nacimiento = form.cleaned_data.get('fecha_nacimiento')
            v_edad = form.cleaned_data.get('edad')
            v_observaciones = form.cleaned_data.get('observaciones')
            v_id_ciudad_nacimiento = form.cleaned_data.get('id_ciudad_nacimiento')
            
            paciente.numero_identificacion=v_numero_identificacion
            paciente.nombre1= v_nombre1 
            paciente.nombre2= v_nombre2           
            paciente.apellido_paterno= v_apellido_paterno  
            paciente.apellido_materno= v_apellido_materno           
            paciente.domicilio= v_domicilio
            paciente.correo_contacto= v_correo_contacto
            paciente.id_provincia= v_id_provincia
            paciente.id_ciudad= v_id_ciudad
            paciente.id_tipo_sangre= v_id_tipo_sangre
            paciente.id_estado_civil= v_id_estado_civil
            paciente.id_sexo= v_id_sexo
            paciente.telefono_contacto= v_telefono_contacto
            paciente.fecha_nacimiento= v_fecha_nacimiento
            paciente.edad= v_edad
            paciente.observaciones= v_observaciones
            paciente.id_ciudad_nacimiento= v_id_ciudad_nacimiento
            
            
            
            paciente.save()
            return redirect('consultar_pacientes')
    
    return render(request,"paciente/registro_paciente.html",{'pacienteForm':form,'id':id,'accion':'UDP','opciones_perfil':opciones_perfil,'imagen':imagen}) 

def carga_Provincia(request):
    id=int(request.POST.get("idPaciente",""))
    
    idProvincia=0
    if id!=0:        
        paciente=Paciente.objects.get(pk=id)      
        idProvincia=paciente.id_provincia
            
    catalogoDetalle = CatalogoDetalle.objects.raw("SELECT Provincia.id_catalogo_detalle,Provincia.descripcion FROM mainapp_catalogodetalle Provincia where Provincia.estado=1 and Provincia.id_catalogo=1")  
    list_CatalogoDictionary=[]
    for c in catalogoDetalle:       
        list_CatalogoDictionary.append(catalogoDetalleToDictionary(c))        
 
    return JsonResponse(data={'listProvincia':list(list_CatalogoDictionary),'id_provincia':idProvincia},safe=False, status=200)

def catalogoDetalleToDictionary(catalogoDetalle):
    if catalogoDetalle == None:
        return None
    
    dictionary = {}
    dictionary["id_catalogo"] = catalogoDetalle.id_catalogo_detalle
    dictionary["descripcion"] = catalogoDetalle.descripcion
   
    return dictionary

def carga_Ciudad(request):
    id_provincia=request.POST.get("id_provincia","")   
    id=int(request.POST.get("idPaciente",""))    
    idCiudad=0
    
    if id!=0:        
        paciente=Paciente.objects.get(pk=id)      
        idCiudad=paciente.id_ciudad
        id_provincia=paciente.id_provincia
    
    catalogoDetalle = CatalogoDetalle.objects.raw("SELECT Ciudad.id_catalogo_detalle,Ciudad.descripcion FROM mainapp_catalogodetalle Provincia inner join mainapp_catalogodetalle Ciudad on  Ciudad.id_padre = Provincia.id_catalogo_detalle where Provincia.estado=1 and Ciudad.estado=1 and Ciudad.id_padre= "+ str(id_provincia))  
    print(catalogoDetalle)   
    list_CatalogoDictionary=[]
    for c in catalogoDetalle:       
        list_CatalogoDictionary.append(catalogoDetalleToDictionary(c))   
    
    return JsonResponse(data={'listCiudad':list(list_CatalogoDictionary),'id_ciudad':idCiudad},safe=False, status=200)

def carga_TipoSangre(request):
    id=int(request.POST.get("idPaciente",""))    
    idTipoSangre=0
    
    if id!=0:        
        paciente=Paciente.objects.get(pk=id)      
        idTipoSangre=paciente.id_tipo_sangre        
        
    catalogoDetalle = CatalogoDetalle.objects.raw("SELECT Provincia.id_catalogo_detalle,Provincia.descripcion FROM mainapp_catalogodetalle Provincia where Provincia.estado=1 and Provincia.id_catalogo=5")  
    
    list_CatalogoDictionary=[]
    for c in catalogoDetalle:       
        list_CatalogoDictionary.append(catalogoDetalleToDictionary(c))   
    
    #serialized_qs = serializers.serialize('json', catalogoDetalle.fields)
            # serialize in new friend object in json        
            # send to client side."""
    return JsonResponse(data={'listTipoSangre':list(list_CatalogoDictionary),'id_tipoSangre':idTipoSangre},safe=False, status=200)

def carga_EstadoCivil(request):
    
    catalogoDetalle = CatalogoDetalle.objects.raw("SELECT Provincia.id_catalogo_detalle,Provincia.descripcion FROM mainapp_catalogodetalle Provincia where Provincia.estado=1 and Provincia.id_catalogo=4")  
    
    id=int(request.POST.get("idPaciente",""))    
    idEstadoCivil=0
    
    if id!=0:        
        paciente=Paciente.objects.get(pk=id)      
        idEstadoCivil=paciente.id_estado_civil
    
    list_CatalogoDictionary=[]
    for c in catalogoDetalle:       
        list_CatalogoDictionary.append(catalogoDetalleToDictionary(c))   
          
    return JsonResponse(data={'listEstadoCivil':list(list_CatalogoDictionary),'id_estadoCivil':idEstadoCivil},safe=False, status=200)

def carga_Sexo(request):
    
    catalogoDetalle = CatalogoDetalle.objects.raw("SELECT Provincia.id_catalogo_detalle,Provincia.descripcion FROM mainapp_catalogodetalle Provincia where Provincia.estado=1 and Provincia.id_catalogo=3")  
        
    id=int(request.POST.get("idPaciente",""))    
    idSexo=0
    
    if id!=0:        
        paciente=Paciente.objects.get(pk=id)      
        idSexo=paciente.id_sexo
        
    list_CatalogoDictionary=[]
    for c in catalogoDetalle:       
        list_CatalogoDictionary.append(catalogoDetalleToDictionary(c))   
  
    return JsonResponse(data={'listSexo':list(list_CatalogoDictionary),'id_sexo':idSexo},safe=False, status=200)

def carga_CiudadNac(request):    
    id=int(request.POST.get("idPaciente",""))    
    idCiudadNac=0
    
    if id!=0:        
        paciente=Paciente.objects.get(pk=id)      
        idCiudadNac=paciente.id_ciudad_nacimiento
        
    catalogoDetalle = CatalogoDetalle.objects.raw("SELECT Ciudad.id_catalogo_detalle,Ciudad.descripcion FROM mainapp_catalogodetalle Provincia inner join mainapp_catalogodetalle Ciudad on Ciudad.id_padre = Provincia.id_catalogo_detalle where Provincia.estado=1 and Ciudad.estado=1;")
    
    list_CatalogoDictionary=[]
    for c in catalogoDetalle:       
        list_CatalogoDictionary.append(catalogoDetalleToDictionary(c))   
   
    return JsonResponse(data={'listCiudadNac':list(list_CatalogoDictionary),'id_ciudadNac':idCiudadNac},safe=False, status=200)

@login_required(login_url='login')
def consultar_pacientes_filtro(request):
    opciones_perfil = Opciones.objects.raw("SELECT  mainapp_opciones.id_opciones, mainapp_opciones.descripcion,mainapp_opciones.url  FROM mainapp_opciones_perfil inner join mainapp_opciones  on mainapp_opciones.id_opciones=mainapp_opciones_perfil.id_opcion where mainapp_opciones_perfil.id_perfil = "+ str(request.user.id_perfil))
    if request.method=='POST':
        print('formulario POST')
        print(request.POST)
        filtro = request.POST["txtBuscar"]
        print("SELECT `id_paciente`,`numero_identificacion`,`nombre1`,`nombre2`,`apellido_paterno`,`apellido_materno`,`domicilio`,`correo_contacto` FROM mainapp_paciente where mainapp_paciente.estado =1  and mainapp_paciente.numero_identificacion like '%"+(filtro)+"%'")
        pacientes = Paciente.objects.raw("SELECT `id_paciente`,`numero_identificacion`,`nombre1`,`nombre2`,`apellido_paterno`,`apellido_materno`,`domicilio`,`correo_contacto` FROM mainapp_paciente where mainapp_paciente.estado =1  and mainapp_paciente.numero_identificacion like '%"+str(filtro)+"%'",None)
        
        return render(request,"paciente/consultar_paciente_citaFiltro.html",{'listPacientes':pacientes,
        'opciones_perfil':opciones_perfil})
        
    pacientes = Paciente.objects.raw("SELECT `id_paciente`,`numero_identificacion`,`nombre1`,`nombre2`,`apellido_paterno`,`apellido_materno`,`domicilio`,`correo_contacto` FROM mainapp_paciente where mainapp_paciente.estado =1 ")
    
    return render(request,"paciente/consultar_paciente_citaFiltro.html",{'listPacientes':pacientes,
        'opciones_perfil':opciones_perfil})

@login_required(login_url='login')
def agendar_cita(request,id):
    
    paciente=Paciente.objects.get(pk=id)
    nombre=paciente.nombre1 +''+paciente.apellido_paterno
    agendar_citaForm=CitaForm
    print(agendar_citaForm)
    opciones_perfil = Opciones.objects.raw("SELECT  mainapp_opciones.id_opciones, mainapp_opciones.descripcion,mainapp_opciones.url  FROM mainapp_opciones_perfil inner join mainapp_opciones  on mainapp_opciones.id_opciones=mainapp_opciones_perfil.id_opcion where mainapp_opciones_perfil.id_perfil = "+ str(request.user.id_perfil))
    if request.method=='POST':
        print('formulario POST')
        print(request.POST)
        
        cita=Agendar_cita()
        form=CitaForm(request.POST)
                
        if form.is_valid(): 
            print('formulario valido')     
            v_observacion=form.cleaned_data.get("observacion")
            v_id_doctor= form.cleaned_data.get('id_doctor')            
            v_fecha_cita= form.cleaned_data.get('fecha_cita')            
            v_hora= form.cleaned_data.get('hora')
            
            cita.observacion=v_observacion
            cita.id_doctor= v_id_doctor            
            cita.fecha_cita= v_fecha_cita           
            cita.hora= v_hora
            cita.id_paciente= id
            
            cita.save()
            response=sendCita(id,v_fecha_cita)
            if(response=="ok"):
                return redirect('consultar_pacientes_filtro_a')
    
    return render (request, 'paciente/agendar_cita.html',{
        'agendar_cita':agendar_citaForm,        
        'opciones_perfil':opciones_perfil,
        'id_paciente':id,
        'nombre':nombre
    })
    
def carga_horas(request):    
    id=(request.POST.get("idPaciente",""))    
    fecha=request.POST.get("fecha","")    
    id_doctor=request.POST.get("id_doctor","")  
    
    if id_doctor == None:
        id_doctor=1
    
        
    catalogoDetalle = CatalogoDetalle.objects.raw("SELECT horas.id_catalogo_detalle,horas.descripcion FROM mainapp_catalogodetalle horas left join mainapp_agendar_cita cita on cita.fecha_cita=STR_TO_DATE ('"+fecha+"','%d/%m/%Y') and cita.hora= horas.id_catalogo_detalle  and cita.id_doctor="+id_doctor+"  where horas.estado=1 and horas.id_catalogo=8  and cita.id_cita is null",None)
    print(catalogoDetalle)
    list_CatalogoDictionary=[]
    for c in catalogoDetalle:       
        list_CatalogoDictionary.append(catalogoDetalleToDictionary(c))   
   
    return JsonResponse(data={'listHoras':list(list_CatalogoDictionary)},safe=False, status=200)

def carga_doctor(request):    
        
    #f id!=0:        
        #paciente=Paciente.objects.get(pk=id)      
        #idCiudadNac=paciente.id_ciudad_nacimiento
        
    doctores = Usuario.objects.raw("SELECT usu.id_persona, usu.nombres ,usu.apellidos, usu.username  FROM mainapp_usuario usu where usu.is_active=1 and id_perfil=1 ")
    
    list_CatalogoDictionary=[]
    for c in doctores:       
        list_CatalogoDictionary.append(doctoresToDictionary(c))   
   
    return JsonResponse(data={'listDoctor':list(list_CatalogoDictionary)},safe=False, status=200)


def doctoresToDictionary(catalogoDetalle):
    if catalogoDetalle == None:
        return None
    print(catalogoDetalle.id_persona)
    dictionary = {}
    dictionary["id_persona"] = catalogoDetalle.id_persona
    dictionary["nombres"]  = catalogoDetalle.nombres +' '+ catalogoDetalle.apellidos
   
    return dictionary


@login_required(login_url='login')
def consultar_pacientesCita_filtro(request):
    date_only = datetime.datetime.now().date()
    print(date_only)
    opciones_perfil = Opciones.objects.raw("SELECT  mainapp_opciones.id_opciones, mainapp_opciones.descripcion,mainapp_opciones.url  FROM mainapp_opciones_perfil inner join mainapp_opciones  on mainapp_opciones.id_opciones=mainapp_opciones_perfil.id_opcion where mainapp_opciones_perfil.id_perfil = "+ str(request.user.id_perfil))
    if request.method=='POST':
        print('formulario POST')
        print(request.POST)
        filtro = request.POST["txtBuscar"]
       
        pacientes = Paciente.objects.raw("SELECT  mainapp_agendar_cita.`id_paciente`, mainapp_paciente.`numero_identificacion`,`nombre1`,`nombre2`,`apellido_paterno`,`apellido_materno`,mainapp_agendar_cita.fecha_cita, mainapp_catalogodetalle.descripcion, mainapp_usuario.nombres  as nombreDoctor, mainapp_usuario.apellidos as apellidosDoctor FROM mainapp_paciente  inner join mainapp_agendar_cita on mainapp_agendar_cita.id_paciente = mainapp_paciente.id_paciente inner join mainapp_usuario on mainapp_agendar_cita.id_doctor = mainapp_usuario.id_persona inner join mainapp_catalogodetalle on mainapp_agendar_cita.hora = mainapp_catalogodetalle.id_catalogo_detalle left join mainapp_signos_vitales on mainapp_signos_vitales.id_paciente = mainapp_paciente.id_paciente and mainapp_agendar_cita.fecha_cita=mainapp_signos_vitales.fecha_cita where mainapp_paciente.estado =1  and mainapp_agendar_cita.admitido=1 and mainapp_paciente.numero_identificacion like '%"+str(filtro)+"%' and mainapp_agendar_cita.fecha_cita='"+str(date_only)+"' and mainapp_signos_vitales.id_paciente is  null ",None)
        
        return render(request,"paciente/consultar_paciente_citaFiltro.html",{'listPacientes':pacientes,
        'opciones_perfil':opciones_perfil})
        
    pacientes = Paciente.objects.raw("SELECT  mainapp_agendar_cita.`id_paciente`, mainapp_paciente.`numero_identificacion`,`nombre1`,`nombre2`,`apellido_paterno`,`apellido_materno`,mainapp_agendar_cita.fecha_cita, mainapp_catalogodetalle.descripcion, mainapp_usuario.nombres  as nombreDoctor, mainapp_usuario.apellidos as apellidosDoctor FROM mainapp_paciente  inner join mainapp_agendar_cita on mainapp_agendar_cita.id_paciente = mainapp_paciente.id_paciente inner join mainapp_usuario on mainapp_agendar_cita.id_doctor = mainapp_usuario.id_persona inner join mainapp_catalogodetalle on mainapp_agendar_cita.hora = mainapp_catalogodetalle.id_catalogo_detalle left join mainapp_signos_vitales on mainapp_signos_vitales.id_paciente = mainapp_paciente.id_paciente and mainapp_agendar_cita.fecha_cita=mainapp_signos_vitales.fecha_cita where mainapp_paciente.estado =1  and mainapp_agendar_cita.admitido=1 and mainapp_agendar_cita.fecha_cita='"+str(date_only)+"' and mainapp_signos_vitales.id_paciente is  null")
    
    return render(request,"paciente/consultar_paciente_citaFiltro.html",{'listPacientes':pacientes,
        'opciones_perfil':opciones_perfil,
        'fecha':date_only})
    
@login_required(login_url='login')
def signos_vitales(request,id):
    date_only = datetime.datetime.now().date()
    
    paciente=Paciente.objects.get(pk=id)
    nombre=paciente.nombre1 +''+paciente.apellido_paterno
    Signo_VitalForm=SignoVitalForm
    
    opciones_perfil = Opciones.objects.raw("SELECT  mainapp_opciones.id_opciones, mainapp_opciones.descripcion,mainapp_opciones.url  FROM mainapp_opciones_perfil inner join mainapp_opciones  on mainapp_opciones.id_opciones=mainapp_opciones_perfil.id_opcion where mainapp_opciones_perfil.id_perfil = "+ str(request.user.id_perfil))
    
    if request.method=='POST':
        print('formulario POST')
        print(request.POST)
        
        signo=Signos_vitales()               
        form=SignoVitalForm(request.POST)
        print(form)
        if form.is_valid(): 
            print('formulario valido')     
            v_fecha_cita= form.cleaned_data.get('fecha_cita')    
            v_peso=form.cleaned_data.get("peso")
            v_talla= form.cleaned_data.get('talla')                             
            v_imc= form.cleaned_data.get('imc')
            v_temperatura= form.cleaned_data.get('temperatura') 
            v_f_cardiaca= form.cleaned_data.get('f_cardiaca')                             
            v_f_respiratoria= form.cleaned_data.get('f_respiratoria')
            v_sistolica= form.cleaned_data.get('sistolica') 
            v_distolica= form.cleaned_data.get('distolica') 
            v_oximetria= form.cleaned_data.get('oximetria') 
            
            signo.fecha_cita= v_fecha_cita 
            signo.peso=v_peso
            signo.talla= v_talla   
            signo.imc=v_imc
            signo.temperatura= v_temperatura     
            signo.f_cardiaca=v_f_cardiaca
            signo.f_respiratoria= v_f_respiratoria     
            signo.sistolica=v_sistolica
            signo.distolica= v_distolica     
            signo.oximetria=v_oximetria                                        
            signo.id_paciente= id
            signo.fecha_cita= date_only
            
            signo.save()
            return redirect('consultar_paciente_citaFiltro')
    
    return render (request, 'paciente/signos_vitales.html',{
        'Signo_Vital':Signo_VitalForm,        
        'opciones_perfil':opciones_perfil,
        'id_paciente':id,
        'nombre':nombre
    })
    
    
@login_required(login_url='login')
def consultar_pacientesCita_Doc(request):
    date_only = datetime.datetime.now().date()
    print(date_only)
    opciones_perfil = Opciones.objects.raw("SELECT  mainapp_opciones.id_opciones, mainapp_opciones.descripcion,mainapp_opciones.url  FROM mainapp_opciones_perfil inner join mainapp_opciones  on mainapp_opciones.id_opciones=mainapp_opciones_perfil.id_opcion where mainapp_opciones_perfil.id_perfil = "+ str(request.user.id_perfil))
    if request.method=='POST':
        print('formulario POST')
        print(request.POST)
        filtro = request.POST["txtBuscar"]
       
        pacientes = Paciente.objects.raw("SELECT distinct isnull(mainapp_consulta.`idpaciente`) as ing_consulta, mainapp_consulta.id_consulta, isnull(mainapp_laboratorio.`idpaciente`) as laboratorio, isnull(mainapp_receta.`id_paciente`) as ing_receta, mainapp_agendar_cita.`id_paciente`, mainapp_paciente.`numero_identificacion`,`nombre1`,`nombre2`,`apellido_paterno`,`apellido_materno`,mainapp_agendar_cita.fecha_cita, "
                                         +"mainapp_catalogodetalle.descripcion, mainapp_usuario.nombres  as nombreDoctor, mainapp_usuario.apellidos as apellidosDoctor FROM mainapp_paciente  inner join mainapp_agendar_cita on mainapp_agendar_cita.id_paciente = mainapp_paciente.id_paciente "
                                         +"inner join mainapp_usuario on mainapp_agendar_cita.id_doctor = mainapp_usuario.id_persona inner join mainapp_catalogodetalle on mainapp_agendar_cita.hora = mainapp_catalogodetalle.id_catalogo_detalle inner join mainapp_signos_vitales on mainapp_signos_vitales.id_paciente = mainapp_paciente.id_paciente  "
                                         +"left join mainapp_consulta on mainapp_consulta.idpaciente = mainapp_paciente.id_paciente  left join mainapp_receta on mainapp_receta.id_paciente = mainapp_paciente.id_paciente and mainapp_consulta.iddoctor=mainapp_receta.id_doctor  where mainapp_paciente.estado =1  and mainapp_paciente.numero_identificacion like '%"+str(filtro)+"%' and mainapp_agendar_cita.fecha_cita='"+str(date_only)+"' and  CONVERT(mainapp_catalogodetalle.descripcion, TIME) <=DATE_FORMAT(DATE_ADD(STR_TO_DATE( CONVERT(now(), TIME), '%H%i:%s'),INTERVAL 2 HOUR), '%H:%i:%s') and   CONVERT(mainapp_catalogodetalle.descripcion, TIME) >=DATE_FORMAT(DATE_SUB(STR_TO_DATE( CONVERT(now(), TIME), '%H:%i:%s'),INTERVAL 2 HOUR), '%H:%i:%s') ",None)
        
        return render(request,"paciente/consultar_paciente_cita.html",{'listPacientes':pacientes,
        'opciones_perfil':opciones_perfil})
        
    pacientes = Paciente.objects.raw("SELECT distinct isnull(mainapp_consulta.`idpaciente`) as ing_consulta, mainapp_consulta.id_consulta, isnull(mainapp_laboratorio.`idpaciente`) as laboratorio , isnull(mainapp_receta.`id_paciente`) as ing_receta, mainapp_agendar_cita.`id_paciente`, mainapp_paciente.`numero_identificacion`,`nombre1`,`nombre2`,`apellido_paterno`,`apellido_materno`,mainapp_agendar_cita.fecha_cita, mainapp_catalogodetalle.descripcion,"
                                     +"mainapp_usuario.nombres  as nombreDoctor, mainapp_usuario.apellidos as apellidosDoctor FROM mainapp_paciente  inner join mainapp_agendar_cita on mainapp_agendar_cita.id_paciente = mainapp_paciente.id_paciente"
                                     +" inner join mainapp_usuario on mainapp_agendar_cita.id_doctor = mainapp_usuario.id_persona inner join mainapp_catalogodetalle on mainapp_agendar_cita.hora = mainapp_catalogodetalle.id_catalogo_detalle inner join mainapp_signos_vitales on mainapp_signos_vitales.id_paciente = mainapp_paciente.id_paciente"
                                     +" left join mainapp_consulta on mainapp_consulta.idpaciente = mainapp_paciente.id_paciente left join mainapp_laboratorio on mainapp_laboratorio.idpaciente = mainapp_paciente.id_paciente and mainapp_consulta.iddoctor=mainapp_laboratorio.iddoctor left join mainapp_receta on mainapp_receta.id_paciente = mainapp_paciente.id_paciente and mainapp_consulta.iddoctor=mainapp_receta.id_doctor   where mainapp_paciente.estado =1   and mainapp_agendar_cita.fecha_cita='"+str(date_only)+"' and  CONVERT(mainapp_catalogodetalle.descripcion, TIME) <=DATE_FORMAT(DATE_ADD(STR_TO_DATE( CONVERT(now(), TIME), '%H:%i:%s'),INTERVAL 2 HOUR), '%H:%i:%s')",None)
    #" and   CONVERT(mainapp_catalogodetalle.descripcion, TIME) >=DATE_FORMAT(DATE_SUB(STR_TO_DATE( CONVERT(now(), TIME), '%H:%i:%s'),INTERVAL 2 HOUR), '%H:%i:%s')",None)
    print(pacientes)
    return render(request,"paciente/consultar_paciente_cita.html",{'listPacientes':pacientes,
        'opciones_perfil':opciones_perfil,
        'fecha':date_only})
    
def consulta_medica(request,id):
    date_only = datetime.datetime.now().date()
    
    paciente=Paciente.objects.get(pk=id)
    nombre=paciente.nombre1 +''+paciente.apellido_paterno
    consultaForm=ConsultaForm    
    opciones_perfil = Opciones.objects.raw("SELECT  mainapp_opciones.id_opciones, mainapp_opciones.descripcion,mainapp_opciones.url  FROM mainapp_opciones_perfil inner join mainapp_opciones  on mainapp_opciones.id_opciones=mainapp_opciones_perfil.id_opcion where mainapp_opciones_perfil.id_perfil = "+ str(request.user.id_perfil))
    
    
    id_doctor=request.user.id_persona        
    if request.method=='POST':
        print('formulario POST')
        print(request.POST)
        
        consulta=Consulta()               
        form=ConsultaForm(request.POST)
        print(form)
        if form.is_valid(): 
            print('formulario valido')   
            
            #consulta=Consulta.objects.get(pk=id)  
            v_motivo= form.cleaned_data.get('motivo')    
            v_sintomas_evolucion=form.cleaned_data.get("sintomas_evolucion")
            v_exploracion_fisica= form.cleaned_data.get('exploracion_fisica')                             
            v_diagnostico= form.cleaned_data.get('diagnostico')
           
            consulta.fecha_cita= date_only 
            consulta.motivo=v_motivo
            consulta.sintomas_evolucion= v_sintomas_evolucion   
            consulta.exploracion_fisica=v_exploracion_fisica
            consulta.diagnostico= v_diagnostico     
            consulta.iddoctor= id_doctor                                             
            consulta.idpaciente= id
            
            
            consulta.save()
            return redirect('consultar_pacientesCita_Doc')
   
        
    return render (request, 'paciente/consulta_medica.html',{
        'consulta_M':consultaForm,        
        'opciones_perfil':opciones_perfil,
        'id_paciente':id,
        'nombre':nombre
    })

def laboratorio(request,id,idcons):
    date_only = datetime.datetime.now().date()    
    paciente=Paciente.objects.get(pk=id)    
    nombre=paciente.nombre1 +''+paciente.apellido_paterno
    laboratorioForm=LaboratorioForm    
    opciones_perfil = Opciones.objects.raw("SELECT  mainapp_opciones.id_opciones, mainapp_opciones.descripcion,mainapp_opciones.url  FROM mainapp_opciones_perfil inner join mainapp_opciones  on mainapp_opciones.id_opciones=mainapp_opciones_perfil.id_opcion where mainapp_opciones_perfil.id_perfil = "+ str(request.user.id_perfil))    
    id_doctor=request.user.id_persona    
    listLaborario = Laboratorio.objects.raw("SELECT id_estudioLaboratotio, cat.descripcion,mainapp_laboratorio.notas_recomendaciones  FROM `mainapp_laboratorio` inner join mainapp_catalogodetalle cat on cat.id_catalogo_detalle=mainapp_laboratorio.id_estudio WHERE idpaciente="+str(id)+" and id_consulta ="+str(idcons)+" and mainapp_laboratorio.estado=1")                
    if request.method=='POST':
        print('formulario POST')
        print(request.POST)
        
        laboratorio=Laboratorio()               
        form=LaboratorioForm(request.POST)
        print(form)
        if form.is_valid(): 
            print('formulario valido')   
                        
            v_notas_recomendaciones= form.cleaned_data.get('notas_recomendaciones')    
            v_id_estudio=form.cleaned_data.get("id_estudio")
                      
            laboratorio.fecha= date_only 
            laboratorio.iddoctor= id_doctor                                             
            laboratorio.idpaciente= id
            laboratorio.notas_recomendaciones=v_notas_recomendaciones
            laboratorio.id_estudio= v_id_estudio   
            laboratorio.id_consulta=idcons
                       
            laboratorio.save()
            render (request, 'paciente/laboratorio.html',{
                'laboratorioForm':laboratorioForm,        
                'opciones_perfil':opciones_perfil,
                'id_paciente':id,
                'nombre':nombre,
                'id_consulta':idcons,
                'listLaborario': listLaborario
            })
   
        
    return render (request, 'paciente/laboratorio.html',{
        'laboratorioForm':laboratorioForm,        
        'opciones_perfil':opciones_perfil,
        'id_paciente':id,
        'nombre':nombre,
        'id_consulta':idcons,
        'listLaborario': listLaborario
    })
    

def carga_estudios(request):
        
    catalogoDetalle = CatalogoDetalle.objects.raw("SELECT estudios.id_catalogo_detalle,estudios.descripcion FROM mainapp_catalogodetalle estudios where estudios.estado=1 and estudios.id_catalogo=7")  
    list_CatalogoDictionary=[]
    for c in catalogoDetalle:       
        list_CatalogoDictionary.append(catalogoDetalleToDictionary(c))        
    print (list_CatalogoDictionary)
    return JsonResponse(data={'listEstudios':list(list_CatalogoDictionary)},safe=False, status=200)

def carga_medicina(request):
        
    catalogoDetalle = CatalogoDetalle.objects.raw("SELECT estudios.id_catalogo_detalle,estudios.descripcion FROM mainapp_catalogodetalle estudios where estudios.estado=1 and estudios.id_catalogo=6")  
    list_CatalogoDictionary=[]
    for c in catalogoDetalle:       
        list_CatalogoDictionary.append(catalogoDetalleToDictionary(c))        
    print (list_CatalogoDictionary)
    return JsonResponse(data={'listReceta':list(list_CatalogoDictionary)},safe=False, status=200)


def medicina(request,id,idcons):
    date_only = datetime.datetime.now().date()    
    paciente=Paciente.objects.get(pk=id)    
    nombre=paciente.nombre1 +''+paciente.apellido_paterno
    recetaForm=RecetaForm    
    opciones_perfil = Opciones.objects.raw("SELECT  mainapp_opciones.id_opciones, mainapp_opciones.descripcion,mainapp_opciones.url  FROM mainapp_opciones_perfil inner join mainapp_opciones  on mainapp_opciones.id_opciones=mainapp_opciones_perfil.id_opcion where mainapp_opciones_perfil.id_perfil = "+ str(request.user.id_perfil))    
    id_doctor=request.user.id_persona    
    listReceta = Receta.objects.raw("SELECT id_receta, cat.descripcion,mainapp_receta.dosis_observacion FROM `mainapp_receta` inner join mainapp_catalogodetalle cat on cat.id_catalogo_detalle=mainapp_receta.id_medicamento WHERE id_paciente="+str(id)+" and id_consulta ="+str(idcons)+" and mainapp_receta.estado=1")                
    if request.method=='POST':
        print('formulario POST')
        print(request.POST)
        
        receta=Receta()               
        form=RecetaForm(request.POST)
        print(form)
        if form.is_valid(): 
            print('formulario valido')   
                        
            v_dosis_observacion= form.cleaned_data.get('dosis_observacion')    
            v_id_medicamento=form.cleaned_data.get("id_medicamento")
                      
            receta.fecha= date_only 
            receta.id_doctor= id_doctor                                             
            receta.id_paciente= id
            receta.dosis_observacion=v_dosis_observacion
            receta.id_medicamento= v_id_medicamento   
            receta.id_consulta=idcons
                       
            receta.save()
            render (request, 'paciente/receta.html',{
                'recetaForm':recetaForm,        
                'opciones_perfil':opciones_perfil,
                'id_paciente':id,
                'nombre':nombre,
                'id_consulta':idcons,
                'listReceta': listReceta
            })
   
        
    return render (request, 'paciente/receta.html',{
        'recetaForm':recetaForm,        
        'opciones_perfil':opciones_perfil,
        'id_paciente':id,
        'nombre':nombre,
        'id_consulta':idcons,
        'listReceta': listReceta
    })
    

@login_required(login_url='login')
def admision_paciente(request):
    date_only = datetime.datetime.now().date()
    print(date_only)
    opciones_perfil = Opciones.objects.raw("SELECT  mainapp_opciones.id_opciones, mainapp_opciones.descripcion,mainapp_opciones.url  FROM mainapp_opciones_perfil inner join mainapp_opciones  on mainapp_opciones.id_opciones=mainapp_opciones_perfil.id_opcion where mainapp_opciones_perfil.id_perfil = "+ str(request.user.id_perfil))
    if request.method=='POST':
       
        filtro = request.POST["txtBuscar"]
       
        pacientes = Paciente.objects.raw("SELECT mainapp_agendar_cita.id_cita ,  mainapp_agendar_cita.`id_paciente`, mainapp_paciente.`numero_identificacion`,`nombre1`,`nombre2`,`apellido_paterno`,`apellido_materno`,mainapp_agendar_cita.fecha_cita, mainapp_catalogodetalle.descripcion, mainapp_usuario.nombres  as nombreDoctor, mainapp_usuario.apellidos as apellidosDoctor FROM mainapp_paciente  inner join mainapp_agendar_cita on mainapp_agendar_cita.id_paciente = mainapp_paciente.id_paciente inner join mainapp_usuario on mainapp_agendar_cita.id_doctor = mainapp_usuario.id_persona inner join mainapp_catalogodetalle on mainapp_agendar_cita.hora = mainapp_catalogodetalle.id_catalogo_detalle left join mainapp_signos_vitales on mainapp_signos_vitales.id_paciente = mainapp_paciente.id_paciente and mainapp_agendar_cita.fecha_cita=mainapp_signos_vitales.fecha_cita where mainapp_paciente.estado =1   and mainapp_agendar_cita.admitido=0 and mainapp_paciente.numero_identificacion like '%"+str(filtro)+"%' and mainapp_agendar_cita.fecha_cita='"+str(date_only)+"' ",None)
        
        return render(request,"paciente/consultar_confirmarCita.html",{'listPacientes':pacientes,
        'opciones_perfil':opciones_perfil})
        
    pacientes = Paciente.objects.raw("SELECT  mainapp_agendar_cita.id_cita , mainapp_agendar_cita.`id_paciente`, mainapp_paciente.`numero_identificacion`,`nombre1`,`nombre2`,`apellido_paterno`,`apellido_materno`,mainapp_agendar_cita.fecha_cita, mainapp_catalogodetalle.descripcion, mainapp_usuario.nombres  as nombreDoctor, mainapp_usuario.apellidos as apellidosDoctor FROM mainapp_paciente  inner join mainapp_agendar_cita on mainapp_agendar_cita.id_paciente = mainapp_paciente.id_paciente inner join mainapp_usuario on mainapp_agendar_cita.id_doctor = mainapp_usuario.id_persona inner join mainapp_catalogodetalle on mainapp_agendar_cita.hora = mainapp_catalogodetalle.id_catalogo_detalle left join mainapp_signos_vitales on mainapp_signos_vitales.id_paciente = mainapp_paciente.id_paciente and mainapp_agendar_cita.fecha_cita=mainapp_signos_vitales.fecha_cita where mainapp_paciente.estado =1   and mainapp_agendar_cita.admitido=0 and mainapp_agendar_cita.fecha_cita='"+str(date_only)+"' ")
    
    return render(request,"paciente/consultar_confirmarCita.html",{'listPacientes':pacientes,
        'opciones_perfil':opciones_perfil,
        'fecha':date_only})
    
@login_required(login_url='login')
def consultar_pacientes_ficha(request):
    opciones_perfil = Opciones.objects.raw("SELECT  mainapp_opciones.id_opciones, mainapp_opciones.descripcion,mainapp_opciones.url  FROM mainapp_opciones_perfil inner join mainapp_opciones  on mainapp_opciones.id_opciones=mainapp_opciones_perfil.id_opcion where mainapp_opciones_perfil.id_perfil = "+ str(request.user.id_perfil))
    if request.method=='POST':       
        filtro = request.POST["txtBuscar"]        
        pacientes = Paciente.objects.raw("SELECT isnull(mainapp_ficha.id_ficha) as existeFicha , mainapp_ficha.id_ficha,mainapp_paciente.`id_paciente`,`numero_identificacion`,`nombre1`,`nombre2`,`apellido_paterno`,`apellido_materno`,`domicilio`,`correo_contacto` FROM mainapp_paciente left join mainapp_ficha on mainapp_ficha.id_paciente=mainapp_paciente.id_paciente where mainapp_paciente.estado =1  and mainapp_paciente.numero_identificacion like '%"+str(filtro)+"%'",None)
        
        return render(request,"paciente/consultar_paciente_ficha.html",{'listPacientes':pacientes,
        'opciones_perfil':opciones_perfil})
        
    pacientes = Paciente.objects.raw("SELECT isnull(mainapp_ficha.id_ficha) as existeFicha , mainapp_ficha.id_ficha,mainapp_paciente.`id_paciente`,`numero_identificacion`,`nombre1`,`nombre2`,`apellido_paterno`,`apellido_materno`,`domicilio`,`correo_contacto` FROM mainapp_paciente left join mainapp_ficha on mainapp_ficha.id_paciente=mainapp_paciente.id_paciente where mainapp_paciente.estado =1 ")
    
    return render(request,"paciente/consultar_paciente_ficha.html",{'listPacientes':pacientes,
        'opciones_perfil':opciones_perfil})
    
def ficha(request,id, existeFicha,idFicha ):
    #date_only = datetime.datetime.now().date()
    
    paciente=Paciente.objects.get(pk=id)
    nombre=paciente.nombre1 +''+paciente.apellido_paterno
    fichaForm=FichaForm    
    opciones_perfil = Opciones.objects.raw("SELECT  mainapp_opciones.id_opciones, mainapp_opciones.descripcion,mainapp_opciones.url  FROM mainapp_opciones_perfil inner join mainapp_opciones  on mainapp_opciones.id_opciones=mainapp_opciones_perfil.id_opcion where mainapp_opciones_perfil.id_perfil = "+ str(request.user.id_perfil))
    if existeFicha ==0:
            ficha=Ficha.objects.get(pk=idFicha)     
    else:
            ficha=Ficha()
    fichaForm = FichaForm(instance=ficha)      
    if request.method=='POST':
        print('formulario POST')
        print(request.POST)
        
        
                              
        form=FichaForm(request.POST)
        print(form)
        if form.is_valid(): 
            print('formulario valido')   
            
            #consulta=Consulta.objects.get(pk=id)  
            v_ante_hereditario_abuelos= form.cleaned_data.get('ante_hereditario_abuelos')    
            v_ante_hereditario_padres=form.cleaned_data.get("ante_hereditario_padres")
            v_ante_hereditario_hermanos= form.cleaned_data.get('ante_hereditario_hermanos')                             
            v_ante_patologicos= form.cleaned_data.get('ante_patologicos')
            v_id_tabaquismo= form.cleaned_data.get('id_tabaquismo')
            v_id_alcoholismo= form.cleaned_data.get('id_alcoholismo')
            v_alergias= form.cleaned_data.get('alergias')
           
             
            ficha.ante_hereditario_abuelos=v_ante_hereditario_abuelos
            ficha.ante_hereditario_padres= v_ante_hereditario_padres   
            ficha.ante_hereditario_hermanos=v_ante_hereditario_hermanos
            ficha.ante_patologicos= v_ante_patologicos     
            ficha.id_tabaquismo= v_id_tabaquismo
            ficha.id_alcoholismo= v_id_alcoholismo   
            ficha.alergias= v_alergias                                           
            ficha.id_paciente= id
            
            
            ficha.save()
            return redirect('consultar_pacientes_ficha')
   
        
    return render (request, 'paciente/consulta_ficha.html',{
        'ficha':fichaForm,        
        'opciones_perfil':opciones_perfil,
        'id_paciente':id,
        'idFicha':idFicha,
        'existeFicha':existeFicha,
        'nombre':nombre
    })
def consulta_general(request, id, idcons):
    opciones_perfil = Opciones.objects.raw("SELECT  mainapp_opciones.id_opciones, mainapp_opciones.descripcion,mainapp_opciones.url  FROM mainapp_opciones_perfil inner join mainapp_opciones  on mainapp_opciones.id_opciones=mainapp_opciones_perfil.id_opcion where mainapp_opciones_perfil.id_perfil = "+ str(request.user.id_perfil))
    
    paciente=Paciente.objects.get(pk=id)
    nombre=paciente.nombre1 +''+paciente.apellido_paterno
    
    listLaborario = Laboratorio.objects.raw("SELECT id_estudioLaboratotio, cat.descripcion,mainapp_laboratorio.notas_recomendaciones  FROM `mainapp_laboratorio` inner join mainapp_catalogodetalle cat on cat.id_catalogo_detalle=mainapp_laboratorio.id_estudio WHERE idpaciente="+str(id)+" and id_consulta ="+str(idcons)+" and mainapp_laboratorio.estado=1")                
    listReceta = Receta.objects.raw("SELECT id_receta, cat.descripcion,mainapp_receta.dosis_observacion FROM `mainapp_receta` inner join mainapp_catalogodetalle cat on cat.id_catalogo_detalle=mainapp_receta.id_medicamento WHERE id_paciente="+str(id)+" and id_consulta ="+str(idcons)+" and mainapp_receta.estado=1")                    
    #listConsulta =Consulta.objects.raw("SELECT `id_consulta`,`motivo`,`sintomas_evolucion`,`exploracion_fisica`,`iddoctor`,`diagnostico`,`fecha_cita` FROM `mainapp_consulta` inner join mainapp_usuario on mainapp_usuario.id_persona=mainapp_consulta.iddoctor and mainapp_usuario.id_perfil WHERE mainapp_consulta.id_consulta="+str(idcons)+" and mainapp_consulta.idpaciente="+str(id)+"")                    
    
    consulta=Consulta.objects.get(pk=idcons)         
    consultaForm = ConsultaGeneForm(instance=consulta)
    
    return render (request, 'paciente/consulta_general.html',{
           
            'opciones_perfil':opciones_perfil,
            'id_paciente':id,
            'listLaborario':listLaborario,
            'listReceta':listReceta,
            'consulta_M':consultaForm,
            'nombre':nombre
        })  

def consulta_historial(request, id):
    opciones_perfil = Opciones.objects.raw("SELECT  mainapp_opciones.id_opciones, mainapp_opciones.descripcion,mainapp_opciones.url  FROM mainapp_opciones_perfil inner join mainapp_opciones  on mainapp_opciones.id_opciones=mainapp_opciones_perfil.id_opcion where mainapp_opciones_perfil.id_perfil = "+ str(request.user.id_perfil))
    
    paciente=Paciente.objects.get(pk=id)
    nombre=paciente.nombre1 +''+paciente.apellido_paterno
    listConsulta =Consulta.objects.raw("SELECT `id_consulta`,mainapp_usuario.nombres,mainapp_usuario.apellidos,fecha_cita ,`motivo`,`sintomas_evolucion`,`exploracion_fisica`,`iddoctor`,`diagnostico`,`fecha_cita` FROM `mainapp_consulta` inner join mainapp_usuario on mainapp_usuario.id_persona=mainapp_consulta.iddoctor and mainapp_usuario.id_perfil WHERE mainapp_consulta.idpaciente="+str(id)+"")                    
    print (listConsulta)
    return render (request, 'paciente/consultar_historial.html',{
           
            'opciones_perfil':opciones_perfil,
            'id_paciente':id,
            'listConsulta':listConsulta,
            'nombre':nombre
        })  
    

    
def postSend(request):
    print(request.POST.get("idPaciente",""))
    id=int(request.POST.get("idPaciente",""))
    idcons=int(request.POST.get("idconsulta",""))
    tipoCorreo=(request.POST.get("tipoCorreo",""))
    paciente=Paciente.objects.get(pk=id)
    email=paciente.correo_contacto 
    #email = request.POST.get('email')
    print(email)

    
    
    template = get_template('mail/email-order-success.html')

        # Se renderiza el template y se envias parametros
    if tipoCorreo=="Receta":
        listReceta = Receta.objects.raw("SELECT id_receta, cat.descripcion,mainapp_receta.dosis_observacion FROM `mainapp_receta` inner join mainapp_catalogodetalle cat on cat.id_catalogo_detalle=mainapp_receta.id_medicamento WHERE id_paciente="+str(id)+" and id_consulta ="+str(idcons)+" and mainapp_receta.estado=1")                    
        content = template.render({'tabla': listReceta,'col1':'Medicina','col2':'Dosis / observación','tipo':'receta medica'})
    else:
        listLaborario = Laboratorio.objects.raw("SELECT id_estudioLaboratotio, cat.descripcion,mainapp_laboratorio.notas_recomendaciones as dosis_observacion  FROM `mainapp_laboratorio` inner join mainapp_catalogodetalle cat on cat.id_catalogo_detalle=mainapp_laboratorio.id_estudio WHERE idpaciente="+str(id)+" and id_consulta ="+str(idcons)+" and mainapp_laboratorio.estado=1")                
        content = template.render({'tabla': listLaborario,'col1':'Estudio laboratorio','col2':'Notas / Recomendaciones','tipo':' estudio de laboratorio'})
    print (content)

        # Se crea el correo (titulo, mensaje, emisor, destinatario)
    msg = EmailMultiAlternatives(
        'Notificación de ConsultorioGPM',
        'Hola, te enviamos una notificación',
         settings.EMAIL_HOST_USER,
         [email]
    )
    msg.attach_alternative(content, 'text/html')
    msg.send()

    #return render(request, 'mail/send.html')
    return JsonResponse(data={'listReceta':''},safe=False, status=200)

def sendCita(idPaciente,fecha):
    print(idPaciente)
    print(fecha)
    
    paciente=Paciente.objects.get(pk=idPaciente)
    email=paciente.correo_contacto 
    #email = request.POST.get('email')
    print(email)
    paciente_nombre=""
    fecha_cita=""
    hora=""
    doctor=""
    
    
    template = get_template('mail/email-cita.html')

        # Se renderiza el template y se envias parametros
    
    listAgendar_cita = Agendar_cita.objects.raw("SELECT  mainapp_agendar_cita.id_cita ,  mainapp_paciente.`numero_identificacion`,`nombre1`,`nombre2`,`apellido_paterno`,`apellido_materno`,mainapp_agendar_cita.fecha_cita, mainapp_catalogodetalle.descripcion hora, mainapp_usuario.nombres  as nombreDoctor, mainapp_usuario.apellidos as apellidosDoctor FROM mainapp_paciente  inner join mainapp_agendar_cita on mainapp_agendar_cita.id_paciente = mainapp_paciente.id_paciente inner join mainapp_usuario on mainapp_agendar_cita.id_doctor = mainapp_usuario.id_persona inner join mainapp_catalogodetalle on mainapp_agendar_cita.hora = mainapp_catalogodetalle.id_catalogo_detalle where mainapp_paciente.estado =1    and mainapp_agendar_cita.`id_paciente`="+str(idPaciente)+" and  mainapp_agendar_cita.fecha_cita='"+str(fecha)+"'")                    
    for c in listAgendar_cita:
        paciente_nombre=c.nombre1+" "+ c.apellido_paterno
        fecha_cita=c.fecha_cita 
        hora=c.hora
        doctor=c.nombreDoctor +" "+ c.apellidosDoctor
    content = template.render({'paciente_nombre': paciente_nombre, 'fecha_cita':fecha_cita,'hora':hora,'doctor':doctor })
    
    print (content)

        # Se crea el correo (titulo, mensaje, emisor, destinatario)
    msg = EmailMultiAlternatives(
        'Notificación de ConsultorioGPM',
        'Hola, te enviamos una notificación',
         settings.EMAIL_HOST_USER,
         [email]
    )
    msg.attach_alternative(content, 'text/html')
    msg.send()

    #return render(request, 'mail/send.html')
    return  "ok"


@login_required(login_url='login')
def consultar_pacientes_filtro_a(request):
    opciones_perfil = Opciones.objects.raw("SELECT  mainapp_opciones.id_opciones, mainapp_opciones.descripcion,mainapp_opciones.url  FROM mainapp_opciones_perfil inner join mainapp_opciones  on mainapp_opciones.id_opciones=mainapp_opciones_perfil.id_opcion where mainapp_opciones_perfil.id_perfil = "+ str(request.user.id_perfil))
    if request.method=='POST':
        print('formulario POST')
        print(request.POST)
        filtro = request.POST["txtBuscar"]
        print("SELECT `id_paciente`,`numero_identificacion`,`nombre1`,`nombre2`,`apellido_paterno`,`apellido_materno`,`domicilio`,`correo_contacto` FROM mainapp_paciente where mainapp_paciente.estado =1  and mainapp_paciente.numero_identificacion like '%"+(filtro)+"%'")
        pacientes = Paciente.objects.raw("SELECT `id_paciente`,`numero_identificacion`,`nombre1`,`nombre2`,`apellido_paterno`,`apellido_materno`,`domicilio`,`correo_contacto` FROM mainapp_paciente where mainapp_paciente.estado =1  and mainapp_paciente.numero_identificacion like '%"+str(filtro)+"%'",None)
        
        return render(request,"paciente/consultar_pacienteFiltro.html",{'listPacientes':pacientes,
        'opciones_perfil':opciones_perfil})
        
    pacientes = Paciente.objects.raw("SELECT `id_paciente`,`numero_identificacion`,`nombre1`,`nombre2`,`apellido_paterno`,`apellido_materno`,`domicilio`,`correo_contacto` FROM mainapp_paciente where mainapp_paciente.estado =1 ")
    
    return render(request,"paciente/consultar_pacienteFiltro.html",{'listPacientes':pacientes,
        'opciones_perfil':opciones_perfil})