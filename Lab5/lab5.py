ALPHABET = "абвгдежзийклмнопрстуфхцчшщъыьэюя"


CHAR_TO_CODE = {char: str(10 + idx) for idx, char in enumerate(ALPHABET)}
CHAR_TO_CODE[" "] = "99"


CODE_TO_CHAR = {code: char for char, code in CHAR_TO_CODE.items()}



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



def bin_pow_mod(a, n, m):
    if m <= 0:
        return None
    if m == 1:
        return 0
    if n < 0:
        inv = mod_inverse(a, m)
        if inv is None:
            return None
        a = inv
        n = -n

    result = 1
    base = a % m
    exp = n

    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % m
        base = (base * base) % m
        exp //= 2

    return result



def trial_division_factor(n):
    if n < 4:
        return None

    if n % 2 == 0:
        return 2, n // 2

    divisor = 3
    while divisor * divisor <= n:
        if n % divisor == 0:
            return divisor, n // divisor
        divisor += 2

    return None



def recover_private_key(e, n):
    factors = trial_division_factor(n)
    if factors is None:
        return None

    p, q = factors
    phi = (p - 1) * (q - 1)
    d = mod_inverse(e, phi)

    if d is None:
        return None

    return p, q, phi, d



def digits_to_text(digits_str):
    if len(digits_str) % 2 != 0:
        return None

    chars = []
    for i in range(0, len(digits_str), 2):
        code = digits_str[i:i + 2]
        chars.append(CODE_TO_CHAR.get(code, "?"))

    return "".join(chars)



def text_to_digits(text):
    text = text.lower().replace("ё", "е")
    digits = []

    for ch in text:
        if ch in CHAR_TO_CODE:
            digits.append(CHAR_TO_CODE[ch])

    return "".join(digits)



def perform_full_attack(e, n, c):
    print(f"\nИсходные данные:")
    print(f"  открытый ключ: (e, n) = ({e}, {n})")
    print(f"  зашифрованное сообщение: C = {c}")

    print("\n1. Факторизация модуля n методом пробного деления")
    factors = trial_division_factor(n)

    if factors is None:
        print(f"  Не удалось разложить n = {n} на два множителя.")
        return None

    p, q = factors
    print(f"  Найден делитель p = {p}")
    print(f"  q = n / p = {q}")
    print(f"  Проверка: {p} * {q} = {p * q}")

    phi = (p - 1) * (q - 1)
    print(f"  phi(n) = (p - 1)(q - 1) = {phi}")

    print("\n2. Определение закрытого ключа")
    d = mod_inverse(e, phi)

    if d is None:
        print("  Не удалось найти d = e^(-1) mod phi(n).")
        return None

    print(f"  d = e^(-1) mod phi(n) = {d}")
    print(f"  закрытый ключ: (d, n) = ({d}, {n})")

    print("\n3. Расшифрование сообщения")
    m = bin_pow_mod(c, d, n)

    if m is None:
        print("  Не удалось выполнить расшифрование.")
        return None

    print(f"  M = C^d mod n = {m}")

    digits_str = str(m)
    print(f"  Цифровая строка: {digits_str}")

    plain_text = digits_to_text(digits_str)

    if plain_text is None:
        print("  Не удалось восстановить текст: нечетная длина цифровой строки.")
    else:
        print(f"  Расшифрованный текст: \"{plain_text}\"")

    return p, q, phi, d, m, plain_text



def read_ints(prompt_text, count):
    while True:
        raw = input(prompt_text + ": ").strip()
        parts = raw.replace(",", " ").split()

        if len(parts) < count:
            print("Ошибка: недостаточно данных.")
            continue

        try:
            vals = [int(x) for x in parts[:count]]
            return vals[0] if count == 1 else vals
        except ValueError:
            print("Ошибка: введите целые числа.")



def ui_math_gcd():
    a, b = read_ints("Введите a и b", 2)
    g, u, v = gcd_ext(a, b)
    print(f"НОД({a}, {b}) = {g}, u = {u}, v = {v}")



def ui_math_inverse():
    a, m = read_ints("Введите a и m", 2)
    inv = mod_inverse(a, m)

    if inv is None:
        print("Обратного элемента не существует.")
    else:
        print(f"{a}^-1 (mod {m}) = {inv}")



def ui_math_pow():
    a, n, m = read_ints("Введите a, n и m", 3)
    res = bin_pow_mod(a, n, m)

    if res is None:
        print("Невозможно вычислить степень по заданному модулю.")
    else:
        print(f"{a}^{n} (mod {m}) = {res}")



def ui_math_factor():
    n = read_ints("Введите число n для факторизации", 1)
    factors = trial_division_factor(n)

    if factors is None:
        print(f"Число {n} не удалось разложить методом пробного деления (возможно, оно простое или меньше 4).")
    else:
        p, q = factors
        print(f"n = {n} = {p} * {q}")



