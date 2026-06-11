# Breakbeat Calendar

## Content
- [Database](#database)
    - [Database migrations](#database-migrations)
- [Authentication](#authentication)
    - [Access and Refresh tokens](#access-and-refresh-tokens)
- [How to run](#how-to-run)
    - [Installation script](#installation-script)
    - [Manual configuration](#manual-configuration)
        - [Python virtual environment](#python-virtual-environment)
        - [Frontend dependencies](#frontend-dependencies)
        - [API dependencies](#api-dependencies)
        - [Environment variables](#environment-variables)
    - [Docker](#docker)

## Database

Breakbeat uses PostgreSQL as it's primary database

You can self-host PostgreSQL or use a managed provider

I personally use [NeonDB](https://neon.com/) because it's easy to maintain, fast to configure and has free tier

### Database Migrations

Database migrations are handled using [Alembic](https://alembic.sqlalchemy.org/en/latest/)

> [!WARNING]
> Warning: Breakbeat Calendar is currently in active development. Migrations must be run manually for now. In future it will be maintained by installation script

Run migrations:

1. Create and activate [python virtual environment](#python-virtual-environment) if you haven't done it yet

2. Install [API dependencies](#api-dependencies) if you haven't done it yet

3. Ensure your database is running and reachable

4. If you did [manual configuration](#manual-configuration) make sure your `api/.env.local` has a correct db connection string

5. Run:
```bash
cd api
alembic upgrade head
```

## Authentication

### Access and Refresh tokens

Breakbeat Calendar uses JWT-based authentication with two token types:

- **Access token** - short-lived token used for API requests

- **Refresh token** - long-lived token used to generate new access tokens

Tokens lifetime settings are configurable via [environment variables](#manual-configuration)

## How to run

### Installation script

> [!WARNING]
> If you see this it means it's not ready yet ¯\\_(ツ)_/¯

### Manual Configuration

There multiple steps to run this project manually. This guide will show you how to do it step-by-step. For those who knows what are they doing, here is a short list:

1. Clone this repository by:
```bash
git clone https://github.com/takiido/breakbeat.git
```

2. Create [python virtual environment](#python-virtual-environment) in `api` folder

3. Install [API](#api-dependencies) and [frontend](#frontend-dependencies) dependencies

3. Set-up database and run [migrations](#database-migrations)

4. Configure [environment variables](#environment-variables)

#### Python virtual environment

You can create a python virtual environment by running:

```bash
cd api
python -m venv .venv
# If you use nushell this will not work. Read this https://github.com/nushell/nushell/issues/852
source api/.venv/bin/activate
```

#### Frontend dependencies

1. Install dependencies by running:

```bash
cd frontend
npm install
```

#### API dependencies

1. Install dependencies by running:

```bash
pip install -r requirements.txt
```

#### Environment variables

1. Create environment variables files
```bash
cp .env.example .env
cp frontend/.env.example frontend/.env.local
cp api/.env.example api/.env.local
```

2. Edit api `.env.local` replacing:
- `DB_URL` with your connection string to your PostgreSQL database
- `JWT_SECRET` with your jwt token secret. You can generate it with:
```bash
# make sure you have openssl installed
openssl rand -hex 32
```
- `ACCESS_TOKEN_EXPIRE_MINUTES` with desired access token expiration time (default: 15)
- `REFRESH_TOKEN_EXPIRE_DAYS` with desired refresh token expiration - (default: 14)

3. Edit frontend `.env.local` replacing:
- `API_URL` with your API url - default: http://localhost:8000

### Docker

If you did all the steps right the only thing you need to do is:
```bash
docker compose up
```
