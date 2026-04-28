const express = require('express');
const cors = require('cors');
const { connectDB } = require('./config/db');
const laptopRoutes = require('./routes/laptopRoutes');

const app = express();
const port = 8003;

app.use(express.json());
app.use(cors());

// Initialize DB and connect to PostgreSQL
connectDB();

// Routes (API Gateway proxies /laptop -> laptop-service, strips /laptop prefix)
app.use('/api/laptops', laptopRoutes);

// Health check endpoint
app.get('/health', (req, res) => {
  res.send('Laptop Service is healthy');
});

// Start the laptop-service server
app.listen(port, '0.0.0.0', () => {
  console.log(`Laptop Service listening at http://localhost:${port}`);
});
