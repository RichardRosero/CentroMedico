from django import forms
from django.core import validators
from django.contrib.auth import get_user_model
from mainapp.models import Usuario ,Paciente,Agendar_cita, Signos_vitales,Consulta , Laboratorio, Ficha




class RegisterForm (forms.ModelForm):
    
    password1=forms.CharField(label = 'Contraseña', widget = forms.PasswordInput(
         attrs = {
                    'class':'form-control',
                    'placeholder':'Contraseña',
                    'id':'password1',
                    'required':'required',
                    'maxlength':'15'
                }
     ))
    password2=forms.CharField(label= 'Contraseña de confirmación', widget = forms.PasswordInput(
         attrs={
                    'class':'form-control',
                    'placeholder':'Ingrese nuevamente su contraseña',
                    'id':'password2',
                    'required':'required',
                    'maxlength':'15'
                }
     ))
    numero_identificacion= forms.CharField(
        label="Número identificación",        
        max_length=10,
        required=True,
        error_messages={'required': 'Favor ingresa tu número de cédula'},
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':'Numero de Identificación'
            }
        ) ,      
      validators=[
            validators.MinLengthValidator(10,'La cédula debe tener 10 dígitos')
        ]
    ) 
    username= forms.CharField(
        label="Usuario",        
        max_length=10,
        required=True,
        error_messages={'required': 'Favor ingresa tu usuario'},
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':'Usuario'
            }
        ) ,      
      validators=[
            validators.MinLengthValidator(5,'El usuario debe tener mínimo 5 caracteres')
        ]
    ) 
    id_perfil_options=[
         (1,'Doctor'),
         (2,'Operativo'),
         (3,'Enfermera'),
         (4,'Administrador')
    ]
    id_perfil = forms.TypedChoiceField(
        label = "Perfil usuario",
        choices = id_perfil_options,
        required=True,
        widget=forms.Select(
            attrs={
                'class':'form-control'                
            }
        ) ,  
    ) 

    class Meta:
        model = Usuario
        fields = ['username','numero_identificacion','nombres','apellidos','domicilio','correo_contacto','id_perfil']
        widgets = {
            'correo_contacto': forms.EmailInput(
                attrs = {
                    'class':'form-control',
                    'placeholder':'Correo Contacto',
                    'required':'required'
                    }
            ),
            
            'nombres': forms.TextInput(
                attrs = {
                    'class':'form-control',
                    'placeholder':'Nombres',
                    'required':'required'
                }
            ), 
            'apellidos': forms.TextInput(
                attrs = {
                    'class':'form-control',
                    'placeholder':'Apellidos',
                    'required':'required'
                }
            ),
            'domicilio': forms.TextInput(
                attrs = {
                    'class':'form-control',
                    'placeholder':'Domicilio',
                    'required':'required'
                }
            ),
            
            
        }
    
   
    def clean_password2(self):
        """validación de que las dos contraseñas sean validas """
        password1= self.cleaned_data.get('password1')
        password2= self.cleaned_data.get('password2')
        print(password1)
        print(password2)
        if password1!= password2:
           print("Contraseñas no coninciden")
           raise forms.ValidationError("Contraseñas no coninciden")
        return password2
    def save(self, commit=True):
        user=super().save(commit = False)
        user.set_password(self.cleaned_data.get('password1'))
        if commit:
            user.save()
        return user

 

User = get_user_model()

