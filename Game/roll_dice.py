import random


def dice_roll():
    min_val = 1
    max_val = 6
    return random.randint(min_val, max_val)

def player(name, val1, val2):
    if name == "player1":
        val = dice_roll()
        val1 += val
        valA = val
        while valA % 2 == 0:
            valA = dice_roll()

            val1 += valA
    else:
        val = dice_roll()
        val2 += val
        valB = val
        while valB % 2 == 0:
            valB = dice_roll()
            val2 += valB
    return val1, val2

val1 = 0
val2 = 0
valA, valB = player("player1", val1, val2)
j = 1
while (valA <= 100 and valB <= 100):
    i = 1 if j%2 ==0 else 2
    valA, valB = player(("player"+str(i)), valA, valB)
    j += 1

if valA > valB:
    print "Player 1 won the match"
else:
    print "Player 2 won the match"
