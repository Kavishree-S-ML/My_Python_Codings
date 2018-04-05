
var words = [["hangman","Game you are playing now"], ["kavishree", "Name of the developer"]]
var secret_word;
var hint;
var guess_count =  6;
var guesses =[];
var guess_value = false;
var replaced_word;

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
        keys.innerText = char;
        keys.onclick = function() {
           check_letter(this);
           this.disabled = true
           this.style = 'cursor: default'
        };
        document.getElementById("keyboard").appendChild(keys)
    }
}
function createWord() {
    var text_box;
    secret_word = words[Math.floor(Math.random() * words.length)];
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
    var letter;
    var hint;
    guessed_letter = btn.innerText;
    if (guesses.indexOf(guessed_letter) > -1) {
        //alert("Letter is already guessed...!!! Please guess some other letter")
        console.log(document.getElementsByClassName("modal"))
        document.getElementsByClassName("modal")[0].style.display = "block";
    }else
    {
        guesses.push(guessed_letter);
        for (var c = 0; c < secret_word[0].length; c++) {
            letter = secret_word[0][c].toUpperCase();
            if (guessed_letter === letter) {
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
            /*hint_opt = document.createElement("hint");
            hint_opt.setAttribute("type","button"); */
            hint_opt = document.getElementById("hint");
            console.log(hint_opt)
            hint_opt[0].style.display='block';
            //get_hint(hint_opt)
        }
        if (!(guess_value) && guess_count<0) {
            alert("Sorry...!!! You lost")
            game_end()
        }
        if (replaced_word.length === 0) {
            console.log("win")
            alert("Congratulation...!!! You win")
            game_end()
        }
    }
}
function get_hint() {
    if (guess_count === 3) {
        //alert(secret_word[1])
        console.log(document.getElementsByClassName("hint_value"))
        document.getElementsByClassName("hint_value").style = "display: block"
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
