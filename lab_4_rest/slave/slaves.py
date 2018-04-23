import time
import os
from multiprocessing import Process
from slave import Slave


REPOSITORY_BASE_URL = 'http://192.168.182.5:8001/api/'
HTTP_404_NOT_FOUND = 404
NUMBER_OF_SLAVES = 10


def run_slave(url):
    slave = Slave(url)

    while True:
        task, status_code = slave.fetch_next_task()

        if status_code != HTTP_404_NOT_FOUND:
            slave.process_task(task)
            print()
        else:
            print()
            print('PID {}: No tasks found! Sleeping for 2 second...'
                  .format(os.getpid()))
            time.sleep(2)


if __name__ == '__main__':
    url = REPOSITORY_BASE_URL

    for _ in range(NUMBER_OF_SLAVES):
        p = Process(target=run_slave, args=(url,))
        p.start()

    p.join()
