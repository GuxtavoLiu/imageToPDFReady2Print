import os
from PIL import Image
from fpdf import FPDF
import tkinter as tk
from tkinter import filedialog, messagebox
from threading import Thread


def images_to_pdf(folder_path):
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
            # Caminho completo para a imagem
            image_path = os.path.join(folder_path, filename)

            # Abrindo a imagem e obtendo suas dimensões
            with Image.open(image_path) as img:
                width, height = img.size

                # Calculando a proporção da imagem
                ratio = min(max_image_width / width, max_image_height / height)

                # Redimensionando a imagem proporcionalmente
                new_width = int(width * ratio)
                new_height = int(height * ratio)

                # Criando um objeto PDF
                pdf = FPDF(unit="mm", format="A4")
                pdf.add_page()

                # Adicionando a imagem ao PDF
                # Convertendo a posição da margem para milímetros e adicionando a imagem
                pdf.image(image_path, x=margin_mm, y=margin_mm, w=new_width, h=new_height)

                # Salvando o PDF com o mesmo nome da imagem, mas com a extensão .pdf
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
            # Executando a função de conversão em uma thread separada
            Thread(target=images_to_pdf, args=(folder,)).start()
            messagebox.showinfo("Conversão", "Conversão concluída com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", str(e))
    else:
        messagebox.showwarning("Aviso", "Por favor, selecione uma pasta primeiro.")


# images_to_pdf("C:\\Users\\gusta\\Downloads")

# Exemplo de uso:
# images_to_pdf("/caminho/para/a/pasta")
# Nota: Substitua "/caminho/para/a/pasta" com o caminho real da pasta onde estão as imagens.


# Inicializando a janela da interface gráfica
window = tk.Tk()
window.title("Conversor de Imagens para PDF")

# Botão para selecionar a pasta
select_folder_button = tk.Button(window, text="Selecionar Pasta", command=select_folder)
select_folder_button.pack(pady=10)

# Rótulo para exibir o caminho da pasta
folder_path_label = tk.Label(window, text="", fg="blue")
folder_path_label.pack(pady=10)

# Botão para iniciar a conversão
convert_button = tk.Button(window, text="Converter", command=convert_images_to_pdf)
convert_button.pack(pady=10)

# Executando a interface gráfica
window.mainloop()
