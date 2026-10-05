const SpeechRecognition =
window.SpeechRecognition ||
window.webkitSpeechRecognition;

const recognition = new SpeechRecognition();

recognition.continuous = true;

recognition.interimResults = false;

recognition.lang = "en-US";

let waitingForSubmit = false;

function speak(text){

    updateVoiceStatus(text);

    window.speechSynthesis.cancel();

    const speech =
    new SpeechSynthesisUtterance(text);

    speech.rate = 1;

    speech.pitch = 1;

    speech.volume = 1;

    speech.lang = "en-US";

    window.speechSynthesis.speak(speech);

}

function greetStudent(name){

    speak(

    "Welcome " + name +

    ". Voice assistance is enabled successfully. " +

    "Say Start Exam whenever you are ready."

    );

}

function startVoice(){

    recognition.start();

}

recognition.onresult=function(event){

    let command=

    event.results[event.results.length-1][0]

    .transcript

    .toLowerCase()

    .trim();

    console.log(command);

    handleCommand(command);

};

recognition.onerror=function(){

    recognition.start();

};

recognition.onend=function(){

    recognition.start();

};

function handleCommand(command){

    updateVoiceStatus(

    "Command : " + command

    );

    if(command.includes("start exam")){

    speak("Starting examination.");

    setTimeout(function(){

        window.location.href="/exam";

    },1500);

    }
    else if(command.includes("option a")){

        chooseOption("A");

    }

    else if(command.includes("option b")){

        chooseOption("B");

    }

    else if(command.includes("option c")){

        chooseOption("C");

    }

    else if(command.includes("option d")){

        chooseOption("D");

    }

    else if(command.includes("lock answer")){

        lockAnswer();

    }

    else if(command.includes("next question")){

        nextQuestion();

    }

    else if(command.includes("previous question")){

        previousQuestion();

    }

    else if(command.includes("repeat question")){

        readCurrentQuestion();

    }

    else if(command.includes("read options")){

        readOptions();

    }

    else if(command.includes("submit exam")){

        waitingForSubmit=true;

        speak(

        "Are you sure you want to submit your examination? Say Yes or No."

        );

    }

    else if(waitingForSubmit && command.includes("yes")){

        speak(

        "Submitting your examination."

        );

        submitExam();

    }

    else if(waitingForSubmit && command.includes("no")){

        waitingForSubmit=false;

        speak(

        "Submission cancelled."

        );

    }

    else if(command.includes("help")){

        speak(

        "Available commands are. Start Exam. Option A. Option B. Option C. Option D. Lock Answer. Next Question. Previous Question. Repeat Question. Read Options. Submit Exam."

        );

    }

}