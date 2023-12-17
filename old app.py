import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from math import sqrt
from functools import reduce
from operator import mul, truediv, mod, pow
from connection import Connection as Connections
from config import threshold

class Node:
    next_id = 0  # Class variable to keep track of the next available ID
    
    def __init__(self, canvas, app, x, y, circle_size, color="lightblue"):
        self.threshold = 500
        self.canvas = canvas
        self.app = app
        self.id = Node.next_id  # Assign the next available ID to this node
        Node.next_id += 1  # Increment the next available ID
        self.x = x
        self.y = y
        self.connections = []
        self.node_name = "Node"
        text_color = "white"

        self.canvas_item_id = self.canvas.create_oval(x-circle_size, y-circle_size, x+circle_size, y+circle_size, fill=color)
        self.label = self.canvas.create_text(x+circle_size-150, y, text=self.generate_label_text(), fill=text_color, anchor="w")
        self.update_label()

    def generate_label_text(self):
        return f"connections: {len(self.connections)}\n Type: {self.node_name}\n ID: {self.id}"

    def node_label(self, x, y, circle_size, color, text_color):
        self.canvas_item_id = self.canvas.create_oval(x-circle_size, y-circle_size, x+circle_size, y+circle_size, fill=color)
        self.label = self.canvas.create_text(x+circle_size-150, y, text=self.generate_label_text(), fill=text_color, anchor="w")
                
    def remove_label(self):
        self.canvas.delete(self.label)

    def edit_value(self):
        if new_value := simpledialog.askstring(
            "Edit Node", "Enter new value:", initialvalue=self.node_name
        ):
            self.node_name = new_value
            self.update_label()

    def update_label(self):
        if hasattr(self, 'label'):
            new_label_text = "your_new_text_here"
            self.canvas.itemconfig(self.label, text=new_label_text)


    def move(self, x, y):
        dx = x - self.x
        dy = y - self.y
        self.x = x
        self.y = y
        self.canvas.move(self.canvas_item_id, dx, dy)  
        self.canvas.move(self.label, dx, dy)
        self.update_connections()


    def update_connections(self):
        for connection in self.connections:
            connection.update_line()
        self.canvas.itemconfig(self.label, text=self.generate_label_text())


    def connect(self, other_node):
        connection = Connection(self.canvas, self, other_node)
        self.connections.append(connection)
        other_node.connections.append(connection)
        self.update_connections()
        other_node.update_connections()

    def delete(self):
        for connection in self.connections:
            # Remove this connection from the other node's list of connections
            other_node = connection.node1 if connection.node2 == self else connection.node2
            other_node.connections.remove(connection)
            other_node.update_connections()
            
            # Delete the connection
            connection.delete()
            #delete the node
            self.remove_label()
        

        self.canvas.delete(self.id)
        self.canvas.delete(self.label)

class StringNode(Node):
    def __init__(self, canvas, app, x, y):
        self.node_name = "String" 
        super().__init__(canvas, app, x, y, 20, color="red") #these attributes are: canvas, app, x, y, circle_size, color
        self.value = ""

class PreheaderNode(Node):
    def __init__(self, canvas, app, x, y):
        self.node_name = "Preheader"
        super().__init__(canvas, app, x, y, 20, color="teal") #these attributes are: canvas, app, x, y, circle_size, color
        self.value = ""

class IntNode(Node):
    def __init__(self, canvas, app, x, y):
        node_name = "Int"
        super().__init__(canvas, app, x, y, 20, color="green")
        self.value = 0

class FloatNode(Node):
    def __init__(self, canvas, app, x, y):
        node_name = "Float"
        super().__init__(canvas, app, x, y, 20, color="yellow")
        self.value = 0.0

class BooleanNode(Node):
    def __init__(self, canvas, app, x, y):
        node_name = "Boolean"
        super().__init__(canvas, app, x, y, 20, color="purple")
        self.value = False

class CustomFunctionNode(Node):
    def __init__(self, canvas, app, x, y):
        node_name = "Custom Function"
        super().__init__(canvas, app, x, y, 20, color="orange") 
        #set canvas background color to orange
        self.canvas.config(bg="orange")

