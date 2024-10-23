import { NextResponse } from 'next/server';
import { kafka, consumer } from '@/lib/kafka';

export const runtime = 'edge';

export async function GET() {
  console.log('🔄 SSE connection attempt initiated');
  const responseStream = new TransformStream();
  const writer = responseStream.writable.getWriter();
  const encoder = new TextEncoder();

  try {
    console.log('📡 Attempting to connect to Kafka...');
    await consumer.connect();
    console.log('✅ Kafka connection established');

    console.log('🔔 Subscribing to topics...');
    await consumer.subscribe({
      topics: ['research_ideas', 'sentiment_analysis', 'resync'],
      fromBeginning: false,
    });
    console.log('✅ Successfully subscribed to topics');

    await consumer.run({
      eachMessage: async ({ topic, partition, message }) => {
        console.log(`📨 Received message from topic: ${topic}`);
        const update = {
          topic,
          value: message.value?.toString(),
          timestamp: message.timestamp,
        };

        await writer.write(
          encoder.encode(`data: ${JSON.stringify(update)}\n\n`)
        );
        console.log('✅ Message sent to client');
      },
    });
  } catch (error) {
    console.error('❌ Kafka consumer error:', error);
    await writer.close();
    return new NextResponse(
      JSON.stringify({ error: 'Failed to connect to Kafka' }),
      {
        status: 500,
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );
  }

  return new NextResponse(responseStream.readable, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      Connection: 'keep-alive',
    },
  });
}
