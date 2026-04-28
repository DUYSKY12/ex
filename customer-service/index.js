const express = require('express');
const { Sequelize, DataTypes } = require('sequelize');
const cors = require('cors');
const Cart = require('./app/models/Cart');
const Order = require('./app/models/Order');

const app = express();
const port = 8001;

app.use(express.json());
app.use(cors());

const sequelize = new Sequelize(
  process.env.DB_NAME || 'shop_db',
  process.env.DB_USER || 'root',
  process.env.DB_PASSWORD || 'password',
  {
    host: process.env.DB_HOST || 'mysql_db',
    dialect: 'mysql',
    logging: false,
  }
);

const Customer = sequelize.define('Customer', {
  id: { type: DataTypes.UUID, defaultValue: DataTypes.UUIDV4, primaryKey: true },
  username: { type: DataTypes.STRING, unique: true, allowNull: false },
  email: { type: DataTypes.STRING, unique: true, allowNull: false },
  password: { type: DataTypes.STRING, allowNull: false },
  fullName: { type: DataTypes.STRING },
});

// Initialize Models
const CartModel = Cart(sequelize);
const OrderModel = Order(sequelize);

Customer.hasMany(CartModel, { foreignKey: 'customerId' });
CartModel.belongsTo(Customer, { foreignKey: 'customerId' });

Customer.hasMany(OrderModel, { foreignKey: 'customerId' });
OrderModel.belongsTo(Customer, { foreignKey: 'customerId' });

const connectDB = async () => {
    try {
        await sequelize.authenticate();
        console.log('MySQL connected for customer-service');
        await sequelize.sync({ alter: true });
    } catch (err) {
        console.error('Database connection failed:', err);
        process.exit(1);
    }
};

connectDB();

// Auth routes
app.post('/api/auth/register', async (req, res) => {
    try {
        const customer = await Customer.create(req.body);
        res.status(201).json(customer);
    } catch (error) {
        res.status(400).json({ error: error.message });
    }
});

app.post('/api/auth/login', async (req, res) => {
    try {
        const { email, password } = req.body;
        const customer = await Customer.findOne({ where: { email, password } });
        if (!customer) return res.status(401).json({ message: 'Invalid credentials' });
        res.status(200).json({ token: 'mock-token', user: customer });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Cart routes
app.get('/api/cart/:customerId', async (req, res) => {
    try {
        const cart = await CartModel.findAll({
            where: { customerId: req.params.customerId }
        });
        res.json(cart);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.post('/api/cart/add', async (req, res) => {
    try {
        const { customerId, productId, productType, productName, quantity, price } = req.body;
        
        const existingItem = await CartModel.findOne({
            where: { customerId, productId, productType }
        });

        if (existingItem) {
            existingItem.quantity += quantity;
            if (productName) existingItem.productName = productName;
            await existingItem.save();
            res.json(existingItem);
        } else {
            const cartItem = await CartModel.create({
                customerId, productId, productType, productName, quantity, price
            });
            res.status(201).json(cartItem);
        }
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.delete('/api/cart/:customerId/:itemId', async (req, res) => {
    try {
        const result = await CartModel.destroy({
            where: { id: req.params.itemId, customerId: req.params.customerId }
        });
        
        if (result === 0) {
            return res.status(404).json({ error: 'Cart item not found' });
        }
        
        res.json({ message: 'Item removed from cart' });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Order routes
app.post('/api/order/checkout', async (req, res) => {
    try {
        const { customerId, paymentMethod, shippingAddress, customerName, customerPhone } = req.body;
        // Get all cart items
        const cartItems = await CartModel.findAll({ where: { customerId } });
        if (cartItems.length === 0) {
            return res.status(400).json({ error: 'Cart is empty' });
        }
        
        // Calculate total amount
        const totalAmount = cartItems.reduce((acc, item) => acc + (Number(item.price) * item.quantity), 0);
        
        // Create Order
        const order = await OrderModel.create({
            customerId,
            items: cartItems,
            totalAmount,
            status: 'paid',
            paymentMethod: paymentMethod || 'COD',
            shippingAddress: shippingAddress || '',
            customerName: customerName || '',
            customerPhone: customerPhone || ''
        });
        
        // Clear cart
        await CartModel.destroy({ where: { customerId } });
        
        res.status(201).json(order);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.get('/api/order/:customerId', async (req, res) => {
    try {
        const orders = await OrderModel.findAll({
            where: { customerId: req.params.customerId },
            order: [['createdAt', 'DESC']]
        });
        res.json(orders);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.delete('/api/order/:customerId/all', async (req, res) => {
    try {
        const { customerId } = req.params;
        const deleted = await OrderModel.destroy({
            where: { customerId }
        });
        res.json({ success: true, count: deleted, message: 'All orders deleted' });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.delete('/api/order/:customerId/:orderId', async (req, res) => {
    try {
        const { customerId, orderId } = req.params;
        const deleted = await OrderModel.destroy({
            where: { id: orderId, customerId }
        });
        if (deleted === 0) {
            return res.status(404).json({ error: 'Order not found' });
        }
        res.json({ success: true, message: 'Order deleted' });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.listen(port, '0.0.0.0', () => {
    console.log(`Customer Service listening at http://localhost:${port}`);
});
