const express = require('express');
const router = express.Router();
const productRoute = require('./product.route');

router.use('/v1/products', productRoute);

module.exports = router;
