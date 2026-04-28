const { Product, Clothing, Electronics, Laptop, Mobile } = require('../models/product.model');

// ============================================
// Định nghĩa Factory class
// ============================================
class ProductFactory {
    static productRegistry = {};

    static registerProductType(type, classRef) {
        ProductFactory.productRegistry[type] = classRef;
    }

    static async createProduct(type, payload) {
        const productClass = ProductFactory.productRegistry[type];
        if (!productClass) throw new Error(`Invalid Product Type: ${type}`);
        
        return new productClass(payload).createProduct();
    }
}

// ============================================
// Định nghĩa các logic class xử lý Database
// ============================================

// Lớp cha
class BaseProduct {
    constructor(payload) {
        this.name = payload.name;
        this.description = payload.description;
        this.price = payload.price;
        this.quantity = payload.quantity;
        this.category = payload.category;
        this.type = payload.type;
    }

    async createProduct(productModel) {
        return await productModel.create(this);
    }
}

// Đối tượng Clothing
class ClothingEntity extends BaseProduct {
    constructor(payload) {
        super(payload);
        this.brand = payload.brand;
        this.size = payload.size;
        this.material = payload.material;
        this.color = payload.color;
    }

    async createProduct() {
        return super.createProduct(Clothing);
    }
}

// Đối tượng Electronics (Laptop/Mobile tương tự)
class ElectronicsEntity extends BaseProduct {
    constructor(payload) {
        super(payload);
        this.manufacturer = payload.manufacturer;
        this.model = payload.model;
        this.warranty = payload.warranty;
    }

    async createProduct() {
        return super.createProduct(Electronics);
    }
}

class LaptopEntity extends BaseProduct {
    constructor(payload) {
        super(payload);
        this.manufacturer = payload.manufacturer;
        this.model = payload.model;
        this.cpu = payload.cpu;
        this.ram = payload.ram;
        this.storage = payload.storage;
        this.screen = payload.screen;
    }

    async createProduct() {
        return super.createProduct(Laptop);
    }
}

class MobileEntity extends BaseProduct {
    constructor(payload) {
        super(payload);
        this.manufacturer = payload.manufacturer;
        this.model = payload.model;
        this.os = payload.os;
        this.battery = payload.battery;
        this.camera = payload.camera;
    }

    async createProduct() {
        return super.createProduct(Mobile);
    }
}

// Đăng ký cho Factory pattern
ProductFactory.registerProductType('Clothing', ClothingEntity);
ProductFactory.registerProductType('Electronics', ElectronicsEntity);
ProductFactory.registerProductType('Laptop', LaptopEntity);
ProductFactory.registerProductType('Mobile', MobileEntity);


// ============================================
// Service Export Methods
// ============================================
class ProductService {

    // Tạo mới Product dựa trên Factory
    static async createProduct(payload) {
        return await ProductFactory.createProduct(payload.type, payload);
    }

    // Lấy toàn bộ Product
    static async findAllProducts({ limit = 50, sort = 'ctime', page = 1 } = {}) {
        const skip = (page - 1) * limit;
        return await Product.find()
            .sort(sort === 'ctime' ? { _id: -1 } : { _id: 1 })
            .skip(skip)
            .limit(limit)
            .lean();
    }

    // Lấy 1 Product (sẽ trả về đúng subtype dựa trên mongoose discriminator)
    static async findProductById(productId) {
        return await Product.findById(productId).lean();
    }

    // Update Product (Sử dụng Model cha Product)
    static async updateProduct(productId, updates) {
        return await Product.findByIdAndUpdate(productId, updates, { new: true });
    }

    // Delete Product
    static async deleteProduct(productId) {
        return await Product.findByIdAndDelete(productId);
    }
}

module.exports = ProductService;
