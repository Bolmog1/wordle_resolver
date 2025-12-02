import json
from collections import Counter


class Letter:
    def __init__(self, letter, position):
        self.letter = letter
        self.position = position

def word_score(word):
    score = 10
    for letter in word:
        score -= word.count(letter)
    return score

class Wordle:
    def __init__(self):
        self.words: list[str] = []
        self.placed_letters: list[Letter,] = []
        self.misplaced_letters: list[Letter,] = []
        self.not_present_letters: list[str] = []

    def load(self):
        with open("wordle.json",'r') as file:
            self.words = json.load(file)

    def delete_words(self):
        self.delete_words_from_placed()
        self.delete_words_from_misplaced()
        self.delete_words_from_not_present()

    def delete_words_from_placed(self):
        new_words = []
        for word in self.words:
            # mot valide seulement si toutes les lettres placées correspondent
            if all(word[p.position] == p.letter for p in self.placed_letters):
                new_words.append(word)
        self.words = new_words

    def delete_words_from_misplaced(self):
        new_words = []
        for word in self.words:
            # mot valide seulement si :
            # - la lettre existe bien dans le mot
            # - mais pas à cette position
            if all(
                    (m.letter in word) and (word[m.position] != m.letter)
                    for m in self.misplaced_letters
            ):
                new_words.append(word)
        self.words = new_words

    def delete_words_from_not_present(self):
        # Comptage des lettres "autorisées" malgré leur présence dans not_present
        allowed_counts = Counter()

        # placed -> occurrences fixes
        for p in self.placed_letters:
            allowed_counts[p.letter] += 1

        # misplaced -> occurrences existantes dans le mot mais ailleurs
        for m in self.misplaced_letters:
            allowed_counts[m.letter] += 1

        new_words = []
        for word in self.words:
            word_count = Counter(word)
            valid = True

            for letter in self.not_present_letters:
                # combien d'occurrences sont tolérées ?
                allowed = allowed_counts.get(letter, 0)
                # si le mot en contient plus → invalide
                if word_count[letter] > allowed:
                    valid = False
                    break

            if valid:
                new_words.append(word)

        self.words = new_words

    def guess(self) -> list[dict[str,int]]:
        word_score_list: list[dict[str,int]] = []
        for word in self.words:
            word_score_list.append({"word": word, "score": word_score(word)})
        word_score_list = sorted(word_score_list, key=lambda word: word["score"], reverse=True)
        if len(word_score_list) > 5:
            return word_score_list[:5]
        return word_score_list


if __name__ == "__main__":
    wordle = Wordle()
    wordle.load()
    wordle.delete_words()
    print(wordle.guess())
