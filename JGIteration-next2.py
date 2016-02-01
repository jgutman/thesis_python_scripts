#Jacqueline Gutman
#JGIteration-next2.py
#Last updated: 4/19/2011
#FIX!

import csv, random, sys

def main():
	#usage: python JGIteration-next2.py [results_filename.csv] [number of first prod trial: default 29] [number of last prod trial: default 68]
						# [current chain] [current generation] 
	global chain, generation
	lower = int(sys.argv[1])
	upper = int(sys.argv[2])
	chain = int(sys.argv[3])
	generation = int(sys.argv[4]) + 1 #input current generation
	in_filename = 'gen{0}/V2G{0}C{1}.csv'.format(generation-1,chain)
	#generation variable refers to the one you are creating
	read_results = csv.DictReader(open(in_filename), delimiter=',')

	for subject in read_results:
		#print subject['AssignmentStatus']
		if not subject['AssignmentStatus']=='Rejected':
			create_next(subject, lower, upper)	

def create_next(subject, lower, upper):
	global out_filename, output
	#key_values = subject.keys()
	#for key in key_values:
	#	print key	
	#chain = int(subject["chain"])
	#generation = int(subject["generation"]) + 1
	out_filename = "JGItLearnV2C{0}G{1}.txt".format(chain, generation)
	output = open(out_filename, "w")

	global language, lexicon, abbreviation
	global animates, inanimates, verbs, casemarkers

	animates = ["mountie", "ref", "chef", "50swoman"]
	inanimates = ["barstool", "bookstand"]
	verbs = ["headbutt", "hug", "knockover", "punch"]
	casemarkers = ["kah"]

	#rotates items based on current generation and chain
	#verbs rotate forwards, animates rotate backwards between generations
	#verbs rotate backwards, animates rotate forwards between chains
	swaps = generation - chain
	switch(animates, swaps, False)
	switch(inanimates, swaps, False)
	switch(verbs, swaps, True)
	switch(casemarkers, swaps, False)	

	language = {}
	lexicon = {"mountie":"flugit", "ref":"melnawg", "chef":"lombur", "50swoman":"slagum", "barstool":"tombat", "bookstand":"nagid","headbutt":"kleidum", "hug":"dacin", "knockover":"zamper", "punch":"bliffen"}
	abbreviation = {"V1":verbs[0], "V2":verbs[1], "V3":verbs[2], "V4":verbs[3], "A":animates[0], "B":animates[1], "C":animates[2], "D":animates[3], "1":inanimates[0], "2":inanimates[1]}

	#get sentences from csv file
	global sentences
	trials = csv.reader(open('JGItLearnV2_trials.csv'), delimiter='\t')
	sentences = [] #Each row in sentences is a list
	#[verb, subject, object, case marker, word order, block]	
	for item in trials:
		sentences.append(item)

	for prod_trials in range(lower, upper+1):
		field = "Answer.trial{0}".format(prod_trials)
		result = subject[field].split("|")
		sentence = result[2]
		response = result[4]
		language[sentence] = response

	#create blocks - flow of experiment
	intro()
	learn_nouns_1(False) #true: learn animate nouns only. false: learn animates + inanimates
	test_nouns_1(False) #should be same as input to learn_nouns1 method
	learn_sentences_short(2) #takes block number as parameter
	test_sentences_short(2, False) #takes block number, feedback loop as parameters
	learn_sentences_short(3)
	test_sentences_short(3, False) #False: no feedback, no looping
	learn_sentences_4()
	lexical_production()
	speak_1_and_2()
	end()

def switch(my_list, repetitions, verbs):
	if repetitions < 0:
		repetitions *= -1
		verbs = not(verbs)
	for each_swap in range(repetitions):
		if verbs:
			my_list.insert(0,my_list.pop())	
		else:
			my_list.append(my_list.pop(0))

def write(keyword, msg):	
	output.write("{0}\t{1}\n".format(keyword, msg))

def translate(sentence):
	#sentence must be of the form: [verb, subject, object, case marker, word order, block]
	#used for production trials, randomly chooses a sentence out of previous generation's language
	if len(language) > 0:
		return (language.values())[int(random.random()*len(language))]
	else:
		return 'none'

