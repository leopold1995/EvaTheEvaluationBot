let userSound = new Audio('/static/userSend.mp3');
let botSound = new Audio('/static/botSend.mp3');

let responseDelay = 1500; //ms
let questions = 8;
let questionCounter = 0;
let IDKcounter = 0;

let evaluationAnswers = [];
let evaluationRunning = false;

let feedbackFinished = false;

// triggered when document is ready
$(document).ready(function () {
    initialize();
});

// initialize bot
function initialize() {
    console.log("Init Eva bot");
    getFirstResponse();
}

// play user sound
function playUserSound() {
    // console.log("playUserSound()");
    let promise = userSound.play();
    promise.catch((error) => {
        // console.error(error);
    });
}

// play bot sound
function playBotSound() {
    // console.log("playBotSound()");
    let promise = botSound.play();
    promise.catch((error) => {
        // console.error(error);
    });
}

// get current date
function getDate() {
    let date = new Date($.now());
    let year = date.getUTCFullYear();
    let month = date.getUTCMonth() + 1;
    let day = date.getUTCDate();
    let dateString = year + "-" + ((month < 10) ? "0" : "") + month + "-" + ((day < 10) ? "0" : "") + day;
    return dateString;
}

// get current time
function getTime() {
    let date = new Date($.now());
    let hours = date.getHours();
    let minutes = date.getMinutes();
    let time = hours + ":" + ((minutes < 10) ? "0" : "") + minutes;
    return time;
}

// load intro message
function getFirstResponse() {
    addBotMessage(getResponse("Introduction"));
}

// handle suggestion click
function chatSuggest(text) {
    $(".chatSuggest").prop('disabled', true);

    $("#textInput").val(text);
    submitMessage();
}

// add bot message to history
function addBotMessage(text) {
    let botHtml = '<div class="message"><div class="message-botname">Eva</div><div class="botText"><div class="avatar-wrapper"><img class="avatar" src="/static/Eva.png"></div><div class="data-wrapper">' + text + '</div></div><div class="message-time">' + getTime() + '</div></div>';
    $("#chatbox").append(botHtml);

    playBotSound();
    scrollDown();

    $("#buttonSkip").prop('disabled', false);
    $("#buttonInput").prop('disabled', false);
    $("#textInput").prop('disabled', false);
    $("#textInput").focus();

    if (questionCounter == 8) {
        enableFeedbackSkipButton(); // if user already gave feedback
    }

    console.log("add bot message");
}

// add user message to history
function addUserMessage(text) {
    let userHtml = '<div class="message"><p class="userText">' + text + '</p></div>';
    $("#chatbox").append(userHtml);
}

const TRY_AGAIN = "Try again";
const SKIP_QUESTION = "Please skip this.";
const CANNOT_SKIP = "I cannot skip"
const CANNOT_DO = "I cannot do that";
const MORE_DETAILS = "More details";
const IDK_REPLY = "I didn't understand";
const GOOGLE_RESULT = "Show google result";

const START_EVALUATION = "";
const QUESTION_1 = "Course structure"; // 1-5
const QUESTION_2 = "Course lecturer"; // 1-5
const QUESTION_3 = "Media and methods"; // 1-5
const QUESTION_4 = "Written feedback"; // text
const QUESTION_5 = "Course improvement"; // text
const QUESTION_6 = "Further comments"; // text
const QUESTION_7 = "Provide email"; // email regex
const QUESTION_8 = "Give feedback"; // feedback form
const FINISH_EVALUATION = "Finish evaluation";