class UserChangeForm(forms.ModelForm):
    #username = UsernameField(widget = forms.TextInput(attrs = {'class': 'form-control form-control-sm'}))
    
    numero_identificacion= forms.CharField(
        label="Número identificación",        
        max_length=10,
        required=True,
        error_messages={'required': 'Favor ingresa tu número de cédula'},
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':'Numero de Identificación'
            }
        ) ,      
      validators=[
            validators.MinLengthValidator(10,'La cédula debe tener 10 dígitos')
        ]
    ) 
    """username= forms.CharField(
        label="Usuario",        
        max_length=20,
        required=True,
        error_messages={'required': 'Favor ingresa tu usuario'},
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':'Usuario'
            }
        ) ,      
      validators=[
            validators.MinLengthValidator(5,'El usuario debe tener mínimo 5 caracteres')
        ]
    ) """
    id_perfil_options=[
         (1,'Doctor'),
         (2,'Operativo'),
         (3,'Enfermera'),
         (4,'Administrador')
    ]
    id_perfil = forms.TypedChoiceField(
        label = "Perfil usuario",
        choices = id_perfil_options,
        required=True,
        widget=forms.Select(
            attrs={
                'class':'form-control'                
            }
        ) ,  
    ) 
    class Meta:               
        model = Usuario
        fields = ['numero_identificacion','nombres','apellidos','domicilio','correo_contacto','id_perfil']
        widgets = {
            'correo_contacto': forms.EmailInput(
                attrs = {
                    'class':'form-control',
                    'placeholder':'Correo Contacto',
                    'required':'required'
                    }
            ),
            
            'nombres': forms.TextInput(
                attrs = {
                    'class':'form-control',
                    'placeholder':'Nombres',
                    'required':'required'
                }
            ), 
            'apellidos': forms.TextInput(
                attrs = {
                    'class':'form-control',
                    'placeholder':'Apellidos',
                    'required':'required'
                }
            ),
            'domicilio': forms.TextInput(
                attrs = {
                    'class':'form-control',
                    'placeholder':'Domicilio',
                    'required':'required'
                }
            ),
            
            
        }
    
class PacienteForm(forms.ModelForm):
    numero_identificacion= forms.CharField(
        label="Número identificación",        
        max_length=10,
        required=True,
        error_messages={'required': 'Favor ingresa tu número de cédula'},
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':'Numero de Identificación'
            }
        ),      
      validators=[
            validators.MinLengthValidator(10,'La cédula debe tener 10 dígitos')
        ]
    ) 
    nombre1 = forms.CharField(
        max_length=20,
        required=True,
        label="Primer Nombre",
        widget=forms.TextInput(
            attrs = {
                    'class':'form-control',
                    'placeholder':'Primer Nombre',
                    'required':'required'
                }
        ),
    )  
    nombre2 = forms.CharField(
        max_length=20,
        required=True,
        label="Segundo Nombre",
        widget=forms.TextInput(
            attrs = {
                    'class':'form-control',
                    'placeholder':'Segundo Nombre',
                    'required':'required'                   
                }
        ),
    )  
    id_provincia = forms.CharField(        
        required=True,
        label="Provincia",
        widget=forms.Select(
            attrs = {
                    'class':'form-control',
                    'placeholder':'Provincia',
                    'required':'required'                    
                }
        ),
    )  
    id_ciudad = forms.CharField(        
        required=True,
        label="Ciudad",
        widget=forms.Select(
            attrs = {
                    'class':'form-control',
                    'placeholder':'Ciudad',
                    'required':'required'                        
                }
        ),
    )  
    id_tipo_sangre = forms.CharField(        
        required=True,
        label="Tipo sangre",
        widget=forms.Select(
            attrs = {
                    'class':'form-control',
                    'placeholder':'Tipo sangre' ,
                    'required':'required'                       
                }
        ),
    )  
    id_estado_civil = forms.CharField(        
        required=True,
        label="Estado Civil",
        widget=forms.Select(
            attrs = {
                    'class':'form-control',
                    'placeholder':'Estado Civil' ,
                    'required':'required'                       
                }
        ),
    )  
    id_ciudad_nacimiento = forms.CharField(        
        required=True,
        label="Ciudad de nacimiento",
        widget=forms.Select(
            attrs = {
                    'class':'form-control',
                    'placeholder':'Ciudad de nacimiento' ,
                    'required':'required'                        
                }
        ),
    )   
    id_sexo = forms.CharField(        
        required=False,
        label="Sexo",
        widget=forms.Select(
            attrs = {
                    'class':'form-control',
                    'placeholder':'Sexo' ,
                    'required':'required'                       
                }
        ),
    )     
    telefono_contacto = forms.CharField(
        max_length=10,
        required=True,
        label="Teléfono contacto",
        widget=forms.TextInput(
            attrs = {
                    'class':'form-control',
                    'placeholder':'Teléfono contacto',
                    'required':'required'                   
                }
        ),
    )  
    observaciones = forms.CharField(
        max_length=100,
        required=False,
        label="Observaciones",
        widget=forms.TextInput(
            attrs = {
                    'class':'form-control',
                    'placeholder':'Observaciones'                                      
                }
        ),
    ) 
    edad = forms.CharField(
        max_length=2,
        required=True,
        label="Edad",
        widget=forms.TextInput(
            attrs = {
                    'class':'form-control',
                    'placeholder':'Edad' ,
                    'readonly':'True'                                     
                }
        ),
    ) 
    fecha_nacimiento = forms.DateField(        
        required=True,
        label="Fecha Nacimiento",
        widget=forms.TextInput(
            attrs = {
                    'class':'form-control',
                    'placeholder':'Fecha Nacimiento',  
                    'id':'fecha_nacimiento'                                    
                }
        ),
    )     
    
    #input_formats=['%Y-%m-%d']
    class Meta:               
        model = Paciente
        fields = ['numero_identificacion','nombre1','nombre2','apellido_paterno','apellido_materno','domicilio','correo_contacto','id_provincia',
                    'id_ciudad','id_tipo_sangre','id_estado_civil','id_sexo','telefono_contacto','fecha_nacimiento','edad','observaciones','id_ciudad_nacimiento']       
        widgets = {
            'correo_contacto': forms.EmailInput(
                attrs = {
                    'class':'form-control',
                    'placeholder':'Correo Contacto',
                    'required':'required'
                    }
            ),                       
            'apellido_paterno': forms.TextInput(
                attrs = {
                    'class':'form-control',
                    'placeholder':'Apellido Paterno',
                    'required':'required'
                }
            ),
            'apellido_materno': forms.TextInput(
                attrs = {
                    'class':'form-control',
                    'placeholder':'Apellido Materno',
                    'required':'required'
                }
            ),
            'domicilio': forms.TextInput(
                attrs = {
                    'class':'form-control',
                    'placeholder':'Domicilio',
                    'required':'required'
                }
            ),                                                              
        }
       
