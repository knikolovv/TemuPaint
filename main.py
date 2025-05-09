import math
import random
import json
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle
from tkinter import filedialog

selected_items = set()
select_rect = None
start_x = None
start_y = None
move_start = None

colors = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF",
          "#00FFFF", "#FFA500", "#800080", "#008000", "#000000", "#FFFFFF"]
current_color = "#FFFFFF"
current_border_width = 2
current_opacity = 1

group_counter = 1

copied_items = []

opacity_value_label = None


def menu_action():
    print("Menu button clicked")


def tools_action():
    print("Tools button clicked")


def help_action():
    print("Help button clicked")

def reset_figure_characteristics():
    global current_border_width,current_opacity
    current_border_width = 2
    current_opacity = 1


def draw_square():
    reset_figure_characteristics()
    square_size = 100
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    dx = random.randint(0, canvas_width - square_size - 2)
    dy = random.randint(0, canvas_height - square_size - 2)

    points = [
        dx, dy,
        dx + square_size, dy,
        dx + square_size, dy + square_size,
        dx, dy + square_size
    ]

    opacity_tag = f"opacity_{current_opacity}"
    original_color_tag = f"original_color_{current_color}"

    canvas.create_polygon(points, fill="white", outline="black", width=current_border_width,
                          tags=("figure", opacity_tag, original_color_tag))


def draw_star():
    reset_figure_characteristics()
    outer_radius = 80
    inner_radius = 30

    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    if canvas_width > 2 * outer_radius and canvas_height > 2 * outer_radius:
        x_center = random.randint(outer_radius, canvas_width - outer_radius)
        y_center = random.randint(outer_radius, canvas_height - outer_radius)

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

        opacity_tag = f"opacity_{current_opacity}"
        original_color_tag = f"original_color_{current_color}"

        canvas.create_polygon(star_polygon, fill="white", outline="black", width=current_border_width,
                              tags=("figure", opacity_tag, original_color_tag))


def draw_triangle():
    reset_figure_characteristics()
    side_length = 100
    height = (math.sqrt(3) / 2) * side_length

    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    x1 = random.randint(0, canvas_width - side_length)
    y1 = random.randint(0, canvas_height - int(height))

    points = [
        x1 + side_length / 2, y1,
        x1 + side_length, y1 + height,
        x1, y1 + height
    ]

    opacity_tag = f"opacity_{current_opacity}"
    original_color_tag = f"original_color_{current_color}"

    canvas.create_polygon(points, fill="white", outline="black", width=current_border_width,
                          tags=("figure", opacity_tag, original_color_tag))


def draw_circle():
    reset_figure_characteristics()
    radius = 50
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    cx = random.randint(radius, canvas_width - radius)
    cy = random.randint(radius, canvas_height - radius)

    x1 = cx - radius
    y1 = cy - radius
    x2 = cx + radius
    y2 = cy + radius

    opacity_tag = f"opacity_{current_opacity}"
    original_color_tag = f"original_color_{current_color}"

    canvas.create_oval(x1, y1, x2, y2, fill="white", outline="black", width=current_border_width,
                       tags=("figure", opacity_tag, original_color_tag))


def rgb_to_hex(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))


def apply_alpha_to_color(color, opacity):
    if opacity >= 1.0:
        return color

    r, g, b = hex_to_rgb(color)

    bg_r, bg_g, bg_b = 255, 255, 255

    blend_r = int(r * opacity + bg_r * (1 - opacity))
    blend_g = int(g * opacity + bg_g * (1 - opacity))
    blend_b = int(b * opacity + bg_b * (1 - opacity))

    return rgb_to_hex(blend_r, blend_g, blend_b)


def get_original_color(item):
    for tag in canvas.gettags(item):
        if tag.startswith("original_color_"):
            return tag[len("original_color_"):]
    return current_color


def set_color(color):
    global current_color
    current_color = color
    color_label.config(bg=color)
    change_color_of_selected(color)


def update_border_width(value):
    global current_border_width
    current_border_width = int(float(value))
    apply_border_width_to_selected()


def update_opacity(value):
    global current_opacity
    current_opacity = float(value)
    if opacity_value_label:
        opacity_value_label.config(text=f"{int(current_opacity * 100)}%")
    apply_opacity_to_selected()


