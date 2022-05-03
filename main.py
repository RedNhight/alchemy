import multiprocessing
from time import sleep
from handlers.login import *
from handlers.verify import *

from threading import Thread
from multiprocessing.dummy import Pool
# from multiprocessing import Pool


def main(accounts):
    mc = MailConfirmation(accounts)
    mc.login()
    try:
        mc.check_workable()
        mc.mail_confirm()
    except Exception as ex:
        mc.status = 'error'
    mc.save_status()
    mc.driver_close()


if __name__ == '__main__':
    threadings = input('Вы хотите запустить скрипт в многопоточном режиме?(Y/n): ')
    with open('accounts.txt', 'r') as account_list:
        accounts = account_list.readlines()
        if threadings == 'n' or threadings == 'N' or threadings == 'No' or threadings == 'no':
            for account in accounts:
                try:
                    main(account)
                except Exception as ex:
                    print(ex)
        elif threadings == 'y' or threadings == 'Y' or threadings == 'Yes' or threadings == 'yes':
            amount_of_threads = int(input('Введите количество потоков: '))
            with Pool(amount_of_threads) as pl:
                pl.map(main, accounts)
