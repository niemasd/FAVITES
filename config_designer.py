#! /usr/bin/env python3
'''
Design FAVITES Configuration Files via GUI
'''
from urllib.request import urlopen
from tkinter.filedialog import asksaveasfile
from tkinter import font as tkfont
from webbrowser import open_new
import tkinter as tk
ML_URL = "https://raw.githubusercontent.com/niemasd/FAVITES/master/modules/FAVITES_ModuleList.json"
HEADER = "FAVITES Configuration File Designer"
MODULES = ['ContactNetwork','ContactNetworkGenerator','SeedSelection','SeedSequence','EndCriteria','TransmissionTimeSample','TransmissionNodeSample','NodeEvolution','SequenceEvolution','SourceSample','NumTimeSample','TimeSample','NumBranchSample','TreeUnit','NodeAvailability','Sequencing']
PARAMS = []
ML = eval(urlopen(ML_URL).read().decode())
WIDTH = max(len(e) for m in ML for e in ML[m])

# initialize GUI and title
root = tk.Tk()
root.title(HEADER)
header_label = tk.Label(root, text=HEADER)
header_label.config(font=("Helvetica", 32))
header_label.pack()
choice = {m:tk.StringVar(root) for m in MODULES}

# initialize grid
mainframe = tk.Frame(root)
mainframe.grid(column=0, row=0, sticky=(tk.N,tk.W,tk.E,tk.S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)
mainframe.pack(pady=20, padx=10)

# create dropdowns for modules
def go_to_module_page(event):
    open_new(r"https://github.com/niemasd/FAVITES/wiki/Module:-%s"%event.widget.cget("text"))
for i,m in enumerate(MODULES):
    dropdown = tk.OptionMenu(mainframe, choice[m], *sorted(ML[m].keys()))
    dropdown.config(width=WIDTH)
    dropdown.grid(row=i+1, column=1)
    label = tk.Label(mainframe, text=m, fg='blue', cursor='hand2')
    label.grid(row=i+1, column=0)
    label.bind("<Button-1>", go_to_module_page)

# create check button
def check_config():
    param_to_modules = {}
    error = None
    for m in MODULES:
        imp = choice[m].get()
        if len(imp) == 0:
            error = "ERROR: No selection made for %s"%m; break
        for p in ML[m][imp]['req']:
            if p not in param_to_modules:
                param_to_modules[p] = []
                PARAMS.append(p)
            param_to_modules[p].append('%s_%s'%(m,imp))
    popup = tk.Toplevel()
    if error is not None:
        tk.Label(popup, text=error, fg='red').pack()
    else:
        tk.Label(popup, text="All modules are specified. Please specify module parameters", fg='green').pack()
        popupframe = tk.Frame(popup)
        popupframe.grid(column=0, row=0, sticky=(tk.N,tk.W,tk.E,tk.S))
        popupframe.columnconfigure(0, weight=1)
        popupframe.rowconfigure(0, weight=1)
        popupframe.pack(pady=20, padx=10)
        for j,h in enumerate(['Parameter', 'Module Implementation(s)', 'Value']):
            tk.Label(popupframe, text=h, font=tkfont.Font(family="Helvetica", weight="bold")).grid(row=1,column=j)
        for i,p in enumerate(PARAMS):
            tk.Label(popupframe, text=p).grid(row=i+2, column=0)
            tk.Label(popupframe, text=', '.join(sorted(param_to_modules[p]))).grid(row=i+2, column=1)
            choice[p] = tk.Entry(popupframe)
            choice[p].grid(row=i+2, column=2)
        tk.Button(popup, text="Save", command=save_file).pack()
tk.Button(root, text="Check", command=check_config).pack()

# create save button
def format_output():
    out_lines = ['{']
    out_lines.append('    # Module Implementations')
    for m in MODULES:
        out_lines.append('    "%s": "%s",' % (m,choice[m].get()))
    out_lines.append('')
    out_lines.append('    # Parameter Choices')
    for p in sorted(PARAMS):
        pchoice = choice[p].get()
        try:
            out_lines.append('    "%s": %d,' % (p,int(pchoice)))
        except:
            try:
                num_str = ('%f'%float(pchoice)).rstrip('0').rstrip('.')
                out_lines.append('    "%s": %s,' % (p,num_str))
            except:
                out_lines.append('    "%s": "%s",' % (p,pchoice))
    if out_lines[-1].endswith(','):
        out_lines[-1] = out_lines[-1][:-1]
    out_lines.append('}')
    return '\n'.join(out_lines)
def save_file():
    f = tk.filedialog.asksaveasfile(mode='w', defaultextension=".json")
    if f is None:
        return
    f.write(format_output())
    f.close()

# run main loop to make window display
root.mainloop()