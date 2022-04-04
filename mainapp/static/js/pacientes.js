

    $(document).ready(function() {
    
        console.log( "form ready!" );
        CargaProvincia();
        CargaTipoSangre();
        CargaEstadoCivil();
        CargaSexo();
        CargaCiudadNac();    
        CargaCiudad(1);
       
    });

function CargaProvincia(){
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let idPaciente = document.querySelector('[name=idPaciente]').value;
    
    if(idPaciente=='')
    {
        idPaciente=0        
    }
   
    $.ajax({//Inicializamos el Ajax que es parte del JQuery
            url: "../../carga_Provincia/",//Url que se encarga de linkear el método que trae la data
            type: "POST",//Tipo POST - para obtener la lista de datos
            dataType: "json",//Dato tipo json - el método que nos trae la data es un JsonResult
            data: {
                idPaciente:idPaciente
            },//Pasar lo parámetros o filtros si es que existiera
            headers: {'X-CSRFToken': csrftoken}, 
            success: function (data) {//Ejecutamos la función para poder cargar la data al select

                if (data.listProvincia == null) {//Validación de datos nulos
                    alert('Disculpe, No hay provincias que mostrar.');
                    return
                } 
                else 
                {
                    let list= data.listProvincia;
                    let idProvinciaSelect= data.id_provincia;
                    
                    for (var i = 0; i < list.length; i++) {//Recorremos y almacenamos la data en el select (SltDepartamento)
                        if (idProvinciaSelect==list[i].id_catalogo)
                        {
                            $("#id_id_provincia").append("<option value=" + list[i].id_catalogo + " Selected>" + list[i].descripcion + "</option>");
                        }
                        else{
                            $("#id_id_provincia").append("<option value=" + list[i].id_catalogo + ">" + list[i].descripcion + "</option>");
                        }
                        
                        
                    }
                }
            },
            error: function (jqXHR, status, error) {//mensaje de error
                alert('Disculpe, existió un problema método CargaProvincia');
            }
        });

}

function CargaCiudad(id_provincia){
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;    
    let idPaciente = document.querySelector('[name=idPaciente]').value;    
    if(idPaciente=='')
    {
        idPaciente=0        
    }
    
    $.ajax({//Inicializamos el Ajax que es parte del JQuery
            url: "../../carga_Ciudad/",//Url que se encarga de linkear el método que trae la data
            type: "POST",//Tipo POST - para obtener la lista de datos
            dataType: "json",//Dato tipo json - el método que nos trae la data es un JsonResult
            data: { 
                id_provincia : id_provincia,
                idPaciente:idPaciente
            },//Pasar lo parámetros o filtros si es que existiera
            headers: {'X-CSRFToken': csrftoken}, 
            success: function (data) {//Ejecutamos la función para poder cargar la data al select

                if (data.listCiudad == null) {//Validación de datos nulos
                    alert('Disculpe, No hay ciudades que mostrar.');
                    return
                } 
                else 
                {   
                    let list= data.listCiudad;                   
                    let idCiudadSelect= data.id_ciudad;                
                    $('#id_id_ciudad').empty().append('');
                    
                    for (var i = 0; i < list.length; i++) {//Recorremos y almacenamos la data en el select (SltDepartamento)
                        
                        if (idCiudadSelect==list[i].id_catalogo)
                        {
                            $("#id_id_ciudad").append("<option value=" + list[i].id_catalogo + " Selected >" + list[i].descripcion + "</option>");
                        }
                        else{
                            $("#id_id_ciudad").append("<option value=" + list[i].id_catalogo + ">" + list[i].descripcion + "</option>");
                        
                        }
                        
                    }
                }
            },
            error: function (jqXHR, status, error) {//mensaje de error
                alert('Disculpe, existió un problema método CargaCiudad');
            }
        });

}

$("select[name=id_provincia]").change(function(){
    //alert($('select[name=id_provincia]').val());
    id_provincia=$('select[name=id_provincia]').val();    
    CargaCiudad(id_provincia);
});

function CargaTipoSangre(){
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let idPaciente = document.querySelector('[name=idPaciente]').value;    
    if(idPaciente=='')
    {
        idPaciente=0        
    }
    $.ajax({//Inicializamos el Ajax que es parte del JQuery
            url: "../../carga_TipoSangre/",//Url que se encarga de linkear el método que trae la data
            type: "POST",//Tipo POST - para obtener la lista de datos
            dataType: "json",//Dato tipo json - el método que nos trae la data es un JsonResult
            data: {
                idPaciente:idPaciente
            },//Pasar lo parámetros o filtros si es que existiera
            headers: {'X-CSRFToken': csrftoken}, 
            success: function (data) {//Ejecutamos la función para poder cargar la data al select

                if (data.listTipoSangre == null) {//Validación de datos nulos
                    alert('Disculpe, No hay TipoSangre que mostrar.');
                    return
                } 
                else 
                {   
                    let list= data.listTipoSangre;
                    let idTipoSangreSelect= data.id_tipoSangre;

                    for (var i = 0; i < list.length; i++) {//Recorremos y almacenamos la data en el select (SltDepartamento)
                        if (idTipoSangreSelect==list[i].id_catalogo)
                        {
                            $("#id_id_tipo_sangre").append("<option value=" + list[i].id_catalogo + " Selected>" + list[i].descripcion + "</option>");
                        }
                        else{
                            $("#id_id_tipo_sangre").append("<option value=" + list[i].id_catalogo + ">" + list[i].descripcion + "</option>");
                        } 
                        
                    }
                }
            },
            error: function (jqXHR, status, error) {//mensaje de error
                alert('Disculpe, existió un problema método CargaProvincia');
            }
        });

}

