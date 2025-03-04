import math
import random
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle

selected_items = set()
select_rect = None
start_x = None
start_y = None
move_start = None


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

    dx = random.randint(0, canvas_width - square_size - 2)
    dy = random.randint(0, canvas_height - square_size - 2)

    dx2, dy2 = dx + square_size, dy + square_size

    canvas.create_rectangle(dx, dy, dx2, dy2, fill="white", outline="black", width=2, tags=("figure",))


def draw_star():
    outer_radius = 80
    inner_radius = 30

    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    if canvas_width > 2 * outer_radius and canvas_height > 2 * outer_radius:
        x_center = random.randint(outer_radius, canvas_width - outer_radius)
        y_center = random.randint(outer_radius, canvas_height - outer_radius)

        star_tag = f"star_{random.randint(1, 9999)}"

        points = []
        for i in range(10):
            angle_deg = 36 * i - 90
            angel_rad = math.radians(angle_deg)
            r = outer_radius if i % 2 == 0 else inner_radius
            x = x_center + r * math.cos(angel_rad)
            y = y_center + r * math.sin(angel_rad)
            points.append((x, y))

        star_polygon = []
        for (px, py) in points:
            star_polygon.extend([px, py])

        canvas.create_polygon(star_polygon, fill="white", outline="black", width=2, tags=("figure", star_tag))

        for (px, py) in points:
            canvas.create_line(x_center, y_center, px, py, fill="black", width=2, tags=("figure", star_tag))


def deselect():
    global selected_items
    for item in list(selected_items):
        item_type = canvas.type(item)
        if item_type in ["rectangle", "polygon"]:
            canvas.itemconfig(item, outline="black", width=2)
        elif item_type == "line":
            canvas.itemconfig(item, fill="black", width=2)
    selected_items.clear()


def select_item(item):
    selected_items.add(item)
    item_type = canvas.type(item)
    if item_type in ["rectangle", "polygon"]:
        canvas.itemconfig(item, outline="red", width=2)
    elif item_type == "line":
        canvas.itemconfig(item, fill="red", width=2)


def on_canvas_down(event):
    global start_x, start_y, select_rect, move_start
    start_x, start_y = event.x, event.y
    move_start = (event.x, event.y)

    clicked_items = canvas.find_overlapping(event.x, event.y, event.x, event.y)
    figure_items = [item for item in clicked_items if "figure" in canvas.gettags(item)]

    if figure_items:

        star_tags = [tag for tag in canvas.gettags(figure_items[-1]) if tag.startswith("star_")]
        if star_tags:

            star_tag = star_tags[0]
            items_to_select = canvas.find_withtag(star_tag)

            if figure_items[-1] not in selected_items:
                deselect()
                for item in items_to_select:
                    select_item(item)

        if figure_items[-1] not in selected_items:
            deselect()
            select_item(figure_items[-1])
    else:
        deselect()
        select_rect = canvas.create_rectangle(event.x, event.y, event.x, event.y, outline="blue", dash=(2, 2))


def on_canvas_drag(event):
    global select_rect, move_start
    if select_rect:
        canvas.coords(select_rect, start_x, start_y, event.x, event.y)
    elif selected_items and move_start:
        dx = event.x - move_start[0]
        dy = event.y - move_start[1]
        for item in selected_items:
            canvas.move(item, dx, dy)
        move_start = (event.x, event.y)


def on_canvas_release(event):
    global select_rect, move_start

    if select_rect:
        x1, y1, x2, y2 = canvas.coords(select_rect)
        if x1 > x2: x1, x2 = x2, x1
        if y1 > y2: y1, y2 = y2, y1
        items = canvas.find_overlapping(x1, y1, x2, y2)

        star_tags = set()

        for item in items:
            item_tags = canvas.gettags(item)

            if "figure" in item_tags or any(tag.startswith("star_") for tag in item_tags):
                star_tags.update([tag for tag in item_tags if tag.startswith("star_")])
                select_item(item)

        for star_tag in star_tags:
            star_items = canvas.find_withtag(star_tag)
            for item in star_items:
                select_item(item)

        canvas.delete(select_rect)
        select_rect = None
    move_start = None


root = tk.Tk()
root.title("Graphic Editor")
root.geometry("1280x720")

style = ThemedStyle(root)
style.set_theme("equilux")

dark_background = "#303030"

style.configure("Custom.TFrame", background=dark_background)
style.configure("TButton", background=dark_background, relief="flat")
style.map("TButton", foreground=[("active", "#DDDDDD")])

button_frame = ttk.Frame(root, style="Custom.TFrame")
button_frame.pack(anchor="nw", fill="x")

menu_button = ttk.Button(button_frame, text="Menu", command=menu_action)
menu_button.pack(side="left")

tools_button = ttk.Button(button_frame, text="Tools", command=tools_action)
tools_button.pack(side="left")

help_button = ttk.Button(button_frame, text="Help", command=help_action)
help_button.pack(side="left")

shape_frame = ttk.Frame(root, style="Custom.TFrame")
shape_frame.pack(anchor="n", fill="x")

square_button = ttk.Button(shape_frame, text="sqr", command=draw_square)
square_button.pack(side="left")

star_button = ttk.Button(shape_frame, text="star", command=draw_star)
star_button.pack(side="left")

canvas = tk.Canvas(root, bg="white")
canvas.pack(fill="both", expand=True)

canvas.bind("<ButtonPress-1>", on_canvas_down)
canvas.bind("<B1-Motion>", on_canvas_drag)
canvas.bind("<ButtonRelease-1>", on_canvas_release)

root.mainloop()