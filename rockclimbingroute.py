import tkinter as tk
import math

class RockClimbingApp:
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(self.master, width=2560, height=1080, bg='white')
        self.canvas.pack()
        self.holds = {}  # To store hold coordinates
        self.canvas.bind("<Button-1>", self.add_hold)
        self.canvas.bind("<Button-3>", self.remove_hold)
        
    def add_hold(self, event):
        x, y = event.x, event.y
        hold_id = self.canvas.create_oval(x-5, y-5, x+5, y+5, fill="blue")
        self.holds[hold_id] = (x, y)
        self.update_paths()
        
    def remove_hold(self, event):
        if hold_id := self.canvas.find_closest(event.x, event.y):
            self.canvas.delete(hold_id[0])
            del self.holds[hold_id[0]]
            self.update_paths()
        
    def update_paths(self):
        self.canvas.delete("path")
        for id1, (x1, y1) in self.holds.items():
            for id2, (x2, y2) in self.holds.items():
                if id1 != id2:
                    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                    angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
                    if self.check_constraints(distance, angle):
                        self.canvas.create_line(x1, y1, x2, y2, tags="path")
                        
    def check_constraints(self, distance, angle):
        # Add your constraints here, for now, let's just limit the distance
        return distance < 75

if __name__ == "__main__":
    root = tk.Tk()
    app = RockClimbingApp(root)
    root.mainloop()
