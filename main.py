from tkinter import *
from PIL import ImageTk, Image
import os


def main():
    file_name = 'labels.txt'  # input("Qual vai ser o nome do arquivo? ")

    window = Tk()
    window.title('Não é o Labelme')

    images = []
    for file in os.listdir('images/'):
        if '.txt' in file:
            pass
        else:
            images.append(file)
    lines = open(f"outputs/{file_name}", 'r').readlines()
    index = 0
    if len(lines) >= 1:
        last_line = lines.index(lines[-1])
        index = last_line
        last_line_string = open(f"outputs/{file_name}", "r").readlines()[last_line]
        line = index-1
    else:
        pass

    total_images = len(images)
    print(f"Existem {total_images} imagens.")
    print(f"Você está atualmente na imagem {images[index]}")

    im = Image.open(f"images/{images[index]}")
    im.thumbnail((800, 600))
    ph = ImageTk.PhotoImage(im)

    label = Label(image=ph)
    label.image = ph
    label.grid(row=0, column=0, columnspan=3)

    def save(output: str):
        open(f'outputs/{file_name}', 'a+').write(output)
        print(f"Você digitou {output.split(',')[2]} no arquivo {images[index]}")

    def edit(output: str):
        lines_list = open(f"outputs/{file_name}", "r").readlines()
        if lines_list[line] != output:
            lines_list[line] = output
            open(f"outputs/{file_name}", "w").writelines(lines_list)

    # TODO: Consertar o final do loop. Ta travando o programa
    # TODO: Fazer a validação dos dados
    def next_image():
        nonlocal index
        nonlocal label
        nonlocal im
        nonlocal ph

        output = f"{images[index]},None,{input_box.get()}\n"
        if last_line_string.replace('\n', '') == output.replace('\n', '') or input_box.get() == '':
            input_box.delete(0, 'end')

            index += 1

            label.grid_forget()
            im = Image.open(f"images/{images[index]}")
            im.thumbnail((800, 600))
            ph = ImageTk.PhotoImage(im)
            label = Label(image=ph)
            label.image = ph
            label.grid(row=0, column=0, columnspan=3)
        else:
            print(f"[{index+1}/{total_images}] - {images[index+1]}")

            save(output)
            input_box.delete(0, 'end')

            index += 1

            label.grid_forget()
            im = Image.open(f"images/{images[index]}")
            im.thumbnail((800, 600))
            ph = ImageTk.PhotoImage(im)
            label = Label(image=ph)
            label.image = ph
            label.grid(row=0, column=0, columnspan=3)

    def previous_image():
        nonlocal index
        nonlocal label
        nonlocal im
        nonlocal ph

        output = f"{images[index]},None,{input_box.get()}\n"
        if input_box.get() == '':
            if index > 0:
                index -= 1

                input_box.delete(0, 'end')
                input_box.insert(0, lines[index].split(',')[2].replace('\n', ''))

                label.grid_forget()
                im = Image.open(f"images/{images[index]}")
                im.thumbnail((800, 600))
                ph = ImageTk.PhotoImage(im)
                label = Label(image=ph)
                label.image = ph
                label.grid(row=0, column=0, columnspan=3)
            else:
                pass
        else:
            if index > 0:
                edit(output)
                index -= 1

                input_box.delete(0, 'end')
                input_box.insert(0, lines[index].split(',')[2].replace('\n', ''))

                label.grid_forget()
                im = Image.open(f"images/{images[index]}")
                im.thumbnail((800, 600))
                ph = ImageTk.PhotoImage(im)
                label = Label(image=ph)
                label.image = ph
                label.grid(row=0, column=0, columnspan=3)

    button_previous = Button(window, text="Anterior", command=previous_image)
    button_previous.grid(row=1, column=0)

    input_box = Entry(window, width=100)
    input_box.grid(row=1, column=1)

    button_next = Button(window, text="Próximo", command=next_image)
    button_next.grid(row=1, column=2)

    if index > 0:
        input_box.insert(0, lines[index].split(',')[2].replace('\n', ''))

    window.mainloop()


if __name__ == '__main__':
    main()
