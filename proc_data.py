#Filename: proc_data.py
#Directory: /home/jackie/Desktop
#Author: Jacqueline Gutman
#Last modified: April 23, 2011

import csv, sys, random

num_gens = int(sys.argv[1])
midname = 'combinedData_prelim.csv'
endname = 'data_anal_for_excel.csv'
combinedData = csv.writer(open(midname, 'wb'),dialect='excel')

for gen in range(1,num_gens+1):
	for chain in range(1,12):
		filename = "gen{0}/V2G{0}C{1}.csv".format(gen, chain)
		#print filename
		currData = csv.reader(open(filename, 'rb'),dialect='excel')
		row = currData.next()
		row = currData.next()
		while row[16]=="Rejected":
			row = currData.next()
		row_list = [gen, chain]
		row_list.extend(row)
		#print gen, chain, len(row_list)
		combinedData.writerow(row_list)

data = csv.reader(open(midname, 'rb'),dialect='excel')
output = csv.writer(open(endname, 'wb'),dialect='excel')

header = ['WorkerID', 'Chain', 'Generation', 'TrialNum', 'CorrectedTrialNum',
	'AgentEnglish', 'ThemeEnglish', 'VerbEnglish', 'CorrectAgent', 'CorrectTheme',
	'CorrectVerb', 'Production', 'ContainsAgent', 'ContainsTheme', 'ContainsVerb', 
	'HasLexicalErrors', 'NumCaseMarkers', 'NumKahMarkers', 'NumZubMarkers', 
	'ThemeAnimacy',	'ThemeGender', 'WordOrder', 'KahPosition', 'ZubPosition',
	'ResponseTruncated']	
output.writerow(header)	

lexicon = {'chef':'lombur', 'ref':'melnawg', 'mountie':'flugit', 
	'50swoman':'slagum', 'singer':'gentif', 'cowgirl':'dilbuh',
	'barstool':'tombat', 'bookstand':'nagid', 'punch':'bliffen', 
	'knockover':'zamper', 'hug':'dacin', 'headbutt':'kleidum'}

