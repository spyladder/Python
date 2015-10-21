#!/usr/bin/python3
# coding: utf-8

import os
import json
import sys, getopt

def main(argv):
	# Args management
	inputFileName = ""
	outputFileName = ""
	try:
		opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
	except getopt.GetoptError:
		print('Usage: fixJSONLanguage.py -i <inputfile> -o <outputfile>')
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-h':
			print('Usage: fixJSONLanguage.py -i <inputfile> -o <outputfile>')
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputFileName = arg
		elif opt in ("-o", "--ofile"):
			outputFileName = arg

	if inputFileName == "":
		BASE_DIR = os.getcwd()
		fileName = "localizables.de_DE_ori.json"
		# fileName = "localizables.test.json"
		# fileName = "localizables.en_US_ori.json"
		inputFileName = BASE_DIR + "/" + fileName

	if outputFileName == "":
		outputFileName = inputFileName.replace('.json', '_m.json')


	# Input file opening
	try:
		inputFile = open(inputFileName, "r", encoding='utf-8')
	except IOError:
		print('Cannot open', inputFileName)
		sys.exit()

	# File reading
	str = inputFile.read()

	# Remove an unexpected character (0xEFBBBF)
	trashChar = bytes.fromhex('efbbbf').decode()
	str = str.replace(trashChar, '')

	lines = str.split('\n')

	# JSON parsing
	# We try until no error remains
	# For each error found, a log is added in [inputFileName]_err.txt
	# and the line containing the error is removed from the JSON
	isOk = False
	errFile = None

	while not isOk:
		# Remove last comma before '}'
		str = str.replace(', \n}', ' \n}') 
		try:
			jsonObj = json.loads(str)
		except UnicodeDecodeError as e:
			print(e)
			startIndex = e.args[2] - 10
			endIndex = e.args[2] + 20
			print(e.args[1][startIndex:endIndex])
		except json.decoder.JSONDecodeError as e:
			print(e)
			print(e.colno, e.lineno, e.pos, e.msg)
			if errFile == None:
				errFile = open(inputFileName.replace('.json', '_err.txt'), "w", encoding='utf-8')
			errFile.write(lines[e.lineno-1] + '\n')
			errFile.write('-> Line %i, %s\n\n' % (e.lineno, e.msg))
			del lines[e.lineno-1]
			str = '\n'.join(lines)

		except ValueError as e:
			print(type(e))
			print(e)
		else:
			isOk = True
			try:
				outputFile = open(outputFileName, "w", encoding='utf-8')
			except IOError:
				print('Cannot open', outputFileName)
			else:
				json.dump(jsonObj, outputFile, sort_keys = True, indent = 4)
				outputFile.close()

	inputFile.close()
	if errFile != None:
		errFile.close()

# Call of the main function in stand alone execution
if __name__ == "__main__":
	main(sys.argv[1:])
