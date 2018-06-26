#!/usr/bin/env python3

import argparse
import dateutil.parser
from datetime import timedelta
from tkinter import filedialog
from tkinter import *

def shiftTimeGPX(filename, shift):
    output = open(filename.split(".")[0] + "-adjusted.gpx", "w")
    with open(filename) as f:
        for line in f:
            if "<time>" in line:
                s = line.split("T")
                time = s[1].split("Z")[0].split(":")
                date = s[0].replace('<time>', '').strip()
                indentation = s[0].split("<")[0]

                newHour = int(time[0]) + shift
                if newHour < 0:
                    date  = (dateutil.parser.parse(date) - timedelta(1)).isoformat().split("T")[0]
                    newHour = 24 + newHour
                elif newHour >= 24:
                    date = (dateutil.parser.parse(date) + timedelta(1)).isoformat().split("T")[0]
                    newHour = 0 + newHour - 24

                newHourStr = str(newHour)
                if newHour < 10:
                    newHourStr = "0" + newHourStr

                output.write(indentation + "<time>" + date + "T" + newHourStr + ":" + time[1] + ":" + time[2] + "Z</time>\n")

            else:
                output.write(line)
    output.close()


class window:
    def __init__(self, master):
        self.master = master

        self.master.wm_title("GPX TZ")
        self.master.attributes('-type', 'dialog')

        self.fileLabel = Label(master, text = "GPX file:")

        self.fileEntryText = StringVar()
        self.fileEntry = Entry(self.master, textvariable=self.fileEntryText, width = 50)

        self.button = Button(self.master, text="Select GPX file", command=self.fileSelection)

        self.shiftLabel = Label(master, text = "Shift:")
        self.shiftEntryText = StringVar()
        self.shiftEntry = Entry(self.master, textvariable=self.shiftEntryText, width = 10)
        self.shiftEntryText.set("-2")

        self.runButton = Button(self.master, text="Change timezone!", command=self.changeTimezone)

        self.fileLabel.pack(anchor = W)
        self.fileEntry.pack()
        self.button.pack(anchor = E)
        self.shiftLabel.pack(anchor = W)
        self.shiftEntry.pack(anchor = W)
        self.runButton.pack(anchor = E)
        
    def fileSelection(self):
        self.master.filename =  filedialog.askopenfilename(initialdir = ".",title = "Select file",filetypes = (("gpx files","*.gpx"),("all files","*.*")))
        self.fileEntryText.set(self.master.filename)

    def changeTimezone(self):
        print(self.fileEntryText.get())
        shiftTimeGPX(self.fileEntryText.get(), int(self.shiftEntryText.get()))
        self.master.destroy()
        
    def validate(self, action, index, value_if_allowed, prior_value, text, validation_type, trigger_type, widget_name):
        if text in '0123456789.-+':
            try:
                float(value_if_allowed)
                return True
            except ValueError:
                return False
        else:   
            return False


parser = argparse.ArgumentParser(description='Change the timezone of a GPX file')
parser.add_argument("--file", dest = "filename", type = str, required = False,
                    help='Path of the GPX file')
parser.add_argument("--shift", dest = "shift", type = int, required = False,
                    help='Number of hours to be shifted')
args = parser.parse_args()

if (args.filename != None and args.shift != None):
    shiftTimeGPX(args.filename, args.shift)
else:
    root = Tk()
    window(root)
    mainloop()
