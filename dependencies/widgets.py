from tkinter import *
from . import side, commands


def generate_menubar(window, local_vars: list):
    menu_bar = Menu(window)
    file, data = local_vars[7], local_vars[6]

    file_menu = Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Open", command=lambda file=file: side.load_data(file))
    file_menu.add_command(label="Save", command=lambda file=file, data=data: side.save_data_json(file, data))
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=window.quit)
    menu_bar.add_cascade(label="File", menu=file_menu)

    label_menu = Menu(menu_bar, tearoff=0)
    label_menu.add_command(label="All Images", command=commands.test_clicked_button)
    label_menu.add_command(label="Labelled", command=commands.test_clicked_button)
    label_menu.add_command(label="Not Labelled", command=commands.test_clicked_button)
    menu_bar.add_cascade(label="Edit", menu=label_menu)

    window.config(menu=menu_bar)


