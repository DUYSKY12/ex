require('dotenv').config();
const express = require('express');
const cors = require('cors');
const morgan = require('morgan');
const connectDB = require('./config/database');
const routes = require('./routes/index');

const app = express();

// 1. Kết nối Database
connectDB();

// 2. Middlewares
app.use(cors());
app.use(express.json()); // Parser body requests to JSON
app.use(express.urlencoded({ extended: true }));
app.use(morgan('dev')); // Ghi log request ra console

// 3. API Routes
app.use('/api', routes);

// 4. Default error handling middleware
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({
        message: err.message || 'Internal Server Error'
    });
});

const PORT = process.env.PORT || 8006;

if (require.main === module) {
    app.listen(PORT, () => {
        console.log(`[Product-Service] Server listening on port ${PORT}`);
    });
}

module.exports = app;