// response logic
function getBotResponse(text) {
    text = text.toLowerCase(); // convert input text to lowercase
    // console.log("getBotResponse( '" + text + "' )");
    console.log("Question counter: " + questionCounter);

    // restart evaluation
    if (text.includes("restart")) {
        evaluationRunning = false;
        evaluationAnswers = [];
        questionCounter = 0;
        $("#answers #answer-list").empty();
        addBotMessage(getResponse("Introduction"));
        return;
    }

    // start evaluation
    if (text.includes("start") && text.includes("evaluation")) {
        if (!evaluationRunning) {
            evaluationRunning = true;
            evaluationAnswers.push(getDate() + " " + getTime());
            addBotMessage(getResponse(QUESTION_1));
            questionCounter++;
            return;
        } else {
            addBotMessage(getResponse(CANNOT_DO));
            return;
        }
    }

    // skip evaluation question
    if (text.includes("skip")) {
        console.log("skip question " + questionCounter);
        if (evaluationRunning && questionCounter < questions) {
            questionCounter++;

            evaluationAnswers.push(SKIP_QUESTION);
            addBotMessage(getResponse(eval("QUESTION_" + questionCounter)));
            
            return;
        } else {
            addBotMessage(getResponse(CANNOT_SKIP));
            return;
        }
    }

    // continue evaluation after interrupt/smalltalk
    if (text.includes("continue")) {
        if (evaluationRunning) {
            if (questionCounter < questions) {
                addBotMessage(getResponse(eval("QUESTION_" + questionCounter)));
            } else {
                evaluationRunning = false;
                addBotMessage(getResponse(FINISH_EVALUATION));
                submitEvaluationResult();
            }
            return;
        } else {
            addBotMessage(getResponse(CANNOT_DO));
            return;
        }
    }

    // if evaluation is running
    if (evaluationRunning) {
        if (questionCounter >= 1 && questionCounter <= 3) { // question 1-3
            if (/[1-5]/.test(text)) {
                evaluationAnswers.push(text);
                questionCounter++;
                addBotMessage(getResponse(eval("QUESTION_" + questionCounter)));
                return;
            } else if (getResponse(text) != "IDKresponse") {
                addBotMessage(getSmalltalkResponse(text));
                return;
            } else {
                addBotMessage(getResponse(TRY_AGAIN));
                return;
            }
        } else if (questionCounter >= 4 && questionCounter <= 6) { // question 4-6
            if (/\b(lectur|organiz|course|eva|feedback|well|nice|good|ok|satisf|benefit|bad|unclear|love|like|enjoy|hate|bad|worse|should|would|shall|include|contain|interest|quite|miss|need|require|expect|strength)/i.test(text) || text.match(/\S+/g).length >= 5) {
                evaluationAnswers.push(text);
                questionCounter++;
                addBotMessage(getResponse(eval("QUESTION_" + questionCounter)));
                return;
            } else if (getResponse(text) != "IDKresponse") {
                addBotMessage(getSmalltalkResponse(text));
                return;
            } else {
                addBotMessage(getResponse(MORE_DETAILS));
                return;
            }
        } else if (questionCounter == 7) { // question 7
            if (/\S+@\S+\.\S+/.test(text)) {
                questionCounter++;
                submitEmail(text);
                addBotMessage(getResponse(eval("QUESTION_" + questionCounter)));
                return;
            } else if (getResponse(text) != "IDKresponse") {
                addBotMessage(getSmalltalkResponse(text));
                return;
            }  else {
                addBotMessage(getResponse(TRY_AGAIN));
                return;
            }
        } else if (questionCounter == 8) { // question 8
            questionCounter++;
            evaluationRunning = false;
            addBotMessage(getResponse(FINISH_EVALUATION));
            submitEvaluationResult();
            return;
        }
    }

    addBotMessage(getSmalltalkResponse(text));    
}

// get response from python chatterbot backend
function getResponse(text) {

    console.log("getResponse( '" + text + "' )");

    let botReply = null;

    $.ajax({
        url: "/getResponse?msg=" + text,
        method: "GET",
        async: false
    }).done(function (data) {
        botReply = data.botReply;
    });

    setProgress(questionCounter / questions);

    return botReply;
}

