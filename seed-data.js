const http = require('http');

function request(method, path, data) {
    return new Promise((resolve, reject) => {
        const body = data ? JSON.stringify(data) : '';
        const options = {
            hostname: 'localhost',
            port: 8080,
            path,
            method,
            headers: {
                'Content-Type': 'application/json',
                'Content-Length': Buffer.byteLength(body)
            },
            timeout: 8000
        };
        const req = http.request(options, (res) => {
            let d = '';
            res.on('data', c => d += c);
            res.on('end', () => resolve({ status: res.statusCode, body: d }));
        });
        req.on('error', reject);
        req.on('timeout', () => { req.destroy(); reject(new Error('Timeout')); });
        if (body) req.write(body);
        req.end();
    });
}

async function seed() {
    console.log('--- Bắt đầu Seed Data ---');

    // 1. Seed Customer
    try {
        const r = await request('POST', '/api/proxy/customer/api/auth/register', {
            username: 'customer1', email: 'customer@techshop.com', password: '123', fullName: 'Anh Duy Customer'
        });
        console.log(`Customer: ${r.status} - ${r.body.slice(0, 80)}`);
    } catch (e) { console.log('Customer skip:', e.message); }

    // 2. Seed Staff
    try {
        const r = await request('POST', '/api/proxy/staff/api/auth/register', {
            username: 'admin', email: 'admin@techshop.com', password: '123'
        });
        console.log(`Staff: ${r.status} - ${r.body.slice(0, 80)}`);
    } catch (e) { console.log('Staff skip:', e.message); }

    // 3. Seed Laptops
    const laptops = [
        { name: 'MacBook Pro 14 M3', brand: 'Apple', price: 45000000, stock: 10, description: 'Chip M3 mới nhất, màn hình Liquid Retina XDR.', imageUrl: 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400' },
        { name: 'Dell XPS 13 9315', brand: 'Dell', price: 32000000, stock: 15, description: 'Mỏng nhẹ, sang trọng, hiệu năng văn phòng đỉnh cao.', imageUrl: 'https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=400' },
        { name: 'ASUS ROG Zephyrus G14', brand: 'ASUS', price: 38000000, stock: 5, description: 'Laptop gaming 14 inch mạnh mẽ nhất thế giới.', imageUrl: 'https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=400' },
    ];
    for (const laptop of laptops) {
        try {
            const r = await request('POST', '/api/proxy/staff/api/laptop/add', laptop);
            console.log(`Laptop ${laptop.name}: ${r.status}`);
        } catch (e) { console.log(`Laptop ${laptop.name} skip:`, e.message); }
    }

    // 4. Seed Mobiles
    const mobiles = [
        { name: 'iPhone 15 Pro Max', brand: 'Apple', price: 35000000, stock: 20, description: 'Khung viền titan, chip A17 Pro mạnh mẽ.', imageUrl: 'https://images.unsplash.com/photo-1510557880182-3d4d3cba3f21?w=400' },
        { name: 'Samsung Galaxy S24 Ultra', brand: 'Samsung', price: 31000000, stock: 25, description: 'Màn hình phẳng 6.8 inch, camera 200MP.', imageUrl: 'https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?w=400' },
        { name: 'Google Pixel 8 Pro', brand: 'Google', price: 24000000, stock: 12, description: 'Trải nghiệm Android thuần khiết, camera AI cực đỉnh.', imageUrl: 'https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=400' },
    ];
    for (const mobile of mobiles) {
        try {
            const r = await request('POST', '/api/proxy/staff/api/mobile/add', mobile);
            console.log(`Mobile ${mobile.name}: ${r.status}`);
        } catch (e) { console.log(`Mobile ${mobile.name} skip:`, e.message); }
    }

    // 5. Seed Clothes
    const clothes = [
        { name: 'Áo Thun Basic T-Shirt', brand: 'Coolmate', price: 150000, stock: 100, description: 'Áo thun cotton 100% thoáng mát.', imageUrl: 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400', size: 'L', color: 'White' },
        { name: 'Quần Jeans Slim Fit', brand: 'Levi\'s', price: 850000, stock: 50, description: 'Quần jeans thời trang nam bền đẹp.', imageUrl: 'https://images.unsplash.com/photo-1542272604-780c96852d62?w=400', size: '32', color: 'Blue' },
        { name: 'Áo Khoác Bomber', brand: 'Zara', price: 1200000, stock: 30, description: 'Áo khoác mùa đông giữ ấm cực tốt.', imageUrl: 'https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=400', size: 'M', color: 'Black' },
    ];
    for (const item of clothes) {
        try {
            const r = await request('POST', '/api/proxy/staff/api/clothes/add', item);
            console.log(`Clothes ${item.name}: ${r.status}`);
        } catch (e) { console.log(`Clothes ${item.name} skip:`, e.message); }
    }

    console.log('--- Seed Hoàn Thành ---');
}

seed();
