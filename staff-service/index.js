const express = require('express');
const { Sequelize, DataTypes } = require('sequelize');
const cors = require('cors');
const axios = require('axios');

const app = express();
const port = 8002;

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

const Staff = sequelize.define('Staff', {
  id: { type: DataTypes.UUID, defaultValue: DataTypes.UUIDV4, primaryKey: true },
  username: { type: DataTypes.STRING, unique: true, allowNull: false },
  email: { type: DataTypes.STRING, unique: true, allowNull: false },
  password: { type: DataTypes.STRING, allowNull: false },
  role: { type: DataTypes.STRING, defaultValue: 'staff' },
});

const connectDB = async () => {
    try {
        await sequelize.authenticate();
        console.log('MySQL connected for staff-service');
        await sequelize.sync({ force: false });
    } catch (err) {
        console.error('Database connection failed:', err);
        process.exit(1);
    }
};

connectDB();

// Auth routes
app.post('/api/auth/register', async (req, res) => {
    try {
        const staff = await Staff.create(req.body);
        res.status(201).json(staff);
    } catch (error) {
        res.status(400).json({ error: error.message });
    }
});

app.post('/api/auth/login', async (req, res) => {
    try {
        const { email, password } = req.body;
        const staff = await Staff.findOne({ where: { email, password } });
        if (!staff) return res.status(401).json({ message: 'Invalid credentials' });
        res.status(200).json({ token: 'mock-token', user: staff });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// ===== Laptop management routes =====
app.post('/api/laptop/add', async (req, res) => {
    try {
        const response = await axios.post('http://laptop-service:8003/api/laptops', req.body);
        res.status(201).json(response.data);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.put('/api/laptop/update/:id', async (req, res) => {
    try {
        const response = await axios.put(`http://laptop-service:8003/api/laptops/${req.params.id}`, req.body);
        res.json(response.data);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.delete('/api/laptop/delete/:id', async (req, res) => {
    try {
        const response = await axios.delete(`http://laptop-service:8003/api/laptops/${req.params.id}`);
        res.json(response.data);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// ===== Mobile management routes =====
app.post('/api/mobile/add', async (req, res) => {
    try {
        const response = await axios.post('http://mobile-service:8004/api/mobiles', req.body);
        res.status(201).json(response.data);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.put('/api/mobile/update/:id', async (req, res) => {
    try {
        const response = await axios.put(`http://mobile-service:8004/api/mobiles/${req.params.id}`, req.body);
        res.json(response.data);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.delete('/api/mobile/delete/:id', async (req, res) => {
    try {
        const response = await axios.delete(`http://mobile-service:8004/api/mobiles/${req.params.id}`);
        res.json(response.data);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// ===== Clothes management routes =====
app.post('/api/clothes/add', async (req, res) => {
    try {
        const response = await axios.post('http://clothes-service:8005/api/clothes/add', req.body);
        res.status(201).json(response.data);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.put('/api/clothes/update/:id', async (req, res) => {
    try {
        const response = await axios.put(`http://clothes-service:8005/api/clothes/${req.params.id}`, req.body);
        res.json(response.data);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.delete('/api/clothes/delete/:id', async (req, res) => {
    try {
        const response = await axios.delete(`http://clothes-service:8005/api/clothes/${req.params.id}`);
        res.json(response.data);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Get all products (laptops + mobiles + clothes)
app.get('/api/products', async (req, res) => {
    try {
        const [laptopResponse, mobileResponse, clothesResponse] = await Promise.all([
            axios.get('http://laptop-service:8003/api/laptops'),
            axios.get('http://mobile-service:8004/api/mobiles'),
            axios.get('http://clothes-service:8005/api/clothes')
        ]);
        
        res.json({
            laptops: laptopResponse.data,
            mobiles: mobileResponse.data,
            clothes: clothesResponse.data
        });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.listen(port, '0.0.0.0', () => {
    console.log(`Staff Service listening at http://localhost:${port}`);
});
