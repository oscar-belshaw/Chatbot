from newspaper import Article
import random
import string
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import warnings
warnings.filterwarnings('ignore')

nltk.download('punkt', quiet = True)

article = Article('https://www.thesimpledollar.com/save-money/a-walkthrough-and-cost-breakdown-of-brewing-your-own-beer/#:~:text=Boil%20the%20Water%20and%20Steep,for%20twenty%20minutes%20or%20so.')
article.download()
article.parse()
article.nlp()

corpus = article.text

text = corpus
sentence_list = nltk.sent_tokenize(text)	#breaks the text up in to a list of sentences

#The bots initial response to a greeting
def greeting_response(text):
	 text = text.lower()

	 bot_greetings = ["Hello", "Hi", "How are you?", "What can I do for you today", "Hey"]

	 user_greetings = ["hi", "hey", "hello"]

	 for word in text.split():
	 	if word in user_greetings:
	 		return random.choice(bot_greetings)

def index_sort(list_var):
	length = len(list_var)
	list_index = list(range(0, length))

	x = list_var
	for i in range(length):
		for j in range(length):
			if x[list_index[i]] > x[list_index[j]]:
				#swaps the index
				temp = list_index[i]
				list_index[i] = list_index[j]
				list_index[j] = temp

	return list_index

#The bots response to a question
def bot_response(u_input):
	u_input = u_input.lower()
	sentence_list.append(u_input)
	bot_response = ''
	cm = CountVectorizer().fit_transform(sentence_list)
	similarity_scores = cosine_similarity(cm[-1], cm)
	similarity_scores_list = similarity_scores.flatten()
	index = index_sort(similarity_scores_list)
	index = index[1: ]
	response_flag = 0

	j = 0
	while j < 1:
		for i in range(len(index)):
			if similarity_scores_list[index[i]] > 0.0:
				bot_response = bot_response + ' ' + sentence_list[index[i]]
				response_flag = 1
				j += 1

	if response_flag == 0:
		bot_response = bot_response + " I apologise, I don't understand that question."

 	
	sentence_list.remove(user_input)
	
	return bot_response

#starting the chat
print("Hey, I can answer ANY question you have regarding the brewing of beer, the equipment required, or even the amount of money required to undertake such a task. To turn me off type bye")

exit_list = ["Exit",  "See you later", "Quit", "Farewell", "Bye"]

while(True):
	user_input = input()
	if user_input.lower() == "bye":
		print(random.choice(exit_list))
		break
	else:
		if greeting_response(user_input) != None:
			print(greeting_response(user_input))
		else:
			print(bot_response(user_input))


