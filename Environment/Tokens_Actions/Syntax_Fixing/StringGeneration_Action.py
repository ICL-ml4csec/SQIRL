from nltk.corpus import words
import random

from Environment.Tokens_Actions.Basic_Block.Quote_Token import Quote_Token
from Environment.Tokens_Actions.Basic_Block.String_Token import String_Token

class StringGeneration_Action:
    try:
        word = words.words()
    except LookupError:
        import nltk
        nltk.download('words')
        word = words.words()
    def generate_string():
        quote_type = random.randint(0,len(Quote_Token.quote_type_mapping.keys())-1)
        random_word = random.choice(StringGeneration_Action.word)
        return String_Token(random_word,quote_type)