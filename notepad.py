import tkinter as tk
from tkinter import filedialog
from tkinter import font 
from tkinter import colorchooser
from tkinter import messagebox
import webbrowser
import re

global find_window, ReplaceWindow, gotoDialog, fontDialogue, HelpWindow, AboutInfo

find_window = None
ReplaceWindow = None
gotoDialog = None
fontDialogue = None
HelpWindow = None
AboutInfo = None

root = tk.Tk()
root.title("Unsaved - Text Editor")
root.iconbitmap(r'assets/notepad.ico')
root.geometry("1200x690")

openstatusname = False
selected = False

# Create New File Functrion
def new_file(e):
    global openstatusname
    new = messagebox.askokcancel("Warning","This action is going to erase any open text in the app.\nClick 'OK' to proceed")
    if new == 1:
        if e: 
            # Delete previous text
            my_text.delete("1.0", "end") 

            # Update status bars
            root.title("Unsaved - Text Editor") 
            status_bar.config(text="New File")
            openstatusname = False
        else:
            # Delete previous text
            my_text.delete("1.0", "end") 

            # Update status bars
            root.title("Unsaved - Text Editor") 
            status_bar.config(text="Ready")
            openstatusname = False

# Open Files
def open_file(e):
    global openstatusname, name
    if e:
        # Grab filename
        text_file = filedialog.askopenfilename(title="Open File", filetypes=[("Text Files", ".txt")])
        
        # Check if there is a filename
        if text_file:
            # Delete previous text
            my_text.delete("1.0", "end")
            
            # Open the file and read its contents
            try:
                with open(text_file, 'r',encoding="utf8") as file:
                    file_contents = file.read()

                # Insert the contents into the text widget
                my_text.insert("1.0", file_contents)

                # Make filename global to be accessed elsewhere
                openstatusname = text_file
            
                # Update Status Bars
                name = text_file
                status_bar.config(text=name)
                root.title(name+" - Text Editor")
                my_text.index("end")
            except FileNotFoundError:
                    return
    else:
        # Grab filename
        text_file = filedialog.askopenfilename(title="Open File", filetypes=[("Text Files", ".txt")])
        
        # Check if there is a filename
        if text_file:
            # Delete previous text
            my_text.delete("1.0", "end")

            # Open the file and read its contents
            try:
                with open(text_file, 'r',encoding="utf8") as file:
                    file_contents = file.read()
            
                    # Insert the contents into the text widget
                    my_text.insert("1.0", file_contents)

                    # Make filename global to be accessed elsewhere
                    openstatusname = text_file
                    
                # Update Status Bars
                name = text_file
                status_bar.config(text=name)
                root.title(name+" - Text Editor")
                my_text.index("end")
            except FileNotFoundError:
                return

# Save file
def saveas(e):
    if e:
        text_file = filedialog.asksaveasfilename(defaultextension=".*", title="Save As", filetypes=[("Text Files",".txt"),("Ritch Text Format",".rtf"),("All Files","")])
        if text_file:
            # Update Status Bars
            name = text_file
            status_bar.config(text="Ready")
            root.title(f"{name} - Text Editor")

            # Save The File
            text_file = open(text_file, 'w')
            text_file.write(my_text.get("1.0","end"))
            # Close the file
            text_file.close()
    else:
        text_file = filedialog.asksaveasfilename(defaultextension=".*", title="Save As", filetypes=[("Text Files",".txt"),("Ritch Text Format",".rtf"),("All Files","")])
        if text_file:
            # Update Status Bars
            name = text_file
            status_bar.config(text=f"Ready")
            root.title(f"{name} - Text Editor")

            # Save The File
            text_file = open(text_file, 'w')
            text_file.write(my_text.get("1.0","end"))
            # Close the file
            text_file.close()

# Overwrite saved file
def save(e):
    global openstatusname
    try:
        with open(name, 'r',encoding="utf8") as file:
            file_contents = file.read()
            if openstatusname != False and file_contents != my_text.get("1.0","end"):
                responce = messagebox.askyesno("WARNING!","You are about to overwrite an existing file!\nAre you sure you want to proceed?")
                if responce == 0:
                    return
        if e:
            if openstatusname:
                # Save The File
                text_file = open(openstatusname, 'w')
                text_file.write(my_text.get("1.0","end"))
                # Close the file
                text_file.close()
                # Put status update 
                status_bar.config(text=f"Saved: "+openstatusname)
            else:
                saveas(e)
        else:
            if openstatusname:
                # Save The File
                text_file = open(openstatusname, 'w')
                text_file.write(my_text.get("1.0","end"))
                # Close the file
                text_file.close()
                # Put status update 
                status_bar.config(text=f"Saved: "+openstatusname)
            else:
                saveas()
    except Exception:
        saveas(e)

# Cut
def cut(e):
    global selected
     # Check if keyboard shortcut is used
    if e:
        selected = root.clipboard_get()
    else:
        if my_text.selection_get():
            # Grab selected text from textbox
            selected = my_text.selection_get()
            # Delete selected text from textbox
            my_text.delete("sel.first","sel.last")
            # Clear clipboard and append
            root.clipboard_clear()
            root.clipboard_append(selected)

