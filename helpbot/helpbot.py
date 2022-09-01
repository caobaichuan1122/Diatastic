import random

import spacy

from .helper import is_greeting, index_sort
from .constants import BOT_GREETINGS
from .diabetes_info import INFO

nlp = spacy.load("en_core_web_md")


class HelpBot:
    def __init__(self, greetings, responses):
        self._greetings = greetings
        self._responses = [nlp(response) for response in responses]

    @property
    def random_greeting(self):
        return random.choice(self._greetings)

    def respond(self, user_prompt):
        if is_greeting(user_prompt):
            return self.random_greeting
        
        user_prompt = nlp(user_prompt)
        
        similarity_scores = [nlp(user_prompt).similarity(response) for response in self._responses]
        
        best_index = index_sort(similarity_scores)[0]
        
        return self._responses[best_index]

HELPBOT = HelpBot(BOT_GREETINGS, INFO)

def main() -> None:
    ...


if __name__ == "__main__":
    main()
