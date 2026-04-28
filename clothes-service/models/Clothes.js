const { DataTypes } = require('sequelize');
const { sequelize } = require('../config/db');

const Clothes = sequelize.define('Clothes', {
  id: {
    type: DataTypes.UUID,
    defaultValue: DataTypes.UUIDV4,
    primaryKey: true,
  },
  name: {
    type: DataTypes.STRING,
    allowNull: false,
  },
  brand: {
    type: DataTypes.STRING,
    allowNull: false,
  },
  price: {
    type: DataTypes.FLOAT,
    allowNull: false,
    validate: {
      min: 0
    }
  },
  stock: {
    type: DataTypes.INTEGER,
    defaultValue: 0,
    validate: {
      min: 0
    }
  },
  description: {
    type: DataTypes.TEXT,
  },
  imageUrl: {
    type: DataTypes.STRING,
  },
  size: {
    type: DataTypes.STRING,
    defaultValue: 'M',
  },
  color: {
    type: DataTypes.STRING,
    defaultValue: 'Black',
  }
}, {
  timestamps: true,
  tableName: 'clothes'
});

module.exports = Clothes;
