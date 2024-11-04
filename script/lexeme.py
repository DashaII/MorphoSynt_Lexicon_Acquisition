class Lexeme:
    def __init__(self, lexeme, lemma=None, stem=None, tag=None):
        self.lexeme = lexeme
        self.lemma = lemma
        self.stem = stem
        self.tag = tag

    def __str__(self):
        if self.lemma is None:
            return f'Lexeme: {self.lexeme:<20}'
        elif self.stem is None:
            return f'Lexeme: {self.lexeme:<20}  Lemma: {self.lemma:<20}'
        elif self.tag is None:
            return f'Lexeme: {self.lexeme:<20}  Lemma: {self.lemma:<20}  Stem: {self.stem:<20}'
        else:
            return f'Lexeme: {self.lexeme:<20}  Lemma: {self.lemma:<20}  Stem: {self.stem:<20}  Tag: {self.tag:<20}'