def change_color_of_selected(new_color):
    for item in selected_items:
        old_tags = [t for t in canvas.gettags(item) if not t.startswith("original_color_")]
        new_tags = old_tags + [f"original_color_{new_color}"]
        canvas.itemconfig(item, tags=new_tags)

        alpha_color = apply_alpha_to_color(new_color, current_opacity)
        canvas.itemconfig(item, fill=alpha_color)


def apply_opacity_to_selected():
    for item in selected_items:
        original_color = get_original_color(item)
        old_tags = [t for t in canvas.gettags(item) if not t.startswith("opacity_")]
        new_tags = old_tags + [f"opacity_{current_opacity}"]
        alpha_color = apply_alpha_to_color(original_color, current_opacity)
        canvas.itemconfig(item, fill=alpha_color, tags=new_tags)


def apply_border_width_to_selected():
    for item in selected_items:
        canvas.itemconfig(item, width=current_border_width)


def deselect():
    global selected_items
    for item in list(selected_items):
        canvas.itemconfig(item, outline="black")
    selected_items.clear()


def select_item(item):
    if item in selected_items:
        return

    selected_items.add(item)

    group_tags = [tag for tag in canvas.gettags(item) if tag.startswith("group_")]
    if group_tags:
        group_tag = group_tags[0]
        group_items = canvas.find_withtag(group_tag)
        for group_item in group_items:
            canvas.itemconfig(group_item, outline="red")
            select_item(group_item)

        return
    canvas.itemconfig(item, outline="red")


def on_canvas_down(event):
    global start_x, start_y, select_rect, move_start
    start_x, start_y = event.x, event.y
    move_start = (event.x, event.y)

    clicked_items = canvas.find_overlapping(event.x, event.y, event.x, event.y)
    figure_items = [item for item in clicked_items if "figure" in canvas.gettags(item)]

    if figure_items:
        last_item = figure_items[-1]
        group_tags = [tag for tag in canvas.gettags(last_item) if tag.startswith("group_")]
        if last_item not in selected_items:
            deselect()

        if group_tags:
            for item in canvas.find_withtag(group_tags[0]):
                select_item(item)
        else:
            select_item(last_item)

    else:
        deselect()
        select_rect = canvas.create_rectangle(event.x, event.y, event.x, event.y, outline="blue", dash=(2, 2))

    for item in selected_items:
        canvas.tag_raise(item)


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

        for item in items:
            item_tags = canvas.gettags(item)

            if "figure" in item_tags:
                select_item(item)

        canvas.delete(select_rect)
        select_rect = None
    move_start = None


