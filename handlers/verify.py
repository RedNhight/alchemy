from .login import *
from imap_tools import MailBox, A


class MailConfirmation(Alchemy):
    def mail_confirm(self):
        messages = []
        with MailBox('imap.rambler.ru').login(self.data[0], self.data[1]) as mailbox:
            for msg in mailbox.fetch(A(all=True)):
                messages.append(msg)

            for msg in messages[-1:]:
                sender = msg.from_
                print(sender)
                if sender == 'hello@alchemy.com':
                    body = msg.text
                    print(body)
                    bd = body.split(' ')
                    for b in bd:
                        if 'http' in b:
                            self.driver.get(b)


if __name__ == '__main__':
    pass
