import random
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle


def menu_action():
    print("Menu button clicked")

def tools_action():
    print("Tools button clicked")

def help_action():
    print("Help button clicked")

def draw_square():
    square_size = 100
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    dx = random.randint(0,canvas_width - square_size)
    dy = random.randint(0,canvas_height - square_size)

    dx2,dy2 = dx + square_size, dy + square_size

    canvas.create_rectangle(dx,dy,dx2,dy2,fill="white",outline="black",width=2)


root = tk.Tk()
root.title("Graphic Editor")
root.geometry("1280x720")

style = ThemedStyle(root)
style.set_theme("equilux")

dark_background = "#303030"

style.configure("Custom.TFrame", background=dark_background)
style.configure("TButton", background=dark_background,relief="flat")

style.map("TButton",foreground=[("active", "#DDDDDD")])

button_frame = ttk.Frame(root, style="Custom.TFrame")
button_frame.pack(anchor="nw",fill="x")

menu_button = ttk.Button(button_frame, text="Menu", command=menu_action)
menu_button.pack(side="left")

tools_button = ttk.Button(button_frame, text="Tools", command=tools_action)
tools_button.pack(side="left")

help_button = ttk.Button(button_frame, text="Help", command=help_action)
help_button.pack(side="left")

shape_frame = ttk.Frame(root, style="Custom.TFrame")
shape_frame.pack(anchor="n",fill="x")

square_button = ttk.Button(shape_frame,text="sqr", command=draw_square)
square_button.pack(side="left")

canvas = tk.Canvas(root, bg="white")
canvas.pack(fill="both", expand=True)

root.mainloop()
