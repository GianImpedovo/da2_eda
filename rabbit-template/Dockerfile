FROM rabbitmq:4-management

# Copiar configuración y definitions al contenedor
COPY rabbit.conf /etc/rabbitmq/rabbitmq.conf
COPY definitions.json /etc/rabbitmq/definitions.json

# Habilitar definiciones
ENV RABBITMQ_SERVER_ADDITIONAL_ERL_ARGS="-rabbitmq_management load_definitions \"/etc/rabbitmq/definitions.json\""

# Habilitar plugins necesarios
RUN rabbitmq-plugins enable --offline rabbitmq_management rabbitmq_peer_discovery_aws rabbitmq_prometheus
