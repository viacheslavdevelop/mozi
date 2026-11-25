ALPHABET = "абвгдежзийклмнопрстуфхцчшщъыьэюя"

CHAR_TO_CODE = {char: str(10 + idx) for idx, char in enumerate(ALPHABET)}
CHAR_TO_CODE[" "] = "99"

CODE_TO_CHAR = {code: char for char, code in CHAR_TO_CODE.items()}


def gcd(a, b):
    a = abs(a)
    b = abs(b)
    while b != 0:
        a, b = b, a % b
    return a


def gcd_ext(a, b):
    old_r, r = abs(a), abs(b)
    old_x, x = 1, 0
    old_y, y = 0, 1

    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_x, x = x, old_x - q * x
        old_y, y = y, old_y - q * y

    if a < 0:
        old_x = -old_x
    if b < 0:
        old_y = -old_y

    return old_r, old_x, old_y


def mod_inverse(a, m):
    if m <= 1:
        return None

    g, x, _ = gcd_ext(a, m)
    if g != 1:
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


def isqrt(n):
    if n < 0:
        return None
    if n < 2:
        return n
    x = 1 << ((n.bit_length() + 1) // 2)
    while True:
        y = (x + n // x) // 2
        if y >= x:
            return x
        x = y


def odd_primes_generator():
    base_primes = []
    low = 3
    segment_size = 1024

    while True:
        high = low + segment_size
        size = (high - low) // 2
        sieve = bytearray([1]) * size

        for p in base_primes:
            if p * p >= high:
                break
            start = p * p
            if start < low:
                rem = low % p
                start = low if rem == 0 else low + (p - rem)
            if start % 2 == 0:
                start += p
            if start < high:
                idx = (start - low) // 2
                count = (size - 1 - idx) // p + 1
                sieve[idx::p] = bytearray(count)

        for i in range(size):
            if sieve[i]:
                p = low + 2 * i
                if p * p < high:
                    idx = (p * p - low) // 2
                    count = (size - 1 - idx) // p + 1
                    sieve[idx::p] = bytearray(count)
                base_primes.append(p)
                yield p

        low = high
        if segment_size < 131072:
            segment_size *= 2


def trial_division_factor(n):
    if n < 2:
        return None

    factors = []

    while n % 2 == 0:
        factors.append(2)
        n //= 2

    if n == 1:
        return factors

    limit = isqrt(n)
    primes = odd_primes_generator()

    while n > 1:
        p1 = next(primes)
        if p1 > limit:
            break

        triple = [p1]
        p2 = next(primes)
        if p2 <= limit:
            triple.append(p2)
            p3 = next(primes)
            if p3 <= limit:
                triple.append(p3)

        s = 1
        for p in triple:
            s *= p

        while True:
            d = gcd(n, s)
            if d == 1:
                break
            n //= d
            for p in triple:
                if d % p == 0:
                    factors.append(p)
            limit = isqrt(n)

    if n > 1:
        factors.append(n)

    factors.sort()
    return factors


def count_prime_powers(factors):
    counts = {}
    for p in factors:
        counts[p] = counts.get(p, 0) + 1
    return counts


def euler_phi_from_factors(factors):
    if not factors:
        return None
    counts = count_prime_powers(factors)
    phi = 1
    for p, k in counts.items():
        phi *= (p ** (k - 1)) * (p - 1)
    return phi


def format_factorization(n, factors):
    if len(factors) == 1:
        return f"n = {n} — простое число"

    expanded = " * ".join(str(p) for p in factors)
    counts = count_prime_powers(factors)
    canonical_parts = []
    for p, k in counts.items():
        if k == 1:
            canonical_parts.append(str(p))
        else:
            canonical_parts.append(f"{p}^{k}")
    canonical = " * ".join(canonical_parts)

    if canonical != expanded:
        return f"n = {n} = {expanded} = {canonical}"
    return f"n = {n} = {expanded}"


def format_phi_formula(factors):
    counts = count_prime_powers(factors)
    parts = []
    for p, k in counts.items():
        if k == 1:
            parts.append(f"({p} - 1)")
        elif k == 2:
            parts.append(f"{p} * ({p} - 1)")
        else:
            parts.append(f"{p}^{k - 1} * ({p} - 1)")
    return " * ".join(parts)


def recover_private_key(e, n):
    if e <= 0:
        return None

    factors = trial_division_factor(n)
    if factors is None or len(factors) < 2:
        return None

    phi = euler_phi_from_factors(factors)
    d = mod_inverse(e, phi)

    if d is None:
        return None

    return factors, phi, d


def digits_to_text(digits_str):
    if not digits_str or len(digits_str) % 2 != 0 or not digits_str.isdigit():
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
    print("\nИсходные данные:")
    print(f"  открытый ключ: (e, n) = ({e}, {n})")
    print(f"  зашифрованное сообщение: C = {c}")

    print("\n1. Факторизация модуля n методом пробного деления")
    factors = trial_division_factor(n)

    if factors is None:
        print(f"  Не удалось разложить n = {n}: модуль должен быть целым числом больше 1.")
        return None

    if len(factors) < 2:
        print(f"  n = {n} является простым числом. Для RSA требуется составной модуль.")
        return None

    print(f"  {format_factorization(n, factors)}")
    product_check = 1
    for p in factors:
        product_check *= p
    print(f"  Проверка произведения: {product_check}")

    phi = euler_phi_from_factors(factors)
    print(f"  phi(n) = {format_phi_formula(factors)} = {phi}")

    if len(set(factors)) < len(factors):
        print("  Предупреждение: модуль n имеет кратные простые множители; расшифрование корректно при НОД(M, n) = 1.")

    print("\n2. Определение закрытого ключа")
    if e <= 0:
        print(f"  Некорректная открытая экспонента e = {e}: требуется e > 0.")
        return None

    d = mod_inverse(e, phi)

    if d is None:
        print("  Не удалось найти d = e^(-1) mod phi(n): e и phi(n) не взаимно просты.")
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

    return factors, phi, d, m, plain_text


def read_ints(prompt_text, count):
    while True:
        raw = input(prompt_text + ": ").strip()
        parts = raw.replace(",", " ").split()

        if len(parts) != count:
            print(f"Ошибка: введите ровно {count} целых чисел.")
            continue

        try:
            vals = [int(x) for x in parts]
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
        print(f"Для числа {n} разложение на простые множители не определено (введите целое число больше 1).")
    else:
        print(format_factorization(n, factors))


def ui_math_recover():
    e, n = read_ints("Введите e и n", 2)

    if e <= 0:
        print("Открытая экспонента e должна быть положительным целым числом.")
        return

    factors = trial_division_factor(n)
    if factors is None:
        print("Модуль n должен быть целым числом больше 1.")
        return

    if len(factors) < 2:
        print(f"n = {n} — простое число. Для RSA требуется составной модуль.")
        return

    phi = euler_phi_from_factors(factors)
    d = mod_inverse(e, phi)

    if d is None:
        print("Не удалось восстановить закрытый ключ: e и phi(n) не взаимно просты.")
    else:
        print(format_factorization(n, factors))
        print(f"phi(n) = {format_phi_formula(factors)} = {phi}")
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
                print(f"Для n = {n} разложение на простые множители не определено (введите целое число больше 1).")
            else:
                print(format_factorization(n, factors))

        elif choice == "3":
            if e is None or n is None:
                print("Сначала введите e и n.")
                continue

            if e <= 0:
                print("Открытая экспонента e должна быть положительным целым числом.")
                phi = None
                d = None
                continue

            if factors is None:
                factors = trial_division_factor(n)

            if factors is None or len(factors) < 2:
                print("Модуль n должен быть составным целым числом больше 3.")
                phi = None
                d = None
                continue

            phi = euler_phi_from_factors(factors)
            d = mod_inverse(e, phi)

            if d is None:
                print("Обратный элемент d не существует: e и phi(n) не взаимно просты.")
            else:
                if len(set(factors)) < len(factors):
                    print("Предупреждение: модуль n имеет кратные простые множители; расшифрование корректно при НОД(M, n) = 1.")
                print(f"phi(n) = {format_phi_formula(factors)} = {phi}")
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

                factors, phi, d = recovered

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
                factors, phi, d, decrypted_m, _ = result
            else:
                factors = trial_division_factor(n)
                phi = None
                d = None
                decrypted_m = None

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
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nРабота программы завершена.")
