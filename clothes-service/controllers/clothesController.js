const Clothes = require('../models/Clothes');
const { Op } = require('sequelize');

// GET all clothes
exports.getAllClothes = async (req, res) => {
  try {
    const { q } = req.query;
    let whereClause = {};

    if (q) {
      whereClause = {
        [Op.or]: [
          { name: { [Op.iLike]: `%${q}%` } },
          { brand: { [Op.iLike]: `%${q}%` } },
          { description: { [Op.iLike]: `%${q}%` } }
        ]
      };
    }

    const clothes = await Clothes.findAll({ where: whereClause });
    res.json(clothes);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
};

// GET clothes by ID
exports.getClothesById = async (req, res) => {
  try {
    const item = await Clothes.findByPk(req.params.id);
    if (!item) return res.status(404).json({ message: 'Clothes not found' });
    res.json(item);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
};

// POST new clothes
exports.createClothes = async (req, res) => {
  try {
    const newItem = await Clothes.create(req.body);
    res.status(201).json(newItem);
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
};

// PUT update clothes
exports.updateClothes = async (req, res) => {
  try {
    const { id } = req.params;
    const [updated] = await Clothes.update(req.body, { where: { id } });

    if (updated) {
      const updatedItem = await Clothes.findByPk(id);
      return res.json(updatedItem);
    }
    throw new Error('Clothes not found');
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
};

// DELETE clothes
exports.deleteClothes = async (req, res) => {
  try {
    const deleted = await Clothes.destroy({
      where: { id: req.params.id }
    });
    if (deleted) {
      return res.json({ message: 'Clothes deleted successfully' });
    }
    throw new Error('Clothes not found');
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
};
