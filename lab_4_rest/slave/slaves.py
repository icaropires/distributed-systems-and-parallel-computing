from slave import Slave


REPOSITORY_BASE_URL = 'http://192.168.182.5:8001/api/'
HTTP_404_NOT_FOUND = 404


if __name__ == '__main__':
    url = REPOSITORY_BASE_URL
    slave = Slave(url)

    while True:
        task, status_code = slave.fetch_next_task()

        if status_code != HTTP_404_NOT_FOUND:
            slave.process_task(task)
            print()
        else:
            print('Stopping slave, no more tasks.')
            break
