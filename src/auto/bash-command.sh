export OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true
export OTEL_EXPORTER_OTLP_ENDPOINT=0.0.0.0:4317
export OTEL_EXPORTER_OTLP_INSECURE=true
export OTEL_LOGS_EXPORTER=otlp
export OTEL_SERVICE_NAME=instru-log
opentelemetry-instrument python auto-log.py

