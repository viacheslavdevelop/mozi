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

            processed_text.append(new_char)
            '''if char.isupper():
                processed_text.append(new_char.upper())
            else:
                processed_text.append(new_char)'''
        else:
            processed_text.append(char)
            
    return "".join(processed_text)

def get_valid_key():
    while True:
        user_input = input("Введите ключ: ")
        try:
            key = int(user_input)
            residue = key % ALPHABET_LENGTH
            
            if 1 <= residue <= ALPHABET_LENGTH - 1:
                print(f"Ключ: {residue}")
                return residue
            else:
                print("Ключ кратен размеру алфавита. Пожалуйста, введите другое значение.")
        except ValueError:
            print("Ошибка: ключ должен быть целым числом, а не буквами.")

def get_text_input():
    while True:
        choice = input("Получить текст из (1 - файл, 2 - консоль): ")
        if choice == '1':
            filename = input("Введите имя файла: ")
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    return f.read()
            else:
                print("Файл не найден. Попробуйте снова.")
        elif choice == '2':
            return input("Введите текст: ")
        else:
            print("Неверный выбор.")

def output_result(text):
    while True:
        choice = input("Сохранить результат (1 - в файл, 2 - на консоль): ")
        if choice == '1':
            filename = input("Введите имя файла для сохранения: ")
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(text)
            print("Файл успешно сохранен.")
            break
        elif choice == '2':
            print(f"\nРезультат:\n{text}\n")
            break
        else:
            print("Неверный выбор.")

def math_check_menu():
    while True:
        print("\nПроверка 'математики'")
        print("1) Шифрование с известным ключом")
        print("2) Расшифрование с известным ключом")
        print("3) Выход")
        
        choice = input("Выберите действие: ")
        
        if choice == '1':
            key = get_valid_key()
            text = get_text_input()
            encrypted = process_text(text, key)
            output_result(encrypted)
        elif choice == '2':
            key = get_valid_key()
            text = get_text_input()
            decrypted = process_text(text, -key)
            output_result(decrypted)
        elif choice == '3':
            break
        else:
            print("Неверный выбор.")

def variant_execution():
    print("\nВыполнение варианта")
    text = get_text_input()
    
    bruteforce_filename = "all_variants_auto.txt"
    with open(bruteforce_filename, 'w', encoding='utf-8') as f:
        for k in range(1, ALPHABET_LENGTH):
            decrypted_text = process_text(text, -k)
            f.write(f"Ключ {k:02d}: {decrypted_text}\n")
            
    print(f"\nВсе варианты перебора автоматически сохранены в файл: {bruteforce_filename}")
    print("Изучите файл, создайте новый текстовый файл с верным вариантом и именем автора.")
    
    while True:
        user_filename = input("Введите название файла, в котором вы сохранили ответ и автора: ")
        if os.path.exists(user_filename):
            key = get_valid_key()
            
            with open(user_filename, 'r', encoding='utf-8') as uf:
                raw_text = uf.read()
                
            final_data = process_text(raw_text, key)
                
            final_output_filename = "final_result_auto.txt"
            with open(final_output_filename, 'w', encoding='utf-8') as ff:
                ff.write(final_data)
                
            print(f"Итоговые данные успешно зашифрованы и сохранены в файл: {final_output_filename}")
            break
        else:
            print("Указанный файл не найден. Проверьте имя и попробуйте снова.")

def main():
    while True:
        print("\nГлавный интерфейс")
        print("1) Проверка 'математики'")
        print("2) Выполнение варианта")
        print("3) Выход")
        
        choice = input("Выберите действие: ")
        
        if choice == '1':
            math_check_menu()
        elif choice == '2':
            variant_execution()
        elif choice == '3':
            break
        else:
            print("Неверный выбор.")

if __name__ == "__main__":
    main()