import { KafkaMessage } from 'kafkajs';

export interface ResyncMessage {
  type: 'research' | 'sentiment' | 'update';
  content: any;
  timestamp: string;
}

export async function handleResyncMessage(message: KafkaMessage) {
  try {
    const data = JSON.parse(message.value.toString()) as ResyncMessage;
    return data;
  } catch (error) {
    console.error('Error parsing Kafka message:', error);
    return null;
  }
}
