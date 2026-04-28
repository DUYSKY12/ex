const express = require('express');
const cors = require('cors');
const { connectDB, Mobile } = require('./models/Mobile');
const { Op } = require('sequelize');
const app = express();
const port = 8004;

app.use(express.json());
app.use(cors());
connectDB();

// GET all mobiles (with optional search)
app.get('/api/mobiles', async (req, res) => {
    try {
        const query = req.query.q || '';
        const mobiles = await Mobile.findAll({
            where: query ? {
                [Op.or]: [
                    { name: { [Op.iLike]: `%${query}%` } },
                    { brand: { [Op.iLike]: `%${query}%` } },
                ],
            } : {},
        });
        res.status(200).json(mobiles);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// POST add new mobile
app.post('/api/mobiles', async (req, res) => {
    try {
        const newMobile = await Mobile.create(req.body);
        res.status(201).json(newMobile);
    } catch (error) {
        res.status(400).json({ error: error.message });
    }
});

// PUT update mobile
app.put('/api/mobiles/:id', async (req, res) => {
    try {
        const mobile = await Mobile.findByPk(req.params.id);
        if (!mobile) return res.status(404).json({ message: 'Mobile not found' });
        await mobile.update(req.body);
        res.status(200).json(mobile);
    } catch (error) {
        res.status(400).json({ error: error.message });
    }
});

// DELETE mobile
app.delete('/api/mobiles/:id', async (req, res) => {
    try {
        const mobile = await Mobile.findByPk(req.params.id);
        if (!mobile) return res.status(404).json({ message: 'Mobile not found' });
        await mobile.destroy();
        res.status(200).json({ message: 'Mobile deleted successfully' });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.listen(port, '0.0.0.0', () => {
    console.log(`Mobile Service listening at http://localhost:${port}`);
});
