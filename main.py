import tkinter as tk
from nodes import Node, StringNode, PreheaderNode, IntNode, FloatNode, BooleanNode, CustomFunctionNode, MathNode, TextOutputNode
from connection import Connection
from toolbar import Toolbar
from property_explorer import PropertyExplorer
from config import threshold
from math import sqrt




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
    
    def create_text_output_node(self):
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
        #update the label and node_name
        new_node.update_label()
        new_node.update_connections()

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
                
        self.property_explorer.populate()
        node.canvas.itemconfig(node.label, text=f"connections: {len(node.connections)}\n Type: {node.node_name}\n ID: {node.id}\n Value: {node.node_value}")


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