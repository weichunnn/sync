import { Kafka } from 'kafkajs';

const KAFKA_CONFIG = {
  BOOTSTRAP_SERVERS: process.env.CONFLUENT_BOOTSTRAP_SERVERS,
  API_KEY: process.env.CONFLUENT_API_KEY,
  API_SECRET: process.env.CONFLUENT_API_SECRET,
};

export const kafka = new Kafka({
  clientId: 'sync-dashboard',
  brokers: [KAFKA_CONFIG.BOOTSTRAP_SERVERS],
  ssl: true,
  sasl: {
    mechanism: 'plain',
    username: KAFKA_CONFIG.API_KEY,
    password: KAFKA_CONFIG.API_SECRET,
  },
  // Disable compression for Edge compatibility
  compression: null,
});

export const consumer = kafka.consumer({
  groupId: 'sync-dashboard-group',
  // Confluent Cloud specific configurations
  sessionTimeout: 45000,
  heartbeatInterval: 15000,
  maxWaitTimeInMs: 5000,
  // Retry configurations
  retry: {
    initialRetryTime: 100,
    retries: 8,
  },
});
