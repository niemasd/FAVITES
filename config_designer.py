#! /usr/bin/env python3
'''
Design FAVITES Configuration Files via GUI
'''
from urllib.request import urlopen
from tkinter.filedialog import asksaveasfile
import tkinter as tk
ML_URL = "https://raw.githubusercontent.com/niemasd/FAVITES/master/modules/FAVITES_ModuleList.json"
HEADER = "FAVITES Configuration File Designer"
MODULES = ['ContactNetworkGenerator','SeedSelection','SeedSequence','EndCriteria','TransmissionTimeSample','TransmissionNodeSample','NodeEvolution','SequenceEvolution','SourceSample','NumTimeSample','TimeSample','NumBranchSample','TreeUnit','NodeAvailability','Sequencing']
ML = eval(urlopen(ML_URL).read().decode())
WIDTH = max(len(e) for m in ML for e in ML[m])

# initialize GUI and title
root = tk.Tk()
root.title(HEADER)
tk.Label(root, text=HEADER).pack()
choice = {m:tk.StringVar(root) for m in MODULES}

# helper function to save file
def save_file():
    out = {}
    for m in MODULES:
        out[m] = choice[m].get()
    f = tk.filedialog.asksaveasfile(mode='w', defaultextension=".json")
    f.write(str(out))
    f.close()

# initialize grid
mainframe = tk.Frame(root)
mainframe.grid(column=0, row=0, sticky=(tk.N,tk.W,tk.E,tk.S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)
mainframe.pack(pady=20, padx=10)

# create dropdowns for modules
for i,m in enumerate(MODULES):
    dropdown = tk.OptionMenu(mainframe, choice[m], *sorted(ML[m].keys()))
    dropdown.config(width=WIDTH)
    dropdown.grid(row=i+1, column=1)
    tk.Label(mainframe, text=m).grid(row=i+1, column=0)

# create save button
tk.Button(root, text="Save Config File", command=save_file).pack()

# run main loop to make window display
root.mainloop()