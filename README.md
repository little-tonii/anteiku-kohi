# Anteiku-Kohi - Installation and Setup Guide

## Introduction

Anteiku-Kohi is a backend system for a mini food ordering store, built with modern technologies and design patterns for performance, security, and scalability. The system uses Domain Driven Design and CQRS patterns to create a maintainable and robust architecture.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white" alt="Python 3.11" />
  <img src="https://img.shields.io/badge/FastAPI-005571?logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/PostgreSQL-336791?logo=postgresql&logoColor=white" alt="PostgreSQL" />
  <img src="https://img.shields.io/badge/Redis-DD0031?logo=redis&logoColor=white" alt="Redis" />
  <img src="https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white" alt="Docker" />
  <img src="https://img.shields.io/badge/WebSocket-Communication-orange" alt="WebSocket" />
  <img src="https://img.shields.io/badge/JWT-Auth-000000?logo=jsonwebtokens&logoColor=white" alt="JWT" />
  <img src="https://img.shields.io/badge/Gunicorn-Worker-499848?logo=gunicorn&logoColor=white" alt="Gunicorn" />
  <img src="https://img.shields.io/badge/VNPay-Payment-blueviolet" alt="VNPay" />
</p>


## Technology Stack

- **Backend**: Python with FastAPI framework
- **Database**: PostgreSQL with SQLAlchemy (async support)
- **Caching**: Redis for API caching and performance optimization
- **Architecture**: Domain Driven Design (DDD) with Command Query Responsibility Segregation (CQRS)
- **Security**:
  - JWT authentication
  - API authorization
  - Rate limiting via Redis
  - CORS protection
- **Performance**:
  - Redis caching
  - Threaded image processing
  - Distributed locking with Redlock for race conditions
- **Concurrency**: Gunicorn multi-worker setup
- **Realtime Communication**: WebSocket integration
- **Payment Processing**: VNPay integration for online transactions
- **Deployment**: Docker & Docker Compose

## System Requirements

- Docker and Docker Compose
- Git (for cloning the repository)

## Step 1: Clone the Project

```bash
git clone https://github.com/little-tonii/Anteiku-Kohi.git
cd Anteiku-Kohi
```

## Step 2: Environment Configuration

The project requires two environment files:

1. Create `.env.database` for PostgreSQL configuration:

```
POSTGRES_USER=your_postgres_user
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=anteiku_kohi
```

2. Create `.env.app` using the provided example:

```
DATABASE_URL=postgresql+asyncpg://your_postgres_user:your_secure_password@anteiku_kohi_database:5432/anteiku_kohi
SECRET_KEY=your_generated_secret_key
HASH_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRES=1440
REFRESH_TOKEN_EXPIRES=10080
ANTEIKU_KOHI_EMAIL_APP_PASSWORD=your_email_app_password
ANTEIKU_KOHI_EMAIL=your_email@example.com
EMAIL_SALT_VERIFYCATION=your_email_salt

VNPAY_RETURN_URL=http://localhost:8000/order/payment-return
VNPAY_PAYMENT_URL=https://sandbox.vnpayment.vn/paymentv2/vpcpay.html
VNPAY_API_URL=https://sandbox.vnpayment.vn/merchant_webapi/api/transaction
VNPAY_TMN_CODE=your_vnpay_tmn_code
VNPAY_HASH_SECRET_KEY=your_vnpay_hash_secret

REDIS_URL=redis://anteiku_kohi_redis:6379
REDLOCK_URL_1=redis://anteiku_kohi_redlock_1:6379
REDLOCK_URL_2=redis://anteiku_kohi_redlock_2:6379
REDLOCK_URL_3=redis://anteiku_kohi_redlock_3:6379
```

You can generate a secure secret key with:
```bash
openssl rand -hex 32
```

## Step 3: Launch the Project

Start all services using Docker Compose:

```bash
docker compose up -d
```

This command:
- Pulls all required Docker images
- Builds the application container
- Sets up all services with health checks
- Configures volume mounts for persistent data

## Available Services and Ports

After startup, the following services will be available:

- **Main API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs or http://localhost:8000/redoc
- **PostgreSQL Database**: localhost:5432
- **Redis Cache**: localhost:6379
- **Redis Redlock Instances**:
  - Instance 1: localhost:6380
  - Instance 2: localhost:6381
  - Instance 3: localhost:6382
- **RedisInsight** (Redis management tool): http://localhost:5540

## Data Persistence

The project uses Docker volumes for persistent data storage:

- `postgres_data`: PostgreSQL database files
- `redis_data`: Redis cache data
- `redlock_1`, `redlock_2`, `redlock_3`: Redis Redlock instances data
- `meal_images`: Storage for uploaded meal images
- `redisinsight_data`: RedisInsight configuration and data

## Development Workflow

The Docker setup is configured for active development:

- Source code (`./src`): Mounted into the container, allowing live code changes
- Image storage: Configured with a persistent volume

To make changes:
1. Edit code in your local IDE
2. Changes are automatically reflected in the container
3. Restart the application if needed: `docker compose restart anteiku_kohi`

## System Management

### Viewing Logs

```bash
docker compose logs -f anteiku_kohi
```

You can replace `anteiku_kohi` with any service name to view specific logs.

### Stopping the Application

To stop all containers while preserving data:

```bash
docker compose down
```

To completely remove all containers and persistent data:

```bash
docker compose down -v
```

### Container Management

- Check status: `docker compose ps`
- Restart a service: `docker compose restart [service_name]`
- Rebuild after Dockerfile changes: `docker compose up -d --build anteiku_kohi`

## Email Configuration

For email verification functionality, you'll need to:
1. Use an email account with app password support (Gmail recommended)
2. Configure the `ANTEIKU_KOHI_EMAIL` and `ANTEIKU_KOHI_EMAIL_APP_PASSWORD` in `.env.app`
3. Set a unique `EMAIL_SALT_VERIFYCATION` value for security

## VNPay Integration

To test payment integration:
1. Register for a VNPay sandbox account
2. Update the `VNPAY_TMN_CODE` and `VNPAY_HASH_SECRET_KEY` in `.env.app`
3. The default configuration uses VNPay's sandbox environment
