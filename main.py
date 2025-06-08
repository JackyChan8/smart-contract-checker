import time
import redis
import requests
from web3 import Web3


from src.logger import logger
from src.config import settings


class CheckSmartContractAddress:
    """
        Проверка Контракт Адреса
    """

    def __init__(self) -> None:
        """
            Инициализация класса
        """

        self.tg_chat_id = settings.CHAT_ID
        self.tg_bot_token = settings.BOT_TOKEN.get_secret_value()

        self.rpc_url = settings.RPC_URL
        self.current_symbol = settings.CURRENT_SYMBOL
        self.contract_address = settings.CONTRACT_ADDRESS
        self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))

        self.cache = redis.from_url(settings.build_redis_url())
        self.cache_key = f"balance:{self.contract_address.lower()}"

        self.poll_interval_seconds = 10


    def send_telegram(self, text: str) -> None:
        """
            Отправка сообщения в Телеграм
        """

        url = f'https://api.telegram.org/bot{self.tg_bot_token}/sendMessage'
        payload = {
            'text': text,
            'chat_id': self.tg_chat_id,
        }
        resp = requests.post(url, json=payload)
        if not resp.ok:
            logger.error("Ошибка при отправке в Telegram:", resp.text)


    def get_balance_wei(self) -> int:
        """
            Получения баланса
        """

        return self.w3.eth.get_balance(self.contract_address)

    def main(self) -> None:
        """
            Функция запуска
        """

        last = self.cache.get(self.cache_key)
        last = int(last) if last and last.isdigit() else 0

        logger.info(f"Начинаем слежение за {self.contract_address}, текущий баланс в кэше: {self.w3.from_wei(last,'ether')} {self.current_symbol}")

        while True:
            try:
                current = self.get_balance_wei()
                logger.info(f'Текущий баланс: {current}')
                if current != last:
                    eth_old = self.w3.from_wei(last,    "ether")
                    eth_new = self.w3.from_wei(current, "ether")
                    msg = (
                        f"⚡️ Баланс изменился для {self.contract_address}:\n"
                        f"▶️ Было: {eth_old} {self.current_symbol}\n"
                        f"▶️ Стало: {eth_new} {self.current_symbol}"
                    )
                    self.send_telegram(msg)
                    # обновляем кэш
                    self.cache.set(self.cache_key, str(current))
                    last = current
                # иначе — без изменений
            except Exception as e:
                logger.error(f"Ошибка при проверке баланса: {e}")

            time.sleep(settings.SECONDS_CHECK)


if __name__ == '__main__':
    logger.info('✅ Чекер Успешно Запущен')
    check_smart_contract = CheckSmartContractAddress()
    check_smart_contract.main()
    logger.info('✅ Чекер Успешно Завершен')
