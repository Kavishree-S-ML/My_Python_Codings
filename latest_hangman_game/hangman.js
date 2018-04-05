
var words = [["hangman","Game you are playing now"], ["kavishree", "Name of the developer"]]
var secret_word;
var hint;
var guess_count =  6;
var guessed_list =[];
var replaced_word, word, word_len;

function start_game() {
    console.log("Game started");
    document.getElementById("home").innerHTML = "";
    createKeyboard();
    createWord();
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
            };
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
function check_letter(btn) {
    var guessed_letter;
    var hint;
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
        }
        if (guess_count === 3) {
            console.log("create hint button")
            console.log(guess_count)
            hint_opt = document.getElementById("hint");
            console.log(hint_opt)
            hint_opt[0].style.display='block';
            //get_hint(hint_opt)
        }
        if (!(guess_value) && guess_count<0) {
            document.getElementById("lost").style.visibility = "visible";
            //game_end()
        }
        if (replaced_word.length === 0) {
            console.log("win")
            document.getElementById("win").style.visibility = "visible";
            //game_end()
        }
    }
}
function get_hint() {
    if (guess_count === 3) {
        //alert(secret_word[1])
        console.log(document.getElementsById("hint"))
        document.getElementsById("hint").style = "display: block"
    }
}
function game_end(){
    reset();
    start_game();
}
function reset() {
    document.getElementById("word").innerHTML = ""
    document.getElementById("keyboard").innerHTML = "";
    guess_count = 6;
    guesses =[];
    guess_value = false;
    replaced_word = "";

}
