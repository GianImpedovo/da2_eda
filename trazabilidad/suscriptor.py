import json
import pika

credentials = pika.PlainCredentials('user_emergencias', 'pass_emergencias')
parameters = pika.ConnectionParameters(
    host='3.85.212.112',
    port=5672,
    virtual_host='/',
    credentials=credentials
)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()

queues = [
    'emergencias_def',
    'emergencias_dlx',

]


def callback(ch, method, properties, body):
    trace_data = {}

    try:
        msg_body = json.loads(body.decode())
        if not isinstance(msg_body, dict):
            msg_body = {}
    except Exception:
        msg_body = {}

    trace_data["user"] = msg_body.get("user", "guest")
    trace_data["routing_keys"] = msg_body.get("routing_keys", [])

    headers = getattr(properties, "headers", {}) or {}
    trace_data["exchange_name"] = headers.get("exchange_name")
    trace_data["node"] = headers.get("node")
    trace_data["state"] = headers.get("state")
    trace_data["subscriber"] = method.routing_key
    trace_data["publisher"] = trace_data["routing_keys"][0].split(".")[0] if trace_data["routing_keys"] else None

    if properties.headers and 'x-death' in properties.headers:
        death_info = properties.headers['x-death'][0]
        trace_data["original_routing_key"] = death_info.get('routing-keys', [None])[0]
        trace_data["original_queue"] = death_info.get('queue')
        trace_data["original_exchange"] = death_info.get('exchange')
        trace_data["death_reason"] = death_info.get('reason')
        trace_data["death_count"] = death_info.get('count', 0)
        trace_data["is_dead_letter"] = True

        print("MENSAJE EN DLX:")
        print(f"   Routing key original: {trace_data['original_routing_key']}")
        print(f"   Queue original: {trace_data['original_queue']}")
        print(f"   Razón: {trace_data['death_reason']}")
        print(f"   Intentos: {trace_data['death_count']}")
    else:
        trace_data["is_dead_letter"] = False

    print(json.dumps(trace_data, indent=2, default=str))
    print("─────────────────────────────")


for q in queues:
    channel.basic_consume(
        queue=q,
        on_message_callback=callback,
        auto_ack=True
    )

print(f"[*] Esperando mensajes en {len(queues)} colas. Ctrl+C para salir")
channel.start_consuming()
