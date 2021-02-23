from tkinter import *
from tkinter import font, filedialog
import os
import json
from PIL import ImageTk, Image


def select_dir(debug=False):
    """
    Abre um diálogo para a seleção de uma pasta, onde ficam as imagens que receberão label.

    :param debug: Booleano que ativa o modo de testes
    :return: O caminho da pasta que contém as imagens
    """
    if debug:
        return "debug/placa"
    return filedialog.askdirectory()


def select_file(debug=False):
    """
    Pergunta o nome do arquivo em que os dados serão salvos no console, caso não exista ele cria um.

    :param debug: Booleano que ativa o modo de testes
    :return: Caminho do arquivo em que os dados serão salvos
    """
    if debug:
        return "debug/debug.json"
    return input("Digite o nome do arquivo: ")


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


def save_data(file, data):
    """
    Salva o objeto Python novamente no arquivo JSON.

    :param file: Arquivo em que serão gravados os dados
    :param data: Dados a serem gravados no arquivo
    """
    print("Salvando")
    with open(f"{file}", "w") as write_file:
        json.dump(data, write_file, indent=1)


def populate_json(images_list):
    """
    Popula o arquivo JSON com todas as imagens na lista

    :param images_list: lista contendo as imagens a serem incluídas no arquivo
    :return: objeto Python populado com as imagens
    """
    data = {}
    for image in images_list:
        data[image] = {'bbox': "None", 'label': ''}
    return data


def load_data(file, images_list, total_images):
    """
    Carrega o arquivo JSON com os dados, transformando tudo em um objeto Python.

    :param total_images: variavel com o número de imagens que serão exibidas
    :param images_list: Lista das imagens que serão exibidas
    :param file: Caminho pro objeto JSON que será lido
    :return: Objeto Python com os mesmo dados contidos no JSON
    """
    print("Carreguei")
    try:
        with open(f"{file}", "r") as read_file:
            data = json.load(read_file)
            if len(data) == 0 or len(data) < total_images:
                data = populate_json(images_list)
    except:
        print("Entrei no except do load_data")
        open(f"{file}", 'w+').close()
        data = populate_json(images_list)
    return data


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

    print(f'{len(files_dict["labelled_files"])} imagens com label foram detectadas no arquivo de entrada.')
    return files_dict


def setup_image(images_dir, list_position):
    """
    Prepara o objeto da imagem do Tkinter pra ser exibido

    :param images_dir: Lista das imagens
    :param list_position: Index na lista
    :return: Objeto no template para ser exibido
    """
    im = Image.open(f"{images_dir}/{list_position}")
    im.thumbnail((800, 600))
    return ImageTk.PhotoImage(im)


def check_labeled(image, data_file):
    """
    Verifica se a imagem que está sendo exibida já tem label. Se tiver, ela é inserida no input

    :param image: Imagem que está sendo visualizada
    :param data_file: Dicionário com os objetos contendo o valor da label
    :return: A label salva no arquivo
    """
    try:
        if data_file[image]['label'] == '':
            return ''
        else:
            return data_file[image]['label']
    except:
        return ''


def show_position(actual, total):
    """
    Gera a posição da imagem dentro da lista

    :param actual: Posição que a imagem exibida tem na lista
    :param total: Total de imagens da lista
    :return:
    """
    return f"[{actual+1}/{total}]"


