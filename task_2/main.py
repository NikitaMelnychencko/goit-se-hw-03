# Напишіть реалізацію функції factorize, яка приймає список чисел та повертає список чисел, на які числа з вхідного списку поділяються без залишку.
# Реалізуйте синхронну версію та виміряйте час виконання.
# Потім покращіть продуктивність вашої функції, реалізувавши використання кількох ядер процесора для паралельних обчислень і замірьте час виконання знову.
# Для визначення кількості ядер на машині використовуйте функцію cpu_count() з пакета multiprocessing
# Для перевірки правильності роботи алгоритму самої функції можете скористатися тестом:
from multiprocessing import Pool, cpu_count
from time import time
import logging

def factorize(*number):
    results = []
    for num in number:
        divisors = []
        for i in range(1, num + 1):
            if num % i == 0:
                divisors.append(i)
        results.append(divisors)
    return results


def factorize_single(num):
  return [i for i in range(1, num + 1) if num % i == 0]


def divisors_in_range(args):
    number, start, stop = args
    return [i for i in range(start, stop) if number % i == 0]

def factorize_parallel(*numbers, workers):
    tasks = []
    counts = []
    for number in numbers:
        chunk = (number + workers - 1) // workers
        count = 0
        for start in range(1, number + 1, chunk):
            stop = min(start + chunk, number + 1)
            print(f"Stop: {stop}")
            tasks.append((number, start, stop))
            count += 1
        counts.append(count)
    with Pool(workers) as pool:
        parts = pool.map(divisors_in_range, tasks)
    results = []
    offset = 0
    for count in counts:
        divisors = []
        for part in parts[offset:offset + count]:
            divisors.extend(part)
        results.append(divisors)
        offset += count
    return results

if __name__ == "__main__":
  logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')
  start_time = time()
  a, b, c, d  = factorize(128, 255, 99999, 10651060)
  assert a == [1, 2, 4, 8, 16, 32, 64, 128]
  assert b == [1, 3, 5, 15, 17, 51, 85, 255]
  assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
  assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
  logging.info(f"Time taken: {time() - start_time} seconds")

  timer = time()
  values = [128, 255, 99999, 10651060]
  with Pool(4) as pool:
    a, b, c, d = pool.map(factorize_single, values)
    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
  logging.info(f"Done by {4} processes: {round(time() - timer, 4)} seconds")


  timer = time()
  values = [128, 255, 99999, 10651060]
  with Pool(cpu_count()) as pool:
    a, b, c, d = pool.map(factorize_single, values)
    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
  logging.info(f"Done by {cpu_count()} processes: {round(time() - timer, 4)} seconds")

  workers = cpu_count()
  timer = time()
  a, b, c, d = factorize_parallel(128, 255, 99999, 10651060, workers=workers)
  assert a == [1, 2, 4, 8, 16, 32, 64, 128]
  assert b == [1, 3, 5, 15, 17, 51, 85, 255]
  assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
  assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
  logging.info(f"Done by ranged {workers} processes: {round(time() - timer, 4)} seconds")
