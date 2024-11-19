import asyncio
import json
import logging
import ssl
from abc import ABC, abstractmethod

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from aiokafka.errors import KafkaError, NoBrokersAvailable, KafkaConnectionError

from config.settings.base import (
    KAFKA_BROKER_URLS,
    KAFKA_GROUP_ID,
    KAFKA_SASL_PASSWORD,
    KAFKA_SASL_USERNAME,
)


# Main Section
class KafkaConsumerService(ABC):
    """
    KafkaConsumerService는 Kafka 토픽으로부터 메시지를 비동기적으로 소비하기 위한 기본 클래스를 제공합니다.
    이 클래스의 핵심 기능은 consume_messages() 메서드이며, 이를 통해 Kafka에서 전달되는 메시지를 처리할 수 있습니다.

    하위 클래스에서는 process_message(msg) 메서드를 구현하여, 특정 메시지 처리 로직을 정의해야 합니다.
    """

    def __init__(self, topic):
        self.topic = topic
        self.group_id = KAFKA_GROUP_ID
        self.servers = KAFKA_BROKER_URLS
        self.consumer = None

    def create_ssl_context(self):
        """
        Kafka와의 SSL 연결을 위한 SSL 컨텍스트를 생성합니다.
        """
        _ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        _ssl_context.options |= ssl.OP_NO_SSLv2
        _ssl_context.options |= ssl.OP_NO_SSLv3
        _ssl_context.check_hostname = True
        _ssl_context.verify_mode = ssl.CERT_REQUIRED
        _ssl_context.load_verify_locations(cafile="keys/ssl_key.pem")
        _ssl_context.load_default_certs(ssl.Purpose.CLIENT_AUTH)
        return _ssl_context

    async def start_consumer(self):
        """
        Kafka Consumer를 초기화하고 시작합니다.
        """
        self.consumer = AIOKafkaConsumer(
            self.topic,
            bootstrap_servers=self.servers,
            group_id=self.group_id,
            security_protocol="SASL_SSL",
            sasl_mechanism="SCRAM-SHA-512",
            sasl_plain_username=KAFKA_SASL_USERNAME,
            sasl_plain_password=KAFKA_SASL_PASSWORD,
            auto_offset_reset="earliest",
            ssl_context=self.create_ssl_context(),
        )
        await self.consumer.start()

    async def stop_consumer(self):
        """
        Kafka Consumer를 안전하게 종료합니다.
        """
        if self.consumer:
            await self.consumer.stop()

    async def consume_messages(self):
        """
        Kafka 토픽에서 메시지를 소비하고,
        하위 클래스에서 정의된 process_message()를 통해 처리합니다.
        """
        while True:
            try:
                await self.start_consumer()
                if not self.consumer:
                    raise Exception("Consumer is not initialized")

                async for msg in self.consumer:
                    try:
                        print(f"{self.topic} Topic's Value : {msg}")
                        await self.process_message(msg)
                    except Exception as e:
                        print(f"An error occurred while processing message: {e}")
            except (KafkaError, NoBrokersAvailable, KafkaConnectionError) as e:
                logging.error(f"Kafka connection error: {e}")
                await self.reconnect()
            finally:
                await self.stop_consumer()

    async def reconnect(self):
        """
        Kafka와의 연결이 끊어졌을 때 재연결을 시도합니다.
        """
        max_retries = 5
        retry_count = 0
        while retry_count < max_retries:
            try:
                await self.start_consumer()
                logging.info("Reconnected to Kafka broker successfully.")
                break
            except (KafkaError, NoBrokersAvailable, KafkaConnectionError) as e:
                retry_count += 1
                logging.error(f"Retry {retry_count}/{max_retries}: Unable to reconnect to Kafka. Error: {e}")
                await asyncio.sleep(2**retry_count)

        if retry_count == max_retries:
            logging.error("Failed to reconnect to Kafka after multiple attempts.")

    @abstractmethod
    async def process_message(self, msg):
        """
        이 메서드는 하위 클래스에서 구현되어야 합니다.
        이곳에서 메시지를 어떻게 처리할지 정의하십시오.
        """
        pass


class KafkaProducerService:
    def __init__(self, topic: str):
        self.topic = topic
        self.servers = KAFKA_BROKER_URLS
        self.producer = None
        self.ssl_context = self.create_ssl_context()

    def create_ssl_context(self):
        """
        Kafka와의 SSL 연결을 위한 SSL 컨텍스트를 생성합니다.
        """
        _ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        _ssl_context.options |= ssl.OP_NO_SSLv2
        _ssl_context.options |= ssl.OP_NO_SSLv3
        _ssl_context.check_hostname = True
        _ssl_context.verify_mode = ssl.CERT_REQUIRED
        _ssl_context.load_verify_locations(cafile="keys/ssl_key.pem")
        _ssl_context.load_default_certs(ssl.Purpose.CLIENT_AUTH)
        return _ssl_context

    async def start_producer(self):
        """
        Kafka Producer를 초기화하고 시작합니다.
        """
        self.producer = AIOKafkaProducer(
            bootstrap_servers=KAFKA_BROKER_URLS,
            security_protocol="SASL_SSL",
            sasl_mechanism="SCRAM-SHA-512",
            sasl_plain_username=KAFKA_SASL_USERNAME,
            sasl_plain_password=KAFKA_SASL_PASSWORD,
            ssl_context=self.create_ssl_context(),
        )
        await self.producer.start()

    async def send_messages(self, messages: list):
        """
        메시지를 Kafka 토픽으로 전송합니다.
        """
        await self.start_producer()
        if not self.producer:
            raise Exception("Producer has not been started. Call start_producer() first.")

        try:
            for message in messages:
                value = json.dumps(message).encode("utf-8")
                await self.producer.send_and_wait(self.topic, value=value)
                print(f"sent: {value}")
        finally:
            await self.producer.stop()

    async def stop_producer(self):
        """
        Kafka Producer를 중지합니다.
        """
        if self.producer:
            await self.producer.stop()
