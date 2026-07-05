const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export type EventHandler<T = unknown> = (data: T) => void;

export class EventStreamClient {
  private eventSource: EventSource | null = null;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  private listeners: Map<string, EventHandler<any>[]> = new Map();

  connect() {
    if (this.eventSource) return;

    this.eventSource = new EventSource(`${API_BASE_URL}/events`);

    this.eventSource.onmessage = (event) => {
      try {
        const payload = JSON.parse(event.data);
        const { type, data } = payload;
        this.emit(type, data);
      } catch (err) {
        console.error("Failed to parse SSE message", err);
      }
    };

    this.eventSource.onerror = (err) => {
      console.error("SSE connection error, attempting to reconnect...", err);
      // EventSource auto-reconnects by default, but we could add custom logic here
    };
  }

  disconnect() {
    if (this.eventSource) {
      this.eventSource.close();
      this.eventSource = null;
    }
  }

  on<T>(eventType: string, handler: EventHandler<T>) {
    if (!this.listeners.has(eventType)) {
      this.listeners.set(eventType, []);
    }
    this.listeners.get(eventType)!.push(handler);
    
    // Auto connect if not connected
    if (!this.eventSource) {
      this.connect();
    }
    
    return () => this.off(eventType, handler); // Returns cleanup function
  }

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  off(eventType: string, handler: EventHandler<any>) {
    const handlers = this.listeners.get(eventType);
    if (handlers) {
      this.listeners.set(
        eventType,
        handlers.filter((h) => h !== handler)
      );
    }
  }

  private emit(eventType: string, data: unknown) {
    const handlers = this.listeners.get(eventType) || [];
    handlers.forEach((handler) => handler(data));
  }
}

// Singleton instance
export const eventStream = new EventStreamClient();
