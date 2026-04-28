const Laptop = require('../models/Laptop');

// Get all laptops for customer products list or search
exports.getAllLaptops = async (req, res) => {
  try {
    const query = req.query.q || '';
    const laptops = await Laptop.findAll({
      where: {
        // Simple case-insensitive search on name or brand
        [require('sequelize').Op.or]: [
          { name: { [require('sequelize').Op.iLike]: `%${query}%` } },
          { brand: { [require('sequelize').Op.iLike]: `%${query}%` } }, 
        ],
      },
    });
    res.status(200).json(laptops);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

// Add a new laptop for staff members
exports.addLaptop = async (req, res) => {
  try {
    const { name, brand, price, stock, description, imageUrl } = req.body;
    const newLaptop = await Laptop.create({
      name,
      brand,
      price,
      stock,
      description,
      imageUrl,
    });
    res.status(201).json(newLaptop);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
};

// Update existing laptop information for staff
exports.updateLaptop = async (req, res) => {
  try {
    const { id } = req.params;
    
    let laptop = await Laptop.findByPk(id);
    if (!laptop) {
      return res.status(404).json({ message: 'Laptop not found' });
    }

    await laptop.update(req.body);
    
    res.status(200).json(laptop);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
};

// Delete a laptop
exports.deleteLaptop = async (req, res) => {
  try {
    const { id } = req.params;
    const laptop = await Laptop.findByPk(id);
    if (!laptop) {
      return res.status(404).json({ message: 'Laptop not found' });
    }
    await laptop.destroy();
    res.status(200).json({ message: 'Laptop deleted successfully' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

