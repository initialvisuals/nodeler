from tkinter import simpledialog
from tkinter import ttk
from config import threshold
from connection import Connection


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
        self.node_value = None
        text_color = "white"

        self.canvas_item_id = self.canvas.create_oval(x-circle_size, y-circle_size, x+circle_size, y+circle_size, fill=color)
        self.label = self.canvas.create_text(x+circle_size-150, y, text=self.generate_label_text(), fill=text_color, anchor="w")
        self.update_label()

    def generate_label_text(self):
        return f"connections: {len(self.connections)}\n Type: {self.node_name}\n ID: {self.id}\n Value: {self.node_value}"

    def node_label(self, x, y, circle_size, color, text_color):
        self.canvas_item_id = self.canvas.create_oval(x-circle_size, y-circle_size, x+circle_size, y+circle_size, fill=color)
        self.label = self.canvas.create_text(x+circle_size-150, y, text=self.generate_label_text(), fill=text_color, anchor="w")
                
    def remove_label(self):
        self.canvas.delete(self.label)

    def edit_value(self):
        if new_value := simpledialog.askstring("Edit Node", "Enter new value:", initialvalue=self.node_value):
            self.node_value = new_value
            self.update_label()

    def update_label(self):
        if hasattr(self, 'label'):
            # Dynamically update the node name to match the class's node_name attribute
            self.node_name = self.node_name  # Access the class's node_name attribute

            updated_label_text = self.generate_label_text()  # Generate the updated label text

            print(f"Updating label for {self.node_name}")
            self.canvas.itemconfig(self.label, text=updated_label_text)


    def move(self, x, y):
        dx = x - self.x
        dy = y - self.y
        self.x = x
        self.y = y
        self.canvas.move(self.canvas_item_id, dx, dy)  
        self.canvas.move(self.label, dx, dy)
        self.update_connections()
        #update label
        self.update_label()


    def update_connections(self):
        print(f"Updating connections for {self.node_name}")
        for connection in self.connections:
            connection.update_line()
        self.canvas.itemconfig(self.label, text=self.generate_label_text())
        self.update_label()
    


    def connect(self, other_node):
        connection = Connection(self.canvas, self, other_node)
        self.connections.append(connection)
        other_node.connections.append(connection)
        self.update_connections()
        other_node.update_connections()
        self.update_label()

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
            self.update_label()
        
        

        self.canvas.delete(self.id)
        self.canvas.delete(self.label)

class StringNode(Node):
    def __init__(self, canvas, app, x, y):
        super().__init__(canvas, app, x, y, 20, color="red")  # Initialize the base class
        self.node_name = "String"  # Set a default node name
        self.value = ""

    def update_label(self):
        # Update the node_name attribute before updating the label
        self.node_name = "String"  # Update the node_name dynamically
        super().update_label()  # Call the base class update_label method


class PreheaderNode(Node):
    def __init__(self, canvas, app, x, y):
        self.node_name = "Preheader"
        super().__init__(canvas, app, x, y, 20, color="teal") #these attributes are: canvas, app, x, y, circle_size, color
        self.value = ""
    
    
    def update_label(self):
        # Update the node_name attribute before updating the label
        self.node_name = "Preheader"  # Update the node_name dynamically
        super().update_label()  # Call the base class update_label method

class IntNode(Node):
    def __init__(self, canvas, app, x, y):
        self.node_name = "Int"
        super().__init__(canvas, app, x, y, 20, color="green")
        self.value = 0
        #display the value
        self.canvas.itemconfig(self.label, text=f"connections: {len(self.connections)}\n Type: {self.node_name}\n ID: {self.id}\n Value: {self.node_value}")
    
    
    def update_label(self):
        # Update the node_name attribute before updating the label
        self.node_name = "Int"  # Update the node_name dynamically
        super().update_label()  # Call the base class update_label method

class FloatNode(Node):
    def __init__(self, canvas, app, x, y):
        self.node_name = "Float"
        super().__init__(canvas, app, x, y, 20, color="yellow")
        self.value = 0.0
    
    
    def update_label(self):
        # Update the node_name attribute before updating the label
        self.node_name = "Float"  # Update the node_name dynamically
        super().update_label()  # Call the base class update_label method

class BooleanNode(Node):
    def __init__(self, canvas, app, x, y):
        self.node_name = "Boolean"
        super().__init__(canvas, app, x, y, 20, color="purple")
        self.value = False
    
    
    def update_label(self):
        # Update the node_name attribute before updating the label
        self.node_name = "Boolean"  # Update the node_name dynamically
        super().update_label()  # Call the base class update_label method

class CustomFunctionNode(Node):
    def __init__(self, canvas, app, x, y):
        self.node_name = "Custom Function"
        super().__init__(canvas, app, x, y, 20, color="orange") 
        #set canvas background color to orange
        self.canvas.config(bg="orange")
    
    
    def update_label(self):
        # Update the node_name attribute before updating the label
        self.node_name = "Custom Function"  # Update the node_name dynamically
        super().update_label()  # Call the base class update_label method

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
        # Place the dropdown on the canvas below the node
        self.canvas.create_window(x, y+50, window=self.dropdown)        

    
    def update_label(self):
        # Update the node_name attribute before updating the label
        self.node_name = "Math"  # Update the node_name dynamically
        super().update_label()  # Call the base class update_label method
    
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
            #update values
            self.values = [node.value for node in self.connections]
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
        self.node_name = "Text Output"
        super().__init__(canvas, app, x, y, 40, color="grey")
        #display the concatenated values of the connected nodes
        self.value = ""


    def update_label(self):
        # Update the node_name attribute before updating the label
        self.node_name = "Text Output"  # Update the node_name dynamically
        super().update_label()  # Call the base class update_label method