import os
from collections import Counter
import itertools

ALPHABET = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
M = 32

def get_input_data(prompt_text, expected_count, cast_type=int):
    while True:
        choice = input("Ввод (1 - консоль, 2 - файл): ").strip()
        raw_data = ""
        if choice == '1':
            raw_data = input(prompt_text + ": ").strip()
        elif choice == '2':
            fname = input("Имя файла: ").strip()
            try:
                with open(fname, 'r', encoding='utf-8') as f:
                    raw_data = f.read().strip()
            except Exception:
                print("Ошибка чтения файла.")
                continue
        else:
            print("Неверный выбор.")
            continue
            
        if not raw_data:
            print("Ошибка: пустой ввод.")
            continue
            
        if cast_type == str and expected_count == 0:
            return raw_data
            
        parts = raw_data.replace(',', ' ').split()
        if len(parts) < expected_count:
            print("Ошибка: недостаточно данных.")
            continue
            
        if cast_type == str:
            return parts[:expected_count] if expected_count > 1 else parts[0]
            
        try:
            res = [cast_type(p) for p in parts[:expected_count]]
            return res[0] if expected_count == 1 else res
        except ValueError:
            print("Ошибка: некорректный формат данных.")

def gcd_ext(a, b):
    def _gcd_ext_pos(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = _gcd_ext_pos(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y

    gcd, x, y = _gcd_ext_pos(abs(a), abs(b))

    if a < 0:
        x = -x
    if b < 0:
        y = -y

    return gcd, x, y

def mod_inverse(a, m):
    if m <= 1:
        return None

    gcd, x, _ = gcd_ext(a, m)
    if gcd != 1:
        return None
    return x % m

def solve_linear_congruence(a, b, m):
    if m <= 0:
        return None

    a = a % m
    b = b % m

    if a == 0:
        if b == 0:
            return list(range(m))
        return []

    gcd, x, _ = gcd_ext(a, m)

    if b % gcd != 0:
        return []

    a_prime = a // gcd
    b_prime = b // gcd
    m_prime = m // gcd

    inv = mod_inverse(a_prime, m_prime)
    x0 = (b_prime * inv) % m_prime

    return [(x0 + i * m_prime) % m for i in range(gcd)]

def solve_system(a, b, c, d, m):
    if m <= 1:
        return None

    a = a % m
    b = b % m
    c = c % m
    d = d % m

    diff_a = (a - c) % m
    diff_b = (b - d) % m

    x_sols = solve_linear_congruence(diff_a, diff_b, m)
    
    results = []
    for x in x_sols:
        y = (b - a * x) % m
        results.append((x, y))

    return results

def char_to_idx(c):
    c = c.lower()
    return ALPHABET.find(c)

def idx_to_char(idx):
    return ALPHABET[idx % M]

def freq_analysis(text):
    filtered = [c.lower() for c in text if c.lower() in ALPHABET]
    counter = Counter(filtered)
    most_common = counter.most_common(2)
    return [item[0] for item in most_common]

def hypothesize(c1, c2, lang_top_chars=['о', 'е', 'а', 'и', 'т', 'н', 'с', 'р', 'в', 'л', 'к', 'м', 'д', 'у', 'я', 'ы', 'з', 'б', 'г', 'ч', 'й', 'х', 'ж', 'ю', 'ш', 'ц', 'э', 'щ', 'ф']):
    if c1 == c2:
        return []

    y1 = char_to_idx(c1)
    y2 = char_to_idx(c2)
    
    guesses = set()
    
    for p1, p2 in itertools.permutations(lang_top_chars, 2):
        x1 = char_to_idx(p1)
        x2 = char_to_idx(p2)
        
        keys = solve_system(x1, y1, x2, y2, M)
        
        for a, b in keys:
            gcd, _, _ = gcd_ext(a, M)
            if gcd == 1:
                guesses.add((a, b))
                
    return list(guesses)

def encrypt_affine(text, a, b):
    res = []
    for c in text:
        idx = char_to_idx(c)
        if idx != -1:
            enc = idx_to_char((a * idx + b) % M)
            res.append(enc.upper() if c.isupper() else enc)
        else:
            res.append(c)
    return "".join(res)

def decrypt_affine(text, a, b):
    res = []
    inv_a = mod_inverse(a, M)
    if inv_a is None:
        return ""
    for c in text:
        idx = char_to_idx(c)
        if idx != -1:
            dec = idx_to_char((inv_a * (idx - b)) % M)
            res.append(dec.upper() if c.isupper() else dec)
        else:
            res.append(c)
    return "".join(res)

def ui_math_1():
    a, b = get_input_data("Введите a и b", 2)
    g, u, v = gcd_ext(a, b)
    print(f"НОД({a}, {b}) = {g}, u = {u}, v = {v}")

def ui_math_2():
    a, m = get_input_data("Введите a и m", 2)
    inv = mod_inverse(a, m)
    if inv is None:
        print("Обратного элемента не существует.")
    else:
        print(f"a^-1 (mod m) = {inv}")

def ui_math_3():
    a, b, m = get_input_data("Введите a, b и m", 3)
    sols = solve_linear_congruence(a, b, m)
    if not sols:
        print("Решений нет.")
    elif len(sols) == 1:
        print(f"Решение одно: x = {sols[0]}")
    else:
        print(f"Решений несколько: {sols}")

def ui_math_4():
    vals = get_input_data("Введите a, b, c, d, m", 5)
    sols = solve_system(*vals)
    if not sols:
        print("Решений нет.")
    elif len(sols) == 1:
        print(f"Решение одно: x = {sols[0][0]}, y = {sols[0][1]}")
    else:
        print(f"Решений несколько: {sols}")

def ui_math_5():
    text = get_input_data("Введите шифр-текст", 0, str)
    top2 = freq_analysis(text)
    print(f"Две самые частые буквы: {top2}")

def ui_math_6():
    chars = get_input_data("Введите два самых частых символа шифр-текста", 2, str)
    keys = hypothesize(chars[0], chars[1])
    if keys:
        print(f"Предполагаемые ключи (a, b): {keys}")
    else:
        print("Не удалось найти ключи на основе стандартных предположений.")

def ui_math_7():
    text = get_input_data("Введите текст", 0, str)
    a, b = get_input_data("Введите ключ (a b)", 2)
    if gcd_ext(a, M)[0] != 1:
        print("Ошибка: a и m должны быть взаимно простыми.")
        return
    print(f"Зашифрованное сообщение: {encrypt_affine(text, a, b)}")

def ui_math_8():
    text = get_input_data("Введите шифр-текст", 0, str)
    a, b = get_input_data("Введите ключ (a b)", 2)
    if gcd_ext(a, M)[0] != 1:
        print("Ошибка: a и m должны быть взаимно простыми.")
        return
    print(f"Расшифрованное сообщение: {decrypt_affine(text, a, b)}")

def math_menu():
    while True:
        print("\n--- Интерфейс Проверка 'математики' ---")
        print("1) Расширенный алгоритм Евклида")
        print("2) Вычисление a^-1(mod m)")
        print("3) Решение сравнения ax = b (mod m)")
        print("4) Решение системы сравнений")
        print("5) Выполнение частотного анализа шифр-текста")
        print("6) Выдвижение предположений о ключах")
        print("7) Шифрование при помощи Афинного Шифра")
        print("8) Расшифровка с известным ключом")
        print("9) Выход")
        choice = input("Выберите пункт: ").strip()
        
        if choice == '1': ui_math_1()
        elif choice == '2': ui_math_2()
        elif choice == '3': ui_math_3()
        elif choice == '4': ui_math_4()
        elif choice == '5': ui_math_5()
        elif choice == '6': ui_math_6()
        elif choice == '7': ui_math_7()
        elif choice == '8': ui_math_8()
        elif choice == '9': break
        else: print("Некорректный ввод.")

def variant_menu():
    print("\n--- Интерфейс Выполнение варианта ---")
    text = get_input_data("Введите зашифрованное сообщение", 0, str)
    
    top2 = freq_analysis(text)
    suggested_keys = []
    if len(top2) == 2:
        suggested_keys = hypothesize(top2[0], top2[1])
    
    all_keys = suggested_keys.copy()
    for a in range(1, M):
        if gcd_ext(a, M)[0] == 1:
            for b in range(M):
                if (a, b) not in all_keys:
                    all_keys.append((a, b))
                    
    for a, b in all_keys:
        decrypted = decrypt_affine(text, a, b)
        print(f"\nКлюч a={a}, b={b}. Текст: {decrypted[:50]}...")
        cmd = input("Подходит? (1 - нет/скип, 2 - да/сохранить): ").strip()
        if cmd == '2':
            fname = input("Введите имя файла для сохранения: ").strip()
            try:
                with open(fname, 'w', encoding='utf-8') as f:
                    f.write(f"Ключ: a={a}, b={b}\n")
                    f.write(decrypted)
                print("Успешно сохранено.")
            except Exception:
                print("Ошибка при сохранении.")
            break

def main():
    while True:
        print("\n## Главный интерфейс")
        print("1) Проверка 'математики'")
        print("2) Выполнение варианта")
        print("3) Выход")
        choice = input("Выберите пункт: ").strip()
        
        if choice == '1':
            math_menu()
        elif choice == '2':
            variant_menu()
        elif choice == '3':
            break
        else:
            print("Некорректный ввод.")

if __name__ == "__main__":
    main()