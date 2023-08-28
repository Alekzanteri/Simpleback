import tkinter as tk
from tkinter import *
from tkinter import filedialog
import os
import Simpleback.core as sc
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from PIL import ImageTk, Image
from tkinter import font
from importlib import resources
import io
import pandas as pd
from pathlib import Path
import pathlib



def gui():
    
    root=tk.Tk(className='Simpleback0.0.1')#creating main window.
    root.configure(bg='#fbd9ff')#background color
    font_size=16
    root.columnconfigure(0, weight=1)
    root.defaultFont = font.nametofont("TkDefaultFont")
    root.defaultFont.configure(size=font_size)

    row_1=tk.Frame(master=root, bg='#ec99ff', height=100)#every row jas it's own frame to make widts work beautifully
    row_1.grid(row=0, column=0, sticky='nw')#grid method is used to position frames
    
    #function for graphically choosing filepath
    def choose_files():
        global file_path#global variable to make it work outside function
        file_path=filedialog.askdirectory()#this line opens file explorer
        
        if(len(file_path)>0):#check if file_path was relly choosed
            folder_variable.config(text=file_path, bg='green')#choosen file path is printed to gui 
            #ats files inside the folder
            files=[]
            for file in os.listdir(file_path):
                if file.endswith('.ats'):
                    files.append(file)
            mes_freqs=[]#data collecting freqs
            for i in range(0, len(files)):#data collecting freqs are saved to list
                hz=int(files[i].split('_')[-1].split('.')[0].split('H')[0])#getting mes_freq from filename
                mes_freqs.append(hz)
            mes_freqs=list(dict.fromkeys(mes_freqs))#only one value of every mes freq is kept in the list.
            
            choose_freq=tk.Toplevel(bg='#fbd9ff')#pop up window for choosing frequency for prosessing
            choose_freq.geometry('500x500')
            
            #function for choosing frequency
            def freq_chooser(i):
                global pros_freq
                pros_freq=mes_freqs[i]
                print_window.config(text=f'Selected measuring period is {pros_freq}', bg='#ec99ff')#printing mes_freq
                choose_freq.destroy()#destroy pop-up after frequency is choosen 
            
            #help function to make calling[i] possible
            def make_freq_chooser_command(i):
                return lambda: freq_chooser(i)
            
            #creating buttons for choosing prosesing frequency
            for i in range (0, len(mes_freqs)):                    
                freq_but=Button(master=choose_freq, text=mes_freqs[i], command=make_freq_chooser_command(i), bg='#cf00ff')
                freq_but.pack(fill='both', expand=True)
            
        return(file_path)

    folder_chooser=Button(row_1, text='Select Folder', bg='#cf00ff', command=choose_files)#button for choosing folder
    folder_chooser.grid(row=0,  column=0,  padx=10,  pady=5)

    settings=tk.Frame(master=row_1, height=50, width=50, bg='#ec99ff')#frame for settings
    settings.grid(row=0,  column=1,  padx=10,  pady=5, sticky="nsew")

    set_width=4 #width of setting entrys
    
    #setting default values
    abs_path=pathlib.Path(__file__).parent.resolve()#path of this exact file.
    rel_path=r'default_settings.csv'
    default_csv_file_path = os.path.join(abs_path, rel_path)
    
    defaults=pd.read_csv(default_csv_file_path, index_col=0)
    global cod_def
    cod_def=defaults.value.cod
    global nper_def
    nper_def=defaults.value.nper
    global overlap_def
    overlap_def=defaults.value.overlap
    global min_factor_def
    min_factor_def=defaults.value.min_factor
    global max_factor_def
    max_factor_def=defaults.value.max_factor
    global freqs_def
    freqs_def=defaults.value.freqs.astype(int)

    #cod label and entry 
    cod_label=Label(settings, text='cod', bg='#ec99ff')
    cod_label.grid(row=0,  column=1,  padx=10,  pady=5)

    cod=Entry(settings, width=set_width, font="TkDefaultFont")
    cod.insert(0, cod_def)
    cod.grid(row=1,  column=1,  padx=10,  pady=5)

    #nper label and entry
    nper_label=Label(settings, text='nper', bg='#ec99ff')
    nper_label.grid(row=0,  column=2,  padx=10,  pady=5)

    nper=Entry(settings, width=set_width, font="TkDefaultFont")
    nper.insert(0, nper_def)
    nper.grid(row=1,  column=2,  padx=10,  pady=5)

    #overlap label and entry
    overlap_label=Label(settings, text='overlap', bg='#ec99ff')
    overlap_label.grid(row=0,  column=3,  padx=10,  pady=5)

    overlap=Entry(settings, width=set_width, font="TkDefaultFont")
    overlap.insert(0, overlap_def)
    overlap.grid(row=1,  column=3,  padx=10,  pady=5)

    #min_factor label and entry
    min_factor_label=Label(settings, text='min_factor', bg='#ec99ff')
    min_factor_label.grid(row=0,  column=4,  padx=10,  pady=5)

    min_factor=Entry(settings, width=set_width, font="TkDefaultFont")
    min_factor.insert(0, min_factor_def)
    min_factor.grid(row=1,  column=4,  padx=10,  pady=5)

    #max_factor label and entry
    max_factor_label=Label(settings, text='max_factor', bg='#ec99ff')
    max_factor_label.grid(row=0,  column=5,  padx=10,  pady=5)

    max_factor=Entry(settings, width=set_width, font="TkDefaultFont")
    max_factor.insert(0, max_factor_def)
    max_factor.grid(row=1,  column=5,  padx=10,  pady=5)

    #freqs label and entry
    freqs_label=Label(settings, text='freqs', bg='#ec99ff')
    freqs_label.grid(row=0,  column=6,  padx=10,  pady=5)

    freqs=Entry(settings, width=set_width, font="TkDefaultFont")
    freqs.insert(0, freqs_def)
    freqs.grid(row=1,  column=6,  padx=10,  pady=5)



    buttons_r1=tk.Frame(master=row_1, bg='#ec99ff') #frame for main commands buttons
    buttons_r1.grid(row=0, column=2, padx=10,  pady=5)
    
    #default settings button
    def set_defaults():
        cod.delete(0, END)#emtying entry
        cod.insert(0, cod_def)#setting default value to entry
        nper.delete(0, END)
        nper.insert(0, nper_def)
        overlap.delete(0, END)
        overlap.insert(0, overlap_def)
        min_factor.delete(0, END)
        min_factor.insert(0, min_factor_def)
        max_factor.delete(0, END)
        max_factor.insert(0, max_factor_def)
        freqs.delete(0, END)
        freqs.insert(0, freqs_def)
        return
    
    
    default=Button(buttons_r1, text='Default \n settings', bg='#cf00ff', command=set_defaults)
    default.grid(row=0, column=0, padx=(0, 20))    

    
    #help button
    def get_help():
        popup=tk.Toplevel(width=600, height=400, bg='#fbd9ff')#creating nedw popup for help text
        popup.wm_title("Help")
        # help text is added row by row
        help_text_row_1=tk.Label(master=popup, text="\"cod\" is razorback filter value. Bigger number means more filtering", bg='#ec99ff')
        help_text_row_1.pack()
        help_text_row_2=tk.Label(master=popup, text="\"nper\" defines prosessing window length bigger number means longer window and therfor smoother curves.", bg='#ec99ff')
        help_text_row_2.pack()
        help_text_row_3=tk.Label(master=popup, text="\"overlap\" defines how much prosessing windows overlap. Bigger overlap makes slower but potentionally beter prosessing.", bg='#ec99ff')
        help_text_row_3.pack()
        help_text_row_4=tk.Label(master=popup, text="\"min_factor\" defines lower end of used frequencies. Lowest frequncy f_min is defined as below:", bg='#ec99ff')
        help_text_row_4.pack()
        #equations are added as a png.
        with resources.open_binary('Simpleback.gui','f_min.png') as fp:
            img=fp.read()
        global f_min_img
        f_min_img=ImageTk.PhotoImage(Image.open(io.BytesIO(img)))
        f_min_label=tk.Label(master=popup, image=f_min_img)
        f_min_label.pack()
        help_text_row_5=tk.Label(master=popup, text="\"max_factor\" defines higher end of used frequencies. Highest frequncy f_min is defined as below:", bg='#ec99ff')
        help_text_row_5.pack()
        with resources.open_binary('Simpleback.gui','f_max.png') as fp:
            img=fp.read()
        global f_max_img
        f_max_img=ImageTk.PhotoImage(Image.open(io.BytesIO(img)))
        f_max_label=tk.Label(master=popup, image=f_max_img)
        f_max_label.pack()
        help_text_row_6=tk.Label(master=popup, text="\"freqs\" is number of individual periods used.", bg='#ec99ff')
        help_text_row_6.pack()
        
        #button for escapeing help window
        def destroy_help():
            popup.destroy()
        ok_but=Button(master=popup, text='OK!', command=destroy_help, bg='#cf00ff')
        ok_but.pack(pady=20)
    
    helpper=Button(buttons_r1, text='Help', bg='#cf00ff', command=get_help)
    helpper.grid(row=0, column=1, padx=(0, 20))

    #prosses button
    def prosses():
        if('file_path' in globals() and 'pros_freq' in globals()):#prosessing is only started if file_path and pros_freqs exit...
            
            #getting settings
            cod_f=float(cod.get())
            nper_f=float(nper.get())
            overlap_f=float(overlap.get())
            min_factor_f=float(min_factor.get())
            max_factor_f=float(max_factor.get())
            freqs_f=int(freqs.get())
            
            #running simpleback prosessing from Simpleback.core
            fig=sc.run.simpleback(file_path, freq_rule=pros_freq, cod=cod_f, nper=nper_f, overlap=overlap_f, min_factor=min_factor_f, max_factor=max_factor_f, freqs=freqs_f)
            
            
            #adding figure to canvas
            canvas=FigureCanvasTkAgg(fig, master=row_3)
            canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            #crerating toolbar to move canvas
            toolbar = NavigationToolbar2Tk(canvas, row_4)
            toolbar.update()
            canvas.get_tk_widget().pack()
            
            
            #canvas and toolbar are collected.
            def on_key_press(event):
                print("you pressed {}".format(event.key))
                key_press_handler(event, canvas, toolbar)
                
            canvas.mpl_connect("key_press_event", on_key_press)
            
            print_window.config(text='Prosessing done!', bg='#ec99ff')
            
        else:
            print_window.config(text='Select folder and measuring frequency first!', bg='red')
        return()
    
    prosses=Button(buttons_r1, text='Process', bg='#cf00ff', height=3, width=10, command=prosses)
    prosses.grid(row=0, column=2, padx=(0, 20))
    
    #clear button to remove tfs from canvas
    def clear_canvas():
        del globals()['file_path']
        folder_variable.config(text='No folder selected.', bg='red')
        print_window.config(text='Select folder define settings and press prosses.', bg='#ec99ff')
        
        #all widgeds in row_3 are deleted
        for widget in row_3.winfo_children():
            widget.destroy()
            
        #all widgeds in row_3 are deleted
        for widget in row_4.winfo_children():
            widget.destroy()
    
    clear=Button(buttons_r1, text='Clear', bg='#cf00ff', command=clear_canvas)
    clear.grid(row=0, column=3, padx=(0, 20))


    #2nd row
    row_2=tk.Frame(master=root, bg='#ec99ff')
    row_2.grid(row=1, column=0, sticky='nw')

    # selected folder label and variable
    folder_info=tk.Frame(master=row_2, bg='#ec99ff')
    folder_info.grid(row=0, column=0)

    folder_label=Label(folder_info, text='Current folder:', bg='#ec99ff')
    folder_label.grid(row=0,  column=0,  padx=15,  pady=5)

    folder_variable=Label(folder_info, text='No folder selected.', bg='red')
    folder_variable.grid(row=0, column=1)


    #window for plotting
    root.columnconfigure(2, weight=1)
    root.rowconfigure(2, weight=1)
    row_3=tk.Frame(master=root, bg='#fbd9ff', height=500)
    row_3.grid(row=2, column=0, sticky='nwse')
    
    #window for plot toolbaar
    row_4=tk.Frame(master=root, bg='#fbd9ff', height=50)
    row_4.grid(row=3, column=0)
    


    #window for printing output:
    row_5=tk.Frame(master=root,height=300)
    row_5.grid(row=4, column=0,)
    
    print_window=tk.Label(master=row_5, text='Select folder define settings and press prosses.', bg='#ec99ff')
    print_window.grid(row=0, column=0, )


    root.mainloop()
    return