import tkinter as tk
from tkinter import ttk, messagebox
import random
import pyperclip

# Словарь с русским алфавитом и соответствующими зашифрованными символами
ALPHABET = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
CIPHER_ALPHABET = ''.join(random.sample(ALPHABET, len(ALPHABET)))


def encrypt(text):
    result = ''
    for char in text.lower():
        if char in ALPHABET:
            index = ALPHABET.index(char)
            result += CIPHER_ALPHABET[index]
        else:
            result += char
    return result


def decrypt(text):
    result = ''
    for char in text.lower():
        if char in CIPHER_ALPHABET:
            index = CIPHER_ALPHABET.index(char)
            result += ALPHABET[index]
        else:
            result += char
    return result


def crack(text):
    results = []
    for i in range(len(ALPHABET)):
        result = ''
        for char in text.lower():
            if char in CIPHER_ALPHABET:
                index = CIPHER_ALPHABET.index(char)
                result += ALPHABET[(index + i) % len(ALPHABET)]
            else:
                result += char
        results.append(f"Вариант {i + 1}: {result}")
    return "\n".join(results)


def main():
    root = tk.Tk()
    root.title("Шифр однобуквенной замены")
    root.geometry("800x500")
    root.resizable(True, True)

    # Стили
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TLabel", font=("Cambria", 20))
    style.configure("TEntry", font=("Cambria", 20))
    style.configure("TButton", font=("Cambria", 20), background="#37d5d7", foreground="black")

    # Виджетов
    label_input = ttk.Label(root, text="Введите текст:")
    entry_input = ttk.Entry(root, width=70)
    label_key = ttk.Label(root, text="Ключ:")
    label_key_value = ttk.Label(root, text=CIPHER_ALPHABET)

    button_encrypt = ttk.Button(root, text="Зашифровать", command=lambda: display_result(encrypt(entry_input.get())))
    button_decrypt = ttk.Button(root, text="Дешифровать", command=lambda: display_result(decrypt(entry_input.get())))
    button_crack = ttk.Button(root, text="Взлом", command=lambda: display_crack_result(crack(entry_input.get())))
    button_transfer_encrypted = ttk.Button(root, text="Перенести зашифрованный/дешифрованный текст",
                                           command=lambda: transfer_encrypted_text())

    label_result = tk.Text(root, height=1, width=70, wrap='word')
    label_crack_result = tk.Text(root, height=15, width=70, wrap='word')

    label_input.grid(row=0, column=0, padx=10, pady=10)
    entry_input.grid(row=0, column=1, padx=10, pady=10)
    label_key.grid(row=1, column=0, padx=10, pady=10)
    label_key_value.grid(row=1, column=1, padx=10, pady=10)

    button_encrypt.grid(row=2, column=0, padx=10, pady=10)
    button_decrypt.grid(row=2, column=1, padx=10, pady=10)

    button_crack.grid(row=3, column=0, padx=10, pady=10)
    button_transfer_encrypted.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    label_result.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
    label_crack_result.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    def display_result(result):
        label_result.delete("1.0", tk.END)
        label_result.insert(tk.END, result)

    def display_crack_result(result):
        label_crack_result.delete("1.0", tk.END)
        label_crack_result.insert(tk.END, result)

    def transfer_encrypted_text():
        encrypted_text = encrypt(entry_input.get())
        entry_input.delete(0, tk.END)
        entry_input.insert(tk.END, encrypted_text)
    root.mainloop()

if __name__ == "__main__":
    main()
