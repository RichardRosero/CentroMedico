$(document).ready(function() {
    CargaEstudios();
    console.log( "form ready!" );
   
   
});

function CargaEstudios(){

    
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            
        $.ajax({//Inicializamos el Ajax que es parte del JQuery
            url: "../../carga_estudios/",//Url que se encarga de linkear el método que trae la data
            type: "POST",//Tipo POST - para obtener la lista de datos
            dataType: "json",//Dato tipo json - el método que nos trae la data es un JsonResult
            data: {
                
            },//Pasar lo parámetros o filtros si es que existiera
            headers: {'X-CSRFToken': csrftoken}, 
            success: function (data) {//Ejecutamos la función para poder cargar la data al select

                if (data.listEstudios == null) {//Validación de datos nulos
                    alert('Disculpe, No hay estudios laboratorio que mostrar.');
                    return
                } 
                else 
                {
                    let list= data.listEstudios;
                    //let idCiudadNacSelect= data.id_ciudadNac; 
                    for (var i = 0; i < list.length; i++) {//Recorremos y almacenamos la data en el select (SltDepartamento)
                        //if (idCiudadNacSelect==list[i].id_catalogo)
                       // {
                            $("#id_id_estudio").append("<option value=" + list[i].id_catalogo + ">" + list[i].descripcion + "</option>");
                        //}
                       // else{
                       //     $("#id_id_ciudad_nacimiento").append("<option value=" + list[i].id_catalogo + ">" + list[i].descripcion + "</option>");
                       // }                                        
                    }
                }
            },
            error: function (jqXHR, status, error) {//mensaje de error
                alert('Disculpe, existió un problema método estudios laboratorio');
            }
        });

    }

function CargaMedicina(){

    
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
                
            $.ajax({//Inicializamos el Ajax que es parte del JQuery
                url: "../../carga_medicina/",//Url que se encarga de linkear el método que trae la data
                type: "POST",//Tipo POST - para obtener la lista de datos
                dataType: "json",//Dato tipo json - el método que nos trae la data es un JsonResult
                data: {
                    
                },//Pasar lo parámetros o filtros si es que existiera
                headers: {'X-CSRFToken': csrftoken}, 
                success: function (data) {//Ejecutamos la función para poder cargar la data al select
    
                    if (data.listReceta == null) {//Validación de datos nulos
                        alert('Disculpe, No hay  medicina que mostrar.');
                        return
                    } 
                    else 
                    {
                        let list= data.listReceta;
                        //let idCiudadNacSelect= data.id_ciudadNac; 
                        for (var i = 0; i < list.length; i++) {//Recorremos y almacenamos la data en el select (SltDepartamento)
                            //if (idCiudadNacSelect==list[i].id_catalogo)
                           // {
                                $("#id_id_medicamento").append("<option value=" + list[i].id_catalogo + ">" + list[i].descripcion + "</option>");
                            //}
                           // else{
                           //     $("#id_id_ciudad_nacimiento").append("<option value=" + list[i].id_catalogo + ">" + list[i].descripcion + "</option>");
                           // }                                        
                        }
                    }
                },
                error: function (jqXHR, status, error) {//mensaje de error
                    alert('Disculpe, existió un problema método  receta');
                }
            });
    

            
        }

    function Send()
    {
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        let idPaciente = document.querySelector('[name=idPaciente]').value;  
        let idconsulta = document.querySelector('[name=idconsulta]').value;  
        let tipoCorreo = document.querySelector('[name=tipoCorreo]').value;  
        console.log(idPaciente)      
        console.log(idconsulta)    
            $.ajax({//Inicializamos el Ajax que es parte del JQuery
                url: "../../send/",//Url que se encarga de linkear el método que trae la data
                type: "POST",//Tipo POST - para obtener la lista de datos
                dataType: "json",//Dato tipo json - el método que nos trae la data es un JsonResult
                data: {
                    idPaciente:idPaciente,
                    idconsulta:idconsulta,
                    tipoCorreo:tipoCorreo
                    
                },//Pasar lo parámetros o filtros si es que existiera
                headers: {'X-CSRFToken': csrftoken}, 
                success: function () {//Ejecutamos la función para poder cargar la data al select
                    console.log("success")
                    var url = $("#Url").attr("data-url");            
                    setTimeout( window.location.href = url, 5000);
                },
                error: function (jqXHR, status, error) {//mensaje de error
                    alert('Disculpe, existió un problema método  receta');
                }
            });

    }