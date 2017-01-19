from konlpy.tag import Mecab
from utility.data_manage import return2type
from utility.exception import AnalysisError


class Tagger:
    __pos_tagger = Mecab()

    def __init__(self, sentence):
        self.sentence = sentence
        self.pos = dict(Tagger.__pos_tagger.pos(self.sentence))
        self.__nouns = Tagger.__pos_tagger.nouns(self.sentence)

    @property
    @return2type(list)
    def pos_list(self):
        return self.pos.values()

    @property
    @return2type(list)
    def morph_list(self):
        return self.pos.keys()

    @property
    def word_list(self):
        return self.__nouns

    def __repr__(self):
        return f"<Tagger {self.sentence}>"


class Analyser:
    """
    Tokenize Sentence
    """
    def __init__(self, tag):
        assert type(tag) == Tagger

        self.tag = tag
        self.name, self.mean, self.bool_type = self.__analysis()

    def __repr__(self):
        return f"<Analyser {self.tag.sentence}>"

    def __analysis(self):
        for pos in self.tag.pos_list:
            if pos.startswith("VC"):
                if pos.endswith("P"):  # positive designator
                    bool_type = True
                elif pos.endswith("N"):  # negative designator
                    bool_type = False
                else:
                    raise AnalysisError("UnKnown Designator")
                break
        else:
            # sentence has no designator
            print(f"Can't Analysis \"{self.tag.sentence}\"")
            raise AnalysisError("UnKnown Sentences")

        name, mean = self.find_direct_object_info()

        return name, mean, bool_type

    def find_direct_object_info(self):
        """
        Find the 'direct object' from self.sentence and its meaning.
        """
        name = None
        mean = None

        for idx in range(len(self.tag.pos)):
            morph = self.tag.morph_list[idx]
            if morph in self.tag.word_list:
                if self.tag.pos_list[idx + 1].startswith("VC"):
                    name = morph
                else:
                    mean = morph

        return name, mean


if __name__ == '__main__':
    tag = Tagger("사과는 과일이다.")