# Copy
def copy(e):
    global selected
    # Chek if keyboard shortcut is used
    if e:
        selected = root.clipboard_get()
    if my_text.selection_get():
        # Grab selected text from textbox
        selected = my_text.selection_get()
        # Clear clipboard and append
        root.clipboard_clear()
        root.clipboard_append(selected)

# Paste
def paste(e):
    global selected
    # Check if keyboard shortcut is used
    if e:
        selected = root.clipboard_get()
    else:
        if selected:
            position = my_text.index("insert")
            my_text.insert(position,selected)

# Bold
def bolding():
    # Create Font
    bold_font = font.Font(my_text, my_text.cget("font"))
    bold_font.configure(weight="bold")

    # Configure a Tag
    my_text.tag_configure("bold", font=bold_font)

    # Define Current Tags
    current_tags = my_text.tag_names("sel.first")

    # Check if tag is set
    if "bold" in current_tags:
        my_text.tag_remove("bold","sel.first","sel.last")
    else:
        my_text.tag_add("bold","sel.first","sel.last")

# Italics
def italicing():
    # Create Font
    italics_font = font.Font(my_text, my_text.cget("font"))
    italics_font.configure(slant="italic")

    # Configure a Tag
    my_text.tag_configure("italic", font=italics_font)

    # Define Current Tags
    current_tags = my_text.tag_names("sel.first")

    # Check if tag is set
    if "italic" in current_tags:
        my_text.tag_remove("italic","sel.first","sel.last")
    else:
        my_text.tag_add("italic","sel.first","sel.last")

# clear textbox
def delete():
    my_text.delete("1.0","end")
    status_bar.config(text="Ready")
    root.title("Unsaved - Text Editor")

# Close App
def on_closing():
    global name
    try:
        if my_text.get(1.0, tk.END).strip():  # Check if the textbox is not empty
            if not name:  # If there's no filename (i.e., new file)
                response = messagebox.askyesnocancel("Unsaved changes detected", "Do you want to save your changes before closing?")
                if response:  # User clicked 'Yes'
                    if saveas(my_text):  # Save the file
                        root.destroy()  # Close the app if the file was saved
                elif response is None:  # User clicked 'Cancel'
                    return  # Do nothing, keep the app open
                else:  # User clicked 'No'
                    root.destroy()  # Close the app without saving
            else:  # If there's an existing filename
                with open(name, 'r', encoding="utf8") as file:
                    file_contents = file.read().strip()
                    if my_text.get(1.0, 'end').strip() != file_contents.strip():  # Check for unsaved changes
                        response = messagebox.askyesnocancel("Unsaved changes detected","Do you want to save your changes before closing?")
                        if response:  # User clicked 'Yes'
                            if save(my_text):  # Save the file
                                root.destroy()
                        elif response is None:  # User clicked 'Cancel'
                            return
                        else:  # User clicked 'No'
                            root.destroy()
                    else:
                        root.destroy()  # No changes, just close the app
        else:
            root.destroy()  # If the textbox is empty, just close the app
    except Exception:
        response = messagebox.askyesnocancel("Unsaved changes detected", "Do you want to save your changes before closing?")
        if response:  # User clicked 'Yes'
            if saveas(my_text):  # Save the file
                root.destroy()
        elif response is None:  # User clicked 'Cancel'
            return
        else:  # User clicked 'No'
            root.destroy()

# Change Selected Text Color
def text_color():
    # Pick a color
    my_color = colorchooser.askcolor()[1]
    if my_color:
        # Create Font
        color_font = font.Font(my_text, my_text.cget("font"))

        # Configure a Tag
        my_text.tag_configure("colored", font=color_font, foreground=my_color)

        # Define Current Tags
        current_tags = my_text.tag_names("sel.first")

        # Check if tag is set
        if "colored" in current_tags:
            my_text.tag_remove("colored","sel.first","sel.last")
        else:
            my_text.tag_add("colored","sel.first","sel.last")

# Change BackGround Color
def bg_color():
    my_color = colorchooser.askcolor()[1]
    if my_color:
        my_text.config(bg=my_color)

# Reset textbox colors
def resetColors():
    my_text.config(foreground='#000000')
    my_text.config(bg='#ffffff')

# Change All Text Color
def all_text_color():
    my_color = colorchooser.askcolor()[1]
    if my_color:
        my_text.config(fg=my_color)

# Select All Text
def selectAll():
    # Add sel tag to select all text
    my_text.tag_add('sel','1.0','end')

# Underline 
def underline():
    # Configure a Tag
    my_text.tag_configure("underline", underline=True)

    # Get the selected text indices
    start_index = my_text.index("sel.first")
    end_index = my_text.index("sel.last")

    # Check if tag is set
    current_tags = my_text.tag_names(start_index)
    if "underline" in current_tags:
        my_text.tag_remove("underline", start_index, end_index)
    else:
        my_text.tag_add("underline", start_index, end_index)

# Strikethrough
def strikethrough():
    # Configure a Tag
    my_text.tag_configure("strikethrough", overstrike=True)

    # Get the selected text indices
    start_index = my_text.index("sel.first")
    end_index = my_text.index("sel.last")

    # Check if tag is set
    current_tags = my_text.tag_names(start_index)
    if "strikethrough" in current_tags:
        my_text.tag_remove("strikethrough", start_index, end_index)
    else:
        my_text.tag_add("strikethrough", start_index, end_index)

