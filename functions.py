import time
def save_log(text):
    file = open('log.txt', 'a')
    print(text)
    file.write(text + time.ctime(
        time.time()) + '\n')
    file.close()