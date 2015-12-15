#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json

class ConfManager:
	def __init__(self, fileName):
		self.fileName = fileName
		self.conf = None

	def loadConf(self):
		if os.path.isfile(self.fileName):
			try:
				inputFile = open(self.fileName, "r", encoding='utf-8')
				self.conf = json.loads(inputFile.read())
				inputFile.close()
			except IOError:
				self.conf = {}
		else:
			print(self.fileName, "not isfile!")
			self.conf = {}

	def saveConf(self):
		try:
			outputFile = open(self.fileName, "w", encoding='utf-8')
			json.dump(self.conf, outputFile, sort_keys = True, indent = 4)
			outputFile.close()
		except IOError:
			print('Cannot open {}'.format(self.fileName))
		
	def getConf(self):
		if self.conf == None:
			self.loadConf()
		return self.conf

	def setConf(self, conf, save=False):
		self.conf = conf
		if save:
			self.saveConf()


# Call of the main function in stand alone execution
if __name__ == "__main__":
	# UT
	confMgr = ConfManager("conf.json")
	conf = confMgr.getConf()
	print(conf)
	conf["toto"] = 5
	conf["tata"] = 8
	confMgr.setConf(conf)
	conf = confMgr.getConf()
	print(conf)
	confMgr.saveConf()
	os.remove("conf.json")
