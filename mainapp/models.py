from datetime import datetime
from distutils.command.upload import upload
from django.db import models


from django.contrib.auth.models import AbstractBaseUser ,BaseUserManager
import os

class UsuarioManager(BaseUserManager):
    def create_user(self,username,numero_identificacion,nombres,apellidos,domicilio,correo_contacto,password,id_perfil,is_active):
        if not correo_contacto:
            raise ValueError ('El usuario debe tener un correo electrónico!')
        usuario = self.model(
            username=username,
            numero_identificacion=numero_identificacion,
            correo_contacto= self.normalize_email(correo_contacto),
            nombres=nombres, 
            apellidos=apellidos,
            domicilio=domicilio,
            id_perfil=id_perfil,
            is_active=is_active)
        usuario.set_password(password)
        usuario.save()
        return usuario
def create_super_user(self,username,numero_identificacion,nombres,apellidos,domicilio,correo_contacto,password,id_perfil,is_active):
    usuario = self.create_user(
        username=username,
        numero_identificacion=numero_identificacion,
        nombres=nombres,
        apellidos=apellidos,
        domicilio=domicilio,
        correo_contacto=correo_contacto,
        password=password,
        id_perfil=id_perfil,
        is_active=is_active)
    usuario.usuario_administrador=True
    usuario.save()

    return usuario


class Usuario(AbstractBaseUser):
    id_persona= models.AutoField(auto_created = True,
                  primary_key = True)
    USERNAME_FIELD = 'username'
    username= models.CharField(max_length= 20,unique=True)
    numero_identificacion= models.CharField(default='',max_length= 10)
    nombres= models.CharField(max_length= 50, default='')     
    apellidos= models.CharField(max_length= 50, default='')    
    domicilio= models.CharField(max_length= 120, default='')
    correo_contacto=models.CharField(max_length= 120, default='')
    id_perfil = models.IntegerField(default='0')
    is_active = models.BooleanField(default=True)
    objects= UsuarioManager()
    """#IS NORMAL USER OR PARTNER OF THE APP    
    is_active = models.BooleanField(default=True)

    #THIS FIELDS JUST MAKESURE THE USER IS NOT ADMIN-PAGE
    is_superuser = None
    is_staff = None
    
    last_login = None
    first_name = None
    first_name = None
    date_joined = None
    last_name = None
    email = None
    """
    def has_perm(self,perm,obj=None):
        return True
    def has_module_perms(self, app_label):
        return True
    
    @property
    def isStff(self):
        return self.usuario_administrador


class Opciones(models.Model):
    id_opciones=models.AutoField(auto_created = True,
                  primary_key = True)
    descripcion= models.CharField(max_length= 100)
    url= models.CharField(max_length= 100, default='')

class Opciones_perfil(models.Model):
    id_opciones_perfil=models.IntegerField(primary_key = True)
    id_perfil= models.IntegerField()
    id_opcion= models.IntegerField()    

#class django_mysql.models.SizedBinaryField(4)

class Paciente(models.Model):
    id_paciente= models.AutoField(auto_created = True,
                  primary_key = True)
    numero_identificacion= models.CharField(max_length= 15, default='')  
    nombre1= models.CharField(max_length= 50, default='')
    nombre2= models.CharField(max_length= 50, default='')  
    apellido_paterno= models.CharField(max_length= 50, default='')  
    apellido_materno= models.CharField(max_length= 50, default='')  
    domicilio= models.CharField(max_length= 150, default='')
    correo_contacto= models.CharField(max_length= 150, default='')
    estado= models.IntegerField(default=1)
    imagen= models.BinaryField(max_length=None, editable = True, null=True, blank=False)
    id_provincia=models.IntegerField(null=True)
    id_ciudad=models.IntegerField(null=True)
    id_sexo=models.IntegerField(null=True)
    id_ciudad_nacimiento=models.IntegerField(null=True)
    id_tipo_sangre=models.IntegerField(null=True)
    id_estado_civil=models.IntegerField(null=True)
    fecha_nacimiento=models.DateField(null=True)
    edad=models.IntegerField(null=True)
    telefono_contacto=models.CharField(max_length= 10, default='')
    observaciones= models.CharField(max_length= 150, default='')

