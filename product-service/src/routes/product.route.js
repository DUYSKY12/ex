const express = require('express');
const router = express.Router();
const ProductController = require('../controllers/product.controller');

router.post('/seed', ProductController.seedProducts);
router.post('/', ProductController.createProduct);
router.get('/', ProductController.getAllProducts);
router.get('/:id', ProductController.getProductById);
router.patch('/:id', ProductController.updateProduct);
router.delete('/:id', ProductController.deleteProduct);

module.exports = router;
