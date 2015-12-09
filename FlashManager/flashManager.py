#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
from tkinter import * 
from tkinter import filedialog
import os

class Window:
	def __init__(self, master):
		self.master = master
		self.flashDir = StringVar()
		self.flashDir.set("C:/flash")
		self.flashRepo = StringVar()
		self.flashRepo.set("C:/flash_repository")
		self.flashRepo.trace("w",
			lambda name, index, mode: self.repoEntryUpdated())

		# Flash frame
		self.flashFrame = Frame(master)
		self.flashFrame.pack()
		# Flash label
		self.chooseFlashLabel = Label(self.flashFrame, text="Flash directory:")
		self.chooseFlashLabel.pack(side=TOP, anchor=NW)
		# Flash input
		self.flashEntry = Entry(self.flashFrame, textvariable=self.flashDir,
			width=60)
		self.flashEntry.pack(side=LEFT)
		# Flash button
		self.chooseFlashButton = Button(self.flashFrame, text="Open",
			command=lambda: self.selectDir(self.flashDir))
		self.chooseFlashButton.pack(side=RIGHT)

		# Repo frame
		self.repoFrame = Frame(master)
		self.repoFrame.pack()
		# Flash repo label
		self.chooseRepoLabel = Label(self.repoFrame, text="Flash repository:")
		self.chooseRepoLabel.pack(side=TOP, anchor=NW)
		# Flash repo input
		self.repoEntry = Entry(self.repoFrame, textvariable=self.flashRepo, width=60)
		self.repoEntry.pack(side=LEFT)
		# Flash repo button
		self.chooseRepoButton = Button(self.repoFrame, text="Open",
			command=lambda: self.selectDir(self.flashRepo))
		self.chooseRepoButton.pack(side=RIGHT)

		# List frame
		self.listFrame = Frame(master)
		self.listFrame.pack(anchor=NW)
		# list label
		self.listLabel = Label(self.listFrame, text="Select the flash you need:")
		self.listLabel.pack(anchor=NW)		
		# List of flash directories
		self.flashList = Listbox(self.listFrame, width=60)
		self.flashList.pack()
		# Select button
		self.selectButton = Button(self.listFrame, text="Select",
			command=lambda: self.selectFlash())
		self.selectButton.pack()

		self.fillFlashList()

	def selectDir(self, inputEntry):
		folder = filedialog.askdirectory(
			parent = self.master,
			initialdir = "/",
			title = 'Select a folder')

		inputEntry.set(folder)


	def repoEntryUpdated(self):
		self.fillFlashList()

	def fillFlashList(self):
		self.flashList.delete(0, END)
		if os.path.exists(self.flashRepo.get()):
			for entry in os.scandir(self.flashRepo.get()):
				if entry.is_dir():
					self.flashList.insert(END, entry.name)

	def selectFlash(self):
		curselection = self.flashList.curselection()
		if len(curselection) > 0:
			curselection = curselection[0]
			print(self.flashList.get(curselection))


# Main
root = Tk()
root.title("Flash manager")
window = Window(root)
root.mainloop()
