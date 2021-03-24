import lxml.etree as ET
import pandas as pd
from nltk.tokenize import word_tokenize
import numpy as np
import argparse
import os.path


parser = argparse.ArgumentParser()
parser.add_argument("--output_file", default=None, type=str, required=True)
parser.add_argument("--start_in", default=0, type=int, required=False)
args = parser.parse_args()

data = pd.read_csv('../corpus.csv')

if os.path.isfile(args.output_file):
	print('This file already exists!') 
	exit()

with open(args.output_file, 'w') as myfile:
	# # for each instance, open the text part 
	for i, instance in enumerate(data.text[args.start_in:]):
		#instance = instance.lower()
		index = i + args.start_in
		print('\n')
		print('##########################################')
		#print('\n')
		print('IDENTIFICADOR:',index)
		print(str(data.user_id[index]))
		print('##########################################')
		print('\n')
		print(instance)
		print('\n')

		# check the twit first
		tweet = ET.Element('tweet', id=str(data.user_id[index]))
		tweet_info = input('If the tweet has a *PROBLEM* type it (OL/NC/NV). Otherwise press ENTER. ')
		print('\n')
		if tweet_info not in ['OL','NC','NV', '']:
			tweet_info = input('That was not a valid option. Type OL/NC/NV or press ENTER. ')
		print('\n')
		#print(tweet_info)
		if tweet_info != "":
			tweet.set('problem', tweet_info)
			mydata = ET.tostring(tweet, encoding='unicode')#.decode("latin1") pretty_print=True, 
			#print(mydata)
			myfile.write(mydata+'\n')
			myfile.flush()
			continue
		
		sentence = ET.SubElement(tweet, 'sentence')  

		tokenised = word_tokenize(instance)
		for i, word in enumerate(tokenised):
			print(i, '\t', word)
		print('\n')
		print(instance)	
		print('\n')
		sentence_info = input('Where is the first *VERB* of the tweet? (Type the position). If there is no other type ENTER. ')
		while sentence_info != "":
			main_verb = tokenised[int(sentence_info)]
			#grupverb = ET.SubElement(sentence, 'grup.verb')
			verb = ET.SubElement(sentence, 'v')
			verb.set('verb', main_verb.lower())
			verb.set('token_id', sentence_info)
			verb_sense = input("What's the verb sense?")
			verb.set('sense', verb_sense)
			
			print('\n')
			argument_info = input('What *ARGUMENT* does the verb "{}" have? If there is no other press ENTER. '.format(main_verb))
			print('\n')
			if argument_info not in ['arg0', 'arg1', 'arg2', 'arg3', 'arg4', 'argM', 'argL', '']:
				argument_info = input("That was not a valid option. Type an argument or press ENTER. Options: ['arg0', 'arg1', 'arg2', 'arg3', 'arg4', 'argM', 'argL'] ")

			while argument_info != "":
				argument = ET.SubElement(verb, 'sn')
				argument.set('arg', argument_info)

				print('\n')
				for i, word in enumerate(tokenised):
					print(i, '\t', word)
				print('\n')
				print(instance)
				print('\n')
				components = input('What *WORDS* are part of "{}"? (Type the positions coma separated): '.format(argument_info))
				for w in components.split(','):
					word = ET.SubElement(argument, 'word')
					word.set('word', tokenised[int(w)])
					word.set('token_id', w)
				#tokenised.pop(components.split(','))
				print('\n')
				print(instance)

				print('\n')
				argument_info = input('What other *ARGUMENT* does the verb "{}" have? If there is no other press ENTER. '.format(main_verb))
				print('\n')
				if argument_info not in ['arg0', 'arg1', 'arg2', 'arg3', 'arg4', 'argM', 'argL', '']:
					argument_info = input("That was not a valid option. Type an argument or press ENTER. Options: ['arg0', 'arg1', 'arg2', 'arg3', 'arg4', 'argM', 'argL'] ")
			print('\n')
			for i, word in enumerate(tokenised):
				print(i, '\t', word)
			print('\n')
			print(instance)
			print('\n')
			sentence_info = input('Where is the next *VERB* of the tweet? (Type the position). If there is no other type ENTER. ')
			if sentence_info != "":
				new_sentence = input('Does it belong to a *NEW SENTENCE*? (y/n) ')
				if new_sentence == 'y':
					sentence = ET.SubElement(tweet, 'sentence')  
			#tweet = ET.indent(tweet)
		mydata = ET.tostring(tweet, encoding='unicode')
		myfile.write(mydata+'\n')
		myfile.flush() 
		 
myfile.close()

