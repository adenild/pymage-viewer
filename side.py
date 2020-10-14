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
        return "images"
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


def check_labels():
    pass


def read_previous_data(file):
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


# TODO: Refazer com uma só lista permitindo ir e voltar
def starter_list(data, images):
    removidas = []
    for key in data.keys():
        if key in images:
            removidas.append(key)
            images.remove(key)

    print(f'{len(removidas)} imagens ja foram detectadas no arquivo de entrada.')
    return images, removidas


def setup_image(images_dir, list_position):
    im = Image.open(f"{images_dir}/{list_position}")
    im.thumbnail((800, 600))
    return ImageTk.PhotoImage(im)


def show_position(actual, total):
    return f"[{actual+1}/{total}]"
