from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image
import os

def hide_message():
    filepath = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
    if not filepath:
        return
    message = text_input.get("1.0", END).strip()
    if not message:
        messagebox.showwarning("Input Error", "Please enter a message to hide.")
        return

    img = Image.open(filepath)
    encoded = img.copy()
    width, height = img.size
    index = 0
    binary_message = ''.join(format(ord(i), '08b') for i in message) + '1111111111111110'

    for row in range(height):
        for col in range(width):
            if index < len(binary_message):
                r, g, b = img.getpixel((col, row))
                r = (r & ~1) | int(binary_message[index])
                encoded.putpixel((col, row), (r, g, b))
                index += 1
            else:
                break

    save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if save_path:
        encoded.save(save_path)
        messagebox.showinfo("Success", f"Message hidden and image saved at:\n{save_path}")

def reveal_message():
    filepath = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
    if not filepath:
        return
    img = Image.open(filepath)
    binary_data = ""
    for row in range(img.height):
        for col in range(img.width):
            r, g, b = img.getpixel((col, row))
            binary_data += str(r & 1)

    all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    decoded_message = ""
    for byte in all_bytes:
        if byte == '11111110':
            break
        decoded_message += chr(int(byte, 2))

    messagebox.showinfo("Hidden Message", decoded_message)

# GUI setup
root = Tk()
root.title("StegoShield – Steganography Tool")
root.geometry("500x400")

Label(root, text="🔐 Enter message to hide:", font=("Arial", 12)).pack(pady=10)
text_input = Text(root, height=6, width=50, font=("Arial", 10))
text_input.pack()

Button(root, text="Hide Message in Image", command=hide_message, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=10)
Button(root, text="Reveal Message from Image", command=reveal_message, bg="#2196F3", fg="white", font=("Arial", 12)).pack(pady=10)

Label(root, text="Created by Mandisi Sibanda — Junior Cybersecurity Analyst", font=("Arial", 8)).pack(side="bottom", pady=10)

root.mainloop()
