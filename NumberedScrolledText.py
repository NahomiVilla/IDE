import tkinter as tk
import tkinter
from tkinter import scrolledtext
import matplotlib.font_manager as fm

class NumberedScrolledText(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)

        self.line_numbers = tk.Text(self, width=4, padx=4, takefocus=0, border=0, background='black', foreground='white', insertbackground='white', selectbackground='white', selectforeground='black', state='disabled')
        self.line_numbers.pack(side='left', fill='y')

        self.text_area = scrolledtext.ScrolledText(self, wrap='none', background='black', foreground='black', insertbackground='black', selectbackground='black', selectforeground='black')
        self.text_area.pack(side='left', fill='both', expand=True)
        self.font_family_var = tk.StringVar(self)
        self.font_size_var = tk.IntVar(self)

        self.text_area.configure(bg='black', fg='white', insertbackground='white', selectbackground='white', selectforeground='black')
        self.text_area.vbar.configure(bg='blue', troughcolor='black', activebackground='blue')

        self.text_area.bind('<Any-KeyPress>', self.on_key_press)
        self.text_area.bind('<B1-Motion>', self.on_mouse_drag)
        self.text_area.bind('<MouseWheel>', self.on_mouse_wheel)
        self.text_area.bind('<Configure>', self.on_configure)
        self.text_area.bind('<FocusIn>', self.on_focus_in)
        self.text_area.bind('<FocusOut>', self.on_focus_out)
        self.text_area.bind('<Control-A>', self.select_all)
        self.text_area.bind('<Control-a>', self.select_all)
        self.text_area.bind('<Control-C>', self.copy)
        self.lines=1
        self.on_update()

    def select_all(self, event=None):
        self.text_area.tag_add('sel', '1.0', 'end')
        return 'break'

    def copy(self, event=None):
        self.text_area.clipboard_clear()
        text = self.text_area.get("sel.first", "sel.last")
        self.text_area.clipboard_append(text)

    def on_update(self, event=None):
        self.line_numbers.config(state='normal')
        self.line_numbers.delete('1.0', 'end')
        for i in range(1, self.lines + 1):
            self.line_numbers.insert('end', f'{i}\n')
        self.line_numbers.config(state='disabled')

    def on_configure(self, event=None):
        self.on_update()

    def on_key_press(self, event=None):
         # Verificar si la tecla presionada es una tecla especial
        special_keys = ['Left', 'Right', 'Up', 'Down', 'Control', 'Alt', 'Shift', 'Delete']
        if event.keysym in special_keys:
            return None
        prev_char = self.text_area.get(self.text_area.index('insert') + ' - 1 chars')
        prev_line_end = self.text_area.get(f'{self.lines - 1}.0', f'{self.lines - 1}.end')
        
        if prev_char == '\n' and prev_line_end.strip().endswith(':'):
            indent_spaces = len(prev_line_end) - len(prev_line_end.lstrip())
            indent_spaces += 4
            self.text_area.insert('insert', ' ' * indent_spaces)
            self.lines += 1
        elif prev_char == '\n': 
            indent_spaces = len(prev_line_end) - len(prev_line_end.lstrip())
            self.text_area.insert('insert', ' ' * indent_spaces)
            self.lines += 1

        self.on_update()
        return None

    def on_mouse_wheel(self, event):
        self.text_area.yview_scroll(int(-1*(event.delta/120)), 'units')
        self.lines = int(self.text_area.index('end-1c').split('.')[0])
        self.on_update()
        return 'break'

    def on_mouse_drag(self, event=None):
        self.lines = int(self.text_area.index('end-1c').split('.')[0])
        self.on_update()
        return None

    def on_focus_in(self, event=None):
        self.on_update()
        return None

    def on_focus_out(self, event=None):
        self.on_update()
        return None
    
