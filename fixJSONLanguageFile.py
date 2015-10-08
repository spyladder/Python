#!/usr/bin/python3
# coding: utf-8

import json

BASE_DIR = "C:\\WORKSPACE\\RunMyMail_Trunk\\WebApps\\browser\\htmls\\REF\\Localization\\"
# fileName = "localizables.en_US"
# fileName = "localizables.test"
fileName = "localizables.en_US_ori"
inputFile = open(BASE_DIR + "\\" + fileName + ".json", "r")

# jsonStr = inputFile.read()
# print(json.loads(jsonStr))
try:
	jsonObj = json.load(inputFile)
	print(type(jsonObj))
	print(jsonObj)
except ValueError as e:
	print(e)


#for line in inputFile:


inputFile.close()


# dico = {}
# dico["nom"] = "heliot"
# dico["prenom"] = "julien"

# print (dico)

# a = 1
# b = a
# print(a, b)

# a = 3
# print(a, b)