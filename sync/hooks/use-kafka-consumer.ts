import { useState, useEffect } from 'react';
import { KafkaMessage } from '@/types/kafka';

export function useKafkaConsumer() {
  const [messages, setMessages] = useState<KafkaMessage[]>([]);
  const [isConnected, setIsConnected] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    console.log('🔄 Initializing EventSource connection...');
    const eventSource = new EventSource('/api/kafka');

    eventSource.onopen = () => {
      console.log('✅ EventSource connection opened');
      setIsConnected(true);
      setError(null);
    };

    eventSource.onmessage = (event) => {
      console.log('📨 Received message:', event.data);
      try {
        const message = JSON.parse(event.data);
        setMessages((prev) => [message, ...prev]);
      } catch (err) {
        console.error('❌ Error parsing message:', err);
        setError('Failed to parse message');
      }
    };

    eventSource.onerror = (err) => {
      console.error('❌ EventSource error:', err);
      setIsConnected(false);
      setError('Connection failed');

      // Attempt to reconnect after 5 seconds
      setTimeout(() => {
        console.log('🔄 Attempting to reconnect...');
        eventSource.close();
        new EventSource('/api/kafka');
      }, 5000);
    };

    return () => {
      console.log('🔄 Cleaning up EventSource connection');
      eventSource.close();
      setIsConnected(false);
    };
  }, []);

  return { messages, isConnected, error };
}
