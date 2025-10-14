# Containerization Guide

This guide covers Docker containerization and container deployment strategies.

## Overview

Containerization provides:
- **Consistent Environments** - Reproducible development and production environments
- **Easy Deployment** - Simplified application deployment and scaling
- **Dependency Isolation** - Self-contained applications with all dependencies
- **Development Workflow** - Standardized development containers

For commands, see [Command Cheatsheet](../command-cheatsheet.md#docker-commands).

## Container Strategy

### Development Containers

**VS Code Dev Containers:**
- Pre-configured development environment
- Consistent tooling across team members
- Isolated from host system dependencies

**Local Development:**
```bash
# Future: Local development with Docker
docker build -t nk-uv-demo:dev .
docker run -it --rm nk-uv-demo:dev
```

### Production Containers

**Multi-stage Builds:**
- Optimized container size
- Separate build and runtime environments
- Security through minimal runtime images

**Container Registry:**
- Automated container building in CI
- Version tagging aligned with package versions
- Security scanning of container images

## Docker Configuration

### Dockerfile Structure

```dockerfile
# Multi-stage build example (future implementation)

# Build stage
FROM python:3.12-slim as builder
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN pip install uv && uv sync --frozen

# Runtime stage
FROM python:3.12-slim as runtime
COPY --from=builder /app/.venv /app/.venv
COPY src/ /app/src/
WORKDIR /app
ENV PATH="/app/.venv/bin:$PATH"
CMD ["python", "-m", "nk_uv_demo"]
```

### Docker Compose

**Development Environment:**
```yaml
# docker-compose.dev.yml (future implementation)
version: '3.8'
services:
  app:
    build: .
    volumes:
      - .:/app
      - /app/.venv
    environment:
      - PYTHONPATH=/app/src
```

## Container CI/CD Integration

### Automated Building

**Container Workflow:**
- Build containers on every commit
- Tag with git commit SHA and version
- Push to container registry
- Run security scans on images

**Registry Strategy:**
```yaml
# Future GitHub Actions workflow
- name: Build and push container
  uses: docker/build-push-action@v5
  with:
    push: true
    tags: |
      ghcr.io/ac-willeke/nk-uv-demo:latest
      ghcr.io/ac-willeke/nk-uv-demo:${{ github.sha }}
```

### Container Security

**Security Scanning:**
- Vulnerability scanning with Trivy
- Base image security updates
- Non-root user configuration
- Minimal attack surface

**Security Best Practices:**
```dockerfile
# Security hardening (future implementation)
RUN groupadd -r appuser && useradd -r -g appuser appuser
USER appuser
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s \
  CMD python -c "import sys; sys.exit(0)"
```

## Deployment Strategies

### Container Orchestration

**Kubernetes Deployment:**
- Helm charts for configuration management
- Horizontal pod autoscaling
- Rolling deployments with zero downtime
- Resource limits and requests

**Docker Swarm (Alternative):**
- Simpler orchestration for smaller deployments
- Built-in load balancing
- Service discovery

### Environment Management

**Configuration:**
- Environment-specific configs via ConfigMaps
- Secrets management for sensitive data
- Health checks and monitoring
- Logging and observability

## Development Workflow

### Container Development

**Dev Container Setup:**
1. Install VS Code Dev Containers extension
2. Open project in container
3. Automatic environment setup
4. Consistent tooling and dependencies

**Hot Reloading:**
- Volume mounts for source code
- Automatic dependency installation
- Debug configuration

### Testing Containers

**Container Testing:**
```bash
# Future: Container testing workflow
docker build -t nk-uv-demo:test .
docker run --rm nk-uv-demo:test pytest
docker run --rm nk-uv-demo:test ruff check
```

**Integration Testing:**
- Multi-container test environments
- Database and service dependencies
- End-to-end testing scenarios

## Monitoring and Observability

### Container Metrics

**Health Monitoring:**
- Container health checks
- Application metrics collection
- Log aggregation and analysis
- Performance monitoring

**Observability Stack:**
- Prometheus for metrics
- Grafana for visualization
- ELK/EFK for logging
- Jaeger for distributed tracing

## Future Implementation

### Planned Features

1. **Dev Container Configuration**
   - `.devcontainer/devcontainer.json`
   - Pre-configured development environment
   - VS Code extensions and settings

2. **Production Dockerfile**
   - Multi-stage optimized builds
   - Security hardening
   - Health checks and monitoring

3. **Container CI/CD**
   - Automated container builds
   - Security scanning integration
   - Container registry publishing

4. **Kubernetes Manifests**
   - Deployment configurations
   - Service definitions
   - Ingress and networking

5. **Docker Compose Configurations**
   - Development environment
   - Testing environment
   - Local production simulation

### Implementation Priority

1. **Phase 1:** Basic Dockerfile and dev container
2. **Phase 2:** CI/CD container building and publishing
3. **Phase 3:** Production deployment configurations
4. **Phase 4:** Orchestration and scaling setup

## Configuration Files

### Container Configuration Files (Future)
- `Dockerfile` - Production container build
- `docker-compose.yml` - Multi-service development
- `.dockerignore` - Build context optimization
- `.devcontainer/devcontainer.json` - VS Code dev container
- `k8s/` - Kubernetes deployment manifests

### Security Configuration
- Container security policies
- Registry authentication
- Image signing and verification
- Runtime security monitoring

This guide will be expanded as containerization features are implemented. Current focus is on establishing the foundation for future container adoption.
