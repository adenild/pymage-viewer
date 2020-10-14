from tkinter import *
import tkinter.font as font
import side as side


def main():
    window = Tk()
    window.title('Não é o Labelme')
    system_font = font.Font(size=16)
    file = side.select_output_file(True)
    images_dir = side.select_images_dir(True)

    data = side.read_previous_data(file)
    images = side.image_loader(images_dir)

    images, removidas = side.starter_list(data, images)
    total_images = len(images)
    index = 0

    if total_images == 0:
        print('Todas as imagens da pasta ja receberam labels')
        exit(200)
    else:
        print(f"Existem {total_images} imagens.")

    image = side.setup_image(images_dir, images[index])
    label = Label(image=image)
    label.image = image
    label.grid(row=0, column=0, columnspan=3)

    # TODO: Consertar o final do loop. Ta travando o programa
    # TODO: Fazer a validação dos dados
    def next_image():
        nonlocal index
        nonlocal label
        nonlocal image

        print(side.show_position(index, total_images))

        save = {images[index]: {'bbox': "None", 'label': input_box.get()}}
        data.update(save)
        print(save)
        side.save_data_json(file, data)

        if index + 1 == total_images:
            print('Fim das imagens.')
            exit(200)
        else:
            index += 1

        input_box.delete(0, 'end')
        label.grid_forget()

        image = side.setup_image(images_dir, images[index])
        label = Label(image=image)
        label.image = image
        label.grid(row=0, column=0, columnspan=3)

    input_box = Entry(window, width=60)
    input_box["font"] = system_font
    input_box.grid(row=1, column=0)

    button_next = Button(window, text="Próximo", command=next_image)
    button_next.grid(row=1, column=2)

    window.mainloop()


if __name__ == '__main__':
    main()