function getSmalltalkResponse(text) {

    if (/\b(joke|wit|gag)/i.test(text)) { // tell joke
        text = "Tell me a joke";
    }

    let response = getResponse(text);
    // interrupt/smalltalk
    if (evaluationRunning) {
        response += "<p> Can we go back to the evaluation? </p> <button class=\"chatSuggest\" onclick=\"chatSuggest('Continue');\">Let's follow up!</button>";
    }
    return response;
}

function getIDKResponse() {
    IDKcounter++; // count IDK
    if (IDKcounter < 3) {
        botReply = getResponse(IDK_REPLY);
    } else { // reply with google suggestion after 3 attempts
        botReply = getResponse(GOOGLE_RESULT);
    }
    return botReply;
}

// submit email to backend
function submitEmail(email) {
    $.post("/email", {
        email: email
    }).done(function (data) {
        console.log(data);
    });
}

// submit evaluation result to backend
function submitEvaluationResult() {
    if (evaluationAnswers && evaluationAnswers != []) {
        let answers = [];
        for (let i = 1; i <= 6; i++) {
            let answer = eval("QUESTION_" + i) + ": " + evaluationAnswers[i];
            $("#answers #answer-list").append("<p>" + answer + "</p>");
        }

        $.post("/result", {
            datetime: evaluationAnswers[0],
            answer1: evaluationAnswers[1],
            answer2: evaluationAnswers[2],
            answer3: evaluationAnswers[3],
            answer4: evaluationAnswers[4],
            answer5: evaluationAnswers[5],
            answer6: evaluationAnswers[6]
        }).done(function (data) {
            console.log(data);
            Swal.fire({
                title: 'Finished!',
                text: 'Thank you for participating! 🤩',
                icon: 'success',
                confirmButtonText: 'Continue',
                confirmButtonColor: '#00762C'
            })
        });
    }
}

// handle chat skip button click
$("#buttonSkip").click(function () {
    skip();
});

// handle chat enter keypress
$("#textInput").keypress(function (e) {
    if (e.which == 13) {
        submitMessage();
    }
});

// handle chat send button click
$("#buttonInput").click(function () {
    submitMessage();
});

// skip question
function skip() {
    $("#textInput").val(SKIP_QUESTION);
    submitMessage();
}

// submit message
function submitMessage() {
    text = $("#textInput").val();
    if (text.trim() == "") {
        return;
    }
    $("#textInput").val("");

    playUserSound();
    $("#buttonSkip").prop('disabled', true);
    $("#buttonInput").prop('disabled', true);
    $("#textInput").prop('disabled', true);

    addUserMessage(text);
    setTimeout(() => {
        getBotResponse(text);
    }, responseDelay);

    scrollDown();
}

// scroll down to last message in history
function scrollDown() {
    $("#scrollbox").animate({ scrollTop: $(".messagecontainer").height() }, 'slow');
}

// set progress bar in evaluation
function setProgress(progress) {
    if (progress > 1) progress = 1;
    let percentage = Math.floor(progress * 100);
    let progressbar = $("#progress");
    progressbar.width(percentage + "%");
    progressbar.text(percentage + "%");
}

// handle privacy show click
$("#show-privacy-button").click(function () {
    showPrivacy();
});

// handle privacy accept button
$("#privacy-accept").click(function () {
    hidePrivacy(); 
    chatSuggest('I have read the declaration of consent and accept it.')
});

// show privacy window
function showPrivacy() {
    $("#open-feedback-button").hide();
    $("#feedback").hide();
    $("#scrollbox").hide();
    $('#userInput').hide();

    $("#privacy").show();
}

// hide privacy window
function hidePrivacy() {
    $("#privacy").hide();

    $("#open-feedback-button").show();
    $("#scrollbox").show();
    $('#userInput').show();
}

// handle show feedback button click
$("#open-feedback-button").click(function () {
    showCloseFeedbackButton();
    showFeedback();
});

$("#close-feedback-button").click(() => {
    showOpenFeedbackButton();
    hideFeedback();
});

