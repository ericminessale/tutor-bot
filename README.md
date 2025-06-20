# SignalWire AI Tutor Bot Demo

A comprehensive demonstration of the SignalWire AI Agent SDK's context/steps feature, showcasing how context-level prompts enable unique teaching philosophies for different subjects.

## 🌟 Features Demonstrated

- **Context-Level Prompts**: Each subject has its own teaching personality and approach
- **Context Isolation**: Teaching philosophies remain separate and don't interfere
- **Multi-Language Support**: Language tutors can speak in their respective languages using ElevenLabs multilingual voices
- **Structured Workflows**: Clear progression through learning steps
- **Pedagogical Diversity**: Different teaching methods for different subjects

## 🎓 Available Tutors

### Professor Marcus - Math Tutor
- **Philosophy**: Mathematics is the language of logic and patterns
- **Approach**: Systematic problem-solving with visual understanding
- **Workflow**: Assessment → Guided Solution → Practice

### Language Tutors
- **Señora Lopez (Spanish)**: Immersion-based learning with cultural connection
- **Madame Dubois (French)**: Focus on elegance, precision, and pronunciation
- **Tanaka-sensei (Japanese)**: Cultural understanding and respect

### Dr. Stevens - Science Tutor
- **Philosophy**: Learning through inquiry and experimentation
- **Approach**: Socratic method, hypothesis formation
- **Workflow**: Inquiry → Hypothesis → Exploration

### Professor Thompson - History Tutor
- **Philosophy**: History as human experience and its lessons
- **Approach**: Narrative analysis and cause-effect relationships

## 🚀 Quick Start

### 1. Clone and Setup

```bash
# Clone the repository (or copy the files)
cd "Tutor Bot"

# Run the setup script
python setup.py
```

The setup script will:
- Create a virtual environment
- Install all dependencies
- Set up configuration files

### 2. Configure (Optional)

Copy `.env.example` to `.env` and customize if needed:

```bash
cp .env.example .env
```

### 3. Set Up Public Access (Required for SignalWire)

⚠️ **Important**: SignalWire needs a publicly accessible URL to send calls to your agent. Localhost alone won't work!

#### Option A: Using ngrok (Recommended for Testing)

