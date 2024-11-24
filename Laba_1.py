import tkinter as tk
from tkinter import ttk, messagebox
import random
import pyperclip
from collections import Counter

# Словарь с русским алфавитом и соответствующими зашифрованными символами
ALPHABET = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
CIPHER_ALPHABET = ''.join(random.sample(ALPHABET, len(ALPHABET)))

# Частоты букв в русском языке
RUSSIAN_FREQ = {
    'а': 0.079, 'б': 0.014, 'в': 0.045, 'г': 0.017,
    'д': 0.031, 'е': 0.085, 'ё': 0.001, 'ж': 0.005,
    'з': 0.016, 'и': 0.073, 'й': 0.015, 'к': 0.038,
    'л': 0.043, 'м': 0.032, 'н': 0.067, 'о': 0.109,
    'п': 0.030, 'р': 0.050, 'с': 0.054, 'т': 0.062,
    'у': 0.029, 'ф': 0.002, 'х': 0.013, 'ц': 0.012,
    'ч': 0.011, 'ш': 0.010, 'щ': 0.009, 'ъ': 0.002,
    'ы': 0.026, 'ь': 0.025, 'э': 0.008, 'ю': 0.007,
    'я': 0.027,
}


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
    # Подсчет частоты символов в зашифрованном тексте
    counter = Counter(char for char in text.lower() if char in CIPHER_ALPHABET)
    most_common = counter.most_common(5)  # 5 самых частых символов

    # Подбор наиболее вероятных замен
    results = []
    for i in range(len(ALPHABET)):
        result = ''
        for char in text.lower():
            if char in CIPHER_ALPHABET:
                index = CIPHER_ALPHABET.index(char)
                result += ALPHABET[(index + i) % len(ALPHABET)]
            else:
                result += char

        # Оценка вероятности результата на основе частот
        score = sum(RUSSIAN_FREQ.get(c, 0) for c in set(result))
        results.append((result, score))

    # Сортировка по вероятности и выбор 5 лучших
    results.sort(key=lambda x: x[1], reverse=True)
    best_results = results[:5]

    return "\n".join(f"Вариант {i + 1}: {res[0]}" for i, res in enumerate(best_results))


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