num_participants = 0		
for row in data: #one row per participant
	num_prod_trials = 0
	verb_errors = 0
	discrim_errors = 0
	discrim_total = 0
	num_trunc = 0
	too_short = 0
	num_participants += 1
	generation = row[0]
	chain = row[1]
	workerID = row[17]
	nickname = 'Worker {0}: C{1}G{2}'.format(workerID,chain, generation)
	print nickname, len(row)

	if int(chain)==11:
		print #'breaking'
	else:
		for field in row: #one field per trial
			#print field
			if field.count('|discrim|') > 0:
				discrim_total += 1
				answer = field.split('|')
				if answer[5]=='F':
					discrim_errors += 1
			elif field.count('|prod|') > 0:
				num_prod_trials += 1
				answer = field.split('|')

				trial_num = answer[0] #range from 149-168, 174-193
				if int(trial_num) <= 168:
					corrected_trial_num = int(trial_num)-148
				else:
					corrected_trial_num = int(trial_num)-153

				description = answer[2]
				sentence = description.split('_')
				agent = sentence[0] #correct english agent
				theme = sentence[1] #correct english theme
				verb = sentence[2] #correct english verb
				response = answer[4] #participant's response
			
				write_to_csv = [workerID, chain, generation, trial_num, 
					corrected_trial_num, agent, theme, verb, lexicon[agent], 
					lexicon[theme], lexicon[verb], response]
				
				contains_agent = (response.count(lexicon[agent]) > 0)
				contains_theme = (response.count(lexicon[theme]) > 0)
				contains_verb = (response.count(lexicon[verb]) > 0)
				if not contains_verb:
					verb_errors += 1
				no_lexical_errors = contains_agent and contains_theme and contains_verb
			
				write_to_csv.extend([contains_agent, contains_theme, contains_verb,
					not(no_lexical_errors)])
			
				num_kahs = response.count('kah')
				num_zubs = response.count('zub')
				write_to_csv.extend([(num_kahs+num_zubs), num_kahs, num_zubs])
			
				gender = 'inanimate'
				animacy = not(theme=='barstool' or theme=='bookstand')
				if (theme=='ref' or theme=='chef' or theme=='mountie'):
					gender='male'
				elif (theme=='50swoman' or theme=='cowgirl' or theme == 'singer'):
					gender='female'
				words = response.split(' ')
			
				
			
				agent_index = 0
				theme_index = 0
				verb_index = 0
			
				#determines word order if no lexical errors
				if no_lexical_errors:
					agent_index = response.find(lexicon[agent])
					theme_index = response.find(lexicon[theme])
					verb_index = response.find(lexicon[verb])
			
				#determines word order if exactly one lexical error 
				#elif (not contains_agent) and contains_theme and contains_verb:
				#	if len(words) == 3+num_kahs+num_zubs:
				#		theme_index = words.index(lexicon[theme])
				#		verb_index = words.index(lexicon[verb])
				#		for word in words:
				#			if ((not word == lexicon[theme]) and 
				#			(not word == lexicon[verb]) and 
				#			(not word == 'kah') and (not word == 'zub')):
				#				agent_index = words.index(word)

				#elif contains_agent and (not contains_theme) and contains_verb:
				#	if len(words) == 3+num_kahs+num_zubs:
				#		agent_index = words.index(lexicon[agent])
				#		verb_index = words.index(lexicon[verb])
				#		for word in words:
				#			if ((not word == lexicon[agent]) and 
				#			(not word == lexicon[verb]) and 
				#			(not word == 'kah') and (not word == 'zub')):
				#				theme_index = words.index(word)
			
				elif contains_agent and contains_theme and (not contains_verb):
					if len(words) == 3+num_kahs+num_zubs:
						agent_index = words.index(lexicon[agent])
						theme_index = words.index(lexicon[theme])
						for word in words:
							if ((not word == lexicon[agent]) and 
							(not word == lexicon[theme]) and 
							(not word == 'kah') and (not word == 'zub')):
								verb_index = words.index(word)
				
				if agent_index < theme_index and theme_index < verb_index:
					word_order = 'SOV'
				elif agent_index < verb_index and verb_index < theme_index:
					word_order = 'SVO'
				elif theme_index < agent_index and agent_index < verb_index:
					word_order = 'OSV'
				elif theme_index < verb_index and verb_index < agent_index:
					word_order = 'OVS'
				elif verb_index < agent_index and agent_index < theme_index:
					word_order = 'VSO'
				elif verb_index < theme_index < agent_index:
					word_order = 'VOS'
					
				else:
					word_order = 'NA'
			
				kah_position = 'NA'
				zub_position = 'NA'
				
				if num_kahs == 1:
					kah_index = words.index('kah')
					if not kah_index == 0:
						previous = words[kah_index-1]
						if previous == lexicon[agent]:
							kah_position = 'subject'
						if previous == lexicon[theme]:
							kah_position = 'object'
						if previous == lexicon[verb]:
							kah_position = 'verb'
				
				if num_zubs == 1:
					zub_index = words.index('zub')
					if not zub_index == 0:
						previous = words[zub_index-1]
						if previous == lexicon[agent]:
							zub_position = 'subject'
						if previous == lexicon[theme]:
							zub_position = 'object'
						if previous == lexicon[verb]:
							zub_position = 'verb'

				truncated = False
				if len(words)<3:
					too_short += 1
				elif len(words)>4:
					print response
					words = [words[0],words[1],words[2],words[3]]
					truncated = True
					num_trunc += 1

				write_to_csv.extend([animacy, gender, word_order, kah_position, zub_position, truncated])
				output.writerow(write_to_csv)

	if int(chain)==11:
		print #'breaking'
	else:
		print 'trials', num_prod_trials, nickname
		print 'verb errors', verb_errors, nickname
		print 'omission errors', too_short, 'truncated', num_trunc, nickname
		print 'discrim errors', discrim_errors, 'of', discrim_total, nickname
		print #
