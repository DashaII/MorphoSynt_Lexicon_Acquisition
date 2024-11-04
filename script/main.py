import lexicon_RL

INPUT_FILE_PATH = "ru.txt"
OUTPUT_FILE_PATH = "russian_lexicon.txt"

if __name__ == "__main__":
    lexicon_RL.create_lexicon(INPUT_FILE_PATH, OUTPUT_FILE_PATH)
