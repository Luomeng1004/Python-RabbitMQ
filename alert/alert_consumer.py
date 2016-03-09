import json
import pika


def send_email(recipients, subject, message):
    """E-mail generator for received alerts."""
    headers = ("From: %s\r\nTo: \r\nDate: \r\n" +
               "Subject: %s\r\n\r\n") % ("alerts@ourcompany.com", subject)

    print message

    #smtp_server = smtplib.SMTP()
    #smtp_server.connect("mail.ourcompany.com", 25)
    #smtp_server.sendmail("alerts@ourcompany.com", recipients, headers + str(message))
    #smtp_server.close()


def critical_notify(channel, method, header, body):
    """Sends CRITICAL alerts to administrators via e-mail."""
    EMAIL_RECIPS = ["ops.team@ourcompany.com", ]

    message = json.loads(body)

    send_email(EMAIL_RECIPS, "CRITIAL ALERT", message)
    print ("Sent alert via e-mail! Alert Text: %s " +
           "Recipients: %s") % (str(message), str(EMAIL_RECIPS))

    channel.basic_ack(delivery_tag=method.delivery_tag)


def rate_limit_notify(channel, method, header, body):
    """Sends the message to the administrators via e-mail."""
    EMAIL_RECIPS = ["api.team@ourcompany.com", ]
    message = json.loads(body)

    send_email(EMAIL_RECIPS, "RATE LIMIT ALERT!", message)

    print ("Sent alert via e-mail! Alert Text: %s " +
           "Recipients: %s") % (str(message), str(EMAIL_RECIPS))

    channel.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == "__main__":
    AMQP_SERVER = "123.57.242.222"
    AMQP_USER = "alert_user"
    AMQP_PASS = "alertme"
    AMQP_VHOST = "/"
    AMQP_EXCHANGE = "alerts"

    creds_broker = pika.PlainCredentials(AMQP_USER, AMQP_PASS)
    conn_params = pika.ConnectionParameters(AMQP_SERVER, virtual_host=AMQP_VHOST, credentials=creds_broker)

    conn_broker = pika.BlockingConnection(conn_params)

    channel = conn_broker.channel()
    channel.exchange_declare(exchange=AMQP_EXCHANGE, type="topic", auto_delete=False)

    channel.queue_declare(queue="critical", auto_delete=False)
    channel.queue_bind(queue="critical", exchange="alerts", routing_key="critical.*")

    channel.queue_declare(queue="rate_limit", auto_delete=False)
    channel.queue_bind(queue="rate_limit", exchange="alerts", routing_key="*.rate_limit")

    channel.basic_consume(critical_notify, queue="critical", no_ack=False, consumer_tag="critical")

    channel.basic_consume(rate_limit_notify, queue="rate_limit", no_ack=False, consumer_tag="rate_limit")

    print "Ready for alerts!"

    channel.start_consuming()
