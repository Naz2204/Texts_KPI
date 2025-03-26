import mongoose from 'mongoose';
import { config } from 'dotenv';
import assert from 'assert';
import Document from './models/document.model.js';
import Topic from './models/topic.module.js';
import Tag from './models/tag.module.js';

config();

const MONGO_URI = process.env.MONGO_URI;
assert(MONGO_URI, 'No connection ulr provided');

await mongoose.connect(MONGO_URI, { autoIndex: true }).then(() => {
  console.log('Conencted to db...');
});

await Document.create({ body: 'BODYA', metadata: { a: 'a', b: 'b', c: 1 } });
await Tag.create({ name: 'Tagington' });
