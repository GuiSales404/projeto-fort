import tkinter as tk
from tkinter import filedialog

selected_path = ""

def select_folder():
    global selected_path 
    folder = filedialog.askdirectory()
    selected_path = folder 
    entry_folder.delete(0, "end") 
    entry_folder.insert(0, folder) 

def generate_dashboard():
    if selected_path:
        print("Gerando Dashboards em:", selected_path)
        window.destroy()

window = tk.Tk()
window.geometry('640x360')
window.title("Selecionar Pasta")

label = tk.Label(window, text="Digitar Caminho:", padx=10)
label.pack(side='left')

entry_folder = tk.Entry(window)
entry_folder.pack(side='left')

button_ok = tk.Button(window, text="Procurar Caminho", command=select_folder, padx=70)
button_ok.pack(side='right')

button_save = tk.Button(window, text="Salvar Caminho", command=lambda: button_generate.place(x=240, y=310))
button_save.pack(side='bottom', pady=70)

button_generate = tk.Button(window, text="Gerar Dashboards", command=generate_dashboard, padx=30)
button_generate.pack_forget()

window.mainloop()