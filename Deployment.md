# Как развернуть систему логирования на стеке EFK
Допустим у вас есть некий проект, развернутый в контейнерах через docker-compose. В качестве примера рассмотрим абстрактное Flask-приложение, реализующее API для некоего сервиса.
Его docker-compose.yml можно найти среди файлов данного репозитория. За само приложение отвечает сервис api, а остальные - для системы логирования:
- _Elasticsearch_ - для хранения логов и работы с ними;
- _Kibana_ - графическая оболочка для Elasticsearch;
- _Fluent-bit_ - для сбора, преобразования/фильтрации и отправки в Elasticsearch.
Чтобы контейнер api отправлял свои логи во fluent-bit прописываем ему драйвер логирования "fluentd" с указанием куда и с каким тегом отправлять логи:
```yaml
    logging:
      driver: "fluentd"
      options:
        fluentd-address: localhost:24224
        tag: api.logs
```
А для fluent-bit указываем соответствующие настройки в файле конфигурации fluent-bit.conf:
```
[INPUT]
    name              forward
    Listen            0.0.0.0
    Port              24224
    Buffer_Chunk_Size 1M
    Buffer_Max_Size   6M
```
Здесь используется плагин forward, который служит для приема логов во fluent-bit. В описании сервиса fluent-bit в docker-compose необходимо открыть порты для этого плагина, а также пробросить конфиги в контейнер:
```yaml
  fluent-bit:
    image: fluent/fluent-bit
    ports:
      - 24224:24224
      - 24224:24224/udp
    volumes:
      - ./fluent-bit/fluent-bit.conf:/fluent-bit/etc/fluent-bit.conf
      - ./fluent-bit/parsers.conf:/fluent-bit/parsers/parsers.conf
```
Для отправки логов в elasticsearch в файле конфигурации fluent-bit.conf указываем блок OUTPUT:
```
[OUTPUT]
    Name  es
    Match *
    Host  127.0.0.1
    Port  9200
    Suppress_Type_Name On
```
Соответственно, elasticsearch должен быть развернут на указанном Host и Port.
Все, минимальные настройки сделаны, теперь при запуске docker compose up все логи, попадающие в stderr будут перенаправлены в elasticsearch и сохранены там.
Для настройки преобразования/фильтрации логов посредством fluetn-bit смотрите [инструкцию](https://github.com/Gena40/EFK-for-logs/blob/main/Configuration.md), в ней также приведен пример организации [такой](https://github.com/Gena40/EFK-for-logs/blob/main/Structure_of_logs.md) структуры логов с использованием библиотеки [loguru](https://github.com/Delgan/loguru).