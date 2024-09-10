from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from pySmartDL import SmartDL
import os

# Filedialog Box
def fileDialogBox():
    filename = filedialog.asksaveasfilename()
    dirname = filedialog.askdirectory()

# Download Now
def download(url, dest):
    # URL to Download from
    url = str(downloadFrom.get())
    # File Save Location
    dest = str(saveLocation.get())

    obj = SmartDL(url, dest)
    obj.start()
    path = obj.get_dest()

root = Tk()
root.title("Python Download Manager")

# Window Size
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

# Variable's Required
downloadFrom = StringVar()
saveLocation = StringVar()

# UI Functions
url_entry = ttk.Entry(mainframe, width = 50, textvariable = downloadFrom)
url_entry.grid(column = 2, row = 5, sticky=(W, E))
ttk.Label(mainframe, text="URL:- ").grid(column = 1, row = 5, sticky = E)

loc_entry = ttk.Entry(mainframe, width = 48, textvariable = saveLocation)
loc_entry.grid(column = 2, row = 8, stick = (W, E))
ttk.Label(mainframe, text = "Download\nLocation:- ").grid(column = 1, row = 8, sticky = E)

def callback(downloadFrom, saveLocation):
    os.system("downloadNow.py")

ttk.Button(mainframe, text="Download", command = lambda: callback(downloadFrom, saveLocation)).grid(column = 2, row = 13, sticky = E)

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

root.mainloop()