def ui_math_recover():
    e, n = read_ints("Введите e и n", 2)
    recovered = recover_private_key(e, n)

    if recovered is None:
        print("Не удалось восстановить закрытый ключ (факторизация не удалась или e и phi(n) не взаимно просты).")
    else:
        p, q, phi, d = recovered
        print(f"p = {p}, q = {q}")
        print(f"phi(n) = (p - 1)(q - 1) = {phi}")
        print(f"d = e^(-1) mod phi(n) = {d}")
        print(f"Закрытый ключ: (d, n) = ({d}, {n})")



def math_menu():
    while True:
        print("\nПроверка математики")
        print("1) Расширенный алгоритм Евклида")
        print("2) Нахождение обратного элемента a^-1 (mod m)")
        print("3) Быстрое возведение в степень a^n (mod m)")
        print("4) Факторизация числа n методом пробного деления")
        print("5) Восстановление закрытого ключа RSA")
        print("6) Назад")

        choice = input("Выберите пункт: ").strip()

        if choice == "1":
            ui_math_gcd()
        elif choice == "2":
            ui_math_inverse()
        elif choice == "3":
            ui_math_pow()
        elif choice == "4":
            ui_math_factor()
        elif choice == "5":
            ui_math_recover()
        elif choice == "6":
            break
        else:
            print("Некорректный ввод.")



def cryptanalysis_menu():
    e = None
    n = None
    c = None

    factors = None
    phi = None
    d = None
    decrypted_m = None

    while True:
        print("\nКриптоанализ шифра RSA")
        print("1) Ввести открытый ключ и шифртекст (e, n, C)")
        print("2) Выполнить факторизацию n методом пробного деления")
        print("3) Определить закрытый ключ")
        print("4) Расшифровать сообщение")
        print("5) Полная демонстрация атаки (пункты 1-4)")
        print("6) Назад")

        choice = input("Выберите пункт: ").strip()

        if choice == "1":
            e, n, c = read_ints("Введите e, n и C", 3)

            factors = None
            phi = None
            d = None
            decrypted_m = None

            print(f"\nВведено: (e, n) = ({e}, {n}), C = {c}")

        elif choice == "2":
            if n is None:
                print("Сначала введите модуль n.")
                continue

            factors = trial_division_factor(n)

            if factors is None:
                print(f"n = {n} не удалось разложить методом пробного деления.")
            else:
                p, q = factors
                print(f"n = {n} = {p} * {q}")

        elif choice == "3":
            if e is None or n is None:
                print("Сначала введите e и n.")
                continue

            if factors is None:
                factors = trial_division_factor(n)

            if factors is None:
                print("Сначала необходимо успешно факторизовать n.")
                continue

            p, q = factors
            phi = (p - 1) * (q - 1)
            d = mod_inverse(e, phi)

            if d is None:
                print("Обратный элемент d не существует: e и phi(n) не взаимно просты.")
            else:
                print(f"phi(n) = ({p} - 1)({q} - 1) = {phi}")
                print(f"d = e^(-1) mod phi(n) = {d}")
                print(f"Закрытый ключ: (d, n) = ({d}, {n})")

        elif choice == "4":
            if n is None or c is None:
                print("Сначала введите n и C.")
                continue

            if d is None:
                if e is None:
                    print("Сначала определите закрытый ключ d или введите e.")
                    continue

                recovered = recover_private_key(e, n)

                if recovered is None:
                    print("Не удалось восстановить закрытый ключ.")
                    continue

                p, q, phi, d = recovered

            decrypted_m = bin_pow_mod(c, d, n)

            if decrypted_m is None:
                print("Не удалось расшифровать сообщение.")
                continue

            print(f"M = C^d mod n = {decrypted_m}")

            digits_str = str(decrypted_m)
            print(f"Цифровая строка: {digits_str}")

            plain_text = digits_to_text(digits_str)

            if plain_text is None:
                print("Текст не восстановлен: нечетная длина цифровой строки.")
            else:
                print(f"Расшифрованный текст: \"{plain_text}\"")

        elif choice == "5":
            if e is None or n is None:
                e, n, c = read_ints("Введите e, n и C", 3)
            elif c is None:
                c = read_ints("Введите C", 1)

            result = perform_full_attack(e, n, c)

            if result is not None:
                p, q, phi, d, decrypted_m, _ = result
                factors = (p, q)

        elif choice == "6":
            break
        else:
            print("Некорректный ввод.")



def main():
    while True:
        print("\nГлавное меню")
        print("1. Проверка математики")
        print("2. Криптоанализ шифра RSA")
        print("3. Выход")

        choice = input("Выберите пункт: ").strip()

        if choice == "1":
            math_menu()
        elif choice == "2":
            cryptanalysis_menu()
        elif choice == "3":
            break
        else:
            print("Некорректный ввод.")



if __name__ == "__main__":
    main()
