import tkinter as tk
from tkinter import ttk
import sys

class Console(tk.Text):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.bind("<Return>", self.execute)

    def execute(self, event):
        # Get the current line
        current_line = self.get("insert linestart", "insert lineend")
    
        # Evaluate and execute the command
        try:
            output = eval(current_line)
            if output is not None:
                self.insert("end", "\n" + str(output))
            else:
                self.insert("end", "")
        except Exception as e:
            self.insert("end", "\n" + str(e))
    
        self.see("end")
        return "break"


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Tkinter Console")

        self.console = Console(root, wrap="word", width=50, height=15)
        self.console.pack(fill="both", expand=True)
        self.console.insert("end", "")
        self.console.focus()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
