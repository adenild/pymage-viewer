from tkinter import Label, filedialog
import side


def change_window_title(local_vars: list):
    index, images, window = local_vars[0], local_vars[5], local_vars[-1]
    window.title(f'Simple Label - {images[index]}')


def test_clicked_button():
    print('This button was clicked')


def load_json_file(local_vars: list):
    pass


def save_json_file(local_vars: list):
    index, input_box, images, data, file = local_vars[0], local_vars[4], local_vars[5], local_vars[6], local_vars[7]
    save = {images[index]: {'bbox': "None", 'label': input_box.get().upper()}}
    data.update(save)
    print(save)
    side.save_data_json(file, data)


def change_image(next_or_prev: str, local_vars: list):
    index = local_vars[0]
    label = local_vars[1]
    image = local_vars[2]
    total_images = local_vars[3]
    input_box = local_vars[4]
    images = local_vars[5]
    data = local_vars[6]
    file = local_vars[7]
    images_dir = local_vars[8]

    print(side.show_position(index, total_images))

    save_json_file(local_vars)

    if next_or_prev == "next":
        if index + 1 == total_images:
            print('Fim das imagens.')
            exit(200)
        else:
            index += 1
    elif next_or_prev == "prev":
        index -= 1

    input_box.delete(0, 'end')
    label_text = side.check_labeled(images[index], data)
    input_box.insert(0, label_text)
    label.grid_forget()

    image = side.setup_image(images_dir, images[index])
    label = Label(image=image)
    label.image = image
    label.grid(row=0, column=0, columnspan=3)

    change_window_title(local_vars)

    local_vars[0], local_vars[1], local_vars[2], local_vars[3] = index, label, image, total_images
    local_vars[4], local_vars[5], local_vars[6], local_vars[7] = input_box, images, data, file
    local_vars[8] = images_dir
    return local_vars
