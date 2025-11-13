# GitHub Copilot Instructions for DOCKER-uvicorn-gunicorn

## Project Overview

This repository maintains a Docker base image that combines Uvicorn and Gunicorn for high-performance FastAPI web applications in Python. The image includes performance auto-tuning and developer-friendly utilities.

**Key Technologies:**
- Docker (multi-platform: amd64, arm64)
- Python (3.11, 3.12, 3.13)
- Uvicorn (ASGI server)
- Gunicorn (WSGI HTTP server with Uvicorn workers)
- FastAPI
- Zsh with Oh-My-Zsh and Powerlevel10k theme

## Repository Structure

```
.
├── 3.11/                   # Python 3.11 Dockerfiles
│   ├── bookworm/          # Debian bookworm base
│   └── bookworm-slim/     # Slim variant
├── 3.12/                   # Python 3.12 Dockerfiles
│   ├── bookworm/
│   └── bookworm-slim/
├── 3.13/                   # Python 3.13 Dockerfiles
│   ├── trixie/
│   └── trixie-slim/
├── app/                    # Sample FastAPI application
│   └── main.py
├── scripts/                # Container startup scripts
│   ├── gunicorn_conf.py   # Gunicorn configuration
│   ├── start-gunicorn     # Main startup script
│   └── start-reload       # Development reload script
├── build_and_tag.py        # Docker build/tag automation
└── requirements.txt        # Python dependencies
```

## Building and Testing

### Building Docker Images

**Test Build (single architecture):**
```bash
python build_and_tag.py <version> --test
```

**Production Build (multi-architecture):**
```bash
python build_and_tag.py <version>
```

**Build with Test Run:**
```bash
python build_and_tag.py <version> --test --run
```

### Testing Changes

1. **Local Docker Testing:**
   ```bash
   # Build a test image
   docker build -t test-uvicorn-gunicorn -f 3.12/bookworm-slim/Dockerfile .
   
   # Run the test container
   docker run -d -p 80:80 --name test-container test-uvicorn-gunicorn
   
   # Check logs
   docker logs test-container
   
   # Test the endpoint
   curl http://localhost:80
   
   # Cleanup
   docker stop test-container && docker rm test-container
   ```

2. **Testing Scripts:**
   - Startup scripts are located in `scripts/` directory
   - Test script modifications in a running container before committing
   - Ensure shell scripts maintain POSIX compatibility where possible

### Linting

- **Python Code:** Follow PEP 8 standards
- **Shell Scripts:** Use shellcheck for validation when available
- **Dockerfile:** Follow Docker best practices (minimize layers, use specific tags, etc.)

## Contribution Guidelines

### Code Standards

1. **Dockerfiles:**
   - Use multi-stage builds when appropriate
   - Minimize image layers
   - Clean up apt cache in the same RUN command as apt-get install
   - Use specific base image versions, not `latest`
   - Set appropriate LABEL metadata including version

2. **Python Code:**
   - Follow PEP 8 style guide
   - Use type hints where appropriate
   - Keep dependencies minimal and up-to-date

3. **Shell Scripts:**
   - Use `set -e` to exit on error
   - Quote variables to prevent word splitting
   - Use meaningful variable names
   - Add comments for complex logic

4. **Version Management:**
   - Follow semantic versioning (MAJOR.MINOR.PATCH)
   - Update version numbers in build_and_tag.py when creating releases
   - Keep README.md badges up to date

### Pull Request Guidelines

- **Keep changes minimal and focused** on a single issue or feature
- **Test all changes** thoroughly before submitting
- **Document breaking changes** clearly in the PR description
- **Update README.md** if user-facing behavior changes
- **Ensure multi-platform compatibility** (amd64 and arm64) for Docker images

### Commit Messages

- Use clear, descriptive commit messages
- Start with a verb in imperative mood (e.g., "Add", "Fix", "Update", "Remove")
- Keep the first line under 72 characters
- Add detailed explanation in the body if needed

## Design Principles

1. **Performance First:** Optimize for production FastAPI workloads with auto-tuning
2. **Developer Experience:** Include useful utilities (zsh, oh-my-zsh, vim, curl, etc.)
3. **Flexibility:** Allow users to customize via environment variables and config files
4. **Multi-Platform:** Build and test for both amd64 and arm64 architectures
5. **Minimal Base:** Keep slim variants as small as possible while maintaining functionality
6. **Security:** Keep dependencies updated and minimize attack surface

## Environment Variables

Key environment variables that can be customized:

- `MODULE_NAME`: Python module name (default: main or app.main)
- `VARIABLE_NAME`: FastAPI app variable name (default: app)
- `APP_MODULE`: Full module path (default: "$MODULE_NAME:$VARIABLE_NAME")
- `GUNICORN_CONF`: Path to gunicorn config (default: /gunicorn_conf.py)
- `WORKER_CLASS`: Gunicorn worker class (default: uvicorn.workers.UvicornWorker)
- `PRE_START_PATH`: Path to prestart script (default: /app/prestart)

## Important Notes

### Prestart Scripts
Users can add a `/app/prestart` script to run migrations or other setup tasks before the server starts. This should be a shell script with execute permissions.

### Custom Gunicorn Configuration
Users can override the default gunicorn configuration by placing their own `gunicorn_conf.py` in the `/app` directory.

### Base Image Dependency
The Dockerfiles depend on `aliciousness/python-base` images. Changes to the base image may require updates here.

## Working with Issues

- Look for issues labeled with `good first issue` for newcomers
- Check CI/CD workflow status before making changes
- Test thoroughly before marking issues as complete
- Reference the issue number in commit messages (e.g., "Fix #123: ...")

## Dependencies

Core Python packages (in requirements.txt):
- uvicorn[standard] - ASGI server implementation
- gunicorn - WSGI HTTP server
- fastapi[all] - Modern web framework
- python-dotenv - Environment variable management
- pydantic - Data validation

When updating dependencies:
- Test compatibility with all supported Python versions
- Check for breaking changes in release notes
- Update requirements.txt with specific versions
- Test build process after updates