# Select text holding shift
def on_shift_select(event):
    if event.state & 0x1:  # Check if the shift key is pressed
        if event.keysym == 'Right':
            my_text.tag_add(tk.SEL, "sel.first", "sel.last + 1c")
        elif event.keysym == 'Left':
            my_text.tag_add(tk.SEL, "sel.first - 1c", "sel.last")

# global my_text
global cur_pos # This is used in find and replace functions

#Replace All
def replaceAll():
    key = find_entry.get()
    if key == "":
        return
    repl = replace_entry.get()

    # Search for the key in the entire text
    start_pos = "1.0"
    replacements_count = 0
    while True:
        pos = my_text.search(key, start_pos, stopindex="end", nocase=True)
        if pos:
            end_index = f"{pos}+{len(key)}c"
            # Replace the key with the replacement text
            my_text.delete(pos, end_index)
            my_text.insert(pos, repl)
            start_pos = end_index
            replacements_count += 1
        else:
            break

    if replacements_count > 0:
        messagebox.showinfo("Replace All", f"{replacements_count} replacements performed.")
    else:
        messagebox.showinfo("Replace All", "No matches found.")

# TopLevel window control
def on_replace_window_close():
    global ReplaceWindow
    ReplaceWindow.destroy()
    ReplaceWindow = None

# Replace widget GUI
def Replace(e):
    global ReplaceWindow
    if ReplaceWindow is None or not ReplaceWindow.winfo_exists():
        ReplaceWindow = tk.Toplevel()
        ReplaceWindow.title("Replace")
        ReplaceWindow.iconbitmap("assets/convert.ico")
        ReplaceWindow.geometry("320x150")
        ReplaceWindow.resizable(False, False)

        ReplaceWhatlabel = tk.Label(ReplaceWindow,text="Find what:")
        ReplaceWhatlabel.grid(row=0, column=0)
        
        global find_entry
        find_entry = tk.Entry(ReplaceWindow,width=20)
        find_entry.grid(row=0, column=1)

        ReplaceWithLabel = tk.Label(ReplaceWindow,text="Replace With:")
        ReplaceWithLabel.grid(row=1,column=0)

        global replace_entry
        replace_entry = tk.Entry(ReplaceWindow,width=20)
        replace_entry.grid(row=1,column=1)

        global matchCaseCheckBx_var    
        matchCaseCheckBx_var = tk.BooleanVar()
        matchCaseCheckBx_var.set(False)

        global wrapAroundCheckBx_var
        wrapAroundCheckBx_var = tk.BooleanVar()
        wrapAroundCheckBx_var.set(False) 

        repl_matchCaseCheckBx = tk.Checkbutton(ReplaceWindow,text="Match Case", variable=matchCaseCheckBx_var)
        repl_matchCaseCheckBx.grid(row=3, column=0, padx=4)

        repl_wrapAroundCheckBx = tk.Checkbutton(ReplaceWindow,text="Wrap around", variable=wrapAroundCheckBx_var)
        repl_wrapAroundCheckBx.grid(row=4, column=0, padx=4)
        
        repl_findNext = tk.Button(ReplaceWindow,text=" Find Next ",command=lambda:FindNext(find_entry.get()))
        repl_findNext.grid(row=0,column=2)

        replacebtn = tk.Button(ReplaceWindow,text="   Replace  ",command=replace)
        replacebtn.grid(row=1, column=2)

        replaceAllbtn = tk.Button(ReplaceWindow,text="Replace All",command=replaceAll)
        replaceAllbtn.grid(row=3, column=2)

        findCancel = tk.Button(ReplaceWindow,text="    Cancel   ",command=ReplaceWindow.destroy)
        findCancel.grid(row=4,column=2)
        ReplaceWindow.protocol("WM_DELETE_WINDOW", on_replace_window_close)
        ReplaceWindow.focus()
    else:
        ReplaceWindow.lift()
        ReplaceWindow.focus_force()

start_pos = ""
def replace():
    global start_pos
    key = find_entry.get()
    repl = replace_entry.get()
    if start_pos == "":
        start_pos = "1.0"
    replacements_count = 0
    pos = my_text.search(key, start_pos, stopindex="end", nocase=matchCaseCheckBx_var)
    
    if pos:
        end_index = f"{pos}+{len(key)}c"
        my_text.delete(pos, end_index)
        my_text.insert(pos, repl)
        start_pos = f"{pos}+{len(repl)}c"  # Move start_pos to just after the replacement text
        replacements_count += 1

    if replacements_count == 0:
        messagebox.showinfo("Replace", "No matches found.")

global r
r = tk.IntVar()

# TopLevel window control
def on_find_window_close():
    global find_window
    find_window.destroy()
    find_window = None

