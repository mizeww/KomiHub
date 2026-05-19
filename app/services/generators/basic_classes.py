class Card:
    def __init__(self, id: int,
                 word_kom: str,
                 word_rus: str,
                 suffix: tuple,
                 examples: tuple,
                 image=''):
        self.id = id
        self.word_kom = word_kom
        self.word_rus = word_rus
        self.suffix = suffix
        self.examples = examples
        self.image = image

