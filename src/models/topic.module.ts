import mongoose from 'mongoose';

const topicSchema = new mongoose.Schema(
  {
    name: {
      type: String,
      required: [true, 'Topic must have a name'],
      unique: true
    },
    parent: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'topics'
    },
    isRoot: {
      type: Boolean,
      default: false
    }
  },
  { timestamps: true }
);

topicSchema.pre('save', async function (next) {
  const existingTopic = await mongoose.models.Topic.findOne({
    name: this.name
  });
  if (existingTopic) return next(new Error('Topic name must be unique'));

  if (this.parent) {
    const topicParent = await mongoose.models.Topic.findById(this.parent);
    if (!topicParent)
      return next(new Error(`Topic with id ${this.parent} does not exist`));
  } else {
    this.isRoot = true;
  }

  next();
});

export default mongoose.model('Topic', topicSchema);