# Find widget
def find(e,direction_inp=None):
    global find_window
    if find_window is None or not find_window.winfo_exists():
        find_window = tk.Toplevel()
        find_window.title("Find")
        find_window.iconbitmap("assets/search.ico")
        find_window.geometry("400x200")
        find_window.resizable(False, False)


        findWhatlabel = tk.Label(find_window,text="Find what")
        findWhatlabel.grid(row=0, column=0)

        tofind = tk.StringVar()
        global searchbar
        searchbar = tk.Entry(find_window,textvariable=tofind, width=35)
        searchbar.grid(row=0, column=1, pady=20)
        searchbar.focus()

        findNext = tk.Button(find_window,text="Find Next",command=lambda:FindNext(searchbar.get(),r.get()))
        findNext.grid(row=0,column=2, padx=10)

        findCancel = tk.Button(find_window,text="Cancel",command=find_window.destroy)
        findCancel.grid(row=1,column=2)

        global matchCaseCheckBx_var    
        matchCaseCheckBx_var = tk.BooleanVar()
        matchCaseCheckBx_var.set(False)

        matchCaseCheckBx = tk.Checkbutton(find_window,text="Match Case",variable=matchCaseCheckBx_var)
        matchCaseCheckBx.grid(row=3, column=0, padx=4)

        global wrapAroundCheckBx_var
        wrapAroundCheckBx_var = tk.BooleanVar()
        wrapAroundCheckBx_var.set(False) 

        wrapAroundCheckBx = tk.Checkbutton(find_window,text="Wrap around",variable=wrapAroundCheckBx_var)
        wrapAroundCheckBx.grid(row=4, column=0, padx=4)

        directionSection = tk.LabelFrame(find_window,text=" Direction ")
        directionSection.grid(row=4,column=1)
        
        def direction(value):
            r.set(value)

        global cur_pos
            
        if direction_inp == 1:
            r.set("1")
            cur_pos = my_text.index("end")
        else:
            r.set("2")
            cur_pos = my_text.index("1.0")

        Upbtn = tk.Radiobutton(directionSection,text="    Up",variable=r,value=1, command=lambda:direction(1))
        Upbtn.pack()

        Downbtn = tk.Radiobutton(directionSection,text="Down",variable=r,value=2, command=lambda:direction(2))
        Downbtn.pack()
        # Bind the destroy event to clear the reference when the window is closed
        find_window.protocol("WM_DELETE_WINDOW", on_find_window_close)
    else:
        find_window.lift()
        find_window.focus_force()

# Right click menu
def rightClickMenu(e):
    rClickMenu.tk_popup(e.x_root, e.y_root)

# Text warping
def wrapping():
    if my_text['wrap']=='word':
        my_text.config(wrap="none")
    else:
        my_text.config(wrap="word")

# Hide/Show status bar
def hideStatusBar():
    if view_menuCheckbuttonVar.get():
        status_bar.pack(side="right")
        words.pack(side="left")
        lines.pack(side="left")

    else:
        status_bar.pack_forget()
        words.pack_forget()
        lines.pack_forget()

# TopLevel window control
def on_gotoDialog_close():
    global gotoDialog
    gotoDialog.destroy()
    gotoDialog = None

# TopLevel window control
def Goto(e):
    global gotoDialog
    if gotoDialog is None or not gotoDialog.winfo_exists():
        gotoDialog = tk.Toplevel()
        gotoDialog.title("Go To Line")
        gotoDialog.iconbitmap("assets/goto.ico")
        gotoDialog.resizable(False,False)
        gotoDialog.geometry("300x100")

        def cancel():
            gotoDialog.destroy()
        
        def gotoLine():
            
            def validateLine():
                input_data = LineNoEntry.get()
                if input_data:
                    try:
                        int(input_data)
                        return True
                    except ValueError:
                        messagebox.showerror("You can only imput nubmers here",f'Integer number expected, got "{input_data}"')

            if validateLine() == True:
                # Try to get the index of the start of the given line
                line_index = f"{LineNoEntry.get()}.0"
                line_end_index = f"{LineNoEntry.get()}.end"
                line_content = my_text.get(line_index, line_end_index)
                # Remove any existing selection
                my_text.tag_remove("sel", "1.0", "end")
                # Add selection tag to the entire line
                my_text.tag_add("sel", line_index, line_end_index) # If line_content is empty, it means the line doesn't exist
                cancel()

                if not line_content.strip():
                    messagebox.showerror("Notepad - Goto Line","The line number is beyond the total number of lines")

        LineNo = tk.Label(gotoDialog,text="Line number:")
        LineNo.pack(anchor="w",padx=25)

        LineNoEntry = tk.Entry(gotoDialog,width=40)
        LineNoEntry.pack()
        LineNoEntry.focus()

        gotoDialogbtns = tk.Frame(gotoDialog)
        gotoDialogbtns.pack()

        GotoOk = tk.Button(gotoDialogbtns,text="Go To",command=gotoLine)
        GotoOk.pack(side="left",pady=10)

        GotoCancel = tk.Button(gotoDialogbtns,text="Cancel",command=cancel)
        GotoCancel.pack(side="left",pady=10)
        # Bind the destroy event to clear the reference when the window is closed
        gotoDialog.protocol("WM_DELETE_WINDOW", on_gotoDialog_close)
    else:
        gotoDialog.lift()
        gotoDialog.focus_force()

