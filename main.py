
import requests
from logger import Logger
import services
import argparse
import time
import schedule
from ResponseTimeError import ResponseTimeError
from logger import Logger
from telegramBot import TelegramBot


logger = Logger()
def main(path):
    service = services.Services(path)
    services_list = service.read_confid()
    for service in services_list['services']:
        url = service['url']
        body = service['body']
        headers = service.get('headers', {})
        #execute_time = timeit.timeit()
        try:
            response = requests.post(url, json=body, headers=headers)
            response.raise_for_status()
            logger.info(f"URL: {url}, Код ответа: {response.status_code}, Время отклика: {response.elapsed.total_seconds():.2f} секунд")
            if response.elapsed.total_seconds() > 2:
                raise ResponseTimeError("Время отклика превышает 2 секунды", response.elapsed.total_seconds(), url)
        except requests.exceptions.HTTPError as err:
            logger.error(f"HTTP ошибка при запросе к {url}: {err}, Код ответа: {response.status_code}")
            #вызвать телеграм бота выскакивает если не 200 код
            msg = f"Сбой в работе сервиса: {service}\nКод: {response.status_code}\nВремя отклика: {response.elapsed.total_seconds()}"
            TelegramBot.send_error_telegram(msg)
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка при запросе к {url}: {e}")
            print(f"Ошибка запроса: {e}")
        except ResponseTimeError as e:
            msg = f"Превышено время ожидания от сервиса: {service}\nКод: {response.status_code}\nВремя отклика: {response.elapsed.total_seconds()}"
            TelegramBot.send_error_telegram(msg)
            # вызвать телеграм бота это если больше 2 секунд




if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('path', type=str, help='Путь к файлу с конфигом')
    args = args.parse_args()
    schedule.every().hour.at(":21").do(main, args.path)
    while True:
        schedule.run_pending()
        time.sleep(10)