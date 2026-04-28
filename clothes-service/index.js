const express = require('express');
const cors = require('cors');
const { connectDB } = require('./config/db');
const clothesRoutes = require('./routes/clothesRoutes');

const app = express();
const port = 8005;

app.use(express.json());
app.use(cors());

// Initialize DB and connect to PostgreSQL
connectDB();

// Routes
app.use('/api/clothes', clothesRoutes);

// Health check endpoint
app.get('/health', (req, res) => {
  res.send('Clothes Service is healthy');
});

// Start the clothes-service server
app.listen(port, '0.0.0.0', () => {
  console.log(`Clothes Service listening at http://localhost:${port}`);
});
