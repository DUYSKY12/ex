const Cart = require('../models/Cart');

// Get customer's cart
const getCart = async (req, res) => {
  try {
    const { customerId } = req.params;
    const cart = await Cart.findAll({
      where: { customerId },
      order: [['createdAt', 'DESC']]
    });
    res.json(cart);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

// Add item to cart
const addToCart = async (req, res) => {
  try {
    const { customerId, productId, productType, quantity, price } = req.body;
    
    // Check if item already exists in cart
    const existingItem = await Cart.findOne({
      where: { customerId, productId, productType }
    });

    if (existingItem) {
      // Update quantity if item exists
      existingItem.quantity += quantity;
      await existingItem.save();
      res.json(existingItem);
    } else {
      // Create new cart item
      const cartItem = await Cart.create({
        customerId,
        productId,
        productType,
        quantity,
        price
      });
      res.status(201).json(cartItem);
    }
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

// Remove item from cart
const removeFromCart = async (req, res) => {
  try {
    const { customerId, itemId } = req.params;
    const result = await Cart.destroy({
      where: { id: itemId, customerId }
    });
    
    if (result === 0) {
      return res.status(404).json({ error: 'Cart item not found' });
    }
    
    res.json({ message: 'Item removed from cart' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

// Update cart item quantity
const updateCartQuantity = async (req, res) => {
  try {
    const { customerId, itemId } = req.params;
    const { quantity } = req.body;
    
    const cartItem = await Cart.findOne({
      where: { id: itemId, customerId }
    });

    if (!cartItem) {
      return res.status(404).json({ error: 'Cart item not found' });
    }

    cartItem.quantity = quantity;
    await cartItem.save();
    res.json(cartItem);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

module.exports = {
  getCart,
  addToCart,
  removeFromCart,
  updateCartQuantity
};
