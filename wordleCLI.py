import curses
import curses.ascii
from curses import wrapper
from wordle import Wordle, Letter

NB_LETTERS = 5
NB_GUESSES = 5

class LetterCLI:
    def __init__(self, letter, status = 2):
        self.letter = letter
        self.status = status

class WordleCLI:
    def __init__(self, stdscr):
        self.stdscr: curses._CursesWindow = stdscr
        self.guesses: list[list[LetterCLI,]] = []
        self.wordle = Wordle()
        self.run()

    def run(self):
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Regular
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)  # Warning
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_GREEN)  # Good guess
        curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_YELLOW)  # misplaced guess
        curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLACK)  # No
        curses.curs_set(False)
        self.wordle.load()
        while True:
            if len(self.guesses) > NB_GUESSES:
                return
            if len(self.wordle.words) == 1:
                return self.draw_win(self.wordle.words[0])
            self.draw()
            letters = self.prompt()
            for pos, letter in enumerate(letters):
                if letter.status == 0:
                    self.wordle.placed_letters.append(Letter(letter.letter, pos))
                elif letter.status == 1:
                    self.wordle.misplaced_letters.append(Letter(letter.letter, pos))
                elif letter.status == 2:
                    self.wordle.not_present_letters.append(letter.letter)
            self.guesses.append(letters)
            self.wordle.delete_words()

    def draw(self):
        self.stdscr.clear()
        rows, cols = self.stdscr.getmaxyx()
        two_thirds = (cols // 3) * 2
        if rows < 15 or cols < 20:
            self.stdscr.addstr(0,0,"Terminal too small!\n", curses.A_BOLD)

        text = "Welcome to Wordle Resolver!"
        self.stdscr.addstr(1, two_thirds // 2 - len(text) // 2, text, curses.color_pair(1))
        self.draw_guessed()
        self.draw_guess()
        self.draw_stats()
        self.stdscr.refresh()

    def draw_guessed(self):
        _, rows_offset = self.stdscr.getmaxyx()
        rows_offset = (rows_offset // 3)- 2
        for line, guess in enumerate(self.guesses):
            for l,letter in enumerate(guess):
                self.stdscr.addstr(line+3, rows_offset+l, letter.letter, curses.color_pair(letter.status + 3))
                # self.stdscr.addstr(row, col + l, letter.letter, curses.color_pair(letter.status + 3))

    def draw_guess(self):
        _, cols_offset = self.stdscr.getmaxyx()
        cols_offset = (cols_offset // 3) * 2
        self.stdscr.addstr(2, cols_offset, "TRY", curses.A_BOLD)
        guess = self.wordle.guess()
        for l,word in enumerate(guess):
            self.stdscr.addstr(3+l, cols_offset, word["word"], curses.color_pair(1))

    def draw_live_guess(self, row, col, guess: list[LetterCLI,]):
        for l,letter in enumerate(guess):
            self.stdscr.addstr(row, col+l, letter.letter, curses.color_pair(letter.status+3))
        self.stdscr.refresh()

    def draw_stats(self):
        rows, _ = self.stdscr.getmaxyx()
        self.stdscr.addstr(rows-  4, 0, f"{len(self.wordle.words)} words remaining", curses.color_pair(1))
        self.stdscr.addstr(rows - 3, 0, f"Well Placed : {','.join([f"({letters.letter}:{letters.position})" for letters in self.wordle.placed_letters])}", curses.color_pair(3))
        self.stdscr.addstr(rows - 2, 0, f"Misplaced : {','.join([f"({letters.letter}:{letters.position})" for letters in self.wordle.misplaced_letters])}", curses.color_pair(4))
        self.stdscr.addstr(rows - 1, 0, f"Not in : {','.join([letters for letters in self.wordle.not_present_letters])}", curses.color_pair(5))

    def draw_win(self, word):
        self.stdscr.clear()
        rows, cols = self.stdscr.getmaxyx()
        self.stdscr.addstr((rows // 2) - 1, (cols // 2) - 1, f"WIN", curses.A_BLINK)
        self.stdscr.addstr((rows // 2), (cols // 2) - 2, word, curses.color_pair(3))
        self.stdscr.refresh()
        self.stdscr.getch()

    def prompt(self):
        _, cols_offset = self.stdscr.getmaxyx()
        cols_offset = (cols_offset // 3) - 2
        rows_offset = len(self.guesses) + 3

        letter = []
        while True:
            # Quit loop if all letter inputed
            if len(letter) >= NB_LETTERS:
                break

            # Preshot the letter
            preshot = False
            for l,val_letter in enumerate(self.wordle.placed_letters):
                if val_letter.position == len(letter):
                    letter.append(LetterCLI(val_letter.letter, 0))
                    self.draw_live_guess(rows_offset, cols_offset, letter)
                    preshot = True
                    break
            if preshot: continue

            self.stdscr.move(rows_offset , cols_offset + len(letter))
            curses.curs_set(True)
            letter_taped = self.stdscr.getch()

            if letter_taped == curses.ascii.DEL:  # Edit previous letter
                letter.pop(-1)
                continue
            letter.append(LetterCLI((chr(letter_taped)).upper()))
            curses.curs_set(False)
            self.draw_live_guess(rows_offset, cols_offset, letter)
            # Iterate between states of the letter
            while True:
                c = self.stdscr.getch()
                if c != curses.ascii.NL:
                    letter[-1].status += 1
                    letter[-1].status %= 3
                    self.draw_live_guess(rows_offset, cols_offset, letter)
                else:
                    break
            self.draw_live_guess(rows_offset, cols_offset, letter)
        return letter

if __name__ == "__main__":
    wrapper(WordleCLI)
