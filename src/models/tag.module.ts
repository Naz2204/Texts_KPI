import mongoose from 'mongoose';

const tagSchema = new mongoose.Schema(
  {
    name: {
      type: String,
      required: [true, 'Tag must have a name'],
      unique: true
    }
  },
  { timestamps: true }
);

tagSchema.pre('save', async function (next) {
  const existingTag = await mongoose.models.Tag.findOne({
    name: this.name
  });
  if (existingTag) return next(new Error('Tag name must be unique'));

  next();
});

export default mongoose.model('Tag', tagSchema);
