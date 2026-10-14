import os
from collections import Counter
import itertools

ALPHABET = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
M = 32

RUSSIAN_FREQ = {
    'о': 0.090,
    'а': 0.062,
    'и': 0.062,
    'н': 0.053,
    'т': 0.053,
    'с': 0.045,
    'р': 0.040,
    'в': 0.038,
    'л': 0.035,
    'к': 0.028,
    'м': 0.026,
    'д': 0.025,
    'п': 0.023,
    'у': 0.021,
    'я': 0.018,
    'ы': 0.016,
    'з': 0.016,
    'б': 0.014,
    'г': 0.013,
    'ч': 0.012,
    'й': 0.010,
    'х': 0.009,
    'ж': 0.007,
    'ш': 0.006,
    'ю': 0.006,
    'ц': 0.004,
    'щ': 0.003,
    'э': 0.003,
    'ф': 0.002,
    'ь': 0.014,
    'ъ': 0.014,
    'е': 0.072
}

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

def solve_system(x1, y1, x2, y2, m):
    if m <= 1:
        return None

    x1 = x1 % m
    y1 = y1 % m
    x2 = x2 % m
    y2 = y2 % m

    diff_x = (x1 - x2) % m
    diff_y = (y1 - y2) % m

    a_sols = solve_linear_congruence(diff_x, diff_y, m)
    
    results = []
    for a_val in a_sols:
        b_val = (y1 - a_val * x1) % m
        results.append((a_val, b_val))

    return results

def char_to_idx(c):
    c = c.lower()
    return ALPHABET.find(c)

def idx_to_char(idx):
    return ALPHABET[idx % M]

def freq_analysis(text):
    filtered = [c.lower() for c in text if c.lower() in ALPHABET]
    if not filtered:
        return {}
    
    counter = Counter(filtered)
    total = len(filtered)
    
    freq_dict = {}
    for char, count in counter.items():
        freq_dict[char] = (count, count / total)
    
    return freq_dict

def get_top_chars(freq_dict, n=2):
    sorted_chars = sorted(freq_dict.items(), key=lambda x: x[1][0], reverse=True)
    return [char for char, _ in sorted_chars[:n]]

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

def math_menu():
    while True:
        print("\nИнтерфейс Проверка 'математики'")
        print("1) Расширенный алгоритм Евклида")
        print("2) Вычисление a^-1(mod m)")
        print("3) Решение сравнения ax = b (mod m)")
        print("4) Решение системы сравнений")
        print("5) Выход")
        choice = input("Выберите пункт: ").strip()
        
        if choice == '1': ui_math_1()
        elif choice == '2': ui_math_2()
        elif choice == '3': ui_math_3()
        elif choice == '4': ui_math_4()
        elif choice == '5': break
        else: print("Некорректный ввод.")

def variant_menu():
    print("\nИнтерфейс Выполнение варианта")
    
    cipher_text = get_input_data("Введите зашифрованное сообщение", 0, str)
    
    print("\nАнализ частоты букв в шифр-тексте")
    cipher_freq = freq_analysis(cipher_text)
    
    if not cipher_freq:
        print("Ошибка: в тексте нет букв русского алфавита.")
        return
    
    sorted_cipher_freq = sorted(cipher_freq.items(), 
                                key=lambda x: x[1][0], 
                                reverse=True)
    print("\nЧастоты букв в шифр-тексте:")
    for char, (count, prob) in sorted_cipher_freq:
        print(f"p({char}) = {count}/{len([c for c in cipher_text if c.lower() in ALPHABET])} = {prob:.4f}")
    
    top2_cipher = get_top_chars(cipher_freq, 2)
    print(f"\nДве самые встречаемые буквы в шифр-тексте: {top2_cipher[0]}, {top2_cipher[1]}")
    print(f"Частоты: {cipher_freq[top2_cipher[0]][1]:.4f}, {cipher_freq[top2_cipher[1]][1]:.4f}")
    
    print("\nВыдвижение гипотез")
    sorted_russian = sorted(RUSSIAN_FREQ.items(), 
                           key=lambda x: x[1], 
                           reverse=True)
    russian_chars = [char for char, _ in sorted_russian]
    
    pairs_with_prob = []
    for p1, p2 in itertools.permutations(russian_chars, 2):
        freq1 = RUSSIAN_FREQ.get(p1, 0)
        freq2 = RUSSIAN_FREQ.get(p2, 0)
        prob = freq1 * freq2
        pairs_with_prob.append(((p1, p2), prob))
    
    pairs_with_prob.sort(key=lambda x: x[1], reverse=True)
    
    print(f"Рассматриваем {len(pairs_with_prob)} гипотез...")
    
    hypothesis_num = 0
    found_key = False
    
    for (p1, p2), prob in pairs_with_prob:
        if found_key:
            break
            
        hypothesis_num += 1
        c1, c2 = top2_cipher[0], top2_cipher[1]
        
        y1 = char_to_idx(c1)
        y2 = char_to_idx(c2)
        x1 = char_to_idx(p1)
        x2 = char_to_idx(p2)
        
        keys = solve_system(x1, y1, x2, y2, M)
        
        if not keys:
            continue
        
        for a, b in keys:
            if gcd_ext(a, M)[0] != 1:
                continue
            
            decrypted = decrypt_affine(cipher_text, a, b)
            
            print(f"\nГипотеза {hypothesis_num}: {p1} -> {c1}, {p2} -> {c2}")
            print(f"Ключ: a = {a}, b = {b}")
            print(f"Расшифрованный текст (первые 100 символов):")
            print(decrypted[:100])
            if len(decrypted) > 100:
                print("...")
            
            while True:
                cmd = input("\nПодходит? (1 - нет, 2 - да): ").strip()
                if cmd in ['1', '2']:
                    break
                print("Некорректный ввод.")
            
            if cmd == '2':
                fname = input("Введите имя файла для сохранения (или Enter для пропуска): ").strip()
                if fname:
                    try:
                        with open(fname, 'w', encoding='utf-8') as f:
                            f.write(f"Ключ: a={a}, b={b}\n")
                            f.write(decrypted)
                        print("Успешно сохранено.")
                    except Exception as e:
                        print(f"Ошибка при сохранении: {e}")
                found_key = True
                break
    
    if not found_key:
        print("\nНе удалось найти подходящий ключ среди рассмотренных гипотез.")

def main():
    while True:
        print("\nГлавный интерфейс")
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
