import time
def save_log(text):
    file = open('log.txt', 'a')
    if text == 'Работа бота начата.':
        print(text+' ')
    file.write(text + time.ctime(
        time.time()) + '\n')
    file.close()