const mongoose = require('mongoose');

const productSchema = new mongoose.Schema({
    productName: {
        type: String,
        required: true,
        trim: true,
    },
    productPrice: {
        type: Number,
        required: true,
        trim: true,
    },
    productDescription: {
        type: String,
        required: true,
        trim: true,
    },
    productCategory: {
        type: String,
        required: true,
        trim: true,
    },
    productImageUrl: {
        type: String,
        required: true,
    },
    tags: {
        type: [String], // Array of strings for tags
        default: [],
        trim: true,
    },
    createdAt: {
        type: Date,
        default: Date.now,
    },
});

const Product = mongoose.model('Product', productSchema);
module.exports = Product;
