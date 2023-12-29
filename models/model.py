import tkinter as tk


class AutoClosingWindow:
    def __init__(self, root, timeout, message):
        self.root = root
        self.root.title("Автоматически закрывающееся окно")
        self.timeout = timeout * 1000  # переводим время из секунд в миллисекунды

        self.label = tk.Label(root, text=message)
        self.label.pack(pady=10)

        self.root.after(self.timeout, self.close_window)

    def close_window(self):
        self.root.destroy()