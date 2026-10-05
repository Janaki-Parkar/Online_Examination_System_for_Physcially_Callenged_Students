let currentQuestion = 0;

let questionBoxes = [];

let totalQuestions = 0;

let answersLocked = {};

function initializeExam(){

    questionBoxes =
    document.querySelectorAll(".question-box");

    totalQuestions =
    questionBoxes.length;

    questionBoxes.forEach(function(box){

        box.classList.remove("active");

    });

    if(totalQuestions>0){

        questionBoxes[0].classList.add("active");

    }

    updateProgress();

}

function updateProgress(){

    document.getElementById("currentQuestion").innerHTML =
    currentQuestion + 1;

}

function chooseOption(option){

    let radio = questionBoxes[currentQuestion]
    .querySelector(
        "input[value='"+option+"']"
    );

    if(radio){

        radio.checked = true;

        speak(
            "Option " +
            option +
            " selected."
        );

    }

}

function lockAnswer(){

    let radios =
    questionBoxes[currentQuestion]
    .querySelectorAll(
        "input[type='radio']"
    );

    let selected = false;

    radios.forEach(function(radio){

        if(radio.checked){

            selected = true;

        }

    });

    if(!selected){

        speak(
            "Please select an option first."
        );

        return false;

    }

    answersLocked[currentQuestion] = true;

    questionBoxes[currentQuestion]
    .classList.add("locked");

    speak(
        "Answer locked successfully."
    );

    return true;

}

function nextQuestion(){

    if(currentQuestion >= totalQuestions-1){

        speak(
            "You are already on the last question."
        );

        return;

    }

    if(!answersLocked[currentQuestion]){

        speak(
            "Please lock your answer before moving to the next question."
        );

        return;

    }

    questionBoxes[currentQuestion]
    .classList.remove("active");

    currentQuestion++;

    questionBoxes[currentQuestion]
    .classList.add("active");

    updateProgress();

    readCurrentQuestion();

}

function previousQuestion(){

    if(currentQuestion==0){

        speak(
            "You are already on the first question."
        );

        return;

    }

    questionBoxes[currentQuestion]
    .classList.remove("active");

    currentQuestion--;

    questionBoxes[currentQuestion]
    .classList.add("active");

    updateProgress();

    readCurrentQuestion();

}

function readCurrentQuestion(){

    let text =
    questionBoxes[currentQuestion]
    .innerText;

    speak(text);

}

function readOptions(){

    let labels =
    questionBoxes[currentQuestion]
    .querySelectorAll("label");

    let text = "";

    labels.forEach(function(label){

        text +=
        label.innerText +
        ". ";

    });

    speak(text);

}

function submitExam(){

    document.getElementById("examForm").submit();

}

function updateVoiceStatus(message){

    document.getElementById("voiceStatus").innerHTML =
    message;

}