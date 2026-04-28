const ProductService = require('../services/product.service');

class ProductController {
    
    // POST /api/v1/products
    static async createProduct(req, res) {
        try {
            const product = await ProductService.createProduct(req.body);
            res.status(201).json({
                message: "Product created successfully",
                data: product
            });
        } catch (error) {
            res.status(400).json({ message: error.message });
        }
    }

    // GET /api/v1/products
    static async getAllProducts(req, res) {
        try {
            const limit = parseInt(req.query.limit) || 50;
            const page = parseInt(req.query.page) || 1;
            
            const products = await ProductService.findAllProducts({ limit, page });
            res.status(200).json({
                message: "Get all products successfully",
                data: products
            });
        } catch (error) {
            res.status(500).json({ message: error.message });
        }
    }

    // GET /api/v1/products/:id
    static async getProductById(req, res) {
        try {
            const product = await ProductService.findProductById(req.params.id);
            if (!product) return res.status(404).json({ message: "Product not found" });
            
            res.status(200).json({
                message: "Get product details successfully",
                data: product
            });
        } catch (error) {
            res.status(500).json({ message: error.message });
        }
    }

    // PATCH /api/v1/products/:id
    static async updateProduct(req, res) {
        try {
            const product = await ProductService.updateProduct(req.params.id, req.body);
            if (!product) return res.status(404).json({ message: "Product not found" });
            
            res.status(200).json({
                message: "Product updated successfully",
                data: product
            });
        } catch (error) {
            res.status(400).json({ message: error.message });
        }
    }

    // DELETE /api/v1/products/:id
    static async deleteProduct(req, res) {
        try {
            const product = await ProductService.deleteProduct(req.params.id);
            if (!product) return res.status(404).json({ message: "Product not found" });
            
            res.status(200).json({
                message: "Product deleted successfully"
            });
        } catch (error) {
            res.status(500).json({ message: error.message });
        }
    }

    // POST /api/v1/products/seed
    static async seedProducts(req, res) {
        try {
            // Danh sách 16 sản phẩm mẫu
            const dummyProducts = [
                // Laptop (4)
                { type: 'Laptop', name: 'Alienware m15 R7', description: 'Laptop gaming cao cấp từ Dell', price: 60000000, quantity: 5, category: 'Gaming', manufacturer: 'Dell', model: 'm15 R7', cpu: 'Core i7', ram: '16GB', storage: '1TB SSD', screen: '15.6 inch FHD 165Hz' },
                { type: 'Laptop', name: 'MacBook Air M2', description: 'Mỏng nhẹ di động, pin trâu', price: 28000000, quantity: 20, category: 'Office', manufacturer: 'Apple', model: 'Air M2', cpu: 'M2', ram: '8GB', storage: '256GB SSD', screen: '13.6 inch Liquid Retina' },
                { type: 'Laptop', name: 'HP Spectre x360', description: 'Laptop doanh nhân mỏng nhẹ màn hình xoay gập', height: 35000000, price: 38000000, quantity: 12, category: 'Business', manufacturer: 'HP', model: 'Spectre 14', cpu: 'Core i7 13th Gen', ram: '16GB', storage: '1TB SSD', screen: '14.0 OLED Touch' },
                { type: 'Laptop', name: 'Asus Zenbook 14', description: 'Siêu mỏng siêu nhẹ siêu xịn', price: 25000000, quantity: 15, category: 'Office', manufacturer: 'Asus', model: 'Zenbook 14 UX3402', cpu: 'Core i5', ram: '16GB', storage: '512GB SSD', screen: '14 inch 2.8K OLED' },
                
                // Mobile (4)
                { type: 'Mobile', name: 'iPhone 14 Plus', description: 'Màn hình lớn pin siêu trâu', price: 21000000, quantity: 30, category: 'Smartphone', manufacturer: 'Apple', model: '14 Plus', os: 'iOS', battery: '4325 mAh', camera: '12 MP' },
                { type: 'Mobile', name: 'Samsung Galaxy Z Fold 5', description: 'Điện thoại màn hình gập cao cấp nhất của Samsung', price: 40000000, quantity: 8, category: 'Smartphone', manufacturer: 'Samsung', model: 'Z Fold 5', os: 'Android', battery: '4400 mAh', camera: '50 MP' },
                { type: 'Mobile', name: 'Xiaomi 13 Pro', description: 'Camera Leica đỉnh cao nhiếp ảnh', price: 25000000, quantity: 10, category: 'Smartphone', manufacturer: 'Xiaomi', model: '13 Pro', os: 'Android', battery: '4820 mAh', camera: '50.3 MP' },
                { type: 'Mobile', name: 'Oppo Find X6 Pro', description: 'Máy ảnh thiết kế hầm hố', price: 22000000, quantity: 12, category: 'Smartphone', manufacturer: 'Oppo', model: 'Find X6 Pro', os: 'Android', battery: '5000 mAh', camera: '50 MP' },

                // Clothing (4)
                { type: 'Clothing', name: 'Áo dài tay thu đông', description: 'Trời lạnh mặc ấm', price: 300000, quantity: 50, category: 'Shirt', brand: 'Uniqlo', size: 'L', material: 'Cotton', color: 'Xám' },
                { type: 'Clothing', name: 'Váy dạ hội', description: 'Sang trọng quyến rũ cho buổi tiệc', price: 1500000, quantity: 15, category: 'Dress', brand: 'H&M', size: 'M', material: 'Silk', color: 'Đỏ' },
                { type: 'Clothing', name: 'Quần tây công sở', description: 'Thanh lịch chuyên nghiệp', price: 450000, quantity: 40, category: 'Pants', brand: 'Owen', size: '32', material: 'Polyester', color: 'Đen' },
                { type: 'Clothing', name: 'Nón kết Sơn', description: 'Chống nắng sành điệu', price: 120000, quantity: 100, category: 'Hat', brand: 'NonSon', size: 'Freesize', material: 'Vải Kaki', color: 'Vàng' },

                // Electronics (4)
                { type: 'Electronics', name: 'Apple Watch Series 9', description: 'Đồng hồ thông minh theo dõi sức khoẻ', price: 10000000, quantity: 20, category: 'Smartwatch', manufacturer: 'Apple', model: 'Watch S9', warranty: '12 months' },
                { type: 'Electronics', name: 'AirPods Pro 2', description: 'Tai nghe chống ồn khử tiếng gió', price: 6000000, quantity: 25, category: 'Headphones', manufacturer: 'Apple', model: 'AirPods Pro 2', warranty: '12 months' },
                { type: 'Electronics', name: 'Samsung Smart TV 4K', description: 'Màn hình 55 inch công nghệ chống loá', price: 15000000, quantity: 10, category: 'Television', manufacturer: 'Samsung', model: 'QLED 55', warranty: '24 months' },
                { type: 'Electronics', name: 'Sony PlayStation 5', description: 'Máy chơi game đỉnh cao của Sony', price: 14000000, quantity: 5, category: 'Console', manufacturer: 'Sony', model: 'PS5 Base', warranty: '12 months' },
            ];

            const { Product } = require('../models/product.model');
            await Product.deleteMany({}); // Clear existing

            for (let pd of dummyProducts) {
                await ProductService.createProduct(pd);
            }

            res.status(200).json({
                message: "Seeded 16 products successfully",
                count: dummyProducts.length
            });
        } catch (error) {
            res.status(500).json({ message: error.message });
        }
    }
}

module.exports = ProductController;