# Helper function for font cotrol
def fontChooser(e):
    global temp_font
    global fontListbox
    global fontStylesListbox
    global fontSizeListbox
    global SampleTextLabel
    global selected_size

    temp_font = font.Font(root,current_font_index)

    selected_font = fontListbox.get(fontListbox.curselection())
    selected_style = fontStylesListbox.get(fontStylesListbox.curselection())
    selected_size = fontSizeListbox.get(fontSizeListbox.curselection())

    temp_font.config(
        family=selected_font,
        weight="bold" if "Bold" in selected_style else "normal",
        slant="italic" if "Italics" in selected_style else "roman",
        size=int(selected_size)
    )
    SampleTextLabel.config(font=temp_font)

# TopLevel window control
def on_fontDialogue_window_close(): 
    global fontDialogue
    fontDialogue.destroy()
    fontDialogue = None
    
# Font GUI
def openFontDialogue():
    global fontDialogue, current_font, current_font_index, current_family, current_size, current_size_idx, current_weight, current_slant

    if fontDialogue is None or not fontDialogue.winfo_exists():
        fontDialogue = tk.Toplevel()
        fontDialogue.title("Font")
        fontDialogue.iconbitmap("assets/FontImg.ico")
        fontDialogue.resizable(False, False)
        fontDialogue.geometry("900x440")

        global current_font_index, selected_font_index, current_size_idx, selected_size_idx, selected_size, selected_font
        # Retrieve current font settings from my_text
        try: #OK
            current_font = font.nametofont(my_text.cget("font"))
            current_font_index = selected_font_index
            current_family = selected_font
            current_size = selected_size
            current_size_idx = selected_size_idx
            current_weight = current_font.actual()["weight"]
            current_slant = current_font.actual()["slant"]
        except Exception:
            try: # cancel
                if current_font_index != "":
                    current_font_index = selected_font_index
                    current_family = current_font.actual()["family"]
                    current_size = current_size
                    current_size_idx = current_size_idx
                    current_weight = current_font.actual()["weight"]
                    current_slant = current_font.actual()["slant"]
    
            except Exception: # 1st time running
                current_font = ""
                current_font_index = 41
                current_family = "Arial"
                current_size = "12"
                current_size_idx = 4
                current_weight = "normal"
                current_slant = "roman"

        # Font Family
        FontFamilySectionFrame = tk.Frame(fontDialogue)
        FontFamilySectionFrame.grid(row=0, column=0)

        fontFamilySection = tk.LabelFrame(FontFamilySectionFrame, text=" Font ", padx=5, pady=5)
        fontFamilySection.pack(padx=15)

        global fontListbox
        fontListbox = tk.Listbox(fontFamilySection, width=30, height=20, selectmode="SINGLE", exportselection=0)
        fontListbox.pack(padx=10, side="left")

        # Get the list of font families and sort them alphabetically
        font_families = sorted(font.families())
        
        current_font_index = -1
        for f in font_families:
            current_font_index += 1
            fontListbox.insert('end', f)
            if current_family == f:
                fontListbox.selection_set(current_font_index)
                fontListbox.see(current_font_index)
        fontListbox.bind('<ButtonRelease-1>', fontChooser)

        font_scroll = tk.Scrollbar(fontFamilySection)
        font_scroll.pack(side="right", fill="y")
        font_scroll.config(command=fontListbox.yview)

        # Configure the listbox to work with the scrollbar
        fontListbox.config(yscrollcommand=font_scroll.set)

        # Font Styles
        FontStylesSectionFrame = tk.Frame(fontDialogue)
        FontStylesSectionFrame.grid(row=0, column=1)
        FontFamilySectionFrame.grid_propagate(False)

        fontStylesSection = tk.LabelFrame(FontStylesSectionFrame, text=" Style ", padx=5, pady=5)
        fontStylesSection.grid(row=0, column=1, padx=15)  # Place the first label frame on the left

        global fontStylesListbox
        fontStylesListbox = tk.Listbox(fontStylesSection, width=30, height=4, selectmode="SINGLE", exportselection=0)
        fontStylesListbox.pack()  # Pack the listbox inside the label frame

        fontStylesListbox.insert("end", "Normal")
        fontStylesListbox.insert("end", "Bold")
        fontStylesListbox.insert("end", "Italics")
        fontStylesListbox.insert("end", "Bold + Italics")

        if current_weight == "bold" and current_slant == "italic":
            fontStylesListbox.selection_set(3)
        elif current_weight == "bold":
            fontStylesListbox.selection_set(1)
        elif current_slant == "italic":
            fontStylesListbox.selection_set(2)
        else:
            fontStylesListbox.selection_set(0)
        fontStylesListbox.bind('<ButtonRelease-1>', fontChooser)

        # Sample Text
        SampleTextLabelFrameFrame = tk.Frame(fontDialogue, width=400, height=100)  # Add explicit dimensions
        SampleTextLabelFrameFrame.grid(row=1, column=1)
        SampleTextLabelFrameFrame.grid_propagate(False)

        SampleTextLabelFrame = tk.LabelFrame(SampleTextLabelFrameFrame, text="Sample", width=380, height=80)
        SampleTextLabelFrame.grid(row=1, column=1)
        SampleTextLabelFrame.grid_propagate(False)

        global SampleTextLabel
        try:
            SampleTextLabel = tk.Label(SampleTextLabelFrame, text="the quick brown fox jumps over the lazy dog\nTHE QUICK BROWN FOX JUMPS OVER THE LAZY DOG",wraplength=360, height=2, width=50, anchor="w",justify="left")
            SampleTextLabel.config(font=temp_font)
            SampleTextLabel.pack(expand=False)
        except Exception:
            SampleTextLabel = tk.Label(SampleTextLabelFrame, text="the quick brown fox jumps over the lazy dog\nTHE QUICK BROWN FOX JUMPS OVER THE LAZY DOG",wraplength=360, height=2, width=50, anchor="w",justify="left")
            SampleTextLabel.pack(expand=False)
        
        # Font Size
        FontSizeSectionFrame = tk.Frame(fontDialogue)
        FontSizeSectionFrame.grid(row=0, column=3)

        global fontSizeListbox
        fontSizeSection = tk.LabelFrame(FontSizeSectionFrame, text=" Size ", padx=5, pady=5)
        fontSizeSection.pack(padx=15, side="left")  # Place the second label frame next to the first one

        fontSizeListbox = tk.Listbox(fontSizeSection, width=30, height=16, selectmode="SINGLE", exportselection=0)
        fontSizeListbox.pack()  # Pack the listbox inside the label frame

        current_size_idx = -1
        for size in ["8", "9", "10", "11", "12", "14", "16", "18", "20", "22", "24", "26", "28", "36", "48", "72"]:
            current_size_idx += 1
            fontSizeListbox.insert("end", size)
            if current_size == size:
                fontSizeListbox.selection_set(current_size_idx)
        fontSizeListbox.bind('<ButtonRelease-1>', fontChooser)

        buttons_frame = tk.Frame(fontDialogue)
        buttons_frame.grid(row=1, column=3, pady=5)

        def cancel():            
            global selected_size, selected_style
            selected_size = current_size
            temp_font.config(family=selected_font,
                             weight="bold" if "Bold" in selected_style else "normal", 
                             slant="italic" if "Italics" in selected_style else "roman",
                             size=selected_size)
            on_fontDialogue_window_close()

        def OK():
            global selected_font_index, selected_size_idx, selected_size, temp_font, current_size_idx, selected_font, selected_style
            selected_font = fontListbox.get(fontListbox.curselection())
            selected_style = fontStylesListbox.get(fontStylesListbox.curselection())
            selected_size = fontSizeListbox.get(fontSizeListbox.curselection())
            selected_font_index = current_font_index
            selected_size_idx = current_size_idx

            temp_font.config(
                family=selected_font,
                weight="bold" if "Bold" in selected_style else "normal",
                slant="italic" if "Italics" in selected_style else "roman",
                size=str(selected_size)
            )
            my_text.config(font=temp_font)
            on_fontDialogue_window_close()
        Cancelbtn = tk.Button(buttons_frame, text="Cancel", command=cancel)
        Cancelbtn.pack(side="left", pady=15, anchor="w")

        OKbtn = tk.Button(buttons_frame, text="   OK   ", command=OK)
        OKbtn.pack(side="left", pady=15, anchor="w")
        fontDialogue.protocol("WM_DELETE_WINDOW",on_fontDialogue_window_close)
        fontDialogue.focus()
    else:
        fontDialogue.lift()
        fontDialogue.focus_force()

