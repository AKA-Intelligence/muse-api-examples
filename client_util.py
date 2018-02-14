
import string

with open('easy_words.txt','r') as fin:
	lines = fin.read().split('\n')
	easy_words_orig = [l.lower().strip() for l in lines]
	easy_words = easy_words_orig + [w+'s' for w in easy_words_orig]
	easy_words = easy_words_orig + [w+'ed' for w in easy_words_orig]
	easy_words = easy_words_orig + [w+'ing' for w in easy_words_orig]





def is_easy(text,leeway=0):
	if leeway < 0:
		return True
	for p in string.punctuation:
		text = text.replace(p,'')
	tokens = text.lower().split()
	easy_words_counts = 0
	
	for token in tokens:
		if token.lower() in easy_words or token.isdigit():
			easy_words_counts += 1

	if easy_words_counts + leeway >= len(tokens):
		return True
	else:
		return False