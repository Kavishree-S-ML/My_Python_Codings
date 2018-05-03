
var words = [["hangman","Game you are playing now"], ["kavishree", "Name of the developer"]]
var secret_word;
var hint;
var guess_count =  6;
var guessed_list =[];
var replaced_word, word, word_len;
var c;
var ctx;

function start_game() {
    console.log("Game started");
    document.getElementById("home").innerHTML = "";
    createKeyboard();
    createWord();
    createHangmanImg();
}
function createKeyboard() {
    var keys;

    for (var i=65; i<=90; i++) {
        var char = String.fromCharCode(i);
        keys = document.createElement("button");
        keys.setAttribute("class", "letters");
        keys.setAttribute("id", "l"+i);
        keys.innerText = char;
        keys.onmouseout = function() {
            if (guessed_list.indexOf(this.innerText) > -1) {
                document.getElementById("popup").style.visibility = "hidden";
            }
        };

        keys.onclick = function() {
            if (guessed_list.indexOf(this.innerText) > -1) {
                document.getElementById("popup").style.visibility = "visible";
            };
            check_letter(this);
            this.style = 'cursor: default'
        };
        document.getElementById("keyboard").appendChild(keys)
    }
}
function createWord() {
    var text_box;
    secret_word = words[Math.floor(Math.random() * words.length)];
    word = secret_word[0].toUpperCase();
    word_len = secret_word[0].length;
    replaced_word = secret_word[0].toUpperCase();
    console.log(secret_word)
    for (var i=0; i<secret_word[0].length; i++) {
        text_box = document.createElement("input");
        text_box.setAttribute("class", "secret_word");
        text_box.setAttribute("maxlength", 1);
        text_box.setAttribute("value", "_")
        text_box.id = "l"+i;
        document.getElementById("word").appendChild(text_box)
    }
}
function createHangmanImg() {
    canvas();
    draw(10,10,240,10);
    draw(30,10,30,150);
    draw(30,120,60,150);
    draw(30,50,60,10);
    draw(140,10,140,30);
    document.getElementById("myCanvas").style.visibility = "visible";
}
function check_letter(btn) {
    var guessed_letter;
    guessed_letter = btn.innerText;
    var guess_value = false;
    if (guessed_list.indexOf(guessed_letter) === -1) {
        guessed_list.push(guessed_letter);
        for (var c = 0; c < word_len; c++) {
            if (guessed_letter === word[c]) {
                document.getElementById("l" + c).value = secret_word[0][c];
                replaced_word = replaced_word.replace(guessed_letter, '');
                guess_value = true;
            }
        }
        if (! guess_value) {
            guess_count -= 1;
            hangman_img(guess_count);
        }
        if (guess_count === 3) {
            hint = document.getElementsByClassName("hint")[0];
            hint.style.visibility = "visible";
            get_hint();
        }
        if (!(guess_value) && guess_count<=0) {
            document.getElementById("lost").style.visibility = "visible";
            //game_end()
        }
        if (replaced_word.length === 0) {
            document.getElementById("win").style.visibility = "visible";
            //game_end()
        }
    }
}
function get_hint(){
        var hint_value = document.getElementsByClassName("hint_value")[0]
        hint_value.innerText = "Hint: " + secret_word[1]
        hint.onclick = function() {
            hint_value.style.visibility = "visible";
        }
        hint.onmouseout = function() {
            hint_value.style.visibility = "hidden";
        }
}
function canvas() {
    c = document.getElementById("myCanvas");
    ctx = c.getContext("2d");
    //Begin a path, move to position . Create a line to position(x,y)
    ctx.beginPath();
    ctx.strokeStyle = "black";
    ctx.lineWidth = 2;
}

head = function() {
    c = document.getElementById("myCanvas");
    ctx = c.getContext("2d");
    //Begin a path, move to position . Create a line to position(x,y)
    ctx.beginPath();
    ctx.arc(140,40,10,0,2*Math.PI);
    ctx.strokeStyle = "black";
    ctx.lineWidth = 2;
    ctx.stroke();
}
function draw(mx, my, tx, ty) {
    ctx.moveTo(mx,my);
    ctx.lineTo(tx,ty);
    ctx.stroke();
}
body = function() {
    draw(140,50,140,90)
}
leftArm = function(){
    draw(140,50,120,70)
}
rightArm = function () {
    draw(140,50,160,70)
}
leftLeg = function () {
    draw(140,90,120,110)
}
rightLeg = function () {
    draw(140,90,160,110)
}

function hangman_img(guess_count){
    canvas();
    switch(guess_count) {
        case 5:
            head();
            break;
        case 4:
            body();
            break;
        case 3:
            leftArm();
            break;
        case 2:
            rightArm();
            break;
        case 1:
            leftLeg();
            break;
        case 0:
            rightLeg();
            break;
        default:
            console.log("Died...!!!");
    }
}
function game_restart(){
    reset();
    start_game();
}
function reset() {
    document.getElementById("word").innerHTML = "";
    document.getElementById("keyboard").innerHTML = "";
    document.getElementById("lost").style.visibility = "hidden";
    document.getElementById("win").style.visibility = "hidden";
    document.getElementById("lost").innerHTML = "";
    document.getElementById("win").innerHTML = "";
    guess_count = 6;
    guesses = [];
    guess_value = false;
    replaced_word = "";
}
