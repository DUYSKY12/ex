const express = require('express');
const router = express.Router();
const laptopController = require('../controllers/laptopController');

// Define API routes (matching what API Gateway proxies to)
router.get('/', laptopController.getAllLaptops);
router.post('/', laptopController.addLaptop);
router.put('/:id', laptopController.updateLaptop);
router.delete('/:id', laptopController.deleteLaptop);

module.exports = router;
