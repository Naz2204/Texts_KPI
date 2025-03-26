import mongoose from 'mongoose';
import { config } from 'dotenv';
import assert from 'assert';
config();
const MONGO_URI = process.env.MONGO_URI;
assert(MONGO_URI, 'No connection ulr provided');
await mongoose.connect(MONGO_URI).then(() => {
    console.log('Conencted to db');
});
