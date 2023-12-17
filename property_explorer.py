import tkinter as tk

class PropertyExplorer:
    def __init__(self, app):
        self.app = app
        self.frame = tk.Frame(app.root, bg="#2E2E2E", width=200)  # Set width to 300px
        self.frame.pack(side="right", fill="y")
        self.frame.pack_propagate(False)  # Keeps the frame from resizing to fit content
        self.create_panel()
        self.labels = {}
        self.buttons = {}
        self.clear_panel()

    def create_panel(self):
        self.panel = tk.Frame(self.frame, bg="#2E2E2E")  # Dark background
        self.panel.pack(side="top", fill="both", expand=True)

    def clear_panel(self):
        for widget in self.panel.winfo_children():
            widget.destroy()
        self.labels.clear()
        self.buttons.clear()

    def populate(self):
        node_attributes = {}
        if self.app.selected_node:
            self.nodeProperties(node_attributes)
        for attribute in node_attributes:
            text_color = "orange" if attribute in ["value", "function"] else "white"  # Special values in orange
            if attribute not in self.labels:
                self.labels[attribute] = tk.Label(self.panel, bg="#2E2E2E", fg=text_color)
                self.labels[attribute].pack(side="top", fill="x", padx=10, pady=5, expand=True)
            self.labels[attribute].config(text=f"{attribute}: {node_attributes[attribute]}")
            
            if attribute not in self.buttons:
                self.buttons[attribute] = tk.Button(self.panel, bg="#2E2E2E", fg="white", borderwidth=2)
                self.buttons[attribute].pack(side="top", fill="x", padx=10, pady=5)
            self.buttons[attribute].config(command=lambda attr=attribute: self.app.change_attribute(attr))
        
        # Call update_label for each node to dynamically update node_name
        for node_instance in self.app.nodes:
            node_instance.update_label()

    def nodeProperties(self, node_attributes):
        node_attributes["x"] = self.app.selected_node.x
        node_attributes["y"] = self.app.selected_node.y
        node_attributes["connections"] = len(self.app.selected_node.connections)
        node_attributes["Type"] = self.app.selected_node.node_name
        if hasattr(self.app.selected_node, "value"):
            node_attributes["value"] = self.app.selected_node.node_value
        if hasattr(self.app.selected_node, "function"):
            node_attributes["function"] = self.app.selected_node.function
        node_attributes["color"] = self.app.canvas.itemcget(self.app.selected_node.id, "fill")

    def close(self):
        self.frame.destroy()
