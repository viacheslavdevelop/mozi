VARIANT_M = 518293


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


def int_sqrt(n):
    if n < 0:
        return None
    if n < 2:
        return n

    x = n
    y = (x + n // x) // 2
    while y < x:
        x = y
        y = (x + n // x) // 2
    return x


def quadratic_residues(mod):
    if mod <= 1:
        return None
    return {(x * x) % mod for x in range(mod)}


def build_quadratic_sieve(m, mod):
    if mod <= 1:
        return None

    residues = quadratic_residues(mod)
    x_values = list(range(mod))
    x2_mod = [(x * x) % mod for x in x_values]
    z_values = [(x * x - m) % mod for x in x_values]
    sieve_ok = [z in residues for z in z_values]

    return {
        "mod": mod,
        "residues": residues,
        "x_values": x_values,
        "x2_mod": x2_mod,
        "z_values": z_values,
        "sieve_ok": sieve_ok,
    }


def rho_func(x, m):
    if m <= 1:
        return None
    return (x * x + 1) % m


def factorize_quadratic_sieve(m, moduli):
    if m <= 1:
        return None

    sieves = [build_quadratic_sieve(m, mod) for mod in moduli]
    if any(s is None for s in sieves):
        return None

    root = int_sqrt(m)
    x_start = root + 1
    x_end = (m + 1) // 2
    shifts = [(s["mod"], x_start % s["mod"]) for s in sieves]

    if m % 2 == 0:
        return {
            "m": m,
            "sieves": sieves,
            "x_start": x_start,
            "x_end": x_end,
            "shifts": shifts,
            "checked_candidates": [],
            "found": True,
            "trivial_note": "Число m четное, делитель 2 найден напрямую.",
            "x": None,
            "y": None,
            "p": m // 2,
            "q": 2,
        }

    if root * root == m:
        return {
            "m": m,
            "sieves": sieves,
            "x_start": x_start,
            "x_end": x_end,
            "shifts": shifts,
            "checked_candidates": [],
            "found": True,
            "trivial_note": f"Число m является полным квадратом: {root}^2 = {m}.",
            "x": root,
            "y": 0,
            "p": root,
            "q": root,
        }

    checked_candidates = []
    for x in range(x_start, x_end + 1):
        passed = True
        for sieve in sieves:
            if not sieve["sieve_ok"][x % sieve["mod"]]:
                passed = False
                break
        if not passed:
            continue

        x2 = x * x
        z = x2 - m
        y = int_sqrt(z)
        is_square = y * y == z

        checked_candidates.append({
            "x": x,
            "x2": x2,
            "z": z,
            "y": y,
            "is_square": is_square,
        })

        if is_square:
            p = x + y
            q = x - y
            return {
                "m": m,
                "sieves": sieves,
                "x_start": x_start,
                "x_end": x_end,
                "shifts": shifts,
                "checked_candidates": checked_candidates,
                "found": True,
                "trivial_note": None,
                "x": x,
                "y": y,
                "p": p,
                "q": q,
            }

    return {
        "m": m,
        "sieves": sieves,
        "x_start": x_start,
        "x_end": x_end,
        "shifts": shifts,
        "checked_candidates": checked_candidates,
        "found": False,
        "trivial_note": None,
        "x": None,
        "y": None,
        "p": None,
        "q": None,
    }


def factorize_rho(m, x1_init, x2_init, max_steps=100000):
    if m <= 1:
        return None

    x1 = x1_init % m
    x2 = x2_init % m
    steps = [{"n": 0, "x1": x1, "x2": x2, "a": None, "d": None}]
    seen = {(x1, x2)}

    for n in range(1, max_steps + 1):
        x1 = rho_func(x1, m)
        x2 = rho_func(rho_func(x2, m), m)
        a_n = abs(x1 - x2)
        d_n, _, _ = gcd_ext(a_n, m)

        steps.append({"n": n, "x1": x1, "x2": x2, "a": a_n, "d": d_n})

        if 1 < d_n < m:
            p = d_n
            q = m // d_n
            return {
                "m": m,
                "steps": steps,
                "found": True,
                "step": n,
                "p": p,
                "q": q,
                "reason": None,
            }

        if d_n == m:
            return {
                "m": m,
                "steps": steps,
                "found": False,
                "step": n,
                "p": None,
                "q": None,
                "reason": "d_n == m",
            }

        if (x1, x2) in seen:
            return {
                "m": m,
                "steps": steps,
                "found": False,
                "step": n,
                "p": None,
                "q": None,
                "reason": "cycle",
            }

        seen.add((x1, x2))

    return {
        "m": m,
        "steps": steps,
        "found": False,
        "step": max_steps,
        "p": None,
        "q": None,
        "reason": "limit",
    }


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


def read_target_m():
    while True:
        use_var = input(f"Использовать m из варианта 15 ({VARIANT_M})? (1 - да, 2 - ввести свое): ").strip()
        if use_var == "1":
            return VARIANT_M
        if use_var == "2":
            m = read_ints("Введите число m (> 1)", 1)
            if m <= 1:
                print("Ошибка: число m должно быть больше 1.")
                continue
            return m
        print("Некорректный ввод.")


def print_sieve_table(m, sieve, chunk_size=17):
    mod = sieve["mod"]
    residues_sorted = sorted(sieve["residues"])
    print(f"\nРешето по модулю {mod} (квадратичные вычеты: {residues_sorted}):")

    labels = [
        "x",
        f"x^2 mod {mod}",
        f"z = (x^2 - {m}) mod {mod}",
        f"S_{mod}",
    ]
    label_width = max(len(lbl) for lbl in labels)
    col_width = max(len(str(mod - 1)), 2)

    for start in range(0, mod, chunk_size):
        end = min(start + chunk_size, mod)
        xs = sieve["x_values"][start:end]
        x2s = sieve["x2_mod"][start:end]
        zs = sieve["z_values"][start:end]
        marks = [" " if ok else "X" for ok in sieve["sieve_ok"][start:end]]

        row_x = f"{labels[0]:<{label_width}} | " + " | ".join(f"{v:>{col_width}}" for v in xs)
        row_x2 = f"{labels[1]:<{label_width}} | " + " | ".join(f"{v:>{col_width}}" for v in x2s)
        row_z = f"{labels[2]:<{label_width}} | " + " | ".join(f"{v:>{col_width}}" for v in zs)
        row_s = f"{labels[3]:<{label_width}} | " + " | ".join(f"{v:>{col_width}}" for v in marks)
        sep = "-" * len(row_x)

        print(row_x)
        print(sep)
        print(row_x2)
        print(row_z)
        print(row_s)
        if end < mod:
            print()


def print_overlay_table(sieves, x_start, x_limit, chunk_size=17):
    total = x_limit - x_start + 1
    max_display = 68

    if total <= max_display:
        ranges = [
            (x_start + i, min(x_start + i + chunk_size - 1, x_limit))
            for i in range(0, total, chunk_size)
        ]
    else:
        first_end = x_start + chunk_size - 1
        last_start = max(first_end + 1, x_limit - chunk_size + 1)
        ranges = [(x_start, first_end), None, (last_start, x_limit)]

    label_width = max(max(len(f"S_{s['mod']}") for s in sieves), 3)

    for rng in ranges:
        if rng is None:
            print("...")
            continue
        start, end = rng
        xs = list(range(start, end + 1))
        col_width = max(len(str(end)), 2)

        header = f"{'x':<{label_width}} | " + " | ".join(f"{x:>{col_width}}" for x in xs)
        sep = "-" * len(header)
        print(header)
        print(sep)

        for sieve in sieves:
            mod = sieve["mod"]
            label = f"S_{mod}"
            marks = []
            for x in xs:
                mark = " " if sieve["sieve_ok"][x % mod] else "X"
                marks.append(f"{mark:>{col_width}}")
            print(f"{label:<{label_width}} | " + " | ".join(marks))
        print()


def print_rho_table(steps):
    max_rows = 60
    if len(steps) <= max_rows:
        display_rows = steps
    else:
        display_rows = steps[:25] + [None] + steps[-25:]

    w_n = max(len(str(steps[-1]["n"])), 3)
    w_val = max(
        max(len(str(s["x1"])) for s in steps),
        max(len(str(s["x2"])) for s in steps),
        max((len(str(s["a"])) for s in steps if s["a"] is not None), default=1),
        6,
    )

    header = (
        f"{'n':>{w_n}} | "
        f"{'x^(1)':>{w_val}} | "
        f"{'x^(2)':>{w_val}} | "
        f"{'a_n':>{w_val}} | "
        f"{'d_n':>{w_val}}"
    )
    print(header)
    print("-" * len(header))

    for row in display_rows:
        if row is None:
            print("...")
            continue
        a_str = "-" if row["a"] is None else str(row["a"])
        d_str = "-" if row["d"] is None else str(row["d"])
        print(
            f"{row['n']:>{w_n}} | "
            f"{row['x1']:>{w_val}} | "
            f"{row['x2']:>{w_val}} | "
            f"{a_str:>{w_val}} | "
            f"{d_str:>{w_val}}"
        )


def ui_math_gcd():
    a, b = read_ints("Введите a и b", 2)
    g, u, v = gcd_ext(a, b)
    print(f"НОД({a}, {b}) = {g}, u = {u}, v = {v}")


def ui_math_isqrt():
    n = read_ints("Введите целое неотрицательное число n", 1)
    root = int_sqrt(n)
    if root is None:
        print("Ошибка: число должно быть неотрицательным.")
        return
    if root * root == n:
        print(f"[sqrt({n})] = {root} (полный квадрат: {root}^2 = {n})")
    else:
        print(f"[sqrt({n})] = {root} (не полный квадрат: {root}^2 = {root * root} < {n} < {(root + 1) ** 2})")


def ui_math_sieve():
    m, mod = read_ints("Введите m и модуль решета k (> 1)", 2)
    if mod <= 1:
        print("Ошибка: модуль k должен быть больше 1.")
        return
    sieve = build_quadratic_sieve(m, mod)
    print_sieve_table(m, sieve)


def ui_math_rho_func():
    x, m = read_ints("Введите x и m (> 1)", 2)
    if m <= 1:
        print("Ошибка: модуль m должен быть больше 1.")
        return
    fx = rho_func(x, m)
    ffx = rho_func(fx, m)
    print(f"f({x}) = ({x}^2 + 1) mod {m} = {fx}")
    print(f"f(f({x})) = ({fx}^2 + 1) mod {m} = {ffx}")


def math_menu():
    while True:
        print("\nПроверка математики")
        print("1) Расширенный алгоритм Евклида")
        print("2) Целозначный квадратный корень")
        print("3) Построение квадратичного решета по модулю k")
        print("4) Циклическая функция f(x) = (x^2 + 1) mod m")
        print("5) Назад")
        choice = input("Выберите пункт: ").strip()

        if choice == "1":
            ui_math_gcd()
        elif choice == "2":
            ui_math_isqrt()
        elif choice == "3":
            ui_math_sieve()
        elif choice == "4":
            ui_math_rho_func()
        elif choice == "5":
            break
        else:
            print("Некорректный ввод.")


def show_quadratic_sieve_process(m, moduli):
    result = factorize_quadratic_sieve(m, moduli)
    if result is None:
        print("Ошибка: некорректные параметры факторизации.")
        return None

    print(f"\n--- Метод квадратичного решета для m = {m} ---")
    print("Шаг 1. Построение квадратичных решет по модулям:", ", ".join(str(k) for k in moduli))
    for sieve in result["sieves"]:
        print_sieve_table(m, sieve)

    if result["trivial_note"] is not None:
        print(f"\n{result['trivial_note']}")
        print(f"Ответ: {m} = {min(result['p'], result['q'])} * {max(result['p'], result['q'])}")
        return result

    x_start = result["x_start"]
    x_end = result["x_end"]
    print(f"\nШаг 2. Наложение решет на интервал от [sqrt({m})] + 1 = {x_start} до (m + 1) / 2 = {x_end}:")
    for mod, shift in result["shifts"]:
        print(f"  Для модуля {mod}: {x_start} mod {mod} = {shift} (начинаем с S_{mod}({shift}))")

    x_limit = min(x_end, max(x_start + 16, result["x"] if result["x"] is not None else x_start + 16))
    print()
    print_overlay_table(result["sieves"], x_start, x_limit)

    candidates = result["checked_candidates"]
    print(f"Шаг 3. Проверка не вычеркнутых чисел x (проверено кандидатов: {len(candidates)}):")
    if len(candidates) <= 30:
        display_candidates = candidates
    else:
        display_candidates = candidates[:15] + [None] + candidates[-10:]

    for cand in display_candidates:
        if cand is None:
            print(f"  ... (пропущено кандидатов: {len(candidates) - 25}) ...")
            continue
        x = cand["x"]
        x2 = cand["x2"]
        z = cand["z"]
        y = cand["y"]
        if cand["is_square"]:
            print(f"  x = {x}: x^2 = {x2}, z = {z}, isqrt(z) = {y} ({y}^2 = {z} — полный квадрат, y = {y})")
        else:
            print(f"  x = {x}: x^2 = {x2}, z = {z}, isqrt(z) = {y} ({y}^2 = {y * y} != {z})")

    print("\nШаг 4. Вычисление делителей:")
    if not result["found"]:
        print("Не удалось найти разложение.")
        return result

    p = result["p"]
    q = result["q"]
    x = result["x"]
    y = result["y"]
    print(f"  p = x + y = {x} + {y} = {p}")
    print(f"  q = x - y = {x} - {y} = {q}")
    if q == 1 or p == m:
        print(f"Найдены только тривиальные делители: число {m} является простым.")
    else:
        print(f"Ответ: {m} = {q} * {p}")
    return result


def show_rho_process(m, x1_init, x2_init):
    result = factorize_rho(m, x1_init, x2_init)
    if result is None:
        print("Ошибка: некорректные параметры факторизации.")
        return None

    print(f"\n--- Ро-метод факторизации для m = {m} ---")
    print(f"Циклическая функция: f(x) = (x^2 + 1) mod {m}")
    print(f"Начальные члены: x0^(1) = {x1_init}, x0^(2) = {x2_init}\n")

    print_rho_table(result["steps"])
    print()

    if result["found"]:
        p = min(result["p"], result["q"])
        q = max(result["p"], result["q"])
        print(f"Результат получен на шаге n = {result['step']}: найден делитель d_{result['step']} = {result['p']}.")
        print(f"Ответ: {m} = {p} * {q}")
    elif result["reason"] == "d_n == m":
        print(f"На шаге n = {result['step']} получено d_n = {m}. Попробуйте другие начальные значения (или m простое).")
    elif result["reason"] == "cycle":
        print(f"На шаге n = {result['step']} последовательности зациклились без нахождения делителя.")
    else:
        print(f"Превышен лимит шагов ({result['step']}). Попробуйте другие начальные значения.")
    return result


def read_sieve_moduli():
    while True:
        a, b, c = read_ints("Введите три модуля решет a, b, c (например, 3 5 7)", 3)
        if a <= 1 or b <= 1 or c <= 1:
            print("Ошибка: все модули должны быть больше 1.")
            continue
        return [a, b, c]


def variant_menu():
    while True:
        print("\nВыполнение варианта")
        print("1) Факторизация методом квадратичного решета")
        print("2) Факторизация ро-методом")
        print("3) Факторизация обоими методами")
        print("4) Назад")
        choice = input("Выберите пункт: ").strip()

        if choice == "1":
            m = read_target_m()
            moduli = read_sieve_moduli()
            show_quadratic_sieve_process(m, moduli)

        elif choice == "2":
            m = read_target_m()
            x1_init, x2_init = read_ints("Введите начальные члены x0^(1) и x0^(2) (например, 2 2)", 2)
            show_rho_process(m, x1_init, x2_init)

        elif choice == "3":
            m = read_target_m()
            moduli = read_sieve_moduli()
            x1_init, x2_init = read_ints("Введите начальные члены x0^(1) и x0^(2) (например, 2 2)", 2)
            qs_res = show_quadratic_sieve_process(m, moduli)
            rho_res = show_rho_process(m, x1_init, x2_init)
            if qs_res and rho_res:
                print("\nСводка по методам:")
                print(f"  Квадратичное решето: проверено кандидатов — {len(qs_res['checked_candidates'])}")
                print(f"  Ро-метод: выполнено шагов — {rho_res['step']}")

        elif choice == "4":
            break
        else:
            print("Некорректный ввод.")


def main():
    while True:
        print("\nГлавное меню")
        print("1. Проверка математики")
        print("2. Выполнение варианта")
        print("3. Выход")
        choice = input("Выберите пункт: ").strip()

        if choice == "1":
            math_menu()
        elif choice == "2":
            variant_menu()
        elif choice == "3":
            break
        else:
            print("Некорректный ввод.")


if __name__ == "__main__":
    main()
