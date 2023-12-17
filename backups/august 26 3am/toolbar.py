import tkinter as tk

class Toolbar:
    def __init__(self, app):
        self.app = app
        self.frame = tk.Frame(app.root, bg="#2E2E2E")  # Dark background to match PropertyExplorer
        self.frame.pack(side="left", fill="y")
        self.create_buttons()
        self.label = tk.Label(self.frame, text="Nodes Toolbar", bg="#2E2E2E", fg="white")  # Text color set to white
        self.label.pack(side="top", fill="x")

    def create_buttons(self):
        node_types = [
            ("Preheader", self.app.create_preheader_node), 
            ("String", self.app.create_string_node),
            ("Int", self.app.create_int_node),
            ("Float", self.app.create_float_node),
            ("Boolean", self.app.create_boolean_node),
            ("Custom Function", self.app.create_custom_function_node),
            ("Text Output", self.app.create_text_output_node),
            ("Math", self.app.create_math_node),
            ("Clear", self.app.clear_canvas),
            ("Close", self.app.root.destroy)
        ]
        for label, command in node_types:
            button = tk.Button(self.frame, text=label, command=command, bg="#2E2E2E", fg="white")  # Button color set to match
            button.pack(side="top", fill="x")
