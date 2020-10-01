from tkinter import *
from PIL import ImageTk, Image
import os


def main():
    # Define a janela do Tkinter
    window = Tk()
    window.title('Não é o Labelme')

    # Pega a lista das imagens
    images = os.listdir('images/')
    index = 0

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

        index += 1

        # Reseta a janela e coloca a imagem nova
        label.grid_forget()
        im = Image.open(f"images/{images[index]}")
        im.thumbnail((800, 600))
        ph = ImageTk.PhotoImage(im)
        label = Label(image=ph)
        label.image = ph
        label.grid(row=0, column=0, columnspan=3)

        # Pega o texto da imagem
        print(input_box.get())

    # Declaração da caixa de texto
    input_box = Entry(window, width=100)
    input_box.grid(row=1, column=0)

    # Declaração do botão
    button_next = Button(window, text="Próximo", command=next_image)
    button_next.grid(row=1, column=1)

    window.mainloop()


if __name__ == '__main__':
    main()
