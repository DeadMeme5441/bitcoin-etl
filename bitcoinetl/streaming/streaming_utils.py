from blockchainetl.jobs.exporters.console_item_exporter import ConsoleItemExporter
from blockchainetl.jobs.exporters.kafka_exporter import KafkaItemExporter


def get_item_exporter(output):
    if output is not None and output.startswith("kafka"):
        item_exporter = KafkaItemExporter(
            output,
            item_type_to_topic_mapping={
                "block": "blocks",
                "transaction": "transactions",
            },
        )

    elif output is not None and output.startswith("google.pubsub://"):
        from blockchainetl.jobs.exporters.google_pubsub_item_exporter import (
            GooglePubSubItemExporter,
        )

        item_exporter = GooglePubSubItemExporter(
            item_type_to_topic_mapping={
                "block": output + ".blocks",
                "transaction": output + ".transactions",
            },
            message_attributes=("item_id",),
        )
    else:
        item_exporter = ConsoleItemExporter()

    return item_exporter
