from tkinter import *
import tkinter.font as font
import side as side


# TODO: Passar todas as funções pra outro arquivo
# TODO: Adicionar hotkeys de passar e voltas
# TODO: Criar os botões para tipos de lista
# TODO: Criar botão de salvar
# TODO: Adicionar campo de ir até x imagem
def main():
    window = Tk()
    window.title('Não é o Labelme')
    system_font = font.Font(size=16)
    file = side.select_output_file()
    images_dir = side.select_images_dir()

    images = side.image_loader(images_dir)
    data = side.load_data(file, images)

    labeled_files = side.starter_list(data)
    total_images = len(images)
    index = 0

    if total_images == 0:
        print('Todas as imagens da pasta ja receberam labels')
        exit(200)
    else:
        print(f"Existem {total_images} imagens.")

    side.generate_menubar(window)

    image = side.setup_image(images_dir, images[index])
    label = Label(image=image)
    label.image = image
    label.grid(row=0, column=0, columnspan=3)

    # TODO: Fazer a validação dos dados
    def change_image(next_or_prev: str):
        nonlocal index
        nonlocal label
        nonlocal image

        print(side.show_position(index, total_images))

        save = {images[index]: {'bbox': "None", 'label': input_box.get().upper()}}
        data.update(save)
        print(save)
        side.save_data_json(file, data)

        if next_or_prev == "next":
            if index + 1 == total_images:
                print('Fim das imagens.')
                exit(200)
            else:
                index += 1
        elif next_or_prev == "prev":
            if index - 1 < 0:
                print("Não existem imagens antes dessa")
                exit(200)
            else:
                index -= 1

        input_box.delete(0, 'end')
        label_text = side.check_labeled(images[index], data)
        input_box.insert(0, label_text)
        label.grid_forget()

        image = side.setup_image(images_dir, images[index])
        label = Label(image=image)
        label.image = image
        label.grid(row=0, column=0, columnspan=3)

    input_box = Entry(window, width=60)
    input_box["font"] = system_font
    input_box.grid(row=1, column=0)
    label_text = side.check_labeled(images[index], data)
    input_box.insert(0, label_text)

    button_prev = Button(window, text="Anterior", command=lambda next_or_prev="prev": change_image(next_or_prev))
    button_prev.grid(row=1, column=2)
    button_next = Button(window, text="Próximo", command=lambda next_or_prev="next": change_image(next_or_prev))
    button_next.grid(row=1, column=3)

    window.mainloop()


if __name__ == '__main__':
    main()
