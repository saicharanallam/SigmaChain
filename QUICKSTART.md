# Quick Start Guide

## Prerequisites Check

```bash
# Check Docker version
docker --version

# Check Docker Compose V2 (included with Docker)
docker compose version
```

If you see `docker compose version`, you're good to go! If not, Docker Compose V2 should be included with your Docker installation.

## Quick Start (3 Steps)

### Step 1: Create Environment File

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

### Step 2: Start Services

```bash
docker compose up -d
```

This will:
- Build the Docker images
- Download the Stable Diffusion model (first time only, ~5GB, takes 10-20 minutes)
- Start both backend and frontend services

### Step 3: Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Useful Commands

```bash
# View logs
docker compose logs -f

# Stop services
docker compose down

# Restart services
docker compose restart

# Rebuild after code changes
docker compose up -d --build

# View running containers
docker compose ps
```

## First Run Notes

- **Model Download**: The first run downloads the Stable Diffusion model (~5GB). This only happens once.
- **Generation Time**: 
  - CPU: 30-60 seconds per image
  - GPU: 5-10 seconds per image (if GPU enabled)
- **Memory**: Requires 8GB+ RAM (16GB recommended)

## Troubleshooting

### Port Already in Use

If ports 3000 or 8000 are busy, modify `docker-compose.yml`:
```yaml
ports:
  - "3001:3000"  # Change frontend port
  - "8001:8000"  # Change backend port
```

### Out of Memory

Reduce image resolution in `backend/agents/image_generator.py`:
```python
width=512,   # Reduce from 1024
height=512,  # Reduce from 1024
```

### View Logs for Errors

```bash
docker compose logs backend
docker compose logs frontend
```

For more detailed troubleshooting, see [DOCKER_SETUP.md](DOCKER_SETUP.md).

