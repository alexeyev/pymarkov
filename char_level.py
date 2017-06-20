# -*- coding: utf-8 -*-

from abstract_generator import AbstractMarkovianGenerator


def read(texts_file):
    parsed = []

    for line in open(texts_file, "r+"):
        line = line.strip().lower().replace("[s]", "S").replace("[e]", "E").replace("<n>", "N")
        splitted = list(line)
        parsed.append(splitted)
    return parsed


WEIRD_SYMBOLS = "йцукенгшщзхъфывапролдячсмитьбю"


class MarkovianCharLevelGenerator(AbstractMarkovianGenerator):

    def __init__(self, depth=2, teleport=0.0):
        super(MarkovianCharLevelGenerator, self).__init__(depth, teleport)

    def __generate_prefix__(self):
        return [WEIRD_SYMBOLS[i] for i in range(self.depth)]

    def generate_list(self):
        return self.__generate_list__(removable_items=["S", "E"])

    def generate_text(self):
        per_element = lambda x: x.replace("N", "\n")
        per_text = lambda x: x.replace(" .", ".").replace(" ,", ",")
        joiner = ""
        return self.__generate_text__(
            removable_items=["S", "E"],
            extra_processor_per_item=per_element,
            extra_text_postprocessor=per_text,
            joiner=joiner)


TEXTS = read("parsed_texts.txt")

if __name__ == "__main__":
    depths = range(15)
    generators = [MarkovianCharLevelGenerator(depth=d + 1).fit(TEXTS) for d in depths]

    for id, gen in enumerate(generators):
        print()
        print("DEPTH", id + 1)
        print(gen.generate_text())