# Help GUI
def viewHelp():
    global HelpWindow
    if HelpWindow is None or not HelpWindow.winfo_exists():
        HelpWindow = tk.Toplevel()
        HelpWindow.title("Help")
        HelpWindow.iconbitmap("assets/lifebelt.ico")
        HelpWindow.geometry("600x700")

        f = open("assets/Help.txt", "r").readlines()
        HelpLabel = tk.Label(HelpWindow,text="\n".join(f))
        HelpLabel.pack(padx=10,pady=10)
        HelpWindow.focus()
    else:
        HelpWindow.lift()
        HelpWindow.focus_force()

# About GUI
def viewAboutInfo():
    global AboutInfo
    if AboutInfo is None or not AboutInfo.winfo_exists():
        AboutInfo = tk.Toplevel()
        AboutInfo.title("About")
        AboutInfo.iconbitmap("asstets/About.ico")
        AboutInfo.geometry("300x100")
        AboutInfo.resizable(False, False)
        AbtLbl = tk.Label(AboutInfo,text="Version: 1.0.0.0\n\nFor newer versions, bug fixes, or suggestions visit:")
        AbtLbl.pack()
        link=tk.Label(AboutInfo,text="https://github.com/GeorgeChatzogiannakis/Notepad",fg="blue",cursor="hand2")
        link.pack()
        link.bind("<Button-1>", lambda e: webbrowser.open_new_tab("https://github.com/GeorgeChatzogiannakis"))
        AboutInfo.focus()
    else:
        AboutInfo.lift()
        AboutInfo.focus_force()

def lineCount(text_content):
    lines = 1
    for line in text_content:
        if "\n" in line:
            lines += 1    
    return str(lines)

