from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
import os
import json


def select_output_file(debug=False):
    """
    Pergunta o nome do arquivo em que os dados serão salvos no console, caso não exista ele cria um.

    :param debug: Booleano que ativa o modo de testes
    :return: Caminho do arquivo em que os dados serão salvos
    """
    if debug:
        return "debug/labels.json"
    return input("Digite o nome do arquivo: ")


def select_images_dir(debug=False):
    """
    Abre um diálogo para a seleção de uma pasta, onde ficam as imagens que receberão label.

    :param debug: Booleano que ativa o modo de testes
    :return: O caminho da pasta que contém as imagens
    """
    if debug:
        return "debug/placa"
    return filedialog.askdirectory()


def image_loader(images_dir):
    """
    Gera uma lista com os nomes das imagens, que será utilizada junto com a pasta delas pra exibição.

    :param images_dir: Caminho das imagens
    :return: Lista com cada objeto sendo um nome de imagem
    """
    images = []
    image_extensions = ['png', 'jpg', 'jpeg', 'tif', 'gif']
    for file in os.listdir(f'{images_dir}/'):
        if file.split('.')[-1] in image_extensions:
            images.append(file)

    if not len(images):
        print("Não foram encontradas imagens na pasta selecionada.")
        quit(200)

    return images


def load_data(file):
    """
    Carrega o arquivo JSON com os dados, transformando tudo em um objeto Python.

    :param file: Caminho pro objeto JSON que será lido
    :return: Objeto Python com os mesmo dados contidos no JSON
    """
    print("Carreguei")
    try:
        with open(f"{file}", "r") as read_file:
            data = json.load(read_file)
    except:
        open(f"{file}", 'w+').close()
        data = {}
    return data


def save_data_json(file, data):
    """
    Salva o objeto Python novamente no arquivo JSON.

    :param file: Arquivo em que serão gravados os dados
    :param data: Dados a serem gravados no arquivo
    """
    with open(f"{file}", "w") as write_file:
        json.dump(data, write_file, indent=1)


def format_data(data):
    """
    Formata os dados, retornando um dicionário com 3 chaves. Essas chaves contém cada lista de imagem

    :param data: A data crua, recém carregada do arquivo
    :return:
    """
    files_dict = {"all_files": {}, "labelled_files": {}, "not_labelled_files": {}}
    for key in data.keys():
        files_dict["all_files"][key] = (data[key])
        if len(data[key]["label"]) > 0:
            files_dict["labelled_files"][key] = (data[key])
        else:
            files_dict["not_labelled_files"][key] = (data[key])

    print(f'{len(files_dict["labelled_files"])} imagens foram detectadas no arquivo de entrada.')
    return files_dict


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