class MathNode(Node):
    def __init__(self, canvas, app, x, y):
        self.node_name = "Math"  # Set as an instance variable
        super().__init__(canvas, app, x, y, 20, color="pink")
        self.operation = "add"  # Default operation
        self.connections = []  # Nodes to take values from
        self.values = []  # Values to take from the connected nodes
        self.result = None  # Result of the operation

        # Dropdown for selecting operation
        self.dropdown = ttk.Combobox(self.canvas, values=["add", "subtract", "multiply", "divide", "modulo", "power", "root", "absolute", "floor", "ceil", "round"])
        self.dropdown.current(0)  # set default value
        self.dropdown.bind("<<ComboboxSelected>>", self.update_operation)
        self.canvas.create_window(x, y, window=self.dropdown)  # Place the dropdown on the canvas

    def update_operation(self, event=None):
        self.operation = self.dropdown.get()
        self.compute()


    def add_connection(self, node):
        self.connections.append(node)
        self.update_values()

    def remove_connection(self, node):
        self.connections.remove(node)
        self.update_values()

    def update_values(self):
        self.values = [node.value for node in self.connections]
        self.compute()

    def compute(self):  # sourcery skip: low-code-quality
        if not self.values:
            self.result = None
            return

        try:
            if self.operation == "add":
                self.result = sum(self.values)
            elif self.operation == "subtract":
                self.result = self.values[0] - sum(self.values[1:])
            elif self.operation == "multiply":
                self.result = 1
                for val in self.values:
                    self.result *= val
            elif self.operation == "divide":
                self.result = self.values[0]
                for val in self.values[1:]:
                    if val != 0:
                        self.result /= val
                    else:
                        self.result = "Cannot divide by zero"
                        return
            elif self.operation == "modulo":
                if len(self.values) >= 2 and self.values[1] != 0:
                    self.result = self.values[0] % self.values[1]
                else:
                    self.result = "Need at least 2 values and divisor != 0"
                    return
            elif self.operation == "power":
                if len(self.values) >= 2:
                    self.result = self.values[0] ** self.values[1]
                else:
                    self.result = "Need at least 2 values"
                    return
            elif self.operation == "root":
                if len(self.values) >= 2 and self.values[1] != 0:
                    self.result = self.values[0] ** (1 / self.values[1])
                else:
                    self.result = "Need at least 2 values and root != 0"
                    return
            elif self.operation == "absolute":
                self.result = abs(self.values[0])
            elif self.operation == "floor":
                self.result = int(self.values[0])
            elif self.operation == "ceil":
                self.result = int(self.values[0]) + 1
            elif self.operation == "round":
                self.result = round(self.values[0])
            else:
                self.result = "Unknown operation"
        except Exception as e:
            self.result = f"Error: {e}"

class TextOutputNode(Node):
    def __init__(self, canvas, app, x, y):
        node_name = "Text Output"
        super().__init__(canvas, app, x, y, 40, color="grey")
        #display the concatenated values of the connected nodes
        self.value = ""

class Connection:
    def __init__(self, canvas, node1, node2):
        self.canvas = canvas
        self.node1 = node1
        self.node2 = node2
        self.line_id = self.canvas.create_line(node1.x, node1.y, node2.x, node2.y)
        #white line
        self.canvas.itemconfig(self.line_id, fill="white")

    def update_line(self):
        self.canvas.coords(self.line_id, self.node1.x, self.node1.y, self.node2.x, self.node2.y)

    def delete(self):
        self.canvas.delete(self.line_id)

class Toolbar:
    def __init__(self, app):
        self.app = app
        self.frame = tk.Frame(app.root, bg="#2E2E2E")  # Dark background to match PropertyExplorer
        self.frame.pack(side="left", fill="y")
        self.create_buttons()
        self.label = tk.Label(self.frame, text="Toolbar", bg="#2E2E2E", fg="white")  # Text color set to white
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
            ("Clear", self.app.clear_canvas)
        ]
        for label, command in node_types:
            button = tk.Button(self.frame, text=label, command=command, bg="#2E2E2E", fg="white")  # Button color set to match
            button.pack(side="top", fill="x")

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

    def nodeProperties(self, node_attributes):
        node_attributes["x"] = self.app.selected_node.x
        node_attributes["y"] = self.app.selected_node.y
        node_attributes["connections"] = len(self.app.selected_node.connections)
        node_attributes["type"] = type(self.app.selected_node).__name__
        if hasattr(self.app.selected_node, "value"):
            node_attributes["value"] = self.app.selected_node.value
        if hasattr(self.app.selected_node, "function"):
            node_attributes["function"] = self.app.selected_node.function
        node_attributes["color"] = self.app.canvas.itemcget(self.app.selected_node.id, "fill")

    def close(self):
        self.frame.destroy()