def wordCount(text_content):
    words = re.findall(r'\b\w+\b', text_content)
    return len(words)

def setToReady():
    try:
        with open(name, 'r', encoding="utf8") as file:
            file_contents = file.read().strip()
            if my_text.get(1.0, 'end').strip() != file_contents.strip():  # Check for unsaved changes
                status_bar.config(text="Unsaved")
    except Exception:
        status_bar.config(text="Unsaved")

def update_counts(event=None):
    text_content = my_text.get("1.0", "end-1c")  # Get text from the text widget
    words_count = wordCount(text_content)  # Count words
    line_count = lineCount(text_content)  # Count letters without counting white spaces
    words.config(text=f"Words: " + str(words_count)+", ")  # Update the words label
    lines.config(text="Lines: " + str(line_count))  # Update the letters label
    status_bar.config(text="Typing...")
    root.after(1800,setToReady)
                

text_wrap = tk.StringVar(value='word')

# Create a Toolbar Frame
toolbar_frame = tk.Frame(root)
toolbar_frame.pack(fill="x")

# Create Main Frame
my_frame = tk.Frame(root,bd=10,width=950,height=620)
my_frame.pack_propagate(0)
my_frame.pack(pady=5)
my_frame.grid_propagate(False)

# Create Scroller For The Textbox
text_scroll = tk.Scrollbar(my_frame)
text_scroll.pack(side="right", fill="y")

# Horizontal Scrollbar
horizontal_scrollbar = tk.Scrollbar(my_frame, orient="horizontal")
horizontal_scrollbar.pack(side="bottom", fill="x")

# Create a Textbox
global sel_font
sel_font = font.Font(root,"Arial",size=12)
my_text = False
my_text = tk.Text(my_frame, width=100, height =32, font=(sel_font,12),selectbackground="blue", selectforeground="white", undo=True, yscrollcommand=text_scroll.set, xscrollcommand=horizontal_scrollbar.set, wrap=text_wrap.get())

# Search in text
def FindNext(key,direction=None):
    global cur_pos
    if direction is None or direction == 2:
        direction = 2
    else: 
        direction = 1
    match_case = matchCaseCheckBx_var.get()

    def highlight_and_focus(pos, end_pos):
        my_text.tag_remove("sel", "1.0", "end")
        my_text.tag_add("sel", pos, end_pos)
        my_text.mark_set("insert", end_pos)
        my_text.see("insert")
        my_text.focus_set()

    if direction == 2:  # Down
        pos = my_text.search(key, cur_pos, stopindex="end", nocase=not match_case)
    elif direction == 1:  # Up
        pos = my_text.search(key, cur_pos, stopindex="1.0", backwards=True, nocase=not match_case)
    
    if pos:
        end_index = f"{pos}+{len(key)}c"
        highlight_and_focus(pos, end_index)
        cur_pos = end_index if direction == 2 else pos
    else:
        # No match found, check if wrap-around is enabled
        if wrapAroundCheckBx_var.get() == True:
            if direction == 2:  # Down
                pos = my_text.search(key, "1.0", stopindex=cur_pos, nocase=not match_case)
            elif direction == 1:  # Up
                pos = my_text.search(key, "end", stopindex=cur_pos, backwards=True, nocase=not match_case)

            if pos:
                end_index = f"{pos}+{len(key)}c"
                highlight_and_focus(pos, end_index)
                cur_pos = end_index if direction == 2 else pos
            else:
                messagebox.showinfo("Find", "No more matches found.")
        else:
            messagebox.showinfo("Find", "No more matches found.")
my_text.pack(fill="both", expand=True)

# Configure Scrollbar
text_scroll.config(command=my_text.yview)
text_scroll.config(command=my_text.xview)

# Create a Menu
my_menu = tk.Menu(root)
root.config(menu=my_menu)

# Create Right-Click Menu
rClickMenu = tk.Menu(root,tearoff=False)
rClickMenu.add_command(label="Undo",command=my_text.edit_undo)
rClickMenu.add_separator()
rClickMenu.add_command(label="Cut",command=lambda:cut(False))
rClickMenu.add_command(label="Copy",command=lambda:copy(False))
rClickMenu.add_command(label="Paste",command=lambda:paste(False))
rClickMenu.add_command(label="Delete",command=delete)
rClickMenu.add_separator()
rClickMenu.add_command(label="Select All",command=selectAll)
rClickMenu.add_separator()
rClickMenu.add_command(label="Undo",command=my_text.edit_undo)
rClickMenu.add_command(label="Redo", command=my_text.edit_redo)

# Add file menu
file_menu = tk.Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="File", menu=file_menu)  
file_menu.add_command(label="New", command=lambda:new_file(False),accelerator="(Ctrl+N)")
file_menu.add_command(label="Open", command=lambda:open_file(False),accelerator="(Ctrl+O)")
file_menu.add_command(label="Save", command=lambda:save(False), accelerator="(Ctrl+S)")
file_menu.add_command(label="Save As", command=lambda:saveas(False),accelerator="(Ctrl+Shift+S)")
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

