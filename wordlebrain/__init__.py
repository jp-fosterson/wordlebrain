"""
wordlebrain -- a python cheat tool for wordle.

wordlebrain is a tool to help you find good guesses for the wordle
word guessing game.  https://www.powerlanguage.co.uk/wordle/

EXAMPLE USAGE

>>> from wordlebrain import *

# input your guesses and wordle's hints
# and it will give you suggestions
#
# Example: (target word "QUERY")
# First two guesses "TRAIN" and "LOUSE"

>>> guess('TRAIN','-+---')
5539 SOREE
5036 BOREE
4857 SHREE
4825 SORRY
4791 DOREE
4711 SERRY
4689 REREE
4638 SOLER
4574 SPREE
4548 SCREE
...and 544 more.

# ... the numbers are a letter-position-frequency score of each word.
# The second parameter encodes Wordle's hints:
    '^' -> Letter in this spot
    '+' -> Letter in word, but in a different spot
    '-' -> Letter not in word




>>> guess('LOUSE','--+-+')
4026 CURER
3896 PURER
3672 PURED
3481 CUBER
3321 BUYER
3299 REBUY
3260 FUMER
3233 FUDER
3232 PUKER
3214 QUEER
...and 22 more.

# Let's try CURER
>>> guess('CURER','-^+++')
3102 QUERY

# QUERY is the only remaining choice.


COMMAND REFERENCE

play():  Run wordlebrain interactively.

guess(word,hint):  Input a guess, hints will add to cumulative
                   constraints on the dictionary.

reset(): Reset all state and start over.

show(limit=N): show the top N highest scoring
               words that fit the constraints
               
showstate():  Show the current set of constraints.

"""
from os import path
import re
from collections import Counter

allwords = []
with open(path.join(path.dirname(__file__),"wordles.txt")) as f:
    for line in f:
        w = line.strip()
        allwords.append(w.upper())
            
def reset():
    """
    Initialize the state of the module.  Run this to start
    over if you start a new puzzle or mess up.
    """
    global _exclude
    global _require
    global _patterns
    global _frequencies
    _exclude = set()
    _require = set()
    _patterns = []
    

def show(limit=None):
    """
    Show all the words that fit the current contstraints.
    """
    scored = [(scoreword(w,get_freqs(words)),w) for w in words]
    scored.sort(reverse=True)
    if len(scored) == 0:
        print("No suggestions.  Did you forget to reset?")
    else:
        for s,w in scored[:limit]:
            print(s,w)
        if limit and limit < len(words):
            print(f"...and {len(words)-limit} more.")
        
def showstate():
    print("== PATTERNS ==")
    for p in _patterns:
        print(p)
    print()
    print(f"EXCLUDE: {_exclude}")
    print(f"REQUIRE: {_require}")

def isok(word):
    for p in _patterns:
        if not p.fullmatch(word):
            return False
    for c in _exclude:
        if c in word:
            return False
    for c in _require:
        if c not in word:
            return False
    return True

def wordle(pattern=None,exclude=None,require=None):
    global words
    global _patterns
    global _exclude
    global _require
    
    if pattern:
        _patterns.append(re.compile(pattern))
    if exclude:
        _exclude.update(exclude)
    if require:
        _require.update(require)
    update()
    
def update():
    global words
    words = [w for w in allwords if isok(w)]
    show(limit=10)

def get_freqs(words):
    result = {}
    for i in range(5):
        result[i] = Counter()
        for w in words:
            result[i][w[i]] += 1
    return result

def scoreword(w,freqs):
    pos_score = sum(freqs[i][c] for i,c in enumerate(w))
    uniq_score = len(set(c for c in w))
    return pos_score * uniq_score
        
USAGE = """
guess(word,hint)

word = a five letter string containing your latest guess
hint = a five character string containing Wordle's hints
       given in response to your guess

hint code: 
    'Y' -> Letter in this spot
    'y' -> Letter in word in different spot
    'n' -> Letter not in word
    
Example:

>>> guess('LOUSE','nnyny')   # U and E are in the word. L, O, and S are not.
>>> guess('BURET','nYyyn')   # U in position 2.  R and E in the word. B and T not.
"""

def guess(word,hint):
    if len(word) != 5:
        print(USAGE)
    elif len(hint) != 5:
        print(USAGE)
    elif any(c not in ".nyY" for c in hint):
        print(USAGE)
    else:
        word = word.upper()
        
        pattern = ''
        require = ''
        temp_exclude = ''

        for letter,code in zip(word,hint):
            if code == 'Y':
                pattern += letter
                require += letter
            elif code == 'y':
                pattern += f'[^{letter}]'
                require += letter
            else:
                pattern += f'[^{letter}]'
                temp_exclude += letter
        wordle(pattern=pattern, require=require, 
               exclude=[c for c in temp_exclude if (c not in _require) and (c not in require)])
        

PLAY_INTRO = """
Welcome to wordlebrain.

Wordlebrain is a suggestion generator 
for the Wordle word game.

Input your guesses like this,

> guess TRAIN nyynY

Hints are n = not in word, y = in word somewhere, 
Y = in word at this spot.  After each guess, 
worldebrain will give suggestions for next guesses,
based on the constraints it's learned.

To start a new game, or start over, type reset.
To quit, type quit or exit
"""

PLAY_USAGE = """
commands:
 > guess <word> <hint> -- give a guess and the resulting 
                          hints e.g. "guess TRAIN nyynY")
 > reset               -- reset the game state to start over
 > exit or quit        -- quit the progam
 > show [N]            -- show [up to N] suggestions
 > showstate           -- show wordlebrain's internal state 
                          (for curious geeks)
"""
RECOMMEND = "New game.  Wordlebrain recommends starting with CARES."
def play():
    print(PLAY_INTRO)
    print(PLAY_USAGE)
    print(RECOMMEND)
    while(True):
        try: 
            argv = input('wordlebrain> ').split()
            if argv[0] in ['exit','quit']:
                break
            elif argv[0] == 'show':
                if len(argv) > 1:
                    N = int(argv[1])
                    show(N)
            elif argv[0] == 'reset':
                reset()
                print(RECOMMEND)
            else:
                globals()[argv[0]](*argv[1:])
        except EOFError:
            break
        except Exception as e:
            print(e)
            #print(f"Sorry, I didn't understand '{' '.join(argv)}'.")
            print()
            print(PLAY_USAGE)

reset()