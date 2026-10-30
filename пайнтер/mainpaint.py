import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw

class PaintPremium:
    def __init__(self, root):
        self.root = root
        self.root.title("Paint Premium 🎨 (IT Step Edition)")
        self.root.geometry("900x650")
        self.root.config(bg="#1e1e1e")

        # Переменные для рисования
        self.brush_size = 5
        self.brush_color = "#000000"
        self.eraser_mode = False
        self.old_x = None
        self.old_y = None

        # Создаем изображение Pillow для сохранения
        self.image = Image.new("RGB", (880, 500), "white")
        self.draw = ImageDraw.Draw(self.image)

        # --- Верхняя панель управления ---
        control_frame = tk.Frame(root, bg="#2d2d2d", height=70)
        control_frame.pack(fill=tk.X, padx=10, pady=10)

        # Кнопка выбора цвета
        self.color_btn = tk.Button(
            control_frame, text="🎨 Цвет", font=("Arial", 10, "bold"),
            bg="#3e3e3e", fg="white", bd=0, padx=10, pady=5, command=self.choose_color
        )
        self.color_btn.pack(side=tk.LEFT, padx=5, pady=10)

        # Индикатор текущего цвета
        self.color_indicator = tk.Label(control_frame, bg=self.brush_color, width=3, height=1)
        self.color_indicator.pack(side=tk.LEFT, padx=5)

        # Ползунок размера кисти
        size_label = tk.Label(control_frame, text="Размер кисти:", bg="#2d2d2d", fg="white", font=("Arial", 10))
        size_label.pack(side=tk.LEFT, padx=(15, 5))
        
        self.size_slider = tk.Scale(
            control_frame, from_=1, to=50, orient=tk.HORIZONTAL,
            bg="#2d2d2d", fg="white", highlightthickness=0, command=self.change_brush_size
        )
        self.size_slider.set(self.brush_size)
        self.size_slider.pack(side=tk.LEFT, padx=5)

        # Кнопка Ластика
        self.eraser_btn = tk.Button(
            control_frame, text="🧹 Ластик", font=("Arial", 10, "bold"),
            bg="#3e3e3e", fg="white", bd=0, padx=10, pady=5, command=self.toggle_eraser
        )
        self.eraser_btn.pack(side=tk.LEFT, padx=10)

        # Кнопка Очистить холст
        clear_btn = tk.Button(
            control_frame, text="🗑️ Очистить", font=("Arial", 10, "bold"),
            bg="#a93226", fg="white", bd=0, padx=10, pady=5, command=self.clear_canvas
        )
        clear_btn.pack(side=tk.LEFT, padx=10)

        # Кнопка Сохранить
        save_btn = tk.Button(
            control_frame, text="💾 Сохранить", font=("Arial", 10, "bold"),
            bg="#27ae60", fg="white", bd=0, padx=10, pady=5, command=self.save_image
        )
        save_btn.pack(side=tk.RIGHT, padx=5)

        # --- Холст для рисования ---
        canvas_frame = tk.Frame(root, bg="#ffffff", bd=2, relief=tk.SUNKEN)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        self.canvas = tk.Canvas(canvas_frame, bg="white", cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Привязка событий мыши
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.reset)

    def paint(self, event):
        if self.old_x and self.old_y:
            current_color = "white" if self.eraser_mode else self.brush_color
            
            # Рисуем на экране Tkinter
            self.canvas.create_line(
                self.old_x, self.old_y, event.x, event.y,
                width=self.brush_size, fill=current_color,
                capstyle=tk.ROUND, smooth=tk.TRUE, splinesteps=36
            )
            
            # Рисуем на объекте Pillow (для сохранения)
            self.draw.line(
                [self.old_x, self.old_y, event.x, event.y],
                fill="white" if self.eraser_mode else self.brush_color,
                width=self.brush_size
            )
            
        self.old_x = event.x
        self.old_y = event.y

    def reset(self, event):
        self.old_x = None
        self.old_y = None

    def choose_color(self):
        color_code = colorchooser.askcolor(title="Выберите цвет кисти")[1]
        if color_code:
            self.brush_color = color_code
            self.color_indicator.config(bg=self.brush_color)
            self.eraser_mode = False
            self.eraser_btn.config(bg="#3e3e3e")

    def change_brush_size(self, val):
        self.brush_size = int(val)

    def toggle_eraser(self):
        self.eraser_mode = not self.eraser_mode
        if self.eraser_mode:
            self.eraser_btn.config(bg="#c0392b") # Красный цвет при активном ластике
        else:
            self.eraser_btn.config(bg="#3e3e3e")

    def clear_canvas(self):
        if messagebox.askyesno("Очистить холст", "Вы уверены, что хотите стереть рисунок?"):
            self.canvas.delete("all")
            self.image = Image.new("RGB", (880, 500), "white")
            self.draw = ImageDraw.Draw(self.image)

    def save_image(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
        )
        if file_path:
            # Масштабируем холст перед сохранением под размер изображения
            self.image.save(file_path)
            messagebox.showinfo("Успех", f"Рисунок успешно сохранен!\n{file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PaintPremium(root)
    root.mainloop()