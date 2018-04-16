#! /usr/bin/env python3
'''
Design FAVITES Configuration Files via GUI
'''
from urllib.request import urlopen
from tkinter.filedialog import asksaveasfile
from tkinter import font as tkfont
from webbrowser import open_new
from tkinter import *
ML_URL = "https://raw.githubusercontent.com/niemasd/FAVITES/master/modules/FAVITES_ModuleList.json"
HEADER = "FAVITES Configuration File Designer"
MODULES = ['Driver','Logging','TreeNode','ContactNetwork','ContactNetworkGenerator','SeedSelection','SeedSequence','EndCriteria','TransmissionTimeSample','TransmissionNodeSample','NodeEvolution','SequenceEvolution','SourceSample','NumTimeSample','TimeSample','NumBranchSample','TreeUnit','NodeAvailability','Sequencing']
ML = eval(urlopen(ML_URL).read().decode())
WIDTH = max(len(e) for m in ML for e in ML[m])
PARAMS = []
MAIN_SIZEX = 560
MAIN_SIZEY = 700
POPUP_SIZEX = 1280
POPUP_SIZEY = 600

# helper functions for scrollbar
def root_scroll(event):
    root_canvas.configure(scrollregion=root_canvas.bbox("all"),width=MAIN_SIZEX-20,height=MAIN_SIZEY-20)
def popup_scroll(event):
    popup_canvas.configure(scrollregion=popup_canvas.bbox("all"),width=POPUP_SIZEX-20,height=POPUP_SIZEY-20)

# initialize main window
root = Tk()
root.title(HEADER)
root.resizable(False, False)
root.wm_geometry("%dx%d+%d+%d" % (MAIN_SIZEX,MAIN_SIZEY,0,0))
root_frame = Frame(root, relief=GROOVE, width=MAIN_SIZEX, height=MAIN_SIZEY, bd=1)
root_frame.place(x=0,y=0)
root_canvas = Canvas(root_frame)
root_canvas_frame = Frame(root_canvas)
root_ybar = Scrollbar(root_frame, orient="vertical", command=root_canvas.yview)
root_xbar = Scrollbar(root_frame, orient="horizontal", command=root_canvas.xview)
root_canvas.configure(xscrollcommand=root_xbar.set, yscrollcommand=root_ybar.set)
root_ybar.pack(side=RIGHT, fill=Y)
root_xbar.pack(side=BOTTOM, fill=X)
root_canvas.pack(side="left")
root_canvas.create_window((0,0), window=root_canvas_frame, anchor='nw')
root_canvas_frame.bind("<Configure>",root_scroll)

# create header
header_label = Label(root_canvas_frame, text="%s%s"%(' '*0,HEADER))
header_label.config(font=("Helvetica", 32))
header_label.grid(row=0, column=0, columnspan=2)
choice = {m:StringVar(root_canvas_frame) for m in MODULES}

# create dropdowns for modules
def go_to_module_page(event):
    open_new(r"https://github.com/niemasd/FAVITES/wiki/Module:-%s"%event.widget.cget("text"))
Label(root_canvas_frame, text="Module", font=tkfont.Font(family="Helvetica", weight="bold")).grid(row=1, column=0)
Label(root_canvas_frame, text="Implementation", font=tkfont.Font(family="Helvetica", weight="bold")).grid(row=1, column=1)
for i,m in enumerate(MODULES):
    dropdown = OptionMenu(root_canvas_frame, choice[m], *sorted(ML[m].keys()))
    dropdown.config(width=WIDTH)
    dropdown.grid(row=i+2, column=1)
    label = Label(root_canvas_frame, text=m, fg='blue', cursor='hand2')
    label.grid(row=i+2, column=0)
    label.bind("<Button-1>", go_to_module_page)

# create check button
def check_config():
    # check params
    param_to_modules = {}
    error = None
    for m in MODULES:
        imp = choice[m].get()
        if len(imp) == 0:
            error = "ERROR: No selection made for %s"%m; break
        for p in ML[m][imp]['req']:
            if p not in param_to_modules:
                if p == 'random_number_seed': # TODO remove this once random number seed is working properly
                    continue
                param_to_modules[p] = []
                PARAMS.append(p)
            param_to_modules[p].append('%s_%s'%(m,imp))

    # create popup window
    popup = Toplevel()
    if error is not None:
        Label(popup, text=error, fg='red').grid(row=0, column=0)
    else:
        popup.resizable(False, False)
        popup.wm_geometry("%dx%d+%d+%d" % (POPUP_SIZEX,POPUP_SIZEY,0,0))
        popup_frame = Frame(popup, relief=GROOVE, width=POPUP_SIZEX, height=POPUP_SIZEY, bd=1)
        popup_frame.place(x=0,y=0)
        global popup_canvas
        popup_canvas = Canvas(popup_frame)
        popup_canvas_frame = Frame(popup_canvas)
        popup_ybar = Scrollbar(popup_frame, orient="vertical", command=popup_canvas.yview)
        popup_xbar = Scrollbar(popup_frame, orient="horizontal", command=popup_canvas.xview)
        popup_canvas.configure(xscrollcommand=popup_xbar.set, yscrollcommand=popup_ybar.set)
        popup_ybar.pack(side=RIGHT, fill=Y)
        popup_xbar.pack(side=BOTTOM, fill=X)
        popup_canvas.pack(side="left")
        popup_canvas.create_window((0,0), window=popup_canvas_frame, anchor='nw')
        popup_canvas_frame.bind("<Configure>",popup_scroll)
        Label(popup_canvas_frame, text="All modules are specified. Please specify module parameters", fg='green').grid(row=0, column=1)
        for j,h in enumerate(['Parameter', 'Module Implementation(s)', 'Value']):
            Label(popup_canvas_frame, text=h, font=tkfont.Font(family="Helvetica", weight="bold")).grid(row=1,column=j)
        for i,p in enumerate(PARAMS):
            Label(popup_canvas_frame, text=p).grid(row=i+2, column=0)
            Label(popup_canvas_frame, text=', '.join(sorted(param_to_modules[p]))).grid(row=i+2, column=1)
            choice[p] = Entry(popup_canvas_frame)
            choice[p].grid(row=i+2, column=2)
        Button(popup_canvas_frame, text="Save", command=save_file).grid(row=2+len(PARAMS), column=0, columnspan=3)
Button(root_canvas_frame, text="Check", command=check_config).grid(row=2+len(MODULES), column=0, columnspan=2)

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
    f = filedialog.asksaveasfile(mode='w', defaultextension=".json")
    if f is None:
        return
    f.write(format_output())
    f.close()

# run main loop to make window display
root.mainloop()