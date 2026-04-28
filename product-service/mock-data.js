require('dotenv').config();
const mongoose = require('mongoose');
const { Product } = require('./src/models/product.model');

// Data mock 10+ mặt hàng thuộc nhiều thể loại khác nhau cho kiến trúc Đa hình (Polymorphism)
const mockProducts = [
    // --- Laptops ---
    {
        name: "MacBook Pro M3 14-inch",
        description: "Apple M3 Chip, 8-Core CPU, 10-Core GPU",
        price: 1599,
        quantity: 50,
        category: "Laptop",
        type: "Laptop", // Đây là Discirminator Key để Mongoose hiểu subtype
        manufacturer: "Apple",
        model: "MacBook Pro 14",
        cpu: "Apple M3",
        ram: "16GB Unified",
        storage: "512GB SSD",
        screen: "14.2 Liquid Retina XDR"
    },
    {
        name: "Dell XPS 15 9530",
        description: "Intel Core i7-13700H, RTX 4050",
        price: 1899,
        quantity: 30,
        category: "Laptop",
        type: "Laptop",
        manufacturer: "Dell",
        model: "XPS 15",
        cpu: "Intel Core i7 13th Gen",
        ram: "32GB DDR5",
        storage: "1TB NVMe SSD",
        screen: "15.6 OLED 3.5K"
    },
    {
        name: "ThinkPad X1 Carbon Gen 11",
        description: "Ultrabook for Business professionals",
        price: 1699,
        quantity: 20,
        category: "Laptop",
        type: "Laptop",
        manufacturer: "Lenovo",
        model: "ThinkPad X1",
        cpu: "Intel Core i7-1355U",
        ram: "16GB LPDDR5",
        storage: "512GB SSD",
        screen: "14.0 WUXGA"
    },
    // --- Mobiles ---
    {
        name: "iPhone 15 Pro Max",
        description: "Titanium body, A17 Pro chip",
        price: 1199,
        quantity: 100,
        category: "Mobile",
        type: "Mobile",
        manufacturer: "Apple",
        model: "iPhone 15 Pro Max",
        os: "iOS 17",
        battery: "4422 mAh",
        camera: "48MP Main, 12MP Ultra Wide, 12MP Telephoto 5x"
    },
    {
        name: "Samsung Galaxy S24 Ultra",
        description: "Galaxy AI, Snapdragon 8 Gen 3",
        price: 1299,
        quantity: 80,
        category: "Mobile",
        type: "Mobile",
        manufacturer: "Samsung",
        model: "Galaxy S24 Ultra",
        os: "Android 14",
        battery: "5000 mAh",
        camera: "200MP Main, 50MP Telephoto 5x"
    },
    {
        name: "Google Pixel 8 Pro",
        description: "Best camera with Google AI magic",
        price: 999,
        quantity: 60,
        category: "Mobile",
        type: "Mobile",
        manufacturer: "Google",
        model: "Pixel 8 Pro",
        os: "Android 14",
        battery: "5050 mAh",
        camera: "50MP Main, 48MP Ultra Wide, 48MP Telephoto"
    },
    // --- Clothing ---
    {
        name: "Nike Dri-FIT Running T-Shirt",
        description: "Comfortable, sweat-wicking shirt for running",
        price: 35,
        quantity: 200,
        category: "Sportswear",
        type: "Clothing",
        brand: "Nike",
        size: "M",
        material: "100% Polyester",
        color: "Black"
    },
    {
        name: "Adidas Originals Hoodie",
        description: "Classic fleece hoodie with trefoil logo",
        price: 65,
        quantity: 150,
        category: "Streetwear",
        type: "Clothing",
        brand: "Adidas",
        size: "L",
        material: "Cotton Fleece",
        color: "Grey"
    },
    {
        name: "Levi's 501 Original Fit Jeans",
        description: "The classic straight fit jean",
        price: 79,
        quantity: 120,
        category: "Fashion",
        type: "Clothing",
        brand: "Levi's",
        size: "32x32",
        material: "100% Cotton Denim",
        color: "Indigo Blue"
    },
    // --- Electronics (General) ---
    {
        name: "Sony WH-1000XM5 Headphones",
        description: "Industry leading noise canceling headphones",
        price: 398,
        quantity: 40,
        category: "Audio",
        type: "Electronics",
        manufacturer: "Sony",
        model: "WH-1000XM5",
        warranty: "24 months"
    },
    {
        name: "LG C3 65-inch OLED TV",
        description: "evo 4K Smart TV with WebOS",
        price: 1596,
        quantity: 15,
        category: "Television",
        type: "Electronics",
        manufacturer: "LG",
        model: "OLED65C3PUA",
        warranty: "12 months"
    }
];

const seedData = async () => {
    try {
        const uri = process.env.MONGO_URI || 'mongodb://localhost:27017/ecommerce_product_db';
        console.log(`Connecting to MongoDB at: ${uri}`);
        
        await mongoose.connect(uri, {
            useNewUrlParser: true,
            useUnifiedTopology: true,
        });
        
        console.log("Connected to MongoDB.");
        
        // Clear old data
        await Product.deleteMany({});
        console.log("Cleared existing products.");

        // Insert mock data
        const insertedData = await Product.insertMany(mockProducts);
        console.log(`Successfully seeded ${insertedData.length} products!`);
        
    } catch (error) {
        console.error("Error seeding data:", error);
    } finally {
        mongoose.connection.close();
        console.log("Database connection closed.");
        process.exit(0);
    }
}

seedData();