class CitaForm(forms.ModelForm):
    observacion = forms.CharField(
        max_length=150,
        required=True,
        label="Observacion",
        widget=forms.TextInput(
            attrs = {
                    'class':'form-control',
                    'placeholder':'Observacion',
                    'required':'required'                   
                }
        ),
    )  
    id_doctor = forms.CharField(        
        required=True,
        label="Doctor",
        widget=forms.Select(
            attrs = {
                    'class':'form-control',
                    'placeholder':'Doctor' ,
                    'required':'required'                       
                }
        ),
    )  
    hora = forms.CharField(
        
        required=True,
        label="Hora",
        widget=forms.Select(
            attrs = {
                    'class':'form-control',
                    'placeholder':'Hora' ,                                                        
                }
        ),
    ) 
    fecha_cita = forms.DateField(        
        required=True,
        label="Fecha Cita",
        widget=forms.TextInput(
            attrs = {
                    'class':'form-control',
                    'placeholder':'Fecha Cita',  
                    'id':'fecha_cita'                                    
                }
        ),
    )     
        
    class Meta:               
        
        model = Agendar_cita
        fields = ['id_doctor','fecha_cita','hora','observacion']   
                        
class SignoVitalForm(forms.ModelForm):   
        
    peso = forms.CharField(
        max_length=6,
        required=True,
        label="Peso KG",
        widget=forms.TextInput(
            attrs = {
                    'class':'form-control',
                    'placeholder':'Peso KG' ,                                                        
                }
        ),
    ) 
    talla = forms.CharField(
        max_length=6,
        required=True,
        label="Talla CM",
        widget=forms.TextInput(
            attrs = {
                    'class':'form-control',
                    'placeholder':'Talla CM' ,                                                        
                }
        ),
    ) 
    imc = forms.CharField(
        max_length=6,
        required=True,
        label="IMC",
        widget=forms.TextInput(
            attrs = {
                    'class':'form-control',
                    'placeholder':'IMC' ,
                    'readonly':'True'                                                            
                }
        ),
    ) 
    temperatura = forms.CharField(
        max_length=2,
        required=True,
        label="Temperatura",
        widget=forms.TextInput(
            attrs = {
                    'class':'form-control',
                    'placeholder':'Temperatura' ,
                                                                               
                }
        ),
    ) 
    f_cardica = forms.CharField(
        max_length=3,
        required=True,
        label="F. Cardiaca",
        widget=forms.TextInput(
            attrs = {
                    'class':'form-control',
                    'placeholder':'F. Cardiaca' ,
                                                                                
                }
        ),
    ) 
    F_respiratoria = forms.CharField(
        max_length=3,
        required=True,
        label="F. Respiratoria",
        widget=forms.TextInput(
            attrs = {
                    'class':'form-control',
                    'placeholder':'F. Respiratoria' ,
                                                                             
                }
        ),
    )
    sistolica = forms.CharField(
        max_length=3,
        required=True,
        label="Sistolica",
        widget=forms.TextInput(
            attrs = {
                    'class':'form-control',
                    'placeholder':'Sistolica' ,
                                                                              
                }
        ),
    ) 
    distolica = forms.CharField(
        max_length=3,
        required=True,
        label="Distolica",
        widget=forms.TextInput(
            attrs = {
                    'class':'form-control',
                    'placeholder':'Distolica' ,
                                                                              
                }
        ),
    ) 
    oximetria = forms.CharField(
        max_length=3,
        required=True,
        label="Oximetría %",
        widget=forms.TextInput(
            attrs = {
                    'class':'form-control',
                    'placeholder':'Oximetría %' ,
                                                                               
                }
        ),
    )       
    
    
    class Meta:                   
        model = Signos_vitales
        fields = ['peso','talla','imc','temperatura','f_cardica','F_respiratoria','sistolica','distolica','oximetria'] 
        
