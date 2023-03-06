import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from api import Api


def main(num):
    return Api.get('future/read/sql/', {"num": num})


if __name__ == '__main__':
    start_td = time.time()
    with ThreadPoolExecutor() as pool:
        futures = [pool.submit(main, num) for num in range(1, 5)]
        for future in as_completed(futures):  # as_completed后的结果顺序是不固定的
            future.result()
            print(1)
    # main(2)