class CatalogoDetalle(models.Model):
    id_catalogo_detalle= models.AutoField(auto_created = True,
                  primary_key = True)
    id_catalogo=models.IntegerField(null=True)
    descripcion= models.CharField(max_length= 50, default='')
    id_padre=models.IntegerField(null=True)
    estado= models.IntegerField(default=1)
    
    
class Catalogo(models.Model):   
    id_catalogo=models.AutoField(auto_created = True,
                  primary_key = True)
    descripcion= models.CharField(max_length= 50, default='')
    estado= models.IntegerField(default=1)

class Agendar_cita(models.Model):   
    id_cita=models.AutoField(auto_created = True,
                  primary_key = True)
    id_paciente= models.IntegerField(null=True)
    id_doctor= models.IntegerField(null=True)
    fecha_cita=models.DateField(null=True)
    hora=models.IntegerField(null=True)
    observacion= models.CharField(max_length= 150, default='')
    admitido= models.IntegerField(default=0)
    estado= models.IntegerField(default=1)
 
class Signos_vitales(models.Model):   
    id_signo_vital=models.AutoField(auto_created = True,
                  primary_key = True)
    id_paciente= models.IntegerField(null=True)    
    fecha_cita=models.DateField(null=True)
    peso=models.DecimalField(null=True,max_digits = 5,decimal_places=2)       
    talla=models.DecimalField(null=True,max_digits = 5,decimal_places=2) 
    imc=models.DecimalField(null=True,max_digits = 5,decimal_places=2)    
    temperatura=models.DecimalField(null=True,max_digits = 5,decimal_places=2) 
    f_cardiaca= models.IntegerField(null=True)
    f_respiratoria= models.IntegerField(null=True) 
    sistolica= models.IntegerField(null=True) 
    distolica= models.IntegerField(null=True) 
    oximetria=models.DecimalField(null=True,max_digits = 5,decimal_places=2) 
    estado= models.IntegerField(default=1)
       
    
class Consulta(models.Model):   
    id_consulta=models.AutoField(auto_created = True,
                  primary_key = True)
    motivo= models.CharField(max_length= 1250, default='')
    sintomas_evolucion= models.CharField(max_length= 250, default='')  
    exploracion_fisica= models.CharField(max_length= 250, default='')
    idpaciente =models.IntegerField(null=True) 
    iddoctor =models.IntegerField(null=True)
    diagnostico = models.CharField(max_length= 250, default='')                
    fecha_cita=models.DateField(null=True)       
    estado= models.IntegerField(default=1)

class Laboratorio(models.Model):   
    id_estudioLaboratotio=models.AutoField(auto_created = True,
                  primary_key = True)  
    id_consulta=models.IntegerField(null=True)    
    idpaciente =models.IntegerField(null=True) 
    iddoctor =models.IntegerField(null=True)
    id_estudio=models.IntegerField(null=True) 
    notas_recomendaciones = models.CharField(max_length= 250, default='')                
    fecha=models.DateField(null=True)       
    estado= models.IntegerField(default=1)
    
class Receta(models.Model):   
    id_receta=models.AutoField(auto_created = True,
                  primary_key = True)  
    id_consulta=models.IntegerField(null=True)    
    id_paciente =models.IntegerField(null=True) 
    id_doctor =models.IntegerField(null=True)
    id_medicamento=models.IntegerField(null=True) 
    dosis_observacion = models.CharField(max_length= 250, default='')                
    fecha=models.DateField(null=True)       
    estado= models.IntegerField(default=1)
    
class Ficha(models.Model):   
    id_ficha=models.AutoField(auto_created = True,
                  primary_key = True)         
    id_paciente =models.IntegerField(null=True) 
    ante_hereditario_abuelos =models.CharField(max_length= 250, default='') 
    ante_hereditario_padres =models.CharField(max_length= 250, default='') 
    ante_hereditario_hermanos =models.CharField(max_length= 250, default='') 
    ante_patologicos =models.CharField(max_length= 250, default='') 
    id_tabaquismo=models.IntegerField(null=True) 
    id_alcoholismo=models.IntegerField(null=True) 
    alergias=models.CharField(max_length= 250, default='')     
    estado= models.IntegerField(default=1)
    

    
    
   

    