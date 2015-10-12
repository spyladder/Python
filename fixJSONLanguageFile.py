#!/usr/bin/python3
# coding: utf-8

import os
import json

BASE_DIR = os.getcwd()
# fileName = "localizables.en_US"
# fileName = "localizables.test"
# fileName = "localizables.en_US_ori"
fileName = "localizables.en_US_bad"
inputFile = open(BASE_DIR + "/" + fileName + ".json", "r")

try:
	jsonObj = json.load(inputFile)
	with open(BASE_DIR + "/" + fileName + "_m.json", "w") as outputFile:
		json.dump(jsonObj, outputFile, sort_keys = True, indent = 4)
except ValueError as e:
	print(e)

inputFile.close()