def create_distractor(subj, obj, verb):
	if inanimates.count(obj) == 0:
			#object is animate, reverse subject and object in distractor
			distractor = "{0}_{1}_{2}".format(obj, subj, verb)
	else:
		if random.random() > .50:
			#object is inanimate, use other inanimate as distractor
			distractor_obj = random.choice(inanimates)
			while (distractor_obj == obj):
				distractor_obj = random.choice(inanimates)
		else:
			#object is inanimate, use animate as distractor
			distractor_obj = random.choice(animates)
			while (distractor_obj == subj):
				distractor_obj = random.choice(animates)
		distractor = "{0}_{1}_{2}".format(subj, distractor_obj, verb)
	return distractor				

def intro():
	write("#", out_filename)
	write("#", "code for webag-iterative learning-jgutman")

	#write("if", "@game = 0") #disallow participants who have done this before
	write("msg", "Welcome to the language game! We're going to find out how good you are at learning new languages!")
	write("msg", "You can learn a language just by looking at the videos and pictures I show you, while listening to the words.")
	write("msg", "You can help advance our scientific understanding of language by playing along, so just remember to pay attention and try your best!")
	write("msg", "Put on your headphones and make sure the volume is turned up!")
	write("msg", "The right side bar will show you how much of the game is still to be played. Try repeating the words out loud after you hear them: it makes it easier!")
	write("msg", "Even saying them quietly to yourself can help.")

	#write("else", "")
	#write("msg", "Oh no! It seems that you have aready participated in one of our language games.")
	#write("msg", "Unfortunately you can only participate in 1 game. Please cancel this HIT.")
	#write("goto", "end")
	#write("endif", "")

def learn_nouns_1(animate_only):
	write("msg", "Okay, let's get started! We'll start off easy and just show you things one at a time so you can learn their names. You can listen as many times as you like by clicking \"Replay\".")
	write("sec", "Learn 1")
	write("label", "learn_nouns_1")
	
	noun_trials_half = []
	for agent in animates:
		noun_trials_half.append(agent)

	if not animate_only:
		for theme in inanimates:
			noun_trials_half.append(theme)

	noun_trials = []
	random.shuffle(noun_trials_half)
	noun_trials.extend(noun_trials_half)
	random.shuffle(noun_trials_half)
	noun_trials.extend(noun_trials_half)
	
	for trial in noun_trials:
		write("exp", "{0}_noun\t{1}".format(trial, lexicon[trial]))	
	write("end", "")

def test_nouns_1(animate_only):
	write("msg", "OK, let's see how many you can remember! I'll show you two characters at a time. Click on the character or object that matches the words you are hearing.")
	write("sec", "Understand 1")
	
	noun_trials_half = []
	nouns = []
	nouns.extend(animates)
	if not animate_only:
		nouns.extend(inanimates)

	for agent in animates:
		noun_trials_half.append(agent)

	if not animate_only:
		for theme in inanimates:
			noun_trials_half.append(theme)

	noun_trials = []
	random.shuffle(noun_trials_half)
	noun_trials.extend(noun_trials_half)
	random.shuffle(noun_trials_half)
	noun_trials.extend(noun_trials_half)

	for trial in noun_trials:
		random.shuffle(nouns)
		while nouns[0] == trial:
			random.shuffle(nouns)
		distractor = nouns[0]
		write("discrim", "{0}_noun\t{1}_noun\t{2}".format(trial, distractor, lexicon[trial]))
	
	write("end", "")
	correct = u"\u007bcorrect(\"Understand 1\")\u007d"
	target = len(noun_trials)
	write("msg", 'You got ${0} out of {1} right.'.format(correct, len(noun_trials)))
	write("if", "correct(\"Understand 1\") = {0}".format(target))
	write("msg", "Well done!")
	write("endif", "")
	write("if", "correct(\"Understand 1\") > {0}".format(target))
	write("msg", "Well done!")
	write("endif", "")
	write("if", "correct(\"Understand 1\") < {0}".format(target))
	write("msg", "Can you do better? Let's listen to the names one more time!")
	write("goto", "learn_nouns_1")
	write("endif", "")

