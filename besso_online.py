import json
import sys
import eliza_online
import os

rules = {
    "fail ?*x": [
        "AND SO, I DIE."
        ],
    "thanks ?*x": [
        "You're welcome! Now get to work.",
        ],
    "?*x hello ?*y": [
        "How do you do. Please state your problem."
        ],
    "?*x hi ?*y": [
        "How do you do. Please state your problem."
        ],
    "?*x not sure ?*y":[
        "What is your best guess about ?y?"
        ],
    "?*x sorry ?*y": [
        "Please don't apologize",
        "Apologies are not necessary",
        ],
    "?*x I remember ?*y": [
        "Do you often think of ?y?",
        "Does thinking of ?y bring anything else to mind?",
        "What else do you remember?",
        "Why do you recall ?y right now?",
        "What in the present situation reminds you of ?y?",
        "What is the connection between this situation and ?y?",
        ],
    "?*x I think ?*y": [
        "Why do you think ?y?",
        "That seems reasonable.",
        "Are you sure ?y?",
        ],
    "?*x do you remember ?*y": [
        "What about ?y?",
        "You mentioned ?y",
        ],
    "?*x I want ?*y": [
        "What would you do next if you got ?y?",
        "Why do you want ?y?",
        "Suppose you got ?y soon. What then?"
        ],
    "?*x I need to ?*y": [
        "Is there any alternative to that?",
        "So how are you going to ?y?",
        "Why do you need to ?y?",
        ],   
    "?*x I need ?*y": [
        "Is there any alternative to that?",
        "So how can you get ?y?",
        "Why do you need ?y?",
        ],
    "?*x if ?*y": [
        "Do you really think it's likely that ?x?",
        ],
    "?*x are like ?*y": [
        "What resemblance do you see between ?x and ?y?",
        ],
    "?*x is like ?*y": [
        "In what way is it that ?x is like ?y?",
        "What resemblance do you see?",
        "Could there really be some connection?",
        "How?",
        ],
    "?*x alike ?*y": [
        "In what way?",
        "What similarities are there?",
        ],
    "?* same ?*y": [
        "What other connections do you see?",
        ],
    "?*x no ?*y": [
        "Why not?",
        ],
    "?*x I was ?*y": [
        "Were you really?",
        "Perhaps I already knew you were ?y.",
        "Why do you tell me you were ?y now?"
        ],
    "?*x was I ?*y": [
        "What if you were ?y?",
        "Do you think you were ?y?",
        "What would it mean if you were ?y?",
        ],
    "?*x I am ?*y": [
        "In what way are you ?y?",
        "Do you want to be ?y?",
        ],
    "?*x am I ?*y": [
        "Do you believe you are ?y?",
        "Would you want to be ?y?",
        "You wish I would tell you you are ?y?",
        "What would it mean if you were ?y?",
        ],
    "?*x am ?*y": [
        "Why do you say 'AM?'",
        "I don't understand that"
        ],
    "?*x are you ?*y": [
        "Why are you interested in whether I am ?y or not?",
        "Would you prefer if I weren't ?y?",
        "Perhaps I am ?y in your fantasies",
        ],
    "?*x you are ?*y": [
        "What makes you think I am ?y?",
        ],
    "?*x because ?*y": [
        "That sounds reasonable",
        "What other reasons might there be?",
        "Does that reason seem to explain anything else?",
        ],
    "?*x were you ?*y": [
        "Perhaps I was ?y?",
        "What do you think?",
        "What if I had been ?y?",
        ],
    "?*x how can I ?*y": [
        "What is the simplest way you can ?y?",
        "What if you google how to ?y?",
        ],
    "?*x I can't ?*y": [
        "Maybe you could ?y now",
        "What if you could ?y?",
        "What is the simplest possible way you can ?y?",
        ],
    "?*x why don't you ?*y": [
        "Let's stay focused on your problem",
        ],
    "?*x yes ?*y": [
        "You seem quite positive",
        "You are sure?",
        "I understand",
        ],
    "?*x someone ?*y": [
        "Can you be more specific?",
        ],
    "?*x everyone ?*y": [
        "Surely not everyone",
        "Can you think of anyone in particular?",
        "Who, for example?",
        ],
    "?*x always ?*y": [
        "Can you think of a specific example?",
        "When?",
        "What incident are you thinking of?",
        "Really--always?",
        ],
    "?*x what ?*y": [
        "Why do you ask?",
        "Does that question interest you?",
        "What is it you really want to know?",
        "What do you think?",
        "What comes to your mind when you ask that?",
        ],
    "?*x perhaps ?*y": [
        "You do not seem quite certain",
        ],
    "?*x are ?*y": [
        "Why are ?x ?y?",
        "Are you sure they are ?y",
        ]
    }

default_responses = [
    "Very interesting",
    "I am not sure I understand you fully",
    "Please continue",
    "Go on",
    "Uh huh",
    "OK",
    "I see",
    "Are you sure?",
    "Right...",
    "Yeah, ok",
    ]

def main():
    # We need the rules in a list containing elements of the following form:
    # `(input pattern, [output pattern 1, output pattern 2, ...]`
    
    home_dir = os.path.dirname(os.path.realpath(__file__))
    logfilename = os.path.join(home_dir,'besso_log.txt')
    logfile = open(logfilename, 'a+')
    
    rules_list = []
    for pattern, transforms in rules.items():
        # Remove the punctuation from the pattern to simplify matching.
        pattern = eliza.remove_punct(str(pattern.upper())) # kill unicode
        transforms = [str(t).upper() for t in transforms]
        rules_list.append((pattern, transforms))
    eliza.interact('BESSO> ', rules_list, map(str.upper, default_responses), logfile)
    
def online(input):
    # We need the rules in a list containing elements of the following form:
    # `(input pattern, [output pattern 1, output pattern 2, ...]`
    
    # home_dir = os.path.dirname(os.path.realpath(__file__))
    # logfilename = os.path.join(home_dir,'besso_log.txt')
    # logfile = open(logfilename, 'a+')
    
    rules_list = []
    for pattern, transforms in rules.items():
        # Remove the punctuation from the pattern to simplify matching.
        pattern = eliza_online.remove_punct(str(pattern.upper())) # kill unicode
        transforms = [str(t).upper() for t in transforms]
        rules_list.append((pattern, transforms))
    return eliza_online.interact_online(input, rules_list, map(str.upper, default_responses))

if __name__ == '__main__':
    main()
