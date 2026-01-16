# Friday Jarvis - LiveKit Cloud Deployment Guide

This document explains how to deploy the Friday Jarvis agent to LiveKit Cloud.

## Prerequisites

1. **LiveKit Cloud Account**: Sign up at [cloud.livekit.io](https://cloud.livekit.io)
2. **LiveKit CLI**: Install the LiveKit CLI tool
   ```bash
   npm install -g livekit
   # or
   brew install livekit-cli
   ```
3. **Docker** (optional): For testing builds locally
4. **Environment Variables**: You'll need:
   - `LIVEKIT_URL`: Your LiveKit Cloud server URL
   - `LIVEKIT_API_KEY`: Your API key
   - `LIVEKIT_API_SECRET`: Your API secret
   - `OPENAI_API_KEY`: OpenAI API key (or other LLM provider keys)
   - `DEEPGRAM_API_KEY`: Deepgram API key (optional, for speech-to-text)
   - Any other API keys your agent uses

## Deployment Steps

### 1. Create a LiveKit Cloud Project

If you haven't already, create a project in LiveKit Cloud:

- Visit https://cloud.livekit.io
- Create a new project
- Copy your `LIVEKIT_URL`, `LIVEKIT_API_KEY`, and `LIVEKIT_API_SECRET`

### 2. Configure Environment Variables

Use LiveKit Cloud's secrets management to store sensitive environment variables:

```bash
lk project secrets set OPENAI_API_KEY "your-key-here"
lk project secrets set DEEPGRAM_API_KEY "your-key-here"
# Add other API keys as needed
```

**Important**: Do NOT include these in your `.env` file or commit them to source control. LiveKit Cloud will inject them at runtime.

### 3. Deploy Using LiveKit CLI

```bash
# Initial deployment
lk agent create

# Or deploy to an existing agent
lk agent deploy
```

The CLI will:

1. Read your Dockerfile
2. Build the container image on LiveKit Cloud
3. Push it to the registry
4. Deploy it automatically

### 4. Monitor Your Deployment

```bash
# View deployment status
lk agent list

# View logs
lk agent logs

# View build logs
lk agent logs --build
```

## Dockerfile Overview

The included `Dockerfile` is configured for LiveKit Cloud deployment with the following features:

- **Base Image**: `python:3.11-slim` - Lightweight Python runtime
- **Non-root User**: Runs as unprivileged `appuser` for security
- **Build Caching**: Dependencies are cached for faster rebuilds
- **Health Check**: Includes health check endpoint on `:8081`
- **Virtual Environment**: Uses Python venv for clean dependency isolation

## Project Structure Requirements

For the Dockerfile to work correctly, ensure your project structure matches:

```
friday_jarvis/
├── Dockerfile
├── .dockerignore
├── requirements.txt
├── agent.py          # Main agent entrypoint
├── prompts.py
├── server.py
├── tools.py
└── README.md
```

## Customizing the Dockerfile

If you need to modify the Dockerfile:

1. **Change Python Version**: Modify `ARG PYTHON_VERSION=3.11`
2. **Install System Packages**: Add packages before `RUN pip install -r requirements.txt`
3. **Pre-download Models**: Add commands before the final `CMD`

Example for downloading models at build time:

```dockerfile
# Pre-download any ML models the agent needs
RUN python -c "from livekit.plugins import openai; openai.download_files()"
```

## Memory and CPU Requirements

Based on LiveKit recommendations:

- **Minimum**: 2 cores, 4GB RAM
- **Recommended**: 4 cores, 8GB RAM
- **Estimated Concurrency**: 10-25 concurrent jobs per agent server

Configure this in LiveKit Cloud when creating your deployment.

## Security Best Practices

1. ✅ Non-root user in Dockerfile
2. ✅ No secrets in image (injected at runtime)
3. ✅ Use `.dockerignore` to exclude sensitive files
4. ✅ Environment variables via LiveKit Cloud secrets management
5. ✅ Pin dependency versions in `requirements.txt`

## Troubleshooting

### Build Fails

- Check build logs: `lk agent logs --build`
- Ensure build completes within 10-minute timeout
- Verify all dependencies are in `requirements.txt`

### Agent Won't Start

- Check deployment logs: `lk agent logs`
- Verify `agent.py` has the correct entrypoint
- Ensure environment variables are properly set

### High Memory Usage

- Profile your agent with `-u` unbuffered flag
- Consider reducing concurrent job limits
- Check for memory leaks in async code

### Connection Issues

- Verify `LIVEKIT_URL` is correct (should include port, e.g., `wss://example.livekit.cloud`)
- Check that `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET` are correct
- Ensure network allows WebSocket connections to LiveKit Cloud

## Testing Locally with Docker

To test your Docker image locally:

```bash
# Build locally
docker build -t friday-jarvis:latest .

# Run with environment variables (get these from LiveKit Cloud)
docker run -e LIVEKIT_URL="your-url" \
           -e LIVEKIT_API_KEY="your-key" \
           -e LIVEKIT_API_SECRET="your-secret" \
           -e OPENAI_API_KEY="your-key" \
           friday-jarvis:latest
```

## Additional Resources

- [LiveKit Agents Documentation](https://docs.livekit.io/agents/)
- [LiveKit Cloud Deployment Guide](https://docs.livekit.io/deploy/agents/cloud/)
- [LiveKit Docker Best Practices](https://docs.livekit.io/deploy/agents/cloud/builds/)
- [Custom Deployments](https://docs.livekit.io/deploy/custom/deployments/)

## Next Steps

After your first deployment:

1. **Set up monitoring**: Use LiveKit Cloud's dashboard to monitor agent health
2. **Configure autoscaling**: Scale agent instances based on load
3. **Add regional deployments**: Deploy to multiple regions for lower latency
4. **Enable analytics**: Monitor agent performance and usage patterns

---

For questions or issues, visit the [LiveKit Slack Community](https://livekit.io/join-slack)