1. **Install ngrok**:
   - Download from [ngrok.com](https://ngrok.com/download)
   - Or install via package manager:
     ```bash
     # macOS
     brew install ngrok/ngrok/ngrok
     
     # Windows (with Chocolatey)
     choco install ngrok
     ```

2. **Start your agent first**:
   ```bash
   # Windows
   run.bat
   
   # macOS/Linux
   ./run.sh
   ```
   The agent will start on port 3000 by default.

3. **In a new terminal, start ngrok**:
   ```bash
   ngrok http 3000
   ```

4. **Copy your public URL**:
   ngrok will display something like:
   ```
   Forwarding  https://abc123.ngrok-free.app -> http://localhost:3000
   ```
   Your SignalWire webhook URL will be: `https://abc123.ngrok-free.app/tutor`

#### Option B: Using localtunnel

```bash
# Install localtunnel
npm install -g localtunnel

# Start tunnel on port 3000
lt --port 3000 --subdomain your-custom-name

# Your URL will be: https://your-custom-name.loca.lt/tutor
```

#### Option C: Using cloudflared (Cloudflare Tunnel)

```bash
# Install cloudflared
# Visit: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/

# Start tunnel
cloudflared tunnel --url http://localhost:3000

# Your URL will be provided in the output
```

### 4. Configure SignalWire

1. Log into your [SignalWire Space](https://signalwire.com)
2. Go to **AI Gateway** → **AI Agents**
3. Create a new agent or update existing one
4. Set the webhook URL to your public URL (e.g., `https://abc123.ngrok-free.app/tutor`)
5. Save and test with a phone call

## 📋 System Requirements

- Python 3.8 or higher
- Internet connection (for SignalWire API and proxy)
- Approximately 500MB disk space for dependencies
- A proxy tool (ngrok, localtunnel, or similar) for public access

## 🔧 Configuration Options

Edit `.env` to customize:

```env
# Server Configuration
TUTOR_BOT_HOST=0.0.0.0
TUTOR_BOT_PORT=3000
TUTOR_BOT_ROUTE=/tutor

# Debug Mode
DEBUG=false

# Optional: Override Multilingual Voice
MULTILINGUAL_VOICE=elevenlabs.bIHbv24MWmeRgasZH58o:multilingual

# SignalWire Credentials (if using authentication)
# SIGNALWIRE_USERNAME=your_username
# SIGNALWIRE_PASSWORD=your_password
```

### 🎙️ Voice Configuration

The tutor bot uses ElevenLabs voices for multilingual support:

**Default Voices:**
- **Multilingual Voice** (EN/ES/FR): `elevenlabs.bIHbv24MWmeRgasZH58o:multilingual`
- **Japanese Voice**: `elevenlabs.Mv8AjrYZCBkdsmDHNwcB`

**Why different voice setups?**
- The multilingual voice handles seamless code-switching between English, Spanish, and French
- Japanese uses a dedicated voice for authentic pronunciation
- This mirrors real-world language teaching scenarios

**Alternative Multilingual Voice Options:**
You can customize the multilingual voice in `.env`:
```env
# Female voices
MULTILINGUAL_VOICE=elevenlabs.21m00Tcm4TlvDq8ikWAM:rachel
MULTILINGUAL_VOICE=elevenlabs.EXAVITQu4vr4xnSDxMaL:bella

# Male voices  
MULTILINGUAL_VOICE=elevenlabs.ErXwobaYiN019PkySvjV:antoni
MULTILINGUAL_VOICE=elevenlabs.VR6AewLTigWG4xSOukaG:arnold
```

## 🎯 How It Works

### Context Flow

```
┌─────────────┐
│   Triage    │ ← Entry point: "What subject do you need help with?"
└──────┬──────┘
       │
       ├─→ Math Context (Professor Marcus)
       ├─→ Language Selection ─┬─→ Spanish (Señora Lopez)
       │                       ├─→ French (Madame Dubois)
       │                       └─→ Japanese (Tanaka-sensei)
       ├─→ Science Context (Dr. Stevens)
       ├─→ History Context (Professor Thompson)
       └─→ Other Context (General Tutor)
```

### Key Concepts

1. **Context Isolation**: Each context has `.set_isolated(True)` to maintain separate teaching personalities
2. **Context-Level Prompts**: Teaching philosophy is defined at the context level, not in individual steps
3. **Step Progression**: Each context has structured steps with completion criteria
4. **Navigation Control**: Steps define which contexts/steps can be accessed next

## 🛠️ Extending the Demo

### Adding Skills

To enhance the tutors with additional capabilities:

```python
# Add web search for smarter responses
self.add_skill("web_search", {
    "api_key": os.getenv("GOOGLE_SEARCH_API_KEY"),
    "search_engine_id": os.getenv("GOOGLE_SEARCH_ENGINE_ID")
})

# Add math calculations
self.add_skill("math")

# Add datetime for scheduling
self.add_skill("datetime")
```

### Creating New Subjects

To add a new subject tutor:

```python
# Create new context
programming = contexts.add_context("programming") \
    .set_isolated(True) \
    .add_section("Role", "You are Professor Ada, a programming mentor...") \
    .add_section("Teaching Philosophy", "Code is poetry that computers can understand...")

# Add steps
programming.add_step("language_choice") \
    .add_section("Current Task", "Determine which programming language to teach") \
    .set_step_criteria("Programming language selected") \
    .set_valid_steps(["concept_introduction"])
```

## 📚 Understanding the Code Structure

### Main Components

1. **TutorBotAgent Class**: The main agent with all contexts and steps
2. **Context Definitions**: Each subject is a separate context with unique prompts
3. **Step Workflows**: Learning progression within each subject
4. **Language Support**: Multi-language configuration with ElevenLabs voices

### Context vs Step Prompts

- **Context Prompts**: Define the overall teaching personality
- **Step Prompts**: Define specific tasks within the learning process

## 🐛 Troubleshooting

### Common Issues

1. **"Can't connect to agent"**
   - Ensure you've set up a proxy (ngrok, localtunnel, etc.)
   - Check that the proxy is running and forwarding to the correct port
   - Verify the webhook URL in SignalWire matches your proxy URL

2. **Port Already in Use**
   ```bash
   # Change port in .env
   TUTOR_BOT_PORT=3001
   # Remember to update your proxy command too:
   ngrok http 3001
   ```

3. **ngrok Connection Issues**
   - Free ngrok has session limits; consider creating a free account
   - Try restarting both the agent and ngrok
   - Check ngrok dashboard for errors: http://localhost:4040

4. **Dependencies Not Installing**
   ```bash
   # Try upgrading pip first
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

5. **Voice Not Working**
   - Ensure you're using valid ElevenLabs voice IDs
   - Check that SignalWire has ElevenLabs integration enabled
   - Try with default voices first before customizing

## 🤝 Contributing

This is a demo project showcasing SignalWire AI Agent SDK features. Feel free to:
- Add new subject tutors
- Enhance existing tutors with skills
- Improve teaching workflows
- Add more languages

## 📄 License

This demo is provided as-is for educational purposes.

## 🔗 Resources

- [SignalWire AI Agent SDK](https://github.com/signalwire/signalwire-agents)
- [SignalWire Documentation](https://docs.signalwire.com)
- [Context/Steps Guide](https://github.com/signalwire/signalwire-agents/docs/contexts_guide.md)
- [ElevenLabs Voice Library](https://elevenlabs.io/voices)
- [ngrok Documentation](https://ngrok.com/docs)

---

Built with ❤️ using SignalWire AI Agent SDK 
