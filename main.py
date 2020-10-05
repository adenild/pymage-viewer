from tkinter import *
from PIL import ImageTk, Image
import os
import json


def image_loader():
    # Pega a lista das imagens
    images = []
    for file in os.listdir('images/'):
        if '.txt' in file:
            pass
        else:
            images.append(file)
    return images

def verifica_labels():
    pass

def read_previous_data(file_name):
    try:
        with open(f"outputs/{file_name}", "r") as read_file:
            data = json.load(read_file)
    except:
        fp = open(f"outputs/{file_name}", 'w+')
        data = {}
        fp.close()
    return data


def save_data_json(data,file_name):
    with open(f"outputs/{file_name}", "w") as write_file:
        json.dump(data, write_file,indent=1)

def starter_list(data,images):
    removidas = []
    for key in data.keys():
        if key in images:
            removidas.append(key)
            images.remove(key)

    print(f'{len(removidas)} imagens ja foram detectadas no arquivo de entrada.')
    return images,removidas

def main():
    # Define a janela do Tkinter
    window = Tk()
    window.title('Não é o Labelme')

    file_name = input("Qual vai ser o nome do arquivo? ")
    images = image_loader()

    # Verificar se o arquivo existe e carrega os dados, se não existir ele cria.
    data = read_previous_data(file_name)

    print(data)

    images,removidas = starter_list(data,images)
    if len(images) == 0:
        print('Todas as imagens do diretório /images ja estão transcritas')
        exit(200)
    
    index = 0
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
        print(f"[{index}/{total_images}]")

        info = {images[index]:{'treco':None,'label':input_box.get()}}
        data.update(info)
        print(data)

        # Salva no arquivo o texto digitado        
        save_data_json(data,file_name)

        if (index+1==total_images):
            print('Finalizadas as imagens')
            exit(200)

        # label_file = open(f'outputs/{file_name}', 'a+')
        # label_file.write(f"{images[index]},None,{input_box.get()}\n")
        input_box.delete(0, 'end')
        # print(f"Você digitou {input_box.get()} no arquivo {images[index]}")
        # label_file.close()

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
