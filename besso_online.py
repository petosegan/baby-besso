import json
import sys
import eliza_online
import os
import collections
import re

rules = collections.OrderedDict([
    (re.compile(r"thanks", flags=re.I), [
        r"You're welcome! Now get to work.",
        ]),
    (re.compile(r"hello", flags=re.I), [
        r"How do you do. Please state your problem."
        ]),
    (re.compile(r"not sure (.*)"),[
        r"What is your best guess about \1?"
        ]),
    (re.compile(r"sorry", flags=re.I), [
        r"Please don't apologize",
        r"Apologies are not necessary",
        ]),
    (re.compile(r"I remember (.*)", flags=re.I), [
        r"Do you often think of \1?",
        r"Does thinking of \1 bring anything else to mind?",
        r"What else do you remember?",
        r"Why do you recall \1 right now?",
        r"What in the present situation reminds you of \1?",
        r"What is the connection between this situation and \1?",
        ]),
    (re.compile(r"I think (.*)", flags=re.I), [
        r"Why do you think \1?",
        r"That seems reasonable.",
        r"Are you sure \1?",
        ]),
    (re.compile(r"do you remember (.*)", flags=re.I), [
        r"What about \1?",
        r"You mentioned \1",
        ]),
    (re.compile(r"I want (.*)", flags=re.I), [
        r"What would you do next if you got \1?",
        r"Why do you want \1?",
        r"Suppose you got \1 soon. What then?"
        ]),
    (re.compile(r"I need to (.*)", flags=re.I), [
        r"Is there any alternative to that?",
        r"So how are you going to \1?",
        r"Why do you need to \1?",
        ]),   
    (re.compile(r"I need (.*)", flags=re.I), [
        r"Is there any alternative to that?",
        r"So how can you get \1?",
        r"Why do you need \1?",
        ]),
    (re.compile(r"(.*) if", flags=re.I), [
        r"Do you really think it's likely that \1?",
        ]),
    (re.compile(r"(.*) are like (.*)", flags=re.I), [
        r"What resemblance do you see between \1 and \2?",
        ]),
    (re.compile(r"(.*) is like (.*)", flags=re.I), [
        r"In what way is it that \1 is like \2?",
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
        r"Perhaps I already knew you were \1.",
        r"Why do you tell me you were \1 now?"
        ]),
    (re.compile(r"was I (.*)", flags=re.I), [
        r"What if you were \1?",
        r"Do you think you were \1?",
        r"What would it mean if you were \1?",
        ]),
    (re.compile(r"I am (.*)", flags=re.I), [
        r"In what way are you \1?",
        r"Do you want to be \1?",
        ]),
    (re.compile(r"am I (.*)", flags=re.I), [
        r"Do you believe you are \1?",
        r"Would you want to be \1?",
        r"You wish I would tell you you are \1?",
        r"What would it mean if you were \1?",
        ]),
    (re.compile(r"are you (.*)", flags=re.I), [
        r"Why are you interested in whether I am \1 or not?",
        r"Would you prefer if I weren't \1?",
        ]),
    (re.compile(r"you are (.*)", flags=re.I), [
        r"What makes you think I am \1?",
        ]),
    (re.compile(r" because ", flags=re.I), [
        r"That sounds reasonable",
        r"What other reasons might there be?",
        r"Does that reason seem to explain anything else?",
        ]),
    (re.compile(r"were you (.*)", flags=re.I), [
        r"Perhaps I was \1?",
        r"What do you think?",
        r"What if I had been \1?",
        ]),
    (re.compile(r"how can I (.*)", flags=re.I), [
        r"What is the simplest way you can \1?",
        r"What if you google how to \1?",
        ]),
    (re.compile(r"I can't (.*)", flags=re.I), [
        r"Maybe you could \1 now",
        r"What if you could \1?",
        r"What is the simplest possible way you can \1?",
        ]),
    (re.compile(r" why don't you ", flags=re.I), [
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
        r"Why do you ask?",
        r"Does that question interest you?",
        r"What is it you really want to know?",
        r"What do you think?",
        r"What comes to your mind when you ask that?",
        ]),
    (re.compile(r" perhaps ", flags=re.I), [
        r"You do not seem quite certain",
        ]),
    (re.compile(r"(.*) are (.*)", flags=re.I), [
        r"Why are \1 \2?",
        r"Are you sure they are \2",
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

    return eliza_online.interact(input, rules, map(str.upper, default_responses))

if __name__ == '__main__':
    main()
