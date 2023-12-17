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
