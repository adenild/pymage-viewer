from tkinter import *
from PIL import ImageTk, Image
import os


def main():
    file_name = input("Qual vai ser o nome do arquivo? ")

    # Define a janela do Tkinter
    window = Tk()
    window.title('Não é o Labelme')

    # Pega a lista das imagens
    images = []
    for file in os.listdir('images/'):
        if '.txt' in file:
            pass
        else:
            images.append(file)
    lines = open(f"outputs/{file_name}", 'r').readlines()
    index = 0
    if len(lines) >= 1:
        print(lines[-1])
        index = lines.index(lines[-1])+1
    else:
        pass

    total_images = len(images)
    print(f"Existem {total_images} imagens.")

    # Salva a imagem no Tk
    im = Image.open(f"images/{images[index]}")
    im.thumbnail((800, 600))
    ph = ImageTk.PhotoImage(im)

    # Exibe a imagem no Tk
    label = Label(image=ph)
    label.image = ph
    label.grid(row=0, column=0, columnspan=3)

    # Muda pra próxima imagem e salva o texto
    # TODO: Consertar o final do loop. Ta travando o programa
    # TODO: Fazer a validação dos dados
    def next_image():
        nonlocal index
        nonlocal label
        nonlocal im
        nonlocal ph

        # Informa a posição atual
        print(f"[{index+1}/{total_images}]")

        # Salva no arquivo o texto digitado
        label_file = open(f'outputs/{file_name}', 'a+')
        label_file.write(f"{images[index]},None,{input_box.get()}\n")
        input_box.delete(0, 'end')
        print(f"Você digitou {input_box.get()} no arquivo {images[index]}")
        label_file.close()

        # Avança na lista
        index += 1

        # Reseta a janela e coloca a imagem nova
        label.grid_forget()
        im = Image.open(f"images/{images[index]}")
        im.thumbnail((800, 600))
        ph = ImageTk.PhotoImage(im)
        label = Label(image=ph)
        label.image = ph
        label.grid(row=0, column=0, columnspan=3)

    # Declaração da caixa de texto
    input_box = Entry(window, width=100)
    input_box.grid(row=1, column=0)

    # Declaração do botão
    button_next = Button(window, text="Próximo", command=next_image)
    button_next.grid(row=1, column=1)

    window.mainloop()


if __name__ == '__main__':
    main()
