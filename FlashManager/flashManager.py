#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
from tkinter import * 
from tkinter import filedialog

fenetre = Tk()

label = Label(fenetre, text="Hello World")
label.pack()

repertoire = filedialog.askdirectory(
	parent = fenetre,
	initialdir = "/",
	title = 'Choisissez un repertoire')

if len(repertoire) > 0:
    print ("vous avez choisi le repertoire %s" % repertoire)


fenetre.mainloop()
