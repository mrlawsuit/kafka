# Python-скрипт kafka

## Описание

Проект представяет собой простую демонстрацию работы распределенной системы обмена сообщениями kafka

## Стек

- Python 3.11
- Kafka
- Docker и Docker - Compose

## Уcтановка и настройка

1. Клонируйте репозиторий:

    bash
    `https://github.com/mrlawsuit/kafka`

2. Находясь в корневой дирректории проекта, выполните команду:
    
    bash
    `docker build -t my_kafka_client .`
    
    Это создаст docker-образ с именем my_kafka_client.

3. Запустите контейнеры zookeeper и kafka в фоновом режиме:

    bash `docker-compose up -d`

## Использование

1. Запустите отправку сообщений в топик hello_topic:
    
    bash `docker run --network host my_kafka_client produce --message 'Hello World!' --topic 'hello_topic' --kafka 'localhost:9092'`

2. Запустите консюмер для полдучения сообщений:

    bash `docker run --network host my_kafka_client consume --topic 'hello_topic' --kafka 'localhost:9092'`
