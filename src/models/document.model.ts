import mongoose from 'mongoose';

const documentSchema = new mongoose.Schema(
  {
    body: {
      type: String
    },
    metadata: { type: JSON }
  },
  { timestamps: true }
);

export default mongoose.model('Document', documentSchema);
