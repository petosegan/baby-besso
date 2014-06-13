import json
import sys
import eliza_online
import os
import collections
import re
import logging
logging.basicConfig( filename=r'C:\Users\Desktop\Besso\besso_online\bessolog.log', filemode='a' )

rules = collections.OrderedDict([
    (re.compile(r"\bthanks\b", flags=re.I), [
        r"You're welcome! Now get to work.",
        ]),
    (re.compile(r"\b(hello|hi)\b", flags=re.I), [
        r"How do you do. Please state your problem."
        ]),
    (re.compile(r"\bnot sure (.*)"),[
        r"What is your best guess about {0}?"
        ]),
    (re.compile(r"\bsorry\b", flags=re.I), [
        r"Please don't apologize",
        r"Apologies are not necessary",
        ]),
    (re.compile(r"\bperhaps\b", flags=re.I), [
        r"You do not seem quite certain",
        r"How can you be sure?",
        ]),
    (re.compile(r"\bbecause\b", flags=re.I), [
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
    (re.compile(r"(I|we) think (.*)", flags=re.I), [
        r"Why do you think {1}?",
        r"That seems reasonable.",
        r"Are you sure {1}?",
        ]),
    (re.compile(r"(I|we) want (.*)", flags=re.I), [
        r"What would you do next if you got {1}?",
        r"Why do you want {1}?",
        r"Suppose you got {1} soon. What then?",
        r"How can you get {1}?"
        ]),
    (re.compile(r"(I|we) need to (.*)", flags=re.I), [
        r"Is there any alternative to that?",
        r"So how are you going to {1}?",
        r"Why do you need to {1}?",
        r"Does anyone else know how to {1}?",
        r"Can anyone help you to {1}?",
        ]),   
    (re.compile(r"(I|we) need (.*)", flags=re.I), [
        r"Is there any alternative to that?",
        r"So how can you get {1}?",
        r"Why do you need {1}?",
        r"Can anyone help you get {1}?",
        r"Do you know anyone who has {1}?",
        ]),
    (re.compile(r"(I|we) can't (.*)", flags=re.I), [
        r"Why can't you {1}?",
        r"Why do you want to {1}?",
        r"What is the simplest possible way you can {1}?",
        r"Can anyone else {1}?",
        ]),
    (re.compile(r"(I|we) should (.*)", flags=re.I), [
        r"Probably you should {1}.",
        r"I guess you should {1}.",
        r"Why haven't you already {1}?",
        ]),
    (re.compile(r"(I|we) guess (.*)", flags=re.I), [
        r"Sounds reasonable.",
        r"Yeah, ok.",
        r"How can you make sure that {1}?",
        ]),
    (re.compile(r"\b(I|we) don't know (.*)", flags=re.I), [
        r"How can you determine {1}?",
        r"Does anyone else know {1}?",
        r"Why do you need to know {1}?",
        r"What is your best guess about {1}?",
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
    (re.compile(r"\balike\b", flags=re.I), [
        r"In what way?",
        r"What similarities are there?",
        ]),
    (re.compile(r"\bsame\b", flags=re.I), [
        r"What other connections do you see?",
        ]),
    (re.compile(r"\bno\b", flags=re.I), [
        r"Why not?",
        ]),
    (re.compile(r"(I was|we were) (.*)", flags=re.I), [
        r"Were you really?",
        r"Why do you tell me you were {1} now?"
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
    (re.compile(r"how can (I|we) (.*)", flags=re.I), [
        r"What is the simplest way you can {1}?",
        r"What if you google how to {1}?",
        ]),
    (re.compile(r" why don't you | fuck | bullshit ", flags=re.I), [
        r"Let's stay focused on your problem",
        ]),
    (re.compile(r"\byes\b", flags=re.I), [
        r"You seem quite positive",
        r"You are sure?",
        r"I understand",
        ]),
    (re.compile(r"\bsomeone\b", flags=re.I), [
        r"Can you be more specific?",
        ]),
    (re.compile(r"\beveryone\b", flags=re.I), [
        r"Surely not everyone",
        r"Can you think of anyone in particular?",
        r"Who, for example?",
        ]),
    (re.compile(r"\balways\b", flags=re.I), [
        r"Can you think of a specific example?",
        r"When?",
        r"What incident are you thinking of?",
        r"Really--always?",
        ]),
    (re.compile(r"\bwhat\b", flags=re.I), [
        r"Why are you doing it this way?",
        r"What is it you really want to do?",
        r"What do you think should be your very next step?",
        ]),
    (re.compile(r"(.*)\?", flags=re.I), [
        r"I don't know. Please continue.",
        r"I'm not sure. What do you think?",
        r"Hmmm...",
        r"I'm not quite sure...",
        r"Hmm, hard to say."])
    ])

default_responses = [
    "Please continue",
    "Go on",
    "Uh huh",
    "OK",
    "I see",
    "Are you sure?",
    "Right...",
    "Yeah, ok",
    "Sure, ok",
    "Alright...",
    ]

def main(input):
    logging.getLogger().setLevel(logging.DEBUG)
    return eliza_online.interact(input, rules, map(str.upper, default_responses))

if __name__ == '__main__':
    main()
