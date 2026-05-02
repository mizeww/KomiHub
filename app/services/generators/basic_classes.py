class Card:
    def __init__(self, word_kom: str,
                 word_rus: str,
                 suffix: tuple,
                 examples: tuple):
        self.word_kom = word_kom
        self.word_rus = word_rus
        self.suffix = suffix
        self.examples = examples