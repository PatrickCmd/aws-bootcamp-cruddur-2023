import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http';
import { WebTracerProvider, BatchSpanProcessor } from '@opentelemetry/sdk-trace-web';
import { ConsoleSpanExporter, SimpleSpanProcessor } from '@opentelemetry/sdk-trace-base';
import { registerInstrumentations } from '@opentelemetry/instrumentation';
import { FetchInstrumentation } from '@opentelemetry/instrumentation-fetch';
// import { HttpInstrumentation } from '@opentelemetry/instrumentation-http';
import { ZoneContextManager } from '@opentelemetry/context-zone';
const { Resource } = require('@opentelemetry/resources');
const { SemanticResourceAttributes } = require('@opentelemetry/semantic-conventions');

const exporter = new OTLPTraceExporter({
    // url: 'https://api.honeycomb.io:443/v1/traces'
  });
const tracerProvider = new WebTracerProvider({
  resource: new Resource({
    [SemanticResourceAttributes.SERVICE_NAME]: 'cruddur-frontend-react',
  }),
});
const consoleExporter = new ConsoleSpanExporter();
const consoleSpanProcessor = new SimpleSpanProcessor(consoleExporter);
tracerProvider.addSpanProcessor(consoleSpanProcessor);
tracerProvider.addSpanProcessor(new BatchSpanProcessor(exporter));

tracerProvider.register({
  contextManager: new ZoneContextManager()  // Zone is required to keep async calls in the same trace
});

const fetchInstrumentation = new FetchInstrumentation({
    propagateTraceHeaderCorsUrls: [
        `${process.env.REACT_APP_BACKEND_URL}/api/.+/g`, //Regex to match your backend urls.
     ]
});
// const httpInstrumentation = new HttpInstrumentation({});

fetchInstrumentation.setTracerProvider(tracerProvider);

// Registering instrumentations
// add auto-instrumentation
registerInstrumentations({
  instrumentations: [
    fetchInstrumentation,
    // httpInstrumentation,
  ],
});

export default function TraceProvider({ children }) {
  return (
    <>
      {children}
    </>
  );
}