# Friday Jarvis - AI Voice Assistant 🎙️

A sophisticated voice-powered AI assistant built with LiveKit and Google Gemini, inspired by Iron Man's J.A.R.V.I.S. This agent provides real-time voice interaction with smart home control, web search, weather updates, and more.

## 🌟 Features

### Voice Interaction

- **Real-time Voice AI**: Powered by Google Gemini 2.5 Flash with native audio support
- **Natural Conversation**: Uses "Charon" voice for a butler-like persona
- **Turkish Language Support**: Fully localized assistant personality

### Smart Home Control (MQTT)

- **Curtain Control**: Open and close curtains via voice commands
- **Light Management**:
  - Yellow light control (on/off)
  - Navy light control (on/off)
- **HiveMQ Integration**: Cloud MQTT broker for reliable IoT communication

### Utility Functions

- **Weather Information**: Get current weather for any city using wttr.in API
- **Web Search**: DuckDuckGo web search integration
- **Date & Time**: Retrieve current date and time on request

## 🏗️ Architecture

```
friday_jarvis/
├── agent.py           # Main LiveKit agent with Gemini integration
├── tools.py           # Function tools (weather, search, smart home)
├── prompts.py         # AI personality and behavior instructions
├── server.py          # MQTT server for IoT device communication
├── requirements.txt   # Python dependencies
├── Dockerfile         # Container configuration for deployment
├── DEPLOYMENT.md      # LiveKit Cloud deployment guide
└── .env              # Environment variables (not committed)
```

## � Getting Started

### Prerequisites

- Python 3.11+
- LiveKit account (for cloud deployment)
- Google Gemini API access
- HiveMQ Cloud account (for MQTT)

### Installation

1. **Clone the repository**

   ```bash
   cd c:\Users\yahya\Documents\CODES\Piton\AiAgent\LivekitGemini\friday_jarvis
   ```

2. **Create virtual environment**

   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   Create a `.env` file:

   ```env
   LIVEKIT_URL=wss://your-livekit-url
   LIVEKIT_API_KEY=your-api-key
   LIVEKIT_API_SECRET=your-api-secret
   GOOGLE_API_KEY=your-gemini-api-key
   ```

### Running Locally

```bash
python agent.py
```

Or use LiveKit CLI:

```bash
lk agent dev
```

## 🛠️ Configuration

### AI Personality (prompts.py)

The assistant is configured with a butler-like persona that:

- Speaks with sophistication and elegance
- Uses sarcastic humor when helping
- Responds in concise, single-sentence replies
- Addresses the user formally ("efendim" - Turkish for "sir")

### Available Tools (tools.py)

| Tool                    | Description                     | Usage                             |
| ----------------------- | ------------------------------- | --------------------------------- |
| `get_time`              | Returns current date and time   | "What time is it?"                |
| `get_weather`           | Fetches weather for a city      | "What's the weather in Istanbul?" |
| `search_web`            | Searches the web via DuckDuckGo | "Search for Python tutorials"     |
| `open_curtain`          | Opens curtains via MQTT         | "Open the curtains"               |
| `close_curtain`         | Closes curtains via MQTT        | "Close the curtains"              |
| `turn_on_yellow_light`  | Activates yellow light          | "Turn on yellow light"            |
| `turn_off_yellow_light` | Deactivates yellow light        | "Turn off yellow light"           |
| `turn_on_navy_light`    | Activates navy light            | "Turn on navy light"              |
| `turn_off_navy_light`   | Deactivates navy light          | "Turn off navy light"             |

### MQTT Configuration (server.py)

The MQTT server connects to HiveMQ Cloud:

- **Broker**: `4009a741e78f4f9989efe8f6315ff960.s1.eu.hivemq.cloud`
- **Port**: 8883 (TLS)
- **Topics**: `home/#` (curtain, yellow, navy)

## 📦 Dependencies

Key libraries:

- `livekit-agents` - LiveKit agent framework
- `livekit-plugins-google` - Google Gemini integration
- `duckduckgo-search` - Web search functionality
- `paho-mqtt` - MQTT client for IoT
- `requests` - HTTP client for weather API
- `langchain_community` - Community tools for LangChain

## 🐳 Deployment

### Docker Build

```bash
docker build -t friday-jarvis:latest .
```

### LiveKit Cloud Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

Quick deploy:

```bash
lk agent deploy
```

## 🔐 Security

- Non-root user in Docker container
- Environment variables for sensitive data
- TLS encryption for MQTT communication
- No hardcoded credentials (use `.env`)

## 🎯 Usage Examples

**Example Conversation:**

```
User: "Merhaba Buğra"
Buğra: "Merhaba, benim adım Buğra, kişisel asistanınızım, nasıl yardımcı olabilirim?"

User: "What's the weather in Istanbul?"
Buğra: "Tabikide efendim, Istanbul için hava durumunu getiriyorum."

User: "Turn on the yellow light"
Buğra: "Anlaşıldı efendim, sarı ışığı açıyorum."
```

## 🧪 Testing

Run the agent in development mode with LiveKit:

```bash
lk agent dev
```

Test MQTT connections:

```bash
python -c "from tools import mqtt_server; mqtt_server.publish('home/curtain', 'ON')"
```

## 📝 Customization

### Adding New Tools

1. Define a function in `tools.py`:

   ```python
   @function_tool()
   async def my_tool(context: RunContext, param: str) -> str:
       """
       Tool description for the AI.
       """
       # Your implementation
       return result
   ```

2. Register in `agent.py`:
   ```python
   tools=[
       # ... existing tools
       my_tool,
   ]
   ```

### Modifying Personality

Edit `AGENT_INSTRUCTION` in `prompts.py` to change:

- Speaking style
- Response length
- Tone and formality
- Language preferences

## 🤝 Contributing

This is a personal project, but feel free to fork and customize for your own use!

## 📄 License

This project is for personal/educational use.

## 🔗 Resources

- [LiveKit Documentation](https://docs.livekit.io/agents/)
- [Google Gemini API](https://ai.google.dev/)
- [HiveMQ Cloud](https://www.hivemq.com/mqtt-cloud-broker/)
- [DEPLOYMENT.md](DEPLOYMENT.md) - Full deployment guide

---

> "And in case I don't see ya, good afternoon, good evening, and good night!"
> **— Yahya 👋**