class App:
    def __init__(self, root):
        self.selected_node = None
        self.root = root
        self.toolbar = Toolbar(self)
        self.property_explorer = PropertyExplorer(self)
        self.canvas = tk.Canvas(root, width=2560, height=1080, bg="black")
        self.canvas.pack(side="left", fill="both", expand=True)  # Changed to make room for Property Explorer
        self.nodes = []
        self.canvas.bind("<Control-Button-1>", self.create_node)
        self.canvas.bind("<B1-Motion>", self.drag_node)
        self.canvas.bind("<Button-3>", self.delete_node)
        self.canvas.bind("<ButtonRelease-1>", self.release_node)
        self.canvas.bind("<Button-1>", self.on_node_click)
        self.root.bind("<Escape>", lambda e: self.root.destroy())
        self.canvas.bind("<Button-2>", self.start_pan)
        self.canvas.bind("<B2-Motion>", self.pan)
        self.canvas.bind("<ButtonRelease-2>", self.end_pan)
        self.canvas.bind("<Double-Button-1>", self.on_canvas_double_click)

    def on_canvas_double_click(self, event):
        item = self.canvas.find_closest(event.x, event.y)[0]
        if node := next(
            (node for node in self.nodes if node.canvas_item_id == item), None
        ):
            node.edit_value()

    def change_attribute(self, attribute):
        if self.selected_node is None:
            print("No node selected, can't change attribute.")
            return
    
    def start_pan(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def pan(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def end_pan(self, event):
        pass
        
    def create_string_node(self):
        self.selected_node_type = StringNode
    
    def create_preheader_node(self):
        self.selected_node_type = PreheaderNode

    def create_int_node(self):
        self.selected_node_type = IntNode

    def create_float_node(self):
        self.selected_node_type = FloatNode

    def create_boolean_node(self):
        self.selected_node_type = BooleanNode

    def create_custom_function_node(self):
        self.selected_node_type = CustomFunctionNode
        
    def create_math_node(self):
        self.selected_node_type = MathNode
    
    def create_text_output_node(self, node_name):
        self.selected_node_type = TextOutputNode

    def create_node(self, event):
        if not hasattr(self, "selected_node_type"):
            print("No node type selected.")
            return

        # Get mouse position, adjusted for canvas pan
        x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)

        # Assuming the selected_node_type constructor expects exactly 4 arguments: canvas, parent, x, y
        new_node = self.selected_node_type(self.canvas, self, x, y)
        self.nodes.append(new_node)

        # Log or print the type of node created, for debugging or other purposes
        print(f"Created a new node at position: ({x}, {y})")

        self.check_all_connections()
        self.selected_node = self.nodes[-1]
        self.property_explorer.populate()

    def drag_node(self, event):
        if self.dragged_node is None:
            self.dragged_node = self.find_node(event.x, event.y)
        if self.dragged_node:
            self.dragged_node.move(event.x, event.y)
            self.property_explorer.populate()
            self.check_all_connections()

    def on_node_click(self, event):
        if clicked_node := self.find_node(event.x, event.y):
            print("clicked node number", self.nodes.index(clicked_node))
            self.selected_node = clicked_node
            self.property_explorer.populate()
        else:
            # Deselect the node and clear the property explorer if the background is clicked
            self.selected_node = None
            self.property_explorer.clear_panel()



    def delete_node(self, event):
        if self.selected_node:
            self.selected_node.delete()  # This will now also remove the label
            self.nodes.remove(self.selected_node)
            self.check_all_connections()
            self.property_explorer.clear_panel()
            self.selected_node = None
            self.property_explorer.populate()
        self.dragged_node = None
        
    def clear_canvas(self):
        for node in self.nodes:
            node.delete()
        self.nodes.clear()
        self.property_explorer.clear_panel()
        self.selected_node = None
        self.property_explorer.populate()
        self.dragged_node = None
    
        
    def release_node(self, event):
        self.dragged_node = None

    def find_node(self, x, y):
        x,y = self.canvas.canvasx(x), self.canvas.canvasy(y)
        click_threshold = 20
        return next(
            (
                node
                for node in reversed(self.nodes)
                if abs(node.x - x) < click_threshold and abs(node.y - y) < click_threshold
            ),
            None,
        )


    def check_connections(self, node):

        to_remove = []  # List to collect connections that need to be removed
    
        for other_node in self.nodes:
            if other_node != node:
                distance = self.distance(node, other_node)
                existing_connection = next((c for c in node.connections if c.node1 == other_node or c.node2 == other_node), None)
    
                if distance <= threshold and existing_connection is None:
                    node.connect(other_node)
                elif distance > threshold and existing_connection is not None:
                    to_remove.append(existing_connection)
    
        # Remove connections that are too far
        for connection in to_remove:
            connection.delete()
            node.connections.remove(connection)
            if connection.node1 == node:
                connection.node2.connections.remove(connection)
            else:
                connection.node1.connections.remove(connection)
    
        # Update the node's label to reflect the new number of connections
        node.canvas.itemconfig(node.label, text=f"connections: {len(node.connections)}\n Type: {node.node_name}\n ID: {node.id}")


    
    def check_all_connections(self):
        for node in self.nodes:
            self.check_connections(node)

    @staticmethod
    def distance(node1, node2):
        return sqrt((node1.x - node2.x)**2 + (node1.y - node2.y)**2)



root = tk.Tk()
root.attributes('-fullscreen', True)
app = App(root)
root.mainloop()