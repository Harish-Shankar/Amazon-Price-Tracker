import time
import bs4
import requests
import smtplib


priceList = []
SENDER_EMAIL = ""
SENDER_PASSWORD = ""
RECEIVER_EMAIL = ""


def check_price():
    URL = ""

    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"}

    source = requests.get(URL, headers=headers)
    sourceParsed = bs4.BeautifulSoup(source.content, "html.parser")

    print(sourceParsed.prettify)

    price = sourceParsed.find(id="priceblock_ourprice").get_text()
    price = float(price.replace(",", "").replace("₹", ""))
    priceList.append(price)

    return price


def send_email(message, senderEmail, senderPassword, receiverEmail):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(senderEmail, senderPassword)
    s.sendmail(senderEmail, receiverEmail, message)
    s.quit()


def price_decrease(priceList):
    if priceList[-1] < priceList[-2]:
        return True
    else:
        return False


count = 1
while True:
    current_price = check_price()
    if count > 1:
        flag = price_decrease(priceList)
        if flag:
            decrease = priceList[-1] - priceList[-2]
            message = f"The price decrease by {decrease} rupees."

            send_email(message, SENDER_EMAIL, SENDER_PASSWORD, RECEIVER_EMAIL)
    time.sleep(43000)
    count += 1
