# -*- coding: utf-8 -*-a

import re

from fluxus_bot.markovchain.abstract_generator import AbstractMarkovianGenerator


def read(texts_file):

    parsed = []

    for line in open(texts_file, "r+"):
        line = line.strip().lower()
        splitted = re.findall(r"[\w'<>\]\[]+|[.,!?;]", line)
        parsed.append(splitted)
    return parsed


class MarkovianWordLevelGenerator(AbstractMarkovianGenerator):
    def __init__(self, depth=2, teleport=0.0):
        super(MarkovianWordLevelGenerator, self).__init__(depth, teleport)

    def __generate_prefix__(self):
        return ["*" + str(i) for i in range(self.depth)]

    def generate_list(self):
        return self.__generate_list__(removable_items=["[s]", "[e]"])

    def generate_text(self):
        per_element = lambda x: x.replace("<n>", "\n")
        per_text = lambda x: x.replace(" .", ".").replace(" ,", ",")
        joiner = " "
        return self.__generate_text__(
            removable_items=["[s]", "[e]"],
            extra_processor_per_item=per_element,
            extra_text_postprocessor=per_text,
            joiner=joiner)


TEXTS = read("parsed_texts.txt")

if __name__ == "__main__":
    depths = range(4)
    generators = [MarkovianWordLevelGenerator(depth=d + 1).fit(TEXTS) for d in range(5)]

    for id, gen in enumerate(generators):
        print()
        print("DEPTH", id + 1)
        print(gen.generate_text())
