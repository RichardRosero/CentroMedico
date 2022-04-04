$(document).ready(function() {
    CargaDoctores();
    console.log( "form ready!" );
   
   
});
function CargaHoras(fecha){

    
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let idPaciente = document.querySelector('[name=idPaciente]').value;
     
    
    if(idPaciente=='')
    {
        idPaciente=0        
    }

        let id_doctor =$('select[name=id_doctor]').val();
        if (id_doctor == null)
            id_doctor=0
        console.log(id_doctor);
        $.ajax({//Inicializamos el Ajax que es parte del JQuery
            url: "../../carga_horas/",//Url que se encarga de linkear el método que trae la data
            type: "POST",//Tipo POST - para obtener la lista de datos
            dataType: "json",//Dato tipo json - el método que nos trae la data es un JsonResult
            data: {
                idPaciente:idPaciente,
                fecha:fecha,
                id_doctor:id_doctor

            },//Pasar lo parámetros o filtros si es que existiera
            headers: {'X-CSRFToken': csrftoken}, 
            success: function (data) {//Ejecutamos la función para poder cargar la data al select

                if (data.listHoras == null) {//Validación de datos nulos
                    alert('Disculpe, No hay horas que mostrar.');
                    return
                } 
                else 
                {
                    let list= data.listHoras;
                    $('#id_hora').empty().append('');
                    for (var i = 0; i < list.length; i++) {//Recorremos y almacenamos la data en el select (SltDepartamento)
                        //if (idCiudadNacSelect==list[i].id_catalogo)
                       // {
                            $("#id_hora").append("<option value=" + list[i].id_catalogo + ">" + list[i].descripcion + "</option>");
                        //}
                       // else{
                       //     $("#id_id_ciudad_nacimiento").append("<option value=" + list[i].id_catalogo + ">" + list[i].descripcion + "</option>");
                       // }                                        
                    }
                }
            },
            error: function (jqXHR, status, error) {//mensaje de error
                alert('Disculpe, existió un problema método CargaHoras');
            }
        });
        
}

function CargaDoctores(){

    
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let idPaciente = document.querySelector('[name=idPaciente]').value;
     
    
    if(idPaciente=='')
    {
        idPaciente=0        
    }
   
        $.ajax({//Inicializamos el Ajax que es parte del JQuery
            url: "../../carga_doctor/",//Url que se encarga de linkear el método que trae la data
            type: "POST",//Tipo POST - para obtener la lista de datos
            dataType: "json",//Dato tipo json - el método que nos trae la data es un JsonResult
            data: {
                
            },//Pasar lo parámetros o filtros si es que existiera
            headers: {'X-CSRFToken': csrftoken}, 
            success: function (data) {//Ejecutamos la función para poder cargar la data al select

                if (data.listDoctor == null) {//Validación de datos nulos
                    alert('Disculpe, No hay doctores que mostrar.');
                    return
                } 
                else 
                {
                    let list= data.listDoctor;
                    //let idCiudadNacSelect= data.id_ciudadNac; 
                    for (var i = 0; i < list.length; i++) {//Recorremos y almacenamos la data en el select (SltDepartamento)
                        //if (idCiudadNacSelect==list[i].id_catalogo)
                       // {
                            $("#id_id_doctor").append("<option value=" + list[i].id_persona + ">" + list[i].nombres + "</option>");
                        //}
                       // else{
                       //     $("#id_id_ciudad_nacimiento").append("<option value=" + list[i].id_catalogo + ">" + list[i].descripcion + "</option>");
                       // }                                        
                    }
                }
            },
            error: function (jqXHR, status, error) {//mensaje de error
                alert('Disculpe, existió un problema método CargaHoras');
            }
        });

    }