def resize_selected(scale_factor):
    for item in selected_items:
        coordinates = canvas.coords(item)
        if not coordinates:
            continue

        cx = sum(coordinates[::2]) / (len(coordinates) // 2)
        cy = sum(coordinates[1::2]) / (len(coordinates) // 2)

        new_coordinates = []
        for i in range(0, len(coordinates), 2):
            x = coordinates[i]
            y = coordinates[i + 1]
            new_x = cx + (x - cx) * scale_factor
            new_y = cy + (y - cy) * scale_factor
            new_coordinates.extend([new_x, new_y])

        canvas.coords(item, new_coordinates)


def rotate_selected(angle_degrees):
    angle_rad = math.radians(angle_degrees)
    for item in selected_items:

        if canvas.type(item) == "oval":
            continue

        coordinates = canvas.coords(item)
        if not coordinates:
            continue

        cx = sum(coordinates[::2]) / (len(coordinates) // 2)
        cy = sum(coordinates[1::2]) / (len(coordinates) // 2)

        new_coordinates = []
        for i in range(0, len(coordinates), 2):
            x = coordinates[i]
            y = coordinates[i + 1]
            dx = x - cx
            dy = y - cy
            new_x = cx + dx * math.cos(angle_rad) - dy * math.sin(angle_rad)
            new_y = cy + dx * math.sin(angle_rad) + dy * math.cos(angle_rad)
            new_coordinates.extend([new_x, new_y])

        canvas.coords(item, new_coordinates)


def group_selected():
    global group_counter
    if not selected_items:
        return

    existing_group_tag = None
    for item in selected_items:
        for tag in canvas.gettags(item):
            if tag.startswith("group_"):
                existing_group_tag = tag
                break
        if existing_group_tag:
            break

    if existing_group_tag:
        group_tag = existing_group_tag
    else:
        group_tag = f"group_{group_counter}"
        group_counter += 1

    for item in selected_items:
        current_tags = canvas.gettags(item)
        if group_tag not in current_tags:
            new_tags = current_tags + (group_tag,)
            canvas.itemconfig(item, tags=new_tags)


def regroup_selected():
    for item in selected_items:
        current_tags = canvas.gettags(item)
        new_tags = tuple(tag for tag in current_tags if not tag.startswith("group_"))
        canvas.itemconfig(item, tags=new_tags)


def on_key_press(event):
    if event.keysym == "Up" and event.state & 0x04:
        resize_selected(1.1)
    elif event.keysym == "Down" and event.state & 0x04:
        resize_selected(0.9)
    elif event.keysym == "Left" and event.state & 0x04:
        rotate_selected(-15)
    elif event.keysym == "Right" and event.state & 0x04:
        rotate_selected(15)
    elif event.keysym.lower() == "g" and event.state & 0x04:
        group_selected()
    elif event.keysym.lower() == "c" and event.state & 0x04:
        copy_selected()
    elif event.keysym.lower() == "v" and event.state & 0x04:
        paste_copied()
    elif event.keysym == "Delete" and event.state & 0x04:
        delete_selected()
    elif event.keysym.lower() == "a" and event.state & 0x04:
        for item in canvas.find_all():
            select_item(item)


def copy_selected():
    global copied_items
    copied_items = list(selected_items)


def paste_copied():
    global copied_items, group_counter
    if not copied_items:
        return

    deselect()
    new_items = []

    new_group_tag = f"group_{group_counter}"
    group_counter += 1

    for item in copied_items:
        item_type = canvas.type(item)
        coords = canvas.coords(item)
        new_coords = []

        for i in range(0, len(coords), 2):
            new_coords.append(coords[i] + 25)
            new_coords.append(coords[i + 1])

        tags = [tag for tag in canvas.gettags(item) if not tag.startswith("group_")]
        tags.append(new_group_tag)

        fill = canvas.itemcget(item, "fill")
        outline = canvas.itemcget(item, "outline")
        width = float(canvas.itemcget(item, "width"))

        if item_type == "oval":
            new_item = canvas.create_oval(new_coords, fill=fill, outline=outline, width=width, tags=tags)
        elif item_type == "polygon":
            new_item = canvas.create_polygon(new_coords, fill=fill, outline=outline, width=width, tags=tags)
        elif item_type == "rectangle":
            new_item = canvas.create_rectangle(new_coords, fill=fill, outline=outline, width=width, tags=tags)
        else:
            continue

        new_items.append(new_item)

    for item in new_items:
        select_item(item)


def delete_selected():
    global selected_items
    for item in list(selected_items):
        canvas.delete(item)
    selected_items.clear()


def save_canvas():
    items = []
    for item in canvas.find_all():
        item_type = canvas.type(item)
        coords = canvas.coords(item)
        tags = canvas.gettags(item)
        options = canvas.itemconfig(item)
        fill = options["fill"][-1] if "fill" in options else ""
        outline = options["outline"][-1] if "outline" in options else ""
        width = options["width"][-1] if "width" in options else ""

        items.append({
            "type": item_type,
            "coords": coords,
            "tags": tags,
            "fill": fill,
            "outline": outline,
            "width": width
        })

    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
    if file_path:
        with open(file_path, "w") as f:
            json.dump(items, f, indent=4)


def load_canvas():
    global selected_items
    file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
    if file_path:
        canvas.delete("all")
        selected_items.clear()
        with open(file_path, "r") as f:
            items = json.load(f)
            for item in items:
                item_id = None
                if item["type"] == "polygon":
                    item_id = canvas.create_polygon(item["coords"], fill=item["fill"], outline=item["outline"],
                                                      width=item["width"])
                elif item["type"] == "oval":
                    item_id = canvas.create_oval(item["coords"], fill=item["fill"], outline=item["outline"],
                                                 width=item["width"])

                if item_id and item["tags"]:
                    canvas.itemconfig(item_id, tags=item["tags"])


root = tk.Tk()
root.title("Graphic Editor")
root.geometry("1600x900")
root.bind("<KeyPress>", on_key_press)
# Added regrouping explicitly here because of Windows reserving the alt key for some operations preventing me from using it in the function somehow
root.bind("<Alt-g>", lambda event: regroup_selected())

style = ThemedStyle(root)
style.set_theme("equilux")

dark_background = "#303030"

style.configure("Custom.TFrame", background=dark_background)
style.configure("TButton", background=dark_background, relief="flat")
style.map("TButton", foreground=[("active", "#DDDDDD")])

menu_button_frame = ttk.Frame(root, style="Custom.TFrame")
menu_button_frame.pack(anchor="nw", fill="x")

menu_button = ttk.Button(menu_button_frame, text="Menu", command=menu_action)
menu_button.pack(side="left")

tools_button = ttk.Button(menu_button_frame, text="Tools", command=tools_action)
tools_button.pack(side="left")

help_button = ttk.Button(menu_button_frame, text="Help", command=help_action)
help_button.pack(side="left")

save_button = ttk.Button(menu_button_frame, text="Save", command=save_canvas)
save_button.pack(side="left")

load_button = ttk.Button(menu_button_frame, text="Open", command=load_canvas)
load_button.pack(side="left")

shape_frame = ttk.Frame(root, style="Custom.TFrame")
shape_frame.pack(anchor="n", fill="x")

square_button = ttk.Button(shape_frame, text="□", command=draw_square)
square_button.pack(side="left")

star_button = ttk.Button(shape_frame, text="☆", command=draw_star)
star_button.pack(side="left")

triangle_button = ttk.Button(shape_frame, text="△", command=draw_triangle)
triangle_button.pack(side="left")

circle_button = ttk.Button(shape_frame, text="○", command=draw_circle)
circle_button.pack(side="left")

properties_frame = ttk.Frame(root, style="Custom.TFrame")
properties_frame.pack(anchor="n", fill="x")

color_frame = ttk.Frame(properties_frame, style="Custom.TFrame")
color_frame.pack(side="left", padx=10)

color_label = ttk.Label(color_frame, text="Color:")
color_label.pack(side="left")

color_label = tk.Label(color_frame, width=3, height=1, bg="#FFFFFF", relief="raised")
color_label.pack(side="left", padx=5)

color_palette = ttk.Frame(color_frame, style="Custom.TFrame")
color_palette.pack(side="left")

for color in colors:
    color_button = tk.Button(color_palette, bg=color, width=2, height=1,
                             command=lambda c=color: set_color(c))
    color_button.pack(side="left", padx=1)

border_frame = ttk.Frame(properties_frame, style="Custom.TFrame")
border_frame.pack(side="left", padx=20)

border_label = ttk.Label(border_frame, text="Border Width:", )
border_label.pack(side="left")

border_width_slider = ttk.Scale(border_frame, from_=1, to=5, orient="horizontal",
                                length=100, command=update_border_width)
border_width_slider.set(current_border_width)
border_width_slider.pack(side="left")

opacity_frame = ttk.Frame(properties_frame, style="Custom.TFrame")
opacity_frame.pack(side="left", padx=20)

opacity_label = ttk.Label(opacity_frame, text="Opacity:")
opacity_label.pack(side="left")

opacity_slider = ttk.Scale(opacity_frame, from_=0.0, to=1.0, orient="horizontal",
                           length=100, command=update_opacity)
opacity_slider.set(current_opacity)
opacity_slider.pack(side="left")

opacity_value_label = ttk.Label(opacity_frame, text="100%", width=4)
opacity_value_label.pack(side="left", padx=5)

resize_up_button = ttk.Button(properties_frame, text="Resize +", command=lambda: resize_selected(1.1))
resize_up_button.pack(side="left", padx=2)

resize_down_button = ttk.Button(properties_frame, text="Resize -", command=lambda: resize_selected(0.9))
resize_down_button.pack(side="left", padx=2)

rotate_left_button = ttk.Button(properties_frame, text="⟲ Rotate", command=lambda: rotate_selected(-15))
rotate_left_button.pack(side="left", padx=2)

rotate_right_button = ttk.Button(properties_frame, text="⟳ Rotate", command=lambda: rotate_selected(15))
rotate_right_button.pack(side="left", padx=2)

group_button = ttk.Button(properties_frame, text="Group", command=group_selected)
group_button.pack(side="left", padx=2)

regroup_button = ttk.Button(properties_frame, text="Regroup", command=regroup_selected)
regroup_button.pack(side="left", padx=2)

delete_button = ttk.Button(properties_frame, text="Delete", command=delete_selected)
delete_button.pack(side="left", padx=2)

canvas = tk.Canvas(root, bg="white")
canvas.pack(fill="both", expand=True)

canvas.bind("<ButtonPress-1>", on_canvas_down)
canvas.bind("<B1-Motion>", on_canvas_drag)
canvas.bind("<ButtonRelease-1>", on_canvas_release)

root.mainloop()