function CargaEstadoCivil(){
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let idPaciente = document.querySelector('[name=idPaciente]').value;
    
    if(idPaciente=='')
    {
        idPaciente=0        
    }
    $.ajax({//Inicializamos el Ajax que es parte del JQuery
            url: "../../carga_EstadoCivil/",//Url que se encarga de linkear el método que trae la data
            type: "POST",//Tipo POST - para obtener la lista de datos
            dataType: "json",//Dato tipo json - el método que nos trae la data es un JsonResult
            data: {
                idPaciente:idPaciente
            },//Pasar lo parámetros o filtros si es que existiera
            headers: {'X-CSRFToken': csrftoken}, 
            success: function (data) {//Ejecutamos la función para poder cargar la data al select

                if (data.listEstadoCivil == null) {//Validación de datos nulos
                    alert('Disculpe, No hay EstadoCivil que mostrar.');
                    return
                } 
                else 
                {
                    let list= data.listEstadoCivil;
                    let idEstadoCivilSelect= data.id_estadoCivil;
                   
                    for (var i = 0; i < list.length; i++) {//Recorremos y almacenamos la data en el select (SltDepartamento)
                        if (idEstadoCivilSelect==list[i].id_catalogo)
                        {
                            $("#id_id_estado_civil").append("<option value=" + list[i].id_catalogo + " Selected>" + list[i].descripcion + "</option>");
                        }
                        else{
                            $("#id_id_estado_civil").append("<option value=" + list[i].id_catalogo + ">" + list[i].descripcion + "</option>");
                        }                        
                    }
                }
            },
            error: function (jqXHR, status, error) {//mensaje de error
                alert('Disculpe, existió un problema método EstadoCivil');
            }
        });

}

function CargaSexo(){
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let idPaciente = document.querySelector('[name=idPaciente]').value;
    
    if(idPaciente=='')
    {
        idPaciente=0        
    }
    $.ajax({//Inicializamos el Ajax que es parte del JQuery
            url: "../../carga_Sexo/",//Url que se encarga de linkear el método que trae la data
            type: "POST",//Tipo POST - para obtener la lista de datos
            dataType: "json",//Dato tipo json - el método que nos trae la data es un JsonResult
            data: {
                idPaciente:idPaciente
            },//Pasar lo parámetros o filtros si es que existiera
            headers: {'X-CSRFToken': csrftoken}, 
            success: function (data) {//Ejecutamos la función para poder cargar la data al select

                if (data.listSexo == null) {//Validación de datos nulos
                    alert('Disculpe, No hay EstadoCivil que mostrar.');
                    return
                } 
                else 
                {   
                    let list= data.listSexo;
                    let idSexoSelect= data.id_sexo;                
                    for (var i = 0; i < list.length; i++) {//Recorremos y almacenamos la data en el select (SltDepartamento)
                        if (idSexoSelect==list[i].id_catalogo)
                        {
                            $("#id_id_sexo").append("<option value=" + list[i].id_catalogo + " Selected>" + list[i].descripcion + "</option>");
                        }
                        else{
                            $("#id_id_sexo").append("<option value=" + list[i].id_catalogo + ">" + list[i].descripcion + "</option>");
                        }  
                    }
                
                }
            },
            error: function (jqXHR, status, error) {//mensaje de error
                alert('Disculpe, existió un problema método EstadoCivil');
            }
        });

}



function getEdad(dateString) {
    
    let hoy = new Date()
    let fechaNacimiento = new Date(dateString)
    let edad = hoy.getFullYear() - fechaNacimiento.getFullYear()
    let diferenciaMeses = hoy.getMonth() - fechaNacimiento.getMonth()
    if (
      diferenciaMeses < 0 ||
      (diferenciaMeses === 0 && hoy.getDate() < fechaNacimiento.getDate())
    ) {
      edad--
    }
    return edad
  }

function CargaCiudadNac(id_provincia){
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let idPaciente = document.querySelector('[name=idPaciente]').value;
    
    if(idPaciente=='')
    {
        idPaciente=0        
    }
    $.ajax({//Inicializamos el Ajax que es parte del JQuery
            url: "../../carga_CiudadNac/",//Url que se encarga de linkear el método que trae la data
            type: "POST",//Tipo POST - para obtener la lista de datos
            dataType: "json",//Dato tipo json - el método que nos trae la data es un JsonResult
            data: {
                idPaciente:idPaciente
            },//Pasar lo parámetros o filtros si es que existiera
            headers: {'X-CSRFToken': csrftoken}, 
            success: function (data) {//Ejecutamos la función para poder cargar la data al select

                if (data.listCiudadNac == null) {//Validación de datos nulos
                    alert('Disculpe, No hay ciudades que mostrar.');
                    return
                } 
                else 
                {
                    let list= data.listCiudadNac;
                    let idCiudadNacSelect= data.id_ciudadNac; 
                    for (var i = 0; i < list.length; i++) {//Recorremos y almacenamos la data en el select (SltDepartamento)
                        if (idCiudadNacSelect==list[i].id_catalogo)
                        {
                            $("#id_id_ciudad_nacimiento").append("<option value=" + list[i].id_catalogo + " Selected>" + list[i].descripcion + "</option>");
                        }
                        else{
                            $("#id_id_ciudad_nacimiento").append("<option value=" + list[i].id_catalogo + ">" + list[i].descripcion + "</option>");
                        }                                        
                    }
                }
            },
            error: function (jqXHR, status, error) {//mensaje de error
                alert('Disculpe, existió un problema método CargaCiudad');
            }
        });

}

