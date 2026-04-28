const express = require('express');
const router = express.Router();
const clothesController = require('../controllers/clothesController');

// Define routes for Clothes
router.get('/', clothesController.getAllClothes);
router.get('/:id', clothesController.getClothesById);
router.post('/add', clothesController.createClothes);
router.put('/:id', clothesController.updateClothes);
router.delete('/:id', clothesController.deleteClothes);

module.exports = router;
