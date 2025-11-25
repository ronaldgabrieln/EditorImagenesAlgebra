import tkinter as tk
from PIL import Image, ImageTk


# ESTA CLASS ES SOLO LA INTERFAZ, NO TIENE NINGUN USO DE ALGEBRA
class ImageSelector:
    def __init__(self, image_paths):
        self.image_paths = image_paths
        self.selected_path = None

        # crear ventana
        self.root = tk.Tk()
        self.root.title("Selecciona tu imagen deseada")
        self.root.geometry("800x600")

        # font del titulo
        title = tk.Label(self.root, text="Selecciona una imagen para transformar", font=("Arial", 16, "bold"))
        title.pack(pady=10)

        # diseno de los botones
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)

        # hacer boton por cada imagen que hay
        self.photo_images = []
        for i, path in enumerate(self.image_paths):
            # cargar en chiquito cada foto para que no esten super grandes
            img = Image.open(path)
            img.thumbnail((150, 150))
            photo = ImageTk.PhotoImage(img)
            self.photo_images.append(photo)

            # hacer diseno de boton por imagen
            btn = tk.Button(
                button_frame,
                image=photo,
                command=lambda p=path: self.select_image(p),
                relief=tk.RAISED,
                borderwidth=3
            )
            btn.grid(row=i // 2, column=i % 2, padx=10, pady=10)

            # labelear
            label = tk.Label(button_frame, text=path.split('/')[-1])
            label.grid(row=i // 2 + 2, column=i % 2, padx=10)

        # imagen seleccionada
        self.selection_label = tk.Label(
            self.root,
            text="Sin imagen",
            font=("Arial", 12),
            fg="gray"
        )
        self.selection_label.pack(pady=20)

        # boton de confirmar
        self.confirm_btn = tk.Button(
            self.root,
            text="Empezar transformación",
            command=self.confirm_selection,
            state=tk.DISABLED,
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=10
        )
        self.confirm_btn.pack(pady=10)

    def select_image(self, path):
        self.selected_path = path
        self.selection_label.config(
            text=f"Seleccionaste: {path.split('/')[-1]}",
            fg="green"
        )
        self.confirm_btn.config(state=tk.NORMAL)

    def confirm_selection(self):
        self.root.destroy()

    def run(self):
        self.root.mainloop()
        return self.selected_path


# AQUI ACABA EL CLASS DEL GUI
# AQUI EMPIEZA EL CLASS DEL GUI PARA SELECCIONAR LO QUE LE VAN A HACER A LA IMAGEN
class ActionSelector:
    def __init__(self, image):
        self.image = image
        self.selected_action = None
        self.action_value = None

        # crear ventana
        self.root = tk.Tk()
        self.root.title("Selecciona la transformación")
        self.root.geometry("600x600")

        # titulo
        title = tk.Label(self.root, text="¿Qué transformación deseas aplicar?", font=("Arial", 16, "bold"))
        title.pack(pady=20)

        # frame para las opciones
        options_frame = tk.Frame(self.root)
        options_frame.pack(pady=20)

        # variable para los radiobuttons
        self.action_var = tk.StringVar(value="")

        # opcion de rotacion
        rotation_radio = tk.Radiobutton(
            options_frame,
            text="Rotación",
            variable=self.action_var,
            value="rotation",
            font=("Arial", 12),
            command=self.update_input_field
        )
        rotation_radio.grid(row=0, column=0, sticky="w", pady=10, padx=20)

        # opcion de reflexion
        reflection_radio = tk.Radiobutton(
            options_frame,
            text="Reflexión",
            variable=self.action_var,
            value="reflection",
            font=("Arial", 12),
            command=self.update_input_field
        )
        reflection_radio.grid(row=1, column=0, sticky="w", pady=10, padx=20)

        # opcion de escalamiento
        scale_radio = tk.Radiobutton(
            options_frame,
            text="Escalamiento",
            variable=self.action_var,
            value="scale",
            font=("Arial", 12),
            command=self.update_input_field
        )
        scale_radio.grid(row=2, column=0, sticky="w", pady=10, padx=20)

        # frame para input de valores
        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(pady=20)

        # label y entry para valores (inicialmente ocultos)
        self.input_label = tk.Label(self.input_frame, text="", font=("Arial", 11))
        self.input_label.pack()

        self.input_entry = tk.Entry(self.input_frame, font=("Arial", 12), width=15)
        self.input_entry.pack(pady=10)

        # ocultar input inicialmente
        self.input_label.pack_forget()
        self.input_entry.pack_forget()

        # frame para opciones de reflexion (inicialmente oculto)
        self.reflection_frame = tk.Frame(self.root)
        self.reflection_var = tk.StringVar(value="x")

        reflection_label = tk.Label(self.reflection_frame, text="Eje de reflexión:", font=("Arial", 11))
        reflection_label.pack()

        tk.Radiobutton(
            self.reflection_frame,
            text="Eje X",
            variable=self.reflection_var,
            value="x",
            font=("Arial", 10)
        ).pack()

        tk.Radiobutton(
            self.reflection_frame,
            text="Eje Y",
            variable=self.reflection_var,
            value="y",
            font=("Arial", 10)
        ).pack()

        # mensaje de estado
        self.status_label = tk.Label(
            self.root,
            text="Selecciona una transformación",
            font=("Arial", 10),
            fg="gray"
        )
        self.status_label.pack(pady=20)

        # boton de aplicar
        self.apply_btn = tk.Button(
            self.root,
            text="Aplicar Transformación",
            command=self.apply_transformation,
            state=tk.DISABLED,
            font=("Arial", 12),
            bg="#2196F3",
            fg="white",
            padx=20,
            pady=10
        )
        self.apply_btn.pack(pady=10)

    def update_input_field(self):
        # limpiar frame
        self.input_label.pack_forget()
        self.input_entry.pack_forget()
        self.reflection_frame.pack_forget()
        self.input_entry.delete(0, tk.END)

        action = self.action_var.get()

        if action == "rotation":
            self.input_label.config(text="Ingresa los grados de rotación:")
            self.input_label.pack()
            self.input_entry.pack(pady=10)
            self.status_label.config(text="Ingresa los grados", fg="blue")

        elif action == "reflection":
            self.reflection_frame.pack(pady=10)
            self.status_label.config(text="Elige el eje", fg="blue")

        elif action == "scale":
            self.input_label.config(text="Ingresa el factor de escalamiento:")
            self.input_label.pack()
            self.input_entry.pack(pady=10)
            self.status_label.config(text="Ingresa el factor", fg="blue")

        self.apply_btn.config(state=tk.NORMAL)

    def apply_transformation(self):
        action = self.action_var.get()

        if not action:
            self.status_label.config(text="⚠️ Debes seleccionar una transformación", fg="red")
            return

        if action == "rotation":
            degrees = float(self.input_entry.get())
            self.selected_action = "rotation"
            self.action_value = degrees
            self.root.destroy()
            return degrees

        elif action == "reflection":
            axis = self.reflection_var.get()
            self.selected_action = "reflection"
            self.action_value = axis
            self.root.destroy()
            return axis
        elif action == "scale":
            scale_factor = float(self.input_entry.get())
            self.selected_action = "scale"
            self.action_value = scale_factor
            self.root.destroy()
            return scale_factor

    def run(self):
        self.root.mainloop()
        return self.selected_action, self.action_value

#ESTAS SON LAS FUNCIONES DE TRANSFORMACION A LA IMAGEN
def rotarImagen(img,scale):
    img = img.rotate(scale)
    img.save("imagenesResultado/imagenRotada.png")
    img.show()
    return img
def reflejarImagen(img,axis):
    if(axis == "x"):
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
        img.save("imagenesResultado/imagenVolteadaEnX.png")
        img.show()
    else:
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
        img.save("imagenesResultado/imagenVolteadaEnY.png")
        img.show()
    return img
def escalarImagen(img,scale):
    width = img.size[0]
    height = img.size[1]
    img = img.resize((int(width*scale),int(height*scale)))
    img.save("imagenesResultado/imagenEscalada.png")
    img.show()
if __name__ == "__main__":
    # AQUI EMPIEZA EL PROGRAMA

    # estas son las direcciones de las imagenes, osea pueden ser otras pero tendrian que cambiarle el nombre
    image_paths = [
        "carros.jpg",
        "atardecer.png",
        "montana.jpg",
        "montana2.jpg"
    ]

    selector = ImageSelector(image_paths)
    selected = selector.run()

    print(f"Selected image: {selected}")
    # AQUI EMPIEZA LA LOGICA DE ALGEBRA PARA EL PROGRAMA
    # PARA ESTE PUNTO YA SELECCIONO LA IMAGEN EL USUARIO
    img = Image.open(selected)
    print(f"Image size: {img.size}")
    print(f"Image mode: {img.mode}")

    transformator = ActionSelector(img)
    action, value = transformator.run()
    #PARA ESTE PUNTO YA TENEMOS IMAGEN Y ACCION SELECCIONADA
    #AQUI MANDO A LA FUNCION QUE CORRESPONDE A LA ACCION y le paso el valor
    if action == "rotation":
        rotarImagen(img,value)
    elif action == "reflection":
        reflejarImagen(img,value)
    else:
        escalarImagen(img,value)


