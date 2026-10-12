import os

ALPHABET = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
ALPHABET_LENGTH = len(ALPHABET)

def process_text(text, key):
    processed_text = []
    
    for char in text:
        lower_char = char.lower()
        
        if lower_char in ALPHABET:
            char_index = ALPHABET.index(lower_char)
            new_index = (char_index + key) % ALPHABET_LENGTH
            new_char = ALPHABET[new_index]
            
            if char.isupper():
                processed_text.append(new_char.upper())
            else:
                processed_text.append(new_char)
        else:
            processed_text.append(char)
            
    return "".join(processed_text)

def encrypt(text, key):
    return process_text(text, key)

def decrypt(text, key):
    return process_text(text, -key)

def save_to_file(filename, content, mode='w'):
    if filename != "":
        with open(filename, mode, encoding='utf-8') as file:
            file.write(content)

def mode_encrypt():
    text = input("Введите текст для шифрования: ")
    key = int(input("Введите ключ (число от 1 до 31): "))
    
    encrypted_text = encrypt(text, key)
    print(f"\nРезультат:\n{encrypted_text}")
    
    filename = input("\nВведите имя файла для сохранения (например, encrypt.txt): ")
    content_to_save = f"Ключ: {key}\nЗашифрованный текст:\n{encrypted_text}\n\n"
    save_to_file(filename, content_to_save)
    print(f"Данные сохранены в файл {filename}.")

def mode_decrypt():
    text = input("Введите текст для расшифровки: ")
    key = int(input("Введите ключ (число от 1 до 31): "))
    
    decrypted_text = decrypt(text, key)
    print(f"\nРезультат:\n{decrypted_text}")
    
    filename = input("\nВведите имя файла для сохранения (например, decrypt.txt): ")
    content_to_save = f"Ключ: {key}\nРасшифрованный текст:\n{decrypted_text}\n\n"
    save_to_file(filename, content_to_save, mode='a')
    print(f"Данные дописаны в файл {filename}.")

def mode_bruteforce():
    text = input("Введите зашифрованный текст для перебора: ")
    filename = input("Введите имя файла для сохранения всех вариантов (например, bruteforce.txt): ")
    
    save_to_file(filename, "Результаты прямого полного перебора:\n\n", mode='w')
    
    for current_key in range(1, ALPHABET_LENGTH):
        decrypted_text = decrypt(text, current_key)
        result_string = f"Ключ {current_key:02d}: {decrypted_text}"
        
        print(result_string)
        save_to_file(filename, result_string + "\n", mode='a')
        
    print(f"\nВсе {ALPHABET_LENGTH - 1} вариантов сохранены в файл {filename}.")

def main():
    while True:
        print("\nШифр Цезаря")
        print("1. Зашифровать текст")
        print("2. Расшифровать текст")
        print("3. Взлом (прямой полный перебор ключей)")
        print("0. Выход")
        
        choice = input("Выберите действие: ")
        
        if choice == '1':
            mode_encrypt()
        elif choice == '2':
            mode_decrypt()
        elif choice == '3':
            mode_bruteforce()
        elif choice == '0':
            break
        else:
            print("Неверный выбор. Пожалуйста, попробуйте снова.")

if __name__ == "__main__":
    main()

# Вариант 15
# главный интерфейс - 1) Проверка "математики", 2) Выполнение варианта 3) Выход
# интерфейс Проверка "математики" - 1) Шифрование с известным ключом, 2) Расшифрование с известным ключом 3) Выход
''' Процесс шифрования с известным ключом - ввод ключа с проверкой (не буквы, интервал - поставить наименьший неотрицательный вычет входящий в k = (1, ..., m-1))
спрашивает - получить текст из файла или из консоли, затем ввод
шифрование и вопрос - сохранить в файл или вывести на консоль
'''
# Расшифрование с известным ключом - аналогично шифрованию
''' Интерфейс Выполнение варианта - 
1) загрузить с файла или считать с консоли зашифрованное сообщение, ввод
2) Перебор всех ключей - сохранение всех вариантов в текстовый файл

пользователь сам смотрит какой шифр подходит

3) Ожидание ввода пользователя: название файла в котором он ввел расшифрованное сообщение с именем автора зашифрованной фразы
4) Загрузка из файла расшфированного сообщения и сохранение в новый файл.

в данном меню все выходящие текстовые файлы именуются автоматически
'''