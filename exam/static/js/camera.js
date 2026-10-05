let video;

let canvas;

let context;

let monitoringStarted = false;

async function startCamera(){

    video = document.getElementById("video");

    canvas = document.getElementById("canvas");

    context = canvas.getContext("2d");

    try{

        const stream =
        await navigator.mediaDevices.getUserMedia({

            video:true,

            audio:false

        });

        video.srcObject = stream;

        await video.play();

        document.getElementById("cameraStatus").innerHTML =
        "Camera Active";

        if(!monitoringStarted){

            monitoringStarted = true;

            setInterval(sendFrame,1000);

        }

    }

    catch(error){

        console.error(error);

        document.getElementById("cameraStatus").innerHTML =
        "Camera Error : " + error.name;

    }

}

function sendFrame(){

    if(!video.srcObject){

        return;

    }

    if(video.readyState !== 4){

        return;

    }

    canvas.width = video.videoWidth;

    canvas.height = video.videoHeight;

    context.drawImage(

        video,

        0,

        0,

        canvas.width,

        canvas.height

    );

    let image = canvas.toDataURL("image/jpeg");

    fetch("/camera_frame",{

        method:"POST",

        headers:{

            "Content-Type":"application/json"

        },

        body:JSON.stringify({

            image:image

        })

    })

    .then(response=>response.json())

    .then(data=>{

        document.getElementById("cameraStatus").innerHTML =

        "Status : " +

        data.status +

        "<br>Warnings : " +

        data.warnings;

        const monitor =
        document.getElementById("monitorStatus");

        if(monitor){

            monitor.innerHTML =

            "Monitoring : " +

            data.status;

        }

        if(data.suspicious){

            speak(

                "Warning. " +

                data.status

            );

        }

    })

    .catch(error=>{

        console.log(error);

    });

}