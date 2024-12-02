import time
import argparse
from confluent_kafka import Producer, Consumer, KafkaError


def produce_message(kafka, topic, message):
    """Функция для отправки сообщения в Kafka"""
    producer = Producer({'bootstrap.servers': kafka})
    
    def delivery_report(err, msg):
        """Callback, вызываемый при успешной или неуспешной доставке сообщения"""
        if err is not None:
            print(f'Ошибка отправки сообщения: {err}')
        else:
            print(f'Сообщение доставлено в {msg.topic()} [{msg.partition()}]')

    try:
        # Запускаем бесконечный цикл для отправки сообщений
        while True:
            producer.produce(topic, value=message, callback=delivery_report)
            time.sleep(0.5)
            producer.flush()
    except Exception as e:
        print(f'Произошла ошибка при отправке сообщения: {e}')


def consume_messages(kafka, topic):
    """Функция для подписки на топик и чтения сообщений"""
    consumer = Consumer({
        'bootstrap.servers': kafka,
        'group.id': 'python-consumer-group',
        'auto.offset.reset': 'earliest'
    })

    consumer.subscribe([topic])  
    print(f'Подписка на топик "{topic}". Ожидание сообщений...')

    try:
        # Запускаем бесконечный цикл для чтения сообщений
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(f'Ошибка Kafka: {msg.error()}')
                    break
            print(f'Получено сообщение: {msg.value().decode("utf-8")}')
    except KeyboardInterrupt:
        print("Консумер завершен по запросу пользователя (Ctrl+C).")
    finally:
        consumer.close()



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Kafka Producer/Consumer Script")
    subparsers = parser.add_subparsers(dest='command', help="Команда")

    # Подкоманда для produce
    produce_parser = subparsers.add_parser('produce', help="Отправка сообщения в Kafka")
    produce_parser.add_argument('--message', required=True, help="Сообщение для отправки")
    produce_parser.add_argument('--topic', required=True, help="Название топика Kafka")
    produce_parser.add_argument('--kafka', required=True, help="Адрес Kafka Bootstrap-сервера (ip:port)")

    # Подкоманда для consume
    consume_parser = subparsers.add_parser('consume', help="Чтение сообщений из Kafka")
    consume_parser.add_argument('--topic', required=True, help="Название топика Kafka")
    consume_parser.add_argument('--kafka', required=True, help="Адрес Kafka Bootstrap-сервера (ip:port)")

    args = parser.parse_args()

    if args.command == 'produce':
        produce_message(args.kafka, args.topic, args.message)
    elif args.command == 'consume':
        consume_messages(args.kafka, args.topic)
    else:
        parser.print_help()
