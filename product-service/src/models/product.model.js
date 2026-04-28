const mongoose = require('mongoose');

// =======================
// BASE PRODUCT SCHEMA
// =======================
const productSchema = new mongoose.Schema({
    name: { type: String, required: true },
    description: { type: String, required: true },
    price: { type: Number, required: true },
    quantity: { type: Number, required: true, default: 0 },
    category: { type: String, required: true },
    type: { type: String, required: true, enum: ['Electronics', 'Clothing', 'Laptop', 'Mobile'] }
}, {
    timestamps: true,
    discriminatorKey: 'type' // Field dùng để xác định class con
});

const Product = mongoose.model('Product', productSchema);

// =======================
// ELECTRONICS PRODUCT SCHEMA
// =======================
const electronicsSchema = new mongoose.Schema({
    manufacturer: { type: String, required: true },
    model: { type: String, required: true },
    warranty: { type: String, default: "12 months" }
});

const Electronics = Product.discriminator('Electronics', electronicsSchema);

// =======================
// LAPTOP PRODUCT SCHEMA (Kế thừa từ Product hoặc Electronics theo thiết kế NoSQL)
// Ở MongoDB, ta có thể đăng ký trực tiếp Laptop Discriminator dưới Product
// =======================
const laptopSchema = new mongoose.Schema({
    manufacturer: { type: String, required: true },
    model: { type: String, required: true },
    cpu: { type: String, required: true },
    ram: { type: String, required: true },
    storage: { type: String, required: true },
    screen: { type: String, required: true }
});

const Laptop = Product.discriminator('Laptop', laptopSchema);

// =======================
// MOBILE PRODUCT SCHEMA
// =======================
const mobileSchema = new mongoose.Schema({
    manufacturer: { type: String, required: true },
    model: { type: String, required: true },
    os: { type: String },
    battery: { type: String },
    camera: { type: String }
});

const Mobile = Product.discriminator('Mobile', mobileSchema);

// =======================
// CLOTHING PRODUCT SCHEMA
// =======================
const clothingSchema = new mongoose.Schema({
    brand: { type: String, required: true },
    size: { type: String, required: true },
    material: { type: String, required: true },
    color: { type: String, required: true }
});

const Clothing = Product.discriminator('Clothing', clothingSchema);


module.exports = {
    Product,
    Electronics,
    Laptop,
    Mobile,
    Clothing
};
