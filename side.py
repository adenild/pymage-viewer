from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
import os
import json


def select_output_file(debug=False):
    if debug:
        return "debug/labels.json"
    return input("Digite o nome do arquivo: ")


def select_images_dir(debug=False):
    if debug:
        return "images/placa"
    return filedialog.askdirectory()


def image_loader(images_dir):
    # Pega a lista das imagens
    images = []
    image_extensions = ['png', 'jpg', 'jpeg', 'tif', 'gif']
    for file in os.listdir(f'{images_dir}/'):
        if file.split('.')[-1] in image_extensions:
            images.append(file)

    if not len(images):
        print("Não foram encontradas imagens na pasta selecionada.")
        quit(200)

    return images


def load_data(file, images_list):
    try:
        with open(f"{file}", "r") as read_file:
            data = json.load(read_file)
    except:
        open(f"{file}", 'w+').close()
        data = {}
    return data


def save_data_json(file, data):
    with open(f"{file}", "w") as write_file:
        json.dump(data, write_file, indent=1)


# TODO: Encontrar um novo nome pra função
def starter_list(data):
    labeled_files = []
    for key in data.keys():
        if len(data[key]["label"]) > 0:
            labeled_files.append(key)

    print(f'{len(labeled_files)} imagens ja foram detectadas no arquivo de entrada.')
    return labeled_files


def setup_image(images_dir, list_position):
    im = Image.open(f"{images_dir}/{list_position}")
    im.thumbnail((800, 600))
    return ImageTk.PhotoImage(im)


def show_position(actual, total):
    return f"[{actual+1}/{total}]"


def check_labeled(image, data_file):
    try:
        if data_file[image]['label'] == '':
            return ''
        else:
            return data_file[image]['label']
    except:
        return ''

def generate_menubar(window):
    menubar = Menu(window)

    # create a dropdown menu.
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Open",command=test_clicked_button)
    filemenu.add_command(label="Save",command=test_clicked_button)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=window.quit)
    menubar.add_cascade(label="File", menu=filemenu)

    labelmenu = Menu(menubar, tearoff=0)
    labelmenu.add_command(label="All Images", command=test_clicked_button)
    labelmenu.add_command(label="Labelled", command=test_clicked_button)
    labelmenu.add_command(label="Not Labelled", command=test_clicked_button)
    menubar.add_cascade(label="Edit", menu=labelmenu)

    window.config(menu=menubar)

def test_clicked_button():
    print('This button was clicked')
