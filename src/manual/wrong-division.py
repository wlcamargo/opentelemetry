from logging import INFO, Filter
from loguru import logger

from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import get_tracer

# Configure OpenTelemetry resources and exporters
resource = Resource({SERVICE_NAME: 'wrong-division'})
provider = LoggerProvider(resource=resource)
processor = BatchLogRecordProcessor(OTLPLogExporter(endpoint='0.0.0.0:4317', insecure=True))
provider.add_log_record_processor(processor)
set_logger_provider(provider)

# Configure tracing
trace_provider = TracerProvider(resource=resource)
trace.set_tracer_provider(trace_provider)
span_processor = BatchSpanProcessor(OTLPSpanExporter(endpoint='0.0.0.0:4317', insecure=True))
trace_provider.add_span_processor(span_processor)

# Create a custom filter to remove 'extra' fields from logs
class RemoveExtra(Filter):
    def filter(self, record):
        del record.extra
        return True

handler = LoggingHandler(level=INFO, logger_provider=provider)
handler.addFilter(RemoveExtra())

# Add the OpenTelemetry Logging Handler to Loguru
logger.add(handler, level='DEBUG', serialize=True)

# Create a tracer instance
tracer = get_tracer(__name__)

@logger.catch
def divide():
    with tracer.start_as_current_span("divide-operation"):
        logger.info("Starting the divide operation")
        
        # Simulate an error
        1 / 0


# Run the functions
divide()