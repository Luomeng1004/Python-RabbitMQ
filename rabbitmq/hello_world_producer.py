# coding=utf-8
import pika

credentials = pika.PlainCredentials("test", "test")
conn_param = pika.ConnectionParameters("123.57.242.222", credentials=credentials)

# 建立到代理服务器的连接
conn_broker = pika.BlockingConnection(conn_param)

# 获得信道
channel = conn_broker.channel()

# 声明交换器
channel.exchange_declare(exchange="hello-exchange", type="direct", passive=False, durable=True, auto_delete=False)

msg = "Python Rabbit MQ Test Message"
msg_props = pika.BasicProperties()
msg_props.content_type = "text/plain"

# 发布消息
channel.basic_publish(body=msg, exchange="hello-exchange", properties=msg_props, routing_key="hola")
