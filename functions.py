import time, json
from datetime import date


def save_log(text):
    file = open('log.txt', 'a')
    file.write(text + ' ' + time.ctime(
        time.time()) + '\n')
    file.close()


def get_spec(number_doc):
    # здесь в дальнейшем будет выдача выбранных направлений
    return ["01.03.02", "09.03.04", "10.03.01", "24.03.04"]


def logging_date(id):
    with open('stats.json', 'r') as fh:  # Здесь будем хранить дату последнего входа для каждого
        STATS = json.load(fh)
        # {id: 'date'} дата последнего входа
    if id not in STATS or STATS[id] != str(date.today()):
        STATS[id] = str(date.today())
        with open('stats.json', 'w') as fp:
            json.dump(STATS, fp)


def get_scores(id, SCORES):
    if id not in SCORES:
        return 'notin'
    A = ['Математика', 'Русский язык', 'Информатика', 'Физика', 'Химия', 'Обществознание', 'Иностранный язык',
         'Дополнительные баллы']
    res = ''
    end = ''
    s = SCORES[id][-1]  # Сумма математика + русский + достижения
    usl = True  # Останется тру если русский и математика есть
    B = []
    if s > 0:
        usl2 = True
    for i in range(8):
        x = SCORES[id][i]
        if x != 0:
            if i < 2:
                s += x
            elif 2 <= i < 7 and usl:
                B.append(s + x)
        else:
            if i < 2:
                usl = False
    if not usl:
        return 'nosum'
    else:
        return max(B)


def read_pr_bl():
    file = open('prbl.txt', 'r')
    PR_BL = {}
    for el in file:
        a, b = el.split()
        PR_BL[a] = int(b)
    file.close()
    return PR_BL
