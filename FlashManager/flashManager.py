#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
# Add my python workspace for Windows
sys.path.insert(0, "C:/Workspace/Python")

from tkinter import * 
from tkinter import filedialog
from tkinter.messagebox import *
import os
import shutil
from utils.confManager import *

class Window(Frame):
	def __init__(self, confMgr, master=None):
		Frame.__init__(self, master)
		self.grid(sticky=N+S+E+W)

		self.confMgr = confMgr
		self.conf = confMgr.getConf()
		self.initConf()
		self.flashRoot = StringVar()
		self.flashRoot.set(self.conf.get("flashRoot"))
		self.flashRoot.trace("w",
			lambda name, index, mode: self.flashEntryUpdated())
		self.flashRepo = StringVar()
		self.flashRepo.set(self.conf.get("flashRepo"))
		self.flashRepo.trace("w",
			lambda name, index, mode: self.repoEntryUpdated())

		# Define a new callback for closing main window
		self.winfo_toplevel().protocol("WM_DELETE_WINDOW",
			self.onClosing)

		# Create components
		self.createComponents()
		# Set the layout
		self.setLayout()
		# Fill the flash list
		self.fillFlashList()

	# Create all widgets
	def createComponents(self):
		# Flash frame
		self.flashFrame = Frame(self)
		# Flash label
		self.chooseFlashLabel = Label(self.flashFrame,
			text="Root of the flash directory:")
		# Flash input
		self.flashEntry = Entry(self.flashFrame,
			textvariable=self.flashRoot)
		# Flash button
		self.chooseFlashButton = Button(self.flashFrame, text="Open",
			command=lambda: self.selectDir(self.flashRoot))

		# Repo frame
		self.repoFrame = Frame(self)
		# Flash repo label
		self.chooseRepoLabel = Label(self.repoFrame,
			text="Flash repository:")
		# Flash repo input
		self.repoEntry = Entry(self.repoFrame,
			textvariable=self.flashRepo, width=60)
		# Flash repo button
		self.chooseRepoButton = Button(self.repoFrame, text="Open",
			command=lambda: self.selectDir(self.flashRepo))

		# List frame
		self.listFrame = Frame(self)
		# list label
		self.listLabel = Label(self.listFrame,
			text="Flash directories of your repository:")
		# List of flash directories
		self.flashList = Listbox(self.listFrame, width=60)
		# Select button
		self.selectButton = Button(self.listFrame, text="Select",
			command=self.selectFlash)

	# Organize the way to display all widgets
	def setLayout(self):
		window = self.winfo_toplevel()
		window.columnconfigure(0, weight=1)
		window.rowconfigure(0, weight=1)
		self.columnconfigure(0, weight=1)
		self.rowconfigure(2, weight=1)

		self.flashFrame.columnconfigure(0, weight=1)
		self.flashFrame.grid(column=0, row=0, padx=5, pady=5, sticky=E+W)
		self.chooseFlashLabel.grid (column=0, row=0, sticky=NW)
		self.flashEntry.columnconfigure(0, weight=1)
		self.flashEntry.grid       (column=0, row=1, sticky=E+W)
		self.chooseFlashButton.grid(column=1, row=1)

		self.repoFrame.columnconfigure(0, weight=1)
		self.repoFrame.grid(column=0, row=1, padx=5, pady=5, sticky=E+W)
		self.chooseRepoLabel.grid (column=0, row=0, sticky=NW)
		self.repoEntry.columnconfigure(0, weight=1)
		self.repoEntry.grid       (column=0, row=1, sticky=E+W)
		self.chooseRepoButton.grid(column=1, row=1)

		self.listFrame.columnconfigure(0, weight=1)
		self.listFrame.rowconfigure(1, weight=1)
		self.listFrame.grid(column=0, row=2, padx=5, pady=5, sticky=N+S+E+W)
		self.listLabel.grid   (column=0, row=0, sticky=NW)	
		self.flashList.columnconfigure(0, weight=1)
		self.flashList.rowconfigure(0, weight=1)
		self.flashList.grid   (column=0, row=1, sticky=N+S+E+W)
		self.selectButton.grid(column=0, row=2)

	# Create missing parameters in conf and set them with default values
	def initConf(self):
		if not self.conf.get("flashRoot"):
			self.conf["flashRoot"] = "C:"
		if not self.conf.get("flashRepo"):
			self.conf["flashRepo"] = "C:/flash_repository"

	# Displays a file dialog to select a directory
	def selectDir(self, inputEntry):
		folder = filedialog.askdirectory(
			parent = self.master,
			initialdir = "/",
			title = 'Select a folder')

		inputEntry.set(folder)

	def repoEntryUpdated(self):
		self.fillFlashList()
		self.conf["flashRepo"] = self.flashRepo.get()

	def flashEntryUpdated(self):
		self.conf["flashRoot"] = self.flashRoot.get()

	def fillFlashList(self):
		self.flashList.delete(0, END)
		if os.path.exists(self.flashRepo.get()):
			for entry in os.scandir(self.flashRepo.get()):
				if entry.is_dir():
					self.flashList.insert(END, entry.name)

	def selectFlash(self):
		curselection = self.flashList.curselection()
		if len(curselection) == 0:
			showwarning('Warning', 'Please select a flash directory.')
		else:
			selectedDir = self.flashRepo.get() + "/" + self.flashList.get(
				curselection[0])
			flashDir = self.flashRoot.get() + "/flash"

			try:
				shutil.rmtree(flashDir)
			except Exception as e:
				showerror("Error", e)
			else:
				try:
					shutil.copytree(selectedDir, flashDir)
				except Exception as e:
					showerror("Error", e)

	def onClosing(self):
		self.confMgr.setConf(self.conf, True)
		self.master.destroy()

# Main
confMgr = ConfManager("conf.json")

window = Window(confMgr)
window.master.title("Flash manager")
window.master.mainloop()
