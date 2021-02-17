from tkinter import *
import tkinter.font as font
import commands
import side
import widgets


def main():
    window = Tk()
    window.title('Simple Label')
    system_font = font.Font(size=16)
    file = side.select_output_file(True)
    images_dir = side.select_images_dir(True)

    images = side.image_loader(images_dir)
    data = side.load_data(file, images)

    labeled_files = side.starter_list(data)
    total_images = len(images)
    index = 0

    if total_images == 0:
        print('Todas as imagens da pasta já receberam labels')
    else:
        print(f"Existem {total_images} imagens.")

    image = side.setup_image(images_dir, images[index])
    label = Label(image=image)
    label.image = image
    label.grid(row=0, column=0, columnspan=3)

    input_box = Entry(window, width=60)
    input_box["font"] = system_font
    input_box.grid(row=1, column=0)
    label_text = side.check_labeled(images[index], data)
    input_box.insert(0, label_text)
    local_vars = [index, label, image, total_images, input_box, images, data, file, images_dir]
    button_prev = Button(window, text="Anterior", command=lambda next_or_prev="prev", local_vars=local_vars: commands.change_image(next_or_prev, local_vars))
    button_prev.grid(row=1, column=2)
    button_next = Button(window, text="Próximo", command=lambda next_or_prev="next", local_vars=local_vars: commands.change_image(next_or_prev, local_vars))
    button_next.grid(row=1, column=3)

    widgets.generate_menubar(window, local_vars)
    window.mainloop()


if __name__ == '__main__':
    main()
