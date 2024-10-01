import json


class Wordle(object):
	"""docstring for Wordle"""
	def __init__(self):
		self.data = self.get_json()
		self.incorrect_letter = []
		self.correct_letter = {}
		self.wrongly_place = {}
		self.main_boucle()

	def main_boucle(self):
		while len(self.data) > 1:
			self.ask_user()
		
	def get_json(self) -> dict:
		with open("wordle.json",'r') as file:
			return json.load(file)
	
	def ask_user(self):
		print("Write the full word you tested :")
		word_test = self.request_input(True)
		print("Write the result (UPPERCASE:Correctly placed/lowercase:Wrongly place/'-': not in the word) :")
		word_result = self.request_input()

		for i in range(5):
			if word_test.upper()[i] == word_result[i]:
				self.correct_letter[word_result[i]] = i
			elif word_result[i] != '-':
				self.wrongly_place[word_result[i]] = i
			else:
				self.incorrect_letter.append(word_test[i])

		self.process()

	def process_word(self, word:str):
		for incorrect_letter in self.incorrect_letter:
			if incorrect_letter in list(word):
				# Il y'a une lettre incorrect dans le mot
				return False
		for correct_letter in self.correct_letter.keys():
			if correct_letter not in list(word):
				# Il n'y a pas les lettres pourtant validé
				return False
			elif correct_letter != word[self.correct_letter[correct_letter]]:
				return False
				# Il y'a une bonne lettre mais pas à la bonne place
		for misplaced_letter in self.wrongly_place:
			if misplaced_letter.upper() == word[self.wrongly_place[misplaced_letter]]:
				return False
			elif misplaced_letter.upper() not in list(word):
				return False
		return True

	def process(self):
		new_data = []
		for word in self.data:
			if self.process_word(word):
				new_data.append(word)
		print(f"{len(new_data)}/{len(self.data)} words remaining, {round((len(new_data)/len(self.data)) * 100 - 100,1)}% of word")
		print(new_data[-10:])
		print("Letter eliminated :", self.incorrect_letter)
		print("Letter misplaced :", self.wrongly_place)
		self.data = new_data
		#print(new_data)

	def request_input(self, is_full_word: bool=False) -> str:
		while True:
			submit = input("-> ")
			if len(submit) == 5:
				if not is_full_word:
					return submit
				elif is_full_word and submit.upper() in self.data:
					return submit
				else :
					print("Word not in the list")
			else:
				print("Not 5 letters")
				continue


if __name__ == '__main__':
	Wordle()