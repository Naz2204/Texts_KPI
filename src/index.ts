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

const task1 = async () => {
  const data = await Tag.find();
  console.log(data);
};

const task2 = async () => {
  const data = await Tag.find({ name: 'Fiction' });
  console.log(data);
};

const task3 = async () => {
  const data = await Document.find(
    { 'metadata.size': { $gt: 120000 } },
    { body: 0 }
  );
  console.log(data);
};

const task4 = async () => {
  const data = await Document.find({}, { metadata: 1, createdAt: 1, _id: 0 });
  console.log(data);
};

const task5 = async () => {
  const data = await Topic.find({ isRoot: true });
  console.log(data);
};

const task6 = async () => {
  const data = await Topic.find({ name: { $in: ['TOPIC1', 'TOPIC2'] } });
  console.log(data);
};

const task7 = async () => {
  const data = await Document.find({}, { body: 0 }).sort({
    'metadata.size': 'asc'
  });
  console.log(data);
};

const task8 = async () => {
  const data = await Tag.countDocuments({ name: 'Fantasy' });
  console.log(data);
};

const task9 = async () => {
  const data = await Topic.aggregate([
    { $group: { _id: '$parent', count: { $sum: 1 } } },
    {
      $lookup: {
        from: 'topics',
        localField: '_id',
        foreignField: '_id',
        as: 'parent'
      }
    },
    {
      $project: {
        _id: 0,
        parentName: '$parent.name',
        count: 1
      }
    }
  ]).exec();
  console.log(data);
};

const task10 = async () => {
  const data = await Document.aggregate([
    {
      $group: {
        _id: null,
        averageSize: { $avg: '$metadata.size' }
      }
    }
  ]).exec();
  console.log(data);
};
