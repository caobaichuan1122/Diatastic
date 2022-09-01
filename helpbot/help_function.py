import spacy
import random

from .helper import is_greeting, index_sort
from .constants import BOT_GREETINGS
from .diabetes_info import INFO

nlp = spacy.load("en_core_web_md")

def random_greeting():
    return random.choice(BOT_GREETINGS)


    

def helpbot_response(user_prompt):
    if is_greeting(user_prompt):
        return random_greeting()
    
    user_prompt = nlp(user_prompt)
    sim_scores = [user_prompt.similarity(nlp(response)) for response in INFO]
    
    best_index = index_sort(sim_scores)[0]
    return INFO[best_index]

def main() -> None:
    helpbot_response("hi")



if __name__ == "__main__":
    main()
