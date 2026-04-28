const { Sequelize } = require('sequelize');

const sequelize = new Sequelize(
  process.env.DB_NAME || 'postgres',
  process.env.DB_USER || 'postgres',
  process.env.DB_PASSWORD || 'password',
  {
    host: process.env.DB_HOST || 'postgres_db',
    dialect: 'postgres',
    logging: false, // Set to true to see SQL queries in logs
  }
);

const connectDB = async () => {
  try {
    await sequelize.authenticate();
    console.log('PostgreSQL connected for laptop-service');
    // Sync models
    await sequelize.sync({ force: false }); // Change to true if needed during dev
  } catch (err) {
    console.error('Database connection failed:', err);
    process.exit(1);
  }
};

module.exports = { sequelize, connectDB };
