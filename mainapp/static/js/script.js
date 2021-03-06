let video = document.getElementById("video")
let model;
let canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");


const setupCamara = () => {
    navigator.mediaDevices
    .getUserMedia({
        video: { width:350, height:350 },
        audio: false,
    })
    .then((stream) => {
        video.srcObject = stream;
    });

};
const detectFaces = async () => {
    const prediction = await model.estimateFaces(video, false)

    ctx.drawImage(video, 0 , 0 , 400 , 400);
    prediction.forEach((pred) => {
        ctx.beginPath();
        ctx.lineWidth = "4";
        ctx.strokeStyle = "blue";
        ctx.rect(
            pred.topLeft[0],
            pred.topLeft[1],
            pred.bottomRight[0] -  pred.topLeft[0],
            pred.bottomRight[1] -  pred.topLeft[1],
        );
        //ctx.stroke();
        /*ctx.fillStyle="red";
        pred.landmarks.forEach((landmark) => {
            ctx.fillRect(landmark[0], landmark[1],5,5);
        });*/
        appendFileAndSubmit();
    });
    
};
setupCamara();

video.addEventListener("loadeddata", async () => {
    model = await blazeface.load();
    detectFaces();
    
});


  function restauraImagen(){
      const datosCanvas =document.getElementById("canvas").toDataURL();
      console.log(datosCanvas)
      document.getElementById("canvasImgsite").src= datosCanvas;
      

  }


    function b64toBlob(b64Data, contentType, sliceSize) {
        contentType = contentType || '';
        sliceSize = sliceSize || 512;

        var byteCharacters = atob(b64Data);
        var byteArrays = [];

        for (var offset = 0; offset < byteCharacters.length; offset += sliceSize) {
            var slice = byteCharacters.slice(offset, offset + sliceSize);

            var byteNumbers = new Array(slice.length);
            for (var i = 0; i < slice.length; i++) {
                byteNumbers[i] = slice.charCodeAt(i);
            }

            var byteArray = new Uint8Array(byteNumbers);

            byteArrays.push(byteArray);
        }

      var blob = new Blob(byteArrays, {type: contentType});
      return blob;
    }

    function appendFileAndSubmit(){
        // Obtener formulario
        //csrftoken = document.getElementsByName('csrfmiddlewaretoken').value;
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        let idPaciente = document.querySelector('[name=idPaciente]').value;       
        ImageURL = document.getElementById("canvas").toDataURL();
        

        
        // Enviar informaci??n y subir archivo
        $.ajax({
            url:"../../subir_foto/",
            // La clase FormData est?? disponible en todos los exploradores modernos
            data: { 
                    image : ImageURL,
                    idPaciente: idPaciente
            },
            type:"POST",                    
            dataType:"json",
            async:true,
            headers: {'X-CSRFToken': csrftoken},            
            error:function(err){
                console.error(err);
            },
            success:function(fun){
                console.log(fun);
                var url = $("#Url").attr("data-url");
                window.location.href = url;

            },
            complete:function(){
                console.log("Solicitud finalizada");
            }
        });
    }