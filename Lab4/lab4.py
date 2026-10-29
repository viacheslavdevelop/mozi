import random

ALPHABET = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"

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


def generate_key_pairs(p, q, count=3):
    n = p * q
    phi = (p - 1) * (q - 1)
    pairs = []
    used_e = set()

    attempts = 0
    while len(pairs) < count and attempts < 10000:
        attempts += 1
        e = random.randint(2, phi - 1)
        if e in used_e:
            continue
        gcd, _, _ = gcd_ext(e, phi)
        if gcd == 1:
            d = mod_inverse(e, phi)
            if d is not None and d != e:
                used_e.add(e)
                pairs.append(((e, n), (d, n)))

    return pairs


def text_to_digits(text):
    text = text.upper().replace("Ё", "Е")
    digits = []
    for ch in text:
        if ch in CHAR_TO_CODE:
            digits.append(CHAR_TO_CODE[ch])
    return "".join(digits)


def digits_to_text(digits_str):
    if len(digits_str) % 2 != 0:
        return None
    chars = []
    for i in range(0, len(digits_str), 2):
        code = digits_str[i:i + 2]
        chars.append(CODE_TO_CHAR.get(code, "?"))
    return "".join(chars)


def split_into_blocks(digits_str, n):
    blocks = []
    i = 0
    length = len(digits_str)

    while i < length:
        j = i + 1
        while j <= length and int(digits_str[i:j]) < n:
            j += 1
        end = j - 1

        if end <= i:
            return None

        while end < length and digits_str[end] == "0":
            end -= 1
            if end <= i:
                return None

        blocks.append(int(digits_str[i:end]))
        i = end

    return blocks


def encrypt_blocks(blocks, public_key):
    e, n = public_key
    return [bin_pow_mod(m, e, n) for m in blocks]


def decrypt_blocks(encrypted_blocks, private_key):
    d, n = private_key
    return [bin_pow_mod(c, d, n) for c in encrypted_blocks]


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


def math_menu():
    while True:
        print("\nПроверка математики")
        print("1) Расширенный алгоритм Евклида")
        print("2) Нахождение обратного элемента a^-1 (mod m)")
        print("3) Быстрое возведение в степень a^n (mod m)")
        print("4) Назад")
        choice = input("Выберите пункт: ").strip()

        if choice == "1":
            ui_math_gcd()
        elif choice == "2":
            ui_math_inverse()
        elif choice == "3":
            ui_math_pow()
        elif choice == "4":
            break
        else:
            print("Некорректный ввод.")


def rsa_menu():
    key_pairs = []
    encrypted_array = []
    active_private_key = None

    while True:
        print("\nШифрование и дешифрование RSA")
        print("1) Генерация множества ключей (k, l) по p и q")
        print("2) Демонстрация шифрования")
        print("3) Демонстрация дешифрования")
        print("4) Назад")
        choice = input("Выберите пункт: ").strip()

        if choice == "1":
            p, q = read_ints("Введите простые числа p и q", 2)
            n = p * q
            phi = (p - 1) * (q - 1)
            if n <= 100:
                print("Ошибка: модуль n = p * q должен быть больше 100.")
                continue

            count = read_ints("Введите количество пар ключей (не менее 3)", 1)
            if count < 3:
                count = 3

            key_pairs = generate_key_pairs(p, q, count)
            if len(key_pairs) < 3:
                print("Не удалось сгенерировать достаточное количество ключей.")
                continue

            print(f"\nПараметры: n = {n}, phi(n) = {phi}")
            print("Сгенерированное множество ключей:")
            for idx, (pub, priv) in enumerate(key_pairs, start=1):
                print(f"Пара №{idx}: открытый ключ k = {pub}, закрытый ключ l = {priv}")

        elif choice == "2":
            text = input("Введите открытый текст (русские буквы и пробел): ").strip()
            digits_str = text_to_digits(text)
            if not digits_str:
                print("Ошибка: текст не содержит допустимых символов русского алфавита.")
                continue

            if key_pairs:
                print("\nДоступные пары ключей:")
                for idx, (pub, priv) in enumerate(key_pairs, start=1):
                    print(f"{idx}) k = {pub}, l = {priv}")
                print("0) Ввести ключи вручную")
                sel = read_ints("Выберите номер пары ключей", 1)
                if 1 <= sel <= len(key_pairs):
                    public_key, active_private_key = key_pairs[sel - 1]
                else:
                    e, n = read_ints("Введите открытый ключ (e и n)", 2)
                    d = read_ints("Введите секретную экспоненту d (или 0, если неизвестна)", 1)
                    public_key = (e, n)
                    active_private_key = (d, n) if d > 0 else None
            else:
                e, n = read_ints("Введите открытый ключ (e и n)", 2)
                d = read_ints("Введите секретную экспоненту d (или 0, если неизвестна)", 1)
                public_key = (e, n)
                active_private_key = (d, n) if d > 0 else None

            e, n = public_key
            if n <= 100:
                print("Ошибка: модуль n должен быть больше 100.")
                continue

            print(f"\nЧисловое представление текста: {digits_str}")
            blocks = split_into_blocks(digits_str, n)
            if not blocks:
                print("Ошибка при разбиении на блоки.")
                continue

            print("Разбиение на блоки M_i:")
            for idx, b in enumerate(blocks, start=1):
                print(f"M{idx} = {b}")

            encrypted_array = encrypt_blocks(blocks, public_key)
            print(f"\nМассив зашифрованных блоков C_i: {encrypted_array}")

        elif choice == "3":
            if encrypted_array:
                use_saved = input(f"Использовать текущий массив {encrypted_array}? (1 - да, 2 - ввести свой): ").strip()
            else:
                use_saved = "2"

            if use_saved == "1":
                cipher_blocks = encrypted_array
            else:
                raw_blocks = input("Введите зашифрованные блоки через пробел: ").strip()
                try:
                    cipher_blocks = [int(x) for x in raw_blocks.replace(",", " ").split()]
                except ValueError:
                    print("Ошибка: некорректный ввод блоков.")
                    continue
                if not cipher_blocks:
                    print("Ошибка: массив пуст.")
                    continue

            if active_private_key is not None:
                use_key = input(f"Использовать закрытый ключ l = {active_private_key}? (1 - да, 2 - ввести другой): ").strip()
            else:
                use_key = "2"

            if use_key == "1":
                private_key = active_private_key
            else:
                if key_pairs:
                    print("\nДоступные закрытые ключи:")
                    for idx, (_, priv) in enumerate(key_pairs, start=1):
                        print(f"{idx}) l = {priv}")
                    print("0) Ввести вручную")
                    sel = read_ints("Выберите номер ключа", 1)
                    if 1 <= sel <= len(key_pairs):
                        private_key = key_pairs[sel - 1][1]
                    else:
                        d, n = read_ints("Введите закрытый ключ (d и n)", 2)
                        private_key = (d, n)
                else:
                    d, n = read_ints("Введите закрытый ключ (d и n)", 2)
                    private_key = (d, n)

            decrypted_blocks = decrypt_blocks(cipher_blocks, private_key)
            print("\nПоэлементно расшифрованные блоки M_i:")
            for idx, m in enumerate(decrypted_blocks, start=1):
                print(f"M{idx} = {m}")

            restored_digits = "".join(str(m) for m in decrypted_blocks)
            print(f"Восстановленная цифровая строка: {restored_digits}")

            plain_text = digits_to_text(restored_digits)
            if plain_text is None:
                print("Ошибка: длина цифровой строки нечетная, проверьте правильность ключа.")
            else:
                print(f"Расшифрованный текст: {plain_text}")

        elif choice == "4":
            break
        else:
            print("Некорректный ввод.")


def main():
    while True:
        print("\nГлавное меню")
        print("1. Проверка математики")
        print("2. Выполнение процедуры шифрования и дешифрования")
        print("3. Выход")
        choice = input("Выберите пункт: ").strip()

        if choice == "1":
            math_menu()
        elif choice == "2":
            rsa_menu()
        elif choice == "3":
            break
        else:
            print("Некорректный ввод.")


if __name__ == "__main__":
    main()
