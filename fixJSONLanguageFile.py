#!/usr/bin/python3
# coding: utf-8

import os
import json
import sys, getopt

def main(argv):
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
		# fileName = "localizables.en_US"
		# fileName = "localizables.test"
		fileName = "localizables.en_US_ori"
		# fileName = "localizables.en_US_bad"
		inputFileName = BASE_DIR + "/" + fileName + ".json"

	if outputFileName == "":
		outputFileName = inputFileName.replace('.json', '_m.json')

	try:
		inputFile = open(inputFileName, "r", encoding='utf-8')
	except IOError:
		print('Cannot open', inputFileName)
		sys.exit()

	try:
		jsonObj = json.loads(inputFile.read())
	except UnicodeDecodeError as e:
		print(e)
		startIndex = e.args[2] - 10
		endIndex = e.args[2] + 20
		print(e.args[1][startIndex:endIndex])
	except json.decoder.JSONDecodeError as e:
		print(e)
	except ValueError as e:
		print(type(e))
		print(e)
	else:
		try:
			outputFile = open(outputFileName, "w", encoding='utf-8')
		except IOError:
			print('Cannot open', outputFileName)
		else:
			json.dump(jsonObj, outputFile, sort_keys = True, indent = 4)
			outputFile.close()

	inputFile.close()


if __name__ == "__main__":
	main(sys.argv[1:])
