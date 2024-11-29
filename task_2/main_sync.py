from time import time

def factorize_sync(*numbers):
    results = []
    for number in numbers:
        divisors = []
        for i in range(1, number + 1):
            if number % i == 0:
                divisors.append(i)
        results.append(divisors)
    return results
 
# Тестування синхронної функції
if __name__ == "__main__":
    # Замір часу синхронної версії
    start_time = time()
    a, b, c, d = factorize_sync(128, 255, 99999, 10651060)
    end_time = time()

    # Виведення результатів
    print(f"Час виконання синхронної версії: {end_time - start_time:.2f} секунд.")
    print("Результати факторизації:")
    print(f"128: {a}")
    print(f"255: {b}")
    print(f"99999: {c}")
    print(f"10651060: {d}")

    # Перевірка коректності результатів
    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
    
    print("Тести успішно пройдені!")

# Час виконання синхронної версії: 0.41 секунд.
