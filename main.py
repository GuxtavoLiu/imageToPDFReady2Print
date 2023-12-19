import os
import tkinter as tk
from threading import Thread
from tkinter import filedialog, messagebox

from PIL import Image
from fpdf import FPDF


def images_to_pdf(folder_path, max_height_mm=None):
    # Definindo as dimensões de uma folha A4 em milímetros e a margem em centímetros
    A4_WIDTH_MM = 210
    A4_HEIGHT_MM = 297
    MARGIN_CM = 1

    # Convertendo a margem para milímetros
    margin_mm = MARGIN_CM * 10

    # Calculando a área máxima da imagem em milímetros
    max_image_width = A4_WIDTH_MM - 2 * margin_mm
    max_image_height = A4_HEIGHT_MM - 2 * margin_mm

    # Listando todos os arquivos da pasta fornecida
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpeg', '.jpg')):
            image_path = os.path.join(folder_path, filename)

            with Image.open(image_path) as img:
                width, height = img.size

                # Aplicar a altura máxima se especificada
                if max_height_mm and height > max_height_mm:
                    ratio = max_height_mm / height
                else:
                    ratio = min(max_image_width / width, max_image_height / height)

                new_width = int(width * ratio)
                new_height = int(height * ratio)

                pdf = FPDF(unit="mm", format="A4")
                pdf.add_page()
                pdf.image(image_path, x=margin_mm, y=margin_mm, w=new_width, h=new_height)

                pdf_filename = os.path.splitext(filename)[0] + '.pdf'
                pdf.output(os.path.join(folder_path, pdf_filename))


def select_folder():
    folder_path = filedialog.askdirectory()
    folder_path_label.config(text=folder_path)
    return folder_path


def convert_images_to_pdf():
    folder = folder_path_label.cget("text")
    if folder:
        try:
            max_height = max_height_entry.get()
            if not max_height or int(max_height) == 0:
                max_height = None
            else:
                max_height = int(max_height) * 10  # Convertendo de cm para mm

            # Executando a função de conversão em uma thread separada
            Thread(target=images_to_pdf, args=(folder, max_height)).start()
            messagebox.showinfo("Conversão", "Conversão concluída com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", str(e))
    else:
        messagebox.showwarning("Aviso", "Por favor, selecione uma pasta primeiro.")


window = tk.Tk()
window.title("Conversor de Imagens para PDF")
window.geometry("400x200")  # Tamanho mínimo da janela

select_folder_button = tk.Button(window, text="Selecionar Pasta", command=select_folder)
select_folder_button.pack(pady=10)

folder_path_label = tk.Label(window, text="", fg="blue")
folder_path_label.pack(pady=10)

max_height_entry = tk.Entry(window)
max_height_entry.pack(pady=10)
max_height_label = tk.Label(window, text="Altura máxima em cm (deixe vazio para padrão):")
max_height_label.pack()

convert_button = tk.Button(window, text="Converter", command=convert_images_to_pdf)
convert_button.pack(pady=10)

footer_label = tk.Label(window, text="2023 © 100LIUMITES LTDA - Todos os direitos reservados", fg="grey")
footer_label.pack(side="bottom", fill="x", pady=10)

window.mainloop()