class ConsultaForm(forms.ModelForm):
    motivo = forms.CharField(
        max_length=250,
        required=True,
        label="Motivo",
        widget=forms.TextInput(
            attrs = {
                    'class':'form-control',
                    'placeholder':'Motivo',
                    'required':'required'                   
                }
        ),
    )
    sintomas_evolucion = forms.CharField(
        max_length=250,
        required=True,
        label="Síntomas / Evolución",
        widget=forms.TextInput(
            attrs = {
                    'class':'form-control',
                    'placeholder':'Síntomas / Evolución',
                    'required':'required'                   
                }
        ),
    )  
    exploracion_fisica = forms.CharField(        
        required=True,
        label="Exploración física",
        widget=forms.TextInput(
            attrs = {
                    'class':'form-control',
                    'placeholder':'Exploración física' ,
                    'required':'required'                       
                }
        ),
    )  
    
    diagnostico = forms.CharField(        
        required=True,
        label="Diagnóstico",
        widget=forms.TextInput(
            attrs = {
                    'class':'form-control',
                    'placeholder':'Diagnóstico' ,
                    'required':'required'                       
                }
        ),
    )
    class Meta:               
        
        model = Consulta
        fields = ['motivo','sintomas_evolucion','exploracion_fisica','diagnostico']   

class LaboratorioForm(forms.ModelForm):
    id_estudio = forms.CharField(
        required=True,
        label="Estudio Laboratorio",
        widget=forms.Select(
            attrs = {
                    'class':'form-control',
                    'placeholder':'Estudio Laboratorio' ,
                    'required':'required'                       
                }
        ),
    )  
    notas_recomendaciones = forms.CharField(
        max_length=250,
        required=True,
        label="Notas / Recomendaciones",
        widget=forms.TextInput(
            attrs = {
                    'class':'form-control',
                    'placeholder':'Notas / Recomendaciones',
                    'required':'required'                   
                }
        ),
    )      
  
    class Meta:               
        
        model = Laboratorio
        fields = ['id_estudio','notas_recomendaciones']   
        
class RecetaForm(forms.ModelForm):
    id_medicamento = forms.CharField(
        required=True,
        label="Medicamento",
        widget=forms.Select(
            attrs = {
                    'class':'form-control',
                    'placeholder':'Medicamento' ,
                    'required':'required'                       
                }
        ),
    )  
    dosis_observacion = forms.CharField(
        max_length=250,
        required=True,
        label="Dosis / Observaciones",
        widget=forms.TextInput(
            attrs = {
                    'class':'form-control',
                    'placeholder':'Dosis / Observaciones',
                    'required':'required'                   
                }
        ),
    )      
  
    class Meta:               
        
        model = Laboratorio
        fields = ['id_medicamento','dosis_observacion']   
        
