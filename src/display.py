import tkinter as tk
from tkinter.simpledialog import askstring

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.canvas = tk.Canvas(self.root, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.create_targets_button = tk.Button(self.root, text="Create Targets", command=self.create_targets)
        self.create_targets_button.place(x=10, y=10)  # Position at top left

        self.create_targets_callback = None

        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()

    def start(self):
        self.root.mainloop()

    def set_click_listener(self, callback):
        self.canvas.bind("<Button-1>", callback)

    def show_popup(self):
        return askstring("Input", "Enter the command:")

    def draw_robot(self, joints):
        self.canvas.create_line(joints[0][0], joints[0][1], joints[1][0], joints[1][1], fill='blue', width=5)
        self.canvas.create_line(joints[1][0], joints[1][1], joints[2][0], joints[2][1], fill='green', width=5)

    def clear_canvas(self):
        self.canvas.delete("all")

    def set_create_targets_listener(self, callback):
        self.create_targets_callback = callback

    def create_targets(self):
        if self.create_targets_callback:
            self.create_targets_callback()
