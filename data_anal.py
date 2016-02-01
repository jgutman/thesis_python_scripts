#Filename: data_anal.py
#Directory: /home/jackie/Downloads/all_generations
#Author: Jacqueline Gutman
#Last modified: April 23, 2011

import csv

combinedData = csv.writer(open('combinedData.csv', 'wb'))

for generation in range(1,2):
	for chain in range(1,11):
		filename = 'V2G{0}C{1}.csv'.format(generation, chain)
		currData = csv.reader(open(filename, 'rb'))
		row = currData.next()
		row = currData.next()
		row_list = [generation, chain]
		row_list.extend(row)
		print row_list
		combinedData.writerow(row_list)
		