class FichaForm(forms.ModelForm):
    ante_hereditario_abuelos = forms.CharField(
        required=True,
        label="Antecedentes hereditarios (abuelos):",
        widget=forms.TextInput(
            attrs = {
                    'class':'form-control',
                    'placeholder':'Antecedentes hereditarios (abuelos):' ,
                    'required':'required'                       
                }
        ),
    ) 
    ante_hereditario_padres = forms.CharField(
        required=True,
        label="Antecedentes hereditarios (padres):",
        widget=forms.TextInput(
            attrs = {
                    'class':'form-control',
                    'placeholder':'Antecedentes hereditarios (padres):' ,
                    'required':'required'                       
                }
        ),
    ) 
    ante_hereditario_hermanos = forms.CharField(
        required=True,
        label="Antecedentes hereditarios (hermanos):",
        widget=forms.TextInput(
            attrs = {
                    'class':'form-control',
                    'placeholder':'Antecedentes hereditarios (hermanos):' ,
                    'required':'required'                       
                }
        ),
    )
    ante_patologicos = forms.CharField(
        max_length=250,
        required=True,
        label="Antecedentes patológicos:",
        widget=forms.TextInput(
            attrs = {
                    'class':'form-control',
                    'placeholder':'Antecedentes patológicos:',
                    'required':'required'                   
                }
        ),
    )      
    
    id_options=[
         (1,'Nunca'),
         (2,'Casual'),
         (3,'Enfermedad'),
         (4,'Moderado')
    ]
    id_tabaquismo = forms.TypedChoiceField(
        required=True,
        choices = id_options,
        label="Tabaquismo",
        widget=forms.Select(
            attrs = {
                    'class':'form-control',
                    'placeholder':'Tabaquismo' ,
                    'required':'required'                       
                }
        ),
    )
    id_alcoholismo = forms.TypedChoiceField(
        required=True,
        choices = id_options,
        label="Alcoholismo",
        widget=forms.Select(
            attrs = {
                    'class':'form-control',
                    'placeholder':'Alcoholismo' ,
                    'required':'required'                       
                }
        ),
    )
    alergias = forms.CharField(
        
        max_length=250,
        required=True,
        label="Alergias:",
        widget=forms.TextInput(
            attrs = {
                    'class':'form-control',
                    'placeholder':'Alergias:',
                    'required':'required'                   
                }
        ),
    )
    
    class Meta:               
        
        model = Ficha
        fields = ['ante_hereditario_abuelos','ante_hereditario_padres','ante_hereditario_hermanos','ante_patologicos','id_tabaquismo','id_alcoholismo','alergias']   
       
       
class ConsultaGeneForm(forms.ModelForm):
    motivo = forms.CharField(    
        label="Motivo",
        widget=forms.TextInput(
            attrs = {
                    'class':'form-control',
                    'placeholder':'Motivo',
                    'readonly':'True'                    
                }
        ),
    )
    sintomas_evolucion = forms.CharField(        
        label="Síntomas / Evolución",
        widget=forms.TextInput(
            attrs = {
                    'class':'form-control',
                    'placeholder':'Síntomas / Evolución',
                    'readonly':'True'                   
                }
        ),
    )  
    exploracion_fisica = forms.CharField(        
        required=True,
        label="Exploración física",
        widget=forms.TextInput(
            attrs = {
                    'class':'form-control',
                    'placeholder':'Exploración física' ,
                    'readonly':'True'                       
                }
        ),
    )  
    
    diagnostico = forms.CharField(        
        required=True,
        label="Diagnóstico",
        widget=forms.TextInput(
            attrs = {
                    'class':'form-control',
                    'placeholder':'Diagnóstico' ,
                    'readonly':'True'                       
                }
        ),
    )
    class Meta:               
        
        model = Consulta
        fields = ['motivo','sintomas_evolucion','exploracion_fisica','diagnostico']   