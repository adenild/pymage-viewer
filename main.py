from tkinter import *
import tkinter.font as font
from dependencies import commands, side


def main():
    # Configuração do aplicativo
    window = Tk()
    window.title('Simple Label')
    system_font = font.Font(size=16)
    file = side.select_output_file(True)
    images_dir = side.select_images_dir(True)

    # Requisição da data
    images = side.image_loader(images_dir)
    data = side.load_data(file)
    files_dict = side.format_data(data)
    """for item in files_dict:
        print(item)

    # Seleção da lista de imagens
    print("\033[96mQual a lista de imagem que você deseja ver?")
    images_list = input("\033[95m 1. Todas as imagens\n\033[94m 2. Imagens com label\n\033[92m 3. Imagens sem "
                        "label\n\033[96mR: ")
    if images_list == "1":
        data = files_dict["all_files"]
    elif images_list == "2":
        data = files_dict["labelled_files"]
        images = [image for image in files_dict["labelled_files"].keys()]
    elif images_list == "3":
        data = files_dict["not_labelled_files"]
        images = [image for image in files_dict["not_labelled_files"].keys()]"""

    # Cálculo de métricas
    total_images, total_dataset = len(images), len(data)
    index = 0
    if total_images == 0:
        print('Todas as imagens da pasta já receberam labels')
    else:
        print(f"Existem {total_images} imagens. Você está visualizando uma lista com {total_dataset} imagens.")

    # Renderização da imagem
    image = side.setup_image(images_dir, images[index])
    label = Label(image=image)
    label.grid(row=0, column=0, columnspan=3)

    # Renderização do input
    input_box = Entry(window, width=60)
    input_box["font"] = system_font
    input_box.grid(row=1, column=0)
    input_box.insert(0, side.check_labeled(images[index], data))

    local_vars = [index, label, image, total_images, input_box, images, data, file, images_dir,
                  window]  # TODO: Remover isso urgente

    # Renderização dos botões de Ir e Voltar
    button_prev = Button(window, text="Anterior", command=lambda: commands.change_image("prev", local_vars))
    button_prev.grid(row=1, column=2)
    button_next = Button(window, text="Próximo", command=lambda: commands.change_image("next", local_vars))
    button_next.grid(row=1, column=3)

    # Renderização da barra de menus
    menu_bar = Menu(window)
    file_menu = Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Open", command=lambda file=file: side.load_data(file))
    file_menu.add_command(label="Save", command=lambda file=file, data=data: side.save_data_json(file, data))
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=window.quit)
    menu_bar.add_cascade(label="File", menu=file_menu)
    label_menu = Menu(menu_bar, tearoff=0)
    label_menu.add_command(label="All Images", command=lambda: commands.toggle_data_list(local_vars, 'all'))
    label_menu.add_command(label="Labelled", command=lambda: commands.toggle_data_list(local_vars, 'labelled'))
    label_menu.add_command(label="Not Labelled", command=lambda: commands.toggle_data_list(local_vars, 'not labelled'))
    menu_bar.add_cascade(label="Edit", menu=label_menu)
    window.config(menu=menu_bar)

    window.mainloop()


if __name__ == '__main__':
    main()
