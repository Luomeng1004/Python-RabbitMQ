# coding=utf-8
import pika

credentials = pika.PlainCredentials("test", "test")

conn_params = pika.ConnectionParameters("123.57.242.222", credentials=credentials)

# 建立到代理服务器的连接
conn_broker = pika.BlockingConnection(conn_params)

# 获得信道
channel = conn_broker.channel()

# 声明交换器
channel.exchange_declare(exchange="hello-exchange",
                         type="direct",
                         passive=False,
                         durable=True,
                         auto_delete=False)

# 声明队列
channel.queue_declare(queue="hello-queue")

channel.queue_bind(queue="hello-queue",
                   exchange="hello-exchange",
                   routing_key="hola")  # 通过"hola"将队列和交换器绑定起来


# 处理消息的函数
def msg_consumer(channel, method, header, body):
    # 确认消息
    channel.basic_ack(delivery_tag=method.delivery_tag)
    if body == "quit":

        # 停止消费并退出
        channel.basic_cancel(consumer_tag="hello-consumer")
        channel.stop_consuming()
    else:
        print body

    return


# 订阅消费者
channel.basic_consume(msg_consumer, queue="hello-queue", consumer_tag="hello-consumer")

# 开始消费
channel.start_consuming()