class App(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        # Configuração do aplicativo
        self.title("Simple Label")
        self.system_font = font.Font(size=13)

        # Configuração das variáveis
        self.debug = True
        self.file = select_file(True)
        self.directory = select_dir(True)
        self.raw_images = image_loader(self.directory)
        self.images = self.raw_images
        self.total_images = len(self.images)
        self.raw_data = load_data(self.file, self.images, self.total_images)
        self.data = self.raw_data
        self.files_dict = format_data(self.data)
        self.index = 0

        # Seleção da lista de imagens
        self.change_data()

        # Cálculos para informação
        self.total_images = len(self.images)
        if self.total_images == 0:
            print('Todas as imagens da pasta já receberam labels')
        else:
            print(f"Você está visualizando {self.total_images} imagens.")

        # Renderização da imagem
        self.image = setup_image(self.directory, self.images[self.index])
        self.label = Label(image=self.image)
        self.label.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        # Renderização do input
        self.image_input = Entry(self, width=60)
        self.image_input["font"] = self.system_font
        self.image_input.grid(row=1, column=2, padx=5)
        self.image_input.insert(0, check_labeled(self.images[self.index], self.data))

        # Renderização dos botões
        self.button_previous = Button(self,font=self.system_font, text="Previous", command=lambda: self.change_image("prev"))
        self.button_previous.grid(row=1, column=1, padx=2.5, pady=2.5)
        self.button_next = Button(self, font=self.system_font, text="Next", command=lambda: self.change_image("next"))
        self.button_next.grid(row=1, column=3, padx=2.5, pady=2.5)

        # Renderização da barra de menu
        self.menu_bar = Menu(self)
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Open", command=lambda: load_data(self.file, self.images, self.total_images))
        self.file_menu.add_command(label="Save", command=lambda: save_data(self.file, self.data))
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.quit)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.label_menu = Menu(self.menu_bar, tearoff=0)
        self.label_menu.add_command(label="All Images", command=lambda: self.menu_change_data("1"))
        self.label_menu.add_command(label="Labelled", command=lambda: self.menu_change_data("2"))
        self.label_menu.add_command(label="Not Labelled", command=lambda: self.menu_change_data("3"))
        self.menu_bar.add_cascade(label="Edit", menu=self.label_menu)
        self.config(menu=self.menu_bar)

        # Execução da janela
        self.mainloop()

    def change_data(self, selected_list: str = None):
        """
        Faz toda a configuração dos dados para o dicionário que o usuário preferir

        :param selected_list: String com um número que representa qual dicionário foi escolhido
        """
        if not selected_list:
            options = ["Todas as imagens", "Imagens com label", "Imagens sem label"]
            if len(self.files_dict["labelled_files"]) == 0:
                options.remove("Imagens com label")

            print("\033[93mQual a lista de imagem que você deseja ver?")
            for option in range(len(options)):
                print(f"\033[91m{option+1}. {options[option]}")
            selected_list = input("\033[96mR: ")
            """selected_list = input("\033[95m 1. Todas as imagens\n\033[94m 2. Imagens com label\n\033[92m 3. Imagens "
                                  "sem label\n\033[96mR: ")"""
        if selected_list == "1":
            self.data = self.files_dict["all_files"]
            self.images = [image for image in self.files_dict["all_files"].keys()]
        elif selected_list == "2":
            self.data = self.files_dict["labelled_files"]
            self.images = [image for image in self.files_dict["labelled_files"].keys()]
        elif selected_list == "3":
            self.data = self.files_dict["not_labelled_files"]
            self.images = [image for image in self.files_dict["not_labelled_files"].keys()]
        self.index = 0
        self.total_images = len(self.images)

    def menu_change_data(self, selected_list: str):
        """
        Versão com mais comandos, configurando o dicionário, limpando o input e mudando a imagem

        :param selected_list: String com um número que representa qual dicionário foi escolhido
        """
        self.change_data(selected_list)
        self.update_input()
        self.update_image()

    def change_window_title(self):
        """
        Muda o título da janela pra colocar o nome da imagem junto
        """
        self.title(f"{self.images[self.index]} - Simple Label")

    def save(self):
        """
        Mescla o dicionário que o usuário edita com o dicionário com todas as imagens e salva no arquivo
        """
        save = {self.images[self.index]: {'bbox': "None", 'label': self.image_input.get().upper()}}
        self.data.update(save)
        self.raw_data.update(save)
        print(save)
        save_data(self.file, self.raw_data)

    def update_input(self):
        """
        Atualiza o input, colocando a label se houver, ou limpando a que tinha
        """
        self.image_input.delete(0, 'end')
        label_text = check_labeled(self.images[self.index], self.data)
        self.image_input.insert(0, label_text)

    def update_image(self):
        """
        Atualiza, efetivamente, a imagem que é exibida na tela
        """
        self.label.grid_forget()
        self.image = setup_image(self.directory, self.images[self.index])
        self.label = Label(image=self.image)
        self.label.grid(row=0, column=0, columnspan=3)

    def change_image(self, next_or_prev: str):
        """
        Função de execução das outras, é chamada quando o botão de mudar a imagem é apertado

        :param next_or_prev: String que diz qual a direção deve ser tomada na lista
        :return:
        """
        print(show_position(self.index, self.total_images))
        self.save()

        if next_or_prev == "next":
            if self.index + 1 == self.total_images:
                self.index = 0
            else:
                self.index += 1
        elif next_or_prev == "prev":
            if self.index - 1 == -1:
                self.index = self.total_images - 1
            else:
                self.index -= 1

        self.update_input()
        self.update_image()
        self.change_window_title()

        if self.debug:
            for dictionary in self.files_dict:
                print(f"{dictionary}: {self.files_dict[dictionary]}")


if __name__ == '__main__':
    app = App()
