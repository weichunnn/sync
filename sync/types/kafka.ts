export interface KafkaMessage {
  topic: string;
  value: string;
  timestamp: string;
}

export interface ResyncMessage {
  type: 'research' | 'sentiment' | 'update';
  content: any;
  timestamp: string;
}
