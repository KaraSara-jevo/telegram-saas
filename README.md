# Telegram SaaS Microservices

A Laravel-based microservices architecture for Telegram bot SaaS platform.

## Architecture

### Services
- **User Service** (Port 8001) - User management, subscriptions, activation codes
- **Inventory Service** (Port 8002) - Product management, stock tracking
- **Sales Service** (Port 8003) - Sales transactions, expenses, accounting

### Infrastructure
- **MySQL** - Separate schemas per service
- **Nginx** - Reverse proxy / API Gateway
- **Docker** - Container orchestration

## Quick Start

### Prerequisites
- Docker Desktop
- Git

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd telegram-saas
```

2. Start all services:
```bash
docker-compose up --build -d
```

3. Run database migrations:
```bash
docker-compose exec user-service php artisan migrate
docker-compose exec inventory-service php artisan migrate
docker-compose exec sales-service php artisan migrate
```

### API Endpoints

#### User Service
- `GET /api/user/users` - List all users
- `POST /api/user/users` - Create new user
- `GET /api/user/subscriptions` - List subscriptions
- `POST /api/user/subscriptions/activate` - Activate subscription

#### Inventory Service
- `GET /api/inventory/products` - List products
- `POST /api/inventory/products` - Create product
- `PATCH /api/inventory/products/{id}/stock` - Update stock

#### Sales Service
- `GET /api/sales/sales` - List sales
- `POST /api/sales/sales` - Create sale
- `GET /api/sales/expenses` - List expenses
- `GET /api/sales/accounting/profit-loss` - Get P&L report

## Database Structure

### User Service (`user_service_db`)
- `users` - Telegram users and shops
- `activation_codes` - Subscription activation codes

### Inventory Service (`inventory_service_db`)
- `products` - Product catalog with stock

### Sales Service (`sales_service_db`)
- `sales` - Sales transactions
- `expenses` - Business expenses

## Development

### Adding New Services
1. Create new directory: `new-service/`
2. Add Dockerfile
3. Add service to docker-compose.yml
4. Configure Nginx routing
5. Update README

### Environment Variables
Each service has its own `.env` file with database configuration.

## Deployment

### Production Considerations
- Use HTTPS certificates
- Configure proper database backups
- Set up monitoring and logging
- Use environment-specific configurations

## License
MIT
