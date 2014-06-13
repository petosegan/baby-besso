import json
import sys
import eliza_online
import os
import collections
import re
import logging
logging.basicConfig( filename=r'C:\Users\Desktop\Besso\besso_online\bessolog.log', filemode='a' )

rules = collections.OrderedDict([
    (re.compile(r"thanks", flags=re.I), [
        r"You're welcome! Now get to work.",
        ]),
    (re.compile(r"hello|hi", flags=re.I), [
        r"How do you do. Please state your problem."
        ]),
    (re.compile(r"not sure (.*)"),[
        r"What is your best guess about {0}?"
        ]),
    (re.compile(r"sorry", flags=re.I), [
        r"Please don't apologize",
        r"Apologies are not necessary",
        ]),
    (re.compile(r" perhaps ", flags=re.I), [
        r"You do not seem quite certain",
        r"How can you be sure?",
        ]),
    (re.compile(r" because ", flags=re.I), [
        r"That sounds reasonable",
        r"What other reasons might there be?",
        r"Does that reason seem to explain anything else?",
        ]),
    (re.compile(r"I remember (.*)", flags=re.I), [
        r"Does thinking of {0} bring anything else to mind?",
        r"What else do you remember?",
        r"Why do you recall {0} right now?",
        r"What in the present situation reminds you of {0}?",
        r"What is the connection between this situation and {0}?",
        ]),
    (re.compile(r"I think (.*)", flags=re.I), [
        r"Why do you think {0}?",
        r"That seems reasonable.",
        r"Are you sure {0}?",
        ]),
    (re.compile(r"I want (.*)", flags=re.I), [
        r"What would you do next if you got {0}?",
        r"Why do you want {0}?",
        r"Suppose you got {0} soon. What then?",
        r"How can you get {0}?"
        ]),
    (re.compile(r"I need to (.*)", flags=re.I), [
        r"Is there any alternative to that?",
        r"So how are you going to {0}?",
        r"Why do you need to {0}?",
        r"Does anyone else know how to {0}?",
        r"Can anyone help you to {0}?",
        ]),   
    (re.compile(r"I need (.*)", flags=re.I), [
        r"Is there any alternative to that?",
        r"So how can you get {0}?",
        r"Why do you need {0}?",
        r"Can anyone help you get {0}?",
        r"Do you know anyone who has {0}?",
        ]),
    (re.compile(r"I can't (.*)", flags=re.I), [
        r"Why can't you {0}?",
        r"Why do you want to {0}?",
        r"What is the simplest possible way you can {0}?",
        r"Can anyone else {0}?",
        ]),
    (re.compile(r"(.*) if", flags=re.I), [
        r"Do you really think it's likely that {0}?",
        ]),
    (re.compile(r"(.*) are like (.*)", flags=re.I), [
        r"What resemblance do you see between {0} and {1}?",
        ]),
    (re.compile(r"(.*) is like (.*)", flags=re.I), [
        r"In what way is it that {0} is like {1}?",
        r"What resemblance do you see?",
        r"Could there really be some connection?",
        r"How?",
        ]),
    (re.compile(r" alike ", flags=re.I), [
        r"In what way?",
        r"What similarities are there?",
        ]),
    (re.compile(r" same ", flags=re.I), [
        r"What other connections do you see?",
        ]),
    (re.compile(r" no ", flags=re.I), [
        r"Why not?",
        ]),
    (re.compile(r"I was (.*)", flags=re.I), [
        r"Were you really?",
        r"Perhaps I already knew you were {0}.",
        r"Why do you tell me you were {0} now?"
        ]),
    (re.compile(r"was I (.*)", flags=re.I), [
        r"What if you were {0}?",
        r"Do you think you were {0}?",
        r"What would it mean if you were {0}?",
        ]),
    (re.compile(r"I am (.*)", flags=re.I), [
        r"In what way are you {0}?",
        r"Do you want to be {0}?",
        ]),
    (re.compile(r"am I (.*)", flags=re.I), [
        r"Do you believe you are {0}?",
        r"Would you want to be {0}?",
        r"You wish I would tell you you are {0}?",
        r"What would it mean if you were {0}?",
        ]),
    (re.compile(r"are you (.*)", flags=re.I), [
        r"Why are you interested in whether I am {0} or not?",
        r"Would you prefer if I weren't {0}?",
        ]),
    (re.compile(r"you are (.*)", flags=re.I), [
        r"What makes you think I am {0}?",
        ]),
    (re.compile(r"were you (.*)", flags=re.I), [
        r"Perhaps I was {0}?",
        r"What do you think?",
        r"What if I had been {0}?",
        ]),
    (re.compile(r"how can I (.*)", flags=re.I), [
        r"What is the simplest way you can {0}?",
        r"What if you google how to {0}?",
        ]),
    (re.compile(r" why don't you | fuck | bullshit ", flags=re.I), [
        r"Let's stay focused on your problem",
        ]),
    (re.compile(r" yes ", flags=re.I), [
        r"You seem quite positive",
        r"You are sure?",
        r"I understand",
        ]),
    (re.compile(r" someone ", flags=re.I), [
        r"Can you be more specific?",
        ]),
    (re.compile(r" everyone ", flags=re.I), [
        r"Surely not everyone",
        r"Can you think of anyone in particular?",
        r"Who, for example?",
        ]),
    (re.compile(r" always ", flags=re.I), [
        r"Can you think of a specific example?",
        r"When?",
        r"What incident are you thinking of?",
        r"Really--always?",
        ]),
    (re.compile(r" what ", flags=re.I), [
        r"Why are you doing it this way?",
        r"What is it you really want to do?",
        r"What do you think should be your very next step?",
        ]),
    (re.compile(r"(.*) are (.*)", flags=re.I), [
        r"Why are {0} {1}?",
        r"Are you sure they are {1}",
        ])
    ])

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

def main(input):
    logging.getLogger().setLevel(logging.DEBUG)
    return eliza_online.interact(input, rules, map(str.upper, default_responses))

if __name__ == '__main__':
    main()