# Add Edit menu
edit_menu = tk.Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Edit", menu=edit_menu) 
edit_menu.add_command(label="Undo", command=my_text.edit_undo, accelerator="(Ctrl+Z)")
edit_menu.add_separator()
edit_menu.add_command(label="Cut", command=lambda:cut(False),accelerator="(Ctrl+X)")
edit_menu.add_command(label="Copy",command=lambda:copy(False),accelerator="(Ctrl+C)")
edit_menu.add_command(label="Paste",command=lambda:paste(False),accelerator="(Ctrl+V)")
edit_menu.add_command(label="Delete",command=delete,accelerator="(Del)")
#edit_menu.add_command(label="Redo", command=my_text.edit_redo, accelerator="(Ctrl+Y)")
edit_menu.add_separator()
#edit_menu.add_command(label="Clear", command=clear)
edit_menu.add_command(label="Find", command=lambda:find(False),accelerator="(Ctrl+F)")
edit_menu.add_command(label="Find Next", command=lambda:find(False),accelerator="(F3)")
edit_menu.add_command(label="Find Previous", command=lambda:find(False,direction_inp=1),accelerator="(Shift+F3)")
edit_menu.add_command(label="Replace...",command=lambda:Replace(False),accelerator="(Ctrl+H)")
edit_menu.add_command(label="Go To...",command=lambda:Goto(False),accelerator="(Ctrl+G)")
edit_menu.add_separator()
edit_menu.add_command(label="Select All", command=selectAll, accelerator="(Ctrl+A)")

# Add Format Menu
isWarping = tk.BooleanVar()
isWarping.set(True)
format_menu = tk.Menu(my_menu,tearoff=False)
my_menu.add_cascade(label="Format", menu=format_menu)
format_menu.add_checkbutton(label="Word Wrap",variable=isWarping, command=lambda:wrapping())
format_menu.add_command(label="Font", command=openFontDialogue)

# Add View Menu
view_menuCheckbuttonVar = tk.BooleanVar()
view_menuCheckbuttonVar.set(True)
view_menu = tk.Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="View",menu=view_menu)
view_menu.add_checkbutton(label="Status Bar", variable=view_menuCheckbuttonVar, command=hideStatusBar)

# Add Color menu
color_menu = tk.Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Colors", menu=color_menu)
color_menu.add_command(label="Change Selected Text", command=text_color)
color_menu.add_command(label="Change All Text",command=all_text_color)
color_menu.add_command(label="Change Backgreound",command=bg_color)
color_menu.add_separator()
color_menu.add_command(label="Reset Colors",command=resetColors)

# Add a Help Menu
help_menu = tk.Menu(my_menu,tearoff=False)
my_menu.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="View Help", command=viewHelp)
help_menu.add_command(label="About", command=viewAboutInfo)

words = tk.Label(root, text="Words: 0, ")
words.pack(side="left")

lines = tk.Label(root, text="Lines: 1")
lines.pack(side="left")

status_bar = tk.Label(root, text="Ready")
status_bar.pack(side="right")

# Edit Bindings
root.bind('<Control-Key-x>',cut)
root.bind('<Control-Key-c>',copy)
root.bind('<Control-Key-v>',paste)
root.bind('<Control-Key-f>',find)
root.bind('<F3>',find)
root.bind('<Control-Key-h>',Replace)
root.bind('<Shift-Right>', on_shift_select)
root.bind('<Shift-Left>', on_shift_select)
root.bind('<Control-Key-n>',new_file)
root.bind('<Control-Key-o>',open_file)
root.bind('<Control-Key-s>',save)
root.bind('<Control-Shift-S>',saveas)
root.bind('<Shift-F3>', lambda e: find(e, direction_inp=1))
root.bind('<Control-Key-g>',Goto)
my_text.bind("<KeyRelease>", update_counts)  # Bind the update_counts function to KeyRelease event
root.protocol("WM_DELETE_WINDOW", on_closing)

# Right-Click Menu
root.bind('<Button-3>',rightClickMenu)

# Create Buttons
Paste = tk.Button(toolbar_frame, text='📋Paste',command=paste)
Paste.grid(row=0,column=0)

Copy = tk.Button(toolbar_frame, text='📄Copy',command=copy)
Copy.grid(row=0,column=1)

Cut = tk.Button(toolbar_frame, text='✂ Cut', command=cut)
Cut.grid(row=0, column=2)

bold = tk.Button(toolbar_frame, text='𝓑old', command=bolding)
bold.grid(row=0, column=3)

italics = tk.Button(toolbar_frame, text='𝐼talics', command=italicing)
italics.grid(row=0, column=4)

Underline = tk.Button(toolbar_frame,text='U̲nderline',command=underline)
Underline.grid(row=0,column=5)

Strikethrough = tk.Button(toolbar_frame, text='l̵i̵k̵e̵ ̵t̵h̵i̵s̵ ', command=strikethrough)
Strikethrough.grid(row=0,column=6)

undo = tk.Button(toolbar_frame, text='↶ Undo', command=my_text.edit_undo)
undo.grid(row=0, column=7)

redo = tk.Button(toolbar_frame, text='↪ Redo', command=my_text.edit_redo)
redo.grid(row=0, column=8)

clear_text = tk.Button(toolbar_frame, text="✖ Clear", command=delete)
clear_text.grid(row=0, column=9)

root.mainloop()
