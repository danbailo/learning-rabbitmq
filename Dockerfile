FROM rabbitmq:3.13.0-management

COPY plugins/ /opt/rabbitmq/plugins/

RUN rabbitmq-plugins enable rabbitmq_delayed_message_exchange