require('dotenv').config();
const express = require('express');
const cors = require('cors');
const morgan = require('morgan');
const axios = require('axios');
const { createProxyMiddleware } = require('http-proxy-middleware');

const app = express();
const PORT = process.env.PORT || 8080;
const AUTH_SERVICE_URL = process.env.AUTH_SERVICE_URL || 'http://auth-service:5000';

app.use(cors());
app.use(morgan('dev'));

// Health check cho Gateway
app.get('/health', (req, res) => {
    res.status(200).json({ status: 'ok', service: 'gateway' });
});

// Middleware: Identity Translation (Xác thực JWT và map Header)
const verifyToken = async (req, res, next) => {
    // Bỏ qua xác thực cho các route công khai
    const publicRoutes = [
        { method: 'POST', path: '/api/auth/login' },
        { method: 'POST', path: '/api/auth/register' },
        { method: 'GET', path: '/api/rooms' }
    ];

    const isPublic = publicRoutes.some(route => 
        req.method === route.method && req.path.startsWith(route.path)
    );

    if (isPublic) {
        return next();
    }

    const authHeader = req.headers['authorization'];
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
        return res.status(401).json({ error: 'Unauthorized', message: 'Missing or invalid token' });
    }

    const token = authHeader.split(' ')[1];

    try {
        // Gọi sang Auth Service để verify token
        const response = await axios.post(`${AUTH_SERVICE_URL}/auth/verify`, { token });
        
        if (response.data && response.data.valid) {
            const user = response.data.user;
            // Xóa header authorization cũ để tránh pass xuống dưới
            delete req.headers['authorization'];
            // Gắn Internal Headers
            req.headers['x-user-id'] = user.id;
            req.headers['x-user-role'] = user.role;
            next();
        } else {
            return res.status(401).json({ error: 'Unauthorized', message: 'Invalid token' });
        }
    } catch (error) {
        console.error('Token verification failed:', error.message);
        return res.status(401).json({ error: 'Unauthorized', message: 'Token verification failed' });
    }
};

// Áp dụng middleware xác thực cho tất cả request bắt đầu bằng /api
app.use('/api', verifyToken);

// Cấu hình Proxy
const proxyOptions = {
    changeOrigin: true,
    pathRewrite: {
        '^/api/auth': '/auth',
        '^/api/users': '/users'
    }
};

app.use('/api/auth', createProxyMiddleware({ target: AUTH_SERVICE_URL, ...proxyOptions }));
app.use('/api/users', createProxyMiddleware({ target: AUTH_SERVICE_URL, ...proxyOptions }));
app.use('/api/rooms', createProxyMiddleware({ target: process.env.ROOM_SERVICE_URL || 'http://room-service:5000', changeOrigin: true, pathRewrite: {'^/api/rooms': '/rooms'} }));
app.use('/api/bookings', createProxyMiddleware({ target: process.env.BOOKING_SERVICE_URL || 'http://booking-service:5000', changeOrigin: true, pathRewrite: {'^/api/bookings': '/bookings'} }));
app.use('/api/payments', createProxyMiddleware({ target: process.env.PAYMENT_SERVICE_URL || 'http://payment-service:5000', changeOrigin: true, pathRewrite: {'^/api/payments': '/payments'} }));

app.listen(PORT, () => {
    console.log(`🚀 API Gateway is running on port ${PORT}`);
});