def lexical_production():
	write("msg", "Okay, now let's try speaking! We'll start off easy and just show you things one at a time so you can say their names.")
	write("msg", "I'll show the words you can choose from at the top of the screen. Click on them to name the character or object in the picture and then click Continue.")
	write("sec", "Speak 1")
	write("label", "noun_prod")
	
	noun_trials = []
	noun_trials.extend(animates)
	noun_trials.extend(inanimates)
	random.shuffle(noun_trials)
	
	for trial in noun_trials:
		num = random.randint(0, len(sentences)-1)
		write("prod1","{0}_noun\t{1}".format(trial, lexicon[trial]))
	write("end", "")
	
	correct = u"\u007bcorrect(\"Speak 1\")\u007d"
	target = len(noun_trials)
	write("msg", 'You got ${0} out of {1} right.'.format(correct, len(noun_trials)))
	write("if", "correct(\"Speak 1\") = {0}".format(target))
	write("msg", "Well done!")
	write("goto", "sent_prod")
	write("endif", "")
	write("if", "correct(\"Speak 1\") > {0}".format(target))
	write("msg", "Well done!")
	write("goto", "sent_prod")
	write("endif", "")
	write("if", "correct(\"Speak 1\") < {0}".format(target))
	write("msg", "Can you do better? Let's listen to the names one more time!")
	
	noun_trials_half = []
	for agent in animates:
		noun_trials_half.append(agent)
	for theme in inanimates:
		noun_trials_half.append(theme)

	noun_trials = []
	random.shuffle(noun_trials_half)
	noun_trials.extend(noun_trials_half)
	random.shuffle(noun_trials_half)
	noun_trials.extend(noun_trials_half)
	
	for trial in noun_trials:
		write("exp", "{0}_noun\t{1}".format(trial, lexicon[trial]))	
	write("goto", "noun_prod")
	write("endif", "")

def learn_sentences_short(block_num):
	if block_num > 2:
		write("msg", "Now I'll show you some more sentences in the language! Remember, some of the words describe what's going on in the scene, not just which people or things are there.")
		trial_num = range(16,24)
	else:
		write("msg", "Now I'll show you some sentences in the language! Some of the words describe what's going on in the scene, not just which people or things are there.")
		trial_num = range(8)

	write("msg", "You'll need to pay attention to who is doing what each time. Good luck!")
	write("sec", "Learn {0}".format(block_num))
	write("label", "learn_sentences_{0}".format(block_num))

	for trial in trial_num:
	#[verb, subject, object, case marker, word order, block]
		item = sentences[trial]
		subj = abbreviation[item[1]]
		obj = abbreviation[item[2]]
		verb = abbreviation[item[0]]
		target = "{0}_{1}_{2}".format(subj, obj, verb)
		write("exp","{0}\t{1}".format(target, language[target]))
	write("end", "")

def test_sentences_short(block_num, do_feedback_loop):
	correct_ratio = .75
	if block_num > 2:
		trial_num = range(16,24)
	else:
		trial_num = range(8)

	write("msg", "Now you'll see two videos and hear a sentence in the language. Click on the video that correctly depicts the meaning of the sentence.")
	write("msg", "You might not know the answer yet, just guess.")
	write("msg", "Try to respond as quickly and as accurately as possible.")
	name = "Understand {0}".format(block_num)
	write("sec", name)

	comp_block = []

	for trial in trial_num:
		#[verb, subject, object, case marker, word order, block]
		item = sentences[trial]
		subj = abbreviation[item[1]]
		obj = abbreviation[item[2]]
		verb = abbreviation[item[0]]
		target = "{0}_{1}_{2}".format(subj, obj, verb)
		distractor = create_distractor(subj, obj, verb)
		comp_block.append("{0}\t{1}\t{2}".format(target, distractor, language[target]))		

	random.shuffle(comp_block)
	for trial in comp_block:
		write("discrim", trial)
	write("end", "")
	
	#test performance and loop back if necessary
	if do_feedback_loop:
		correct = u"\u007bcorrect(\"xxx\")\u007d"
		correct.replace("xxx", name)
		target = int(correct_ratio*len(trial_num))
		write("msg", 'You got ${0} out of {1} right.'.format(correct, len(trial_num)))
		write("if", "correct(\"{0}\") > {1}".format(name, target))
		write("msg", "Feeling bored? Don't give up! It'll get more challenging!")
		write("endif", "")
		write("if", "correct(\"{0}\") = {1}".format(name, target))
		write("msg", "Feeling bored? Don't give up! It'll get more challenging!")
		write("endif", "")
		write("if", "correct(\"{0}\") < {1}".format(name, target))
		write("msg", "Feeling a bit overwhelmed? Don't give up! It'll get easier!")
		write("msg", "Let's listen to these sentences one more time!")
		write("goto", "learn_sentences_{0}".format(block_num))
		write("endif", "")

