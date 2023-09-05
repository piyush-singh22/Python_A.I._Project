import tkinter as tk

def on_button_hover(event):
    root.config(cursor="hand2")

def on_button_leave(event):
    root.config(cursor="")

root = tk.Tk()
root.title("Button Cursor Example")

button = tk.Button(root, text="Hover over me!")
button.pack(pady=20)

button.bind("<Enter>", on_button_hover)
button.bind("<Leave>", on_button_leave)

root.mainloop()






