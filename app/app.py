import os
from flask import Flask
import redis


app = Flask(__name__)
port = int(os.environ.get("PORT", 5000))
r_server=redis.StrictRedis(host='redis',port=6379, decode_responses=True, charset="utf-8")

def get_fib(number):
    if (number == 0) or (number == 1):
        return number
    return get_fib(number-1) + get_fib(number-2)

@app.route('/', methods=['GET'])
def salut():
    return 'Чтобы получить К-ое значение Фибоначчи, необходимо проставить число (Х) в адресной строке после порта (127.0.0.1:8081/Х)'

@app.route('/<k>', methods=['GET'])
def fib_number(k):
    number = int(k)
    q = r_server.get(number)
    if q:
        return '{} Значение Фибонначи = {} - (Значение кэша)'.format(number, q)
    else:
        result = get_fib(number)
        r_server.set(number,result)
    return '{} Значение Фибонначи = {}'.format(number,result)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=port)