const amqp = require('amqplib');

async function send() {
  const connection = await amqp.connect('amqp://localhost');
  const channel = await connection.createChannel();

  const queue = 'sintomas';
  const msg = JSON.stringify({ teste: 'mensagem de teste' });

  await channel.assertQueue(queue, { durable: false });
  channel.sendToQueue(queue, Buffer.from(msg));

  console.log("Mensagem enviada para a fila:", queue);

  setTimeout(() => {
    connection.close();
    process.exit(0);
  }, 500);
}

send().catch(console.error);
