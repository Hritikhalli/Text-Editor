from tkinter import *
from tkinter import filedialog
from tkinter import font

root = Tk()
root.title('Simple TextEditor')
root.iconbitmap('icontext.png')
root.geometry('1200x680')

global open_status_name
open_status_name = False

global selected
selected = False

def new_file():
    my_text.delete("1.0",END)
    root.title('New File - TextEditor!')
    status_bar.config(text="New File     ")
    global open_status_name
    open_status_name = False

def open_file():
    my_text.delete("1.0",END)

    text_file = filedialog.askopenfilename(initialdir="", title="Open File", filetypes=(("Text Files", "*.txt"),("HTML Files", "*.html"),("Pthon Files", "*.py"),("All Files", "*.*") ))
    
    if text_file:
        global open_status_name
        open_status_name = text_file


    name = text_file
    status_bar.config(text=f'{name}        ')
    root.title(f'{name} - textEditor!')

    text_file = open(text_file , 'r')
    stuff = text_file.read()
    my_text.insert(END, stuff)
    text_file.close()

def save_as_file():
    text_file = filedialog.asksaveasfilename(defaultextension=".*",initialdir=" ",title="save File",filetypes=(("Text Files", "*.txt"),("HTML Files", "*.html"),("Pthon Files", "*.py"),("All Files", "*.*") ))
    if text_file:
        name =text_file
        status_bar.config(text=f'Saved: {name}        ')
        root.title(f'{name} - textEditor!')

        text_file = open(text_file, 'w')
        text_file.write(my_text.get(1.0,END))
        text_file.close()

def save_file():
    global open_status_name
    if open_status_name:
        text_file = open(open_status_name, 'w')
        text_file.write(my_text.get(1.0,END))
        text_file.close()
        status_bar.config(text=f'Saved: {open_status_name}        ')

    else:
        save_as_file()

def cut_text(e):
    global selected
    if e:
        selected = root.clipboard_get()

    if my_text.selection_get():
        selected = my_text.selection_get()
        my_text.delete("sel.first","sel.last")
        root.clipboard_clear()
        root.clipboard_append(selected)

def copy_text(e):
    global selected

    if e:
        selected = root.clipboard_get()

    if my_text.selection_get():
        selected = my_text.selection_get()
        root.clipboard_clear()
        root.clipboard_append(selected)

def paste_text(e):
    global selected
    if e:
        selected = root.clipboard_get()
    else :   
        if selected:
                position = my_text.index(INSERT)
                my_text.insert(position, selected)

def bold_it():

    bold_font = font.Font(my_text, my_text.cget("font"))
    bold_font.configure(weight="bold")
    my_text.tag_configure("bold", font=bold_font)

    current_tags = my_text.tag_names("sel.first")
    if "bold" in current_tags:
        my_text.tag_remove("bold","sel.first","sel.last")
    else:
        my_text.tag_add("bold","sel.first","sel.last")

def italics_it():
    
    italics_font = font.Font(my_text, my_text.cget("font"))
    italics_font.configure(slant="italic")
    my_text.tag_configure("italic", font=italics_font)

    current_tags = my_text.tag_names("sel.first")
    if "italic" in current_tags:
        my_text.tag_remove("italic","sel.first","sel.last")
    else:
        my_text.tag_add("italic","sel.first","sel.last")

toolbar_frame = Frame(root)
toolbar_frame.pack(fill=X)

my_frame = Frame(root)
my_frame.pack(pady=5)

text_scroll = Scrollbar(my_frame)
text_scroll.pack(side= RIGHT , fill = Y)

hor_scroll = Scrollbar(my_frame, orient = 'horizontal')
hor_scroll.pack(side= BOTTOM , fill = X)

my_text = Text(my_frame, width = 97, height=25, font =("Helvetica", 16 ) , selectbackground="yellow", selectforeground="black",undo = True, yscrollcommand=text_scroll.set, wrap = "none",xscrollcommand=hor_scroll.set)
my_text.pack()

text_scroll.config(command=my_text.yview)
hor_scroll.config(command=my_text.xview)

my_menu = Menu(root)
root.config(menu=my_menu)

file_menu = Menu(my_menu, tearoff=FALSE)
my_menu.add_cascade(label="File", menu=file_menu)

file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command= save_file)
file_menu.add_command(label="Save As", command =save_as_file)
file_menu.add_separator()
file_menu.add_command(label="Exit",command = root.quit)


edit_menu = Menu(my_menu, tearoff=FALSE)
my_menu.add_cascade(label="Edit", menu=edit_menu)

edit_menu.add_command(label="Cut     (Ctrl+x)", command=lambda: cut_text(False))
edit_menu.add_command(label="Copy     (Ctrl+c)", command=lambda: copy_text(False))
edit_menu.add_command(label="Paste     (Ctrl+v)", command=lambda: paste_text(False))
edit_menu.add_separator()
edit_menu.add_command(label="Undo     (Ctrl+z)", command=my_text.edit_undo)
edit_menu.add_command(label="Redo     (Ctrl+y)", command=my_text.edit_redo)

status_bar = Label(root, text = 'Ready        ', anchor=E)
status_bar.pack(fill=X, side= BOTTOM, ipady=15)  

root.bind('<Control-Key-x>', cut_text)
root.bind('<Control-Key-c>', copy_text)
root.bind('<Control-Key-v>', paste_text)

bold_button = Button(toolbar_frame, text= "Bold", command=bold_it)
bold_button.grid(row=0,column=0,sticky=W,padx=5)

italics_button = Button(toolbar_frame, text= "Italics", command=italics_it)
italics_button.grid(row=0,column=1,padx=5)

undo_button = Button(toolbar_frame, text= "Undo", command=my_text.edit_undo)
undo_button.grid(row=0,column=2,padx=5)

redo_button = Button(toolbar_frame, text= "Redo", command=my_text.edit_redo)
redo_button.grid(row=0,column=3,padx=5)


root.mainloop()