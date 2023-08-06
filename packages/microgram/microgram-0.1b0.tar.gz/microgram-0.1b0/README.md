# Microgram

__English__ | [Russian](README-RU.md)

Microgram is easy to use and asynchronous module for working with [Telegram Bot API](https://core.telegram.org/bots/api), written on Micropython.

[Pypi project](https://pypi.org/project/microgram/)

----

### Example

Simple example of using Microgram features

```python
import network
import uasyncio
from microgram.bot import Bot
from microgram.dispatcher import Dispatcher, Router
from microgram.requests import Requests

nic = network.WLAN(network.STA_IF)
nic.active(True)
nic.connect("SomeNetwork", "SuperSecurePass123")


class TextFilter:
    def __init__(self, text):
        self.text = text

    def __call__(self, message, data):
        if message["text"] == self.text:
            return True
        return False


async def handler(message, kwargs):
    bot_ = kwargs.get("bot")
    text = kwargs.get("text")
    data = {"chat_id": message["from"]["id"], "text": text}
    await bot_.api_request("sendMessage", data)

if __name__ == "__main__":
    dp = Dispatcher()
    router = Router()
    bot = Bot("123456:ABCDEF")

    router.message.register(handler, TextFilter("/start"))
    dp.include_router(router)

    uasyncio.run(dp.start_polling(bot, text="Hi from microgram!\nHowdy?"))
```