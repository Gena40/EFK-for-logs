# Как настроить систему логирования на стеке EFK
## Итак, система логирования развернута, приступим к её более тонкой настройке.
## Предлагаю использовать библиотеку [loguru](https://github.com/Delgan/loguru), вместо стандартной питоновской logging. Она очень проста в применении и отлично подходит для формирования единой структуры логов.
## Кстати, на счет структуры логов: в [этом файле](https://github.com/Gena40/EFK-for-logs/blob/main/Structure_of_logs.md) приведён перечень полей, которых должно хватить для снабжения логов всей необходимой информацией.
## А вот так выглядит применение библиотеки loguru в нашем приложении на Flask:
```Python
from loguru import logger


logger.remove() # удаляем логгер, настроенный по умолчанию
# Устанавливаем в параметре extra сведения, общие для всех логов в данном модуле:
logger.configure(
    extra={
      "service_name": "API",
      "context": "-"
    },
)
log_format = '{level} {time} {extra[service_name]} {file} {function} "{message}" {extra[context]}'
# Добавляем свой обработчик:
logger.add(
    sys.stderr,  # куда выводить логи
    format=log_format,
    catch=True,  # чтобы приложение не падало из-за ошибок во fluent-bit
    backtrace=True,  # для отображения backtrace за пределами точки перехвата ошибки
)
```
