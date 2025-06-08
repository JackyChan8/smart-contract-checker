from pydantic import SecretStr
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    """
        Settings Class
    """

    # Script
    SECONDS_CHECK: int

    # Redis
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_USER: str
    REDIS_PASS: SecretStr

    # Telegram
    CHAT_ID: str
    BOT_TOKEN: SecretStr

    # Web3
    RPC_URL: str
    CURRENT_SYMBOL: str
    CONTRACT_ADDRESS: str

    def build_redis_url(self) -> str:
        """
            Build Redis URL

            :return str
        """
        return f'redis://{self.REDIS_USER}:{self.REDIS_PASS.get_secret_value()}@{self.REDIS_HOST}:{self.REDIS_PORT}/0'

    async def get_telegram_ids(self) -> list[str]:
        """
            Получения списком Telegram IDs
        """
        return self.TELEGRAM_IDS.split(' ')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = AppSettings()