def learn_sentences_4():
	write("msg", "Now let's see some more sentences in the language.")
	write("msg", "This time I'll show you some new actions, along with the old ones.")
	write("msg", "Remember to repeat the sentences to yourself if it helps.")
	write("sec", "Learn 4")

	learn_block = []
	trial_num = range(8, 16)
	trial_num.extend(range(24, 40))

	for trial in trial_num:
		#[verb, subject, object, case marker, word order, block]
		item = sentences[trial]
		subj = abbreviation[item[1]]
		obj = abbreviation[item[2]]
		verb = abbreviation[item[0]]
		target = "{0}_{1}_{2}".format(subj, obj, verb)
		#print target
		learn_block.append([target, language[target]])

	random.shuffle(learn_block)
	for trial in learn_block:
		write("exp","{0}\t{1}".format(trial[0], trial[1]))
	write("end","")	

def speak_1_and_2():
	#[verb, subject, object, case marker, word order, block]
	#V1>V4 ; V2>V1 ; V3>V2 ; V4>V3
	#A>B ; B>C ; C>D ; D>A ; 1>2 ; 2>1
	#kah>zub ; zub>kah
	
	for trial in sentences:
		if trial[0] == "V1":
			trial[0] = "V4"
		elif trial[0] == "V2":
			trial[0] = "V1"
		elif trial[0] == "V3":
			trial[0] = "V2"
		else:
			trial[0] = "V3"

		if trial[1] == "A":
			trial[1] = "B"
		elif trial[1] == "B":
			trial[1] = "C"
		elif trial[1] == "C":
			trial[1] = "D"
		else:
			trial[1] = "A"

		if trial[2] == "A":
			trial[2] = "B"
		elif trial[2] == "B":
			trial[2] = "C"
		elif trial[2] == "C":
			trial[2] = "D"
		elif trial[2] == "D":
			trial[2] = "A"
		elif trial[2] == "1":
			trial[2] = "2"
		else: 
			trial[2] = "1"
	
	write("msg", "Now it gets harder! This time, you need to say who is doing what to whom.")
	write("msg", "I'll show the words you can choose from at the top of the screen. Click on them to make a sentence.")
	write("msg", "Your words will appear under the video. If you make a mistake, you can delete a word by clicking on it.")
	write("msg", "Listen to your sentence by clicking \"Replay\" and click on \"Continue\" when you're happy with it. Good luck!")
	write("sec", "Speak 2")
	write("label", "sent_prod")

	random.shuffle(sentences)
	for trial in range(len(sentences)/2):
		item = sentences[trial]
		subj = abbreviation[item[1]]
		obj = abbreviation[item[2]]
		verb = abbreviation[item[0]]
		target = "{0}_{1}_{2}".format(subj, obj, verb)
		write("prod","{0}\t{1}".format(target, translate(item))) #is translate(item) necessary?
		#write("prod","{0}".format(target))
	write("end", "")		
		
	write("msg", "OK! Almost done! We are at the last stage of the game.")
	write("msg", "Once again you need to say who is doing what to whom.")
	write("msg", "I'll show the words you can choose from at the top of the screen. Click on them to make a sentence.")
	write("msg", "Your words will appear under the video. If you make a mistake, you can delete a word by clicking on it.")
	write("msg", "Listen to your sentence by clicking \"Replay\" and click on \"Continue\" when you're happy with it.") 
	write("sec", "Speak 3")
	
	for trial in range(len(sentences)/2, len(sentences)):
		item = sentences[trial]
		subj = abbreviation[item[1]]
		obj = abbreviation[item[2]]
		verb = abbreviation[item[0]]
		target = "{0}_{1}_{2}".format(subj, obj, verb)
		write("prod","{0}\t{1}".format(target, translate(item))) #is translate(item) necessary?
		#write("prod","{0}".format(target))
	write("end", "")
	
	write("msg", "That's the end of the game! Thanks for partcipating!")
	write("msg", "Hope you had fun! Please press the Submit button now.")			

def end():
	return

main()