function showOpenFeedbackButton() {
    $("#open-feedback-button").show();
    $("#close-feedback-button").hide();
} 

function showCloseFeedbackButton() {
    $("#open-feedback-button").hide();
    $("#close-feedback-button").show();
}

// show feedback window
function showFeedback() {
    $("#scrollbox").hide();
    $('#userInput').hide();

    $("#feedback").show();
}

// hide feedback window
function hideFeedback() {
    $("#feedback").hide();

    $("#scrollbox").show();
    $('#userInput').show();

    enableFeedbackButton();

    if (questionCounter == 8) {
        getBotResponse(FINISH_EVALUATION);
    }
}

function enableFeedbackButton() {
    $("#open-feedback-button").prop("disabled", false);
}

function disableFeedbackButton() {
    $("#open-feedback-button").prop("disabled", true);
}

function enableFeedbackSkipButton() {
    console.log("enable skip button");
    if (feedbackFinished) {
        $("#feedback-skip-button").prop("disabled", false);
    }
}

function skipFeedback() {
    addUserMessage(SKIP_QUESTION);
    hideFeedback();
}

// handle hide answers button click
$("#answers-hide").click(function () {
    hideAnswers();
});

// show answers window
function showAnswers() {
    $("#open-feedback-button").hide();
    $("#scrollbox").hide();
    $('#userInput').hide();

    $("#answers").show();
}

// hide answers window
function hideAnswers() {
    $("#answers").hide();

    $("#open-feedback-button").show();
    $("#scrollbox").show();
    $('#userInput').show();
}

// show answers window
function showHelp() {
    $("#open-feedback-button").hide();
    $("#scrollbox").hide();
    $('#userInput').hide();

    $("#help").show();
}

// hide answers window
function hideHelp() {
    $("#help").hide();

    $("#open-feedback-button").show();
    $("#scrollbox").show();
    $('#userInput').show();
}

// handle feedback submit
$("#feedback-form").submit(e => {
    e.preventDefault();
    e.stopPropagation();

    if (validateFeedback()) {
        submitFeedback();
        hideFeedback();
        feedbackFinished = true;
    } else {
        Swal.fire({
            title: 'Wait a second!',
            text: 'Please fill in all fields and provide some useful text 😅',
            icon: 'warning',
            confirmButtonText: 'Ok',
            confirmButtonColor: '#00762C'
        })
    }
});

// handle feedback form reset
$("#feedback-form").on('reset', function (event) {
    hideFeedback();
});

// validate feedback fields
function validateFeedback() {
    let feedbackRating = $('input[name="feedback-rating"]:checked').val();
    let feedbackUx = $('input[name="feedback-ux"]:checked').val();
    let feedbackText = $("#feedback-text").val();
    if (feedbackRating && feedbackUx && feedbackText && (/\b(lectur|organiz|course|eva|feedback|well|nice|good|ok|satisf|benefit|bad|unclear|love|like|enjoy|hate|bad|worse|should|would|shall|include|contain|interest|quite|miss|need|require|expect|strength)/i.test(feedbackText) || feedbackText.match(/\S+/g).length >= 7)) {
        return true;
    }
    return false;
}

// submit feedback to backend
function submitFeedback() {
    let feedbackRating = $('input[name="feedback-rating"]:checked').val();
    let feedbackUx = $('input[name="feedback-ux"]:checked').val();
    let feedbackText = $("#feedback-text").val();
    let feedbackImprovement = $("#feedback-improve").val();
    $.post("/feedback", {
        rating: feedbackRating, 
        ux: feedbackUx, 
        text: feedbackText,
        improve: feedbackImprovement
    }).done((data) => {
        console.log(data);
        Swal.fire({
            title: 'Done!',
            text: 'Thank you for submitting feedback! 🤩',
            icon: 'success',
            confirmButtonText: 'Continue',
            confirmButtonColor: '#00762C'
        })
    });
    $("#feedback-form").trigger("reset");
}