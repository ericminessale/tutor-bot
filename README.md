# SignalWire AI Tutor Bot Demo

A comprehensive demonstration of the SignalWire AI Agent SDK's context/steps feature, showcasing how one intelligent tutor bot adapts its teaching approach and personality for different subjects using context-level prompts.

## 🌟 Features Demonstrated

- **Context-Level Prompts**: The tutor adapts its teaching personality and approach for each subject
- **Context Isolation**: Subject-specific teaching philosophies remain separate and don't interfere
- **Multi-Language Support**: Seamlessly switches languages for language tutoring using ElevenLabs multilingual voices
- **Structured Workflows**: Clear progression through learning steps within each subject
- **Pedagogical Diversity**: Different teaching methods automatically applied based on subject matter

## 🎓 Subject Specializations

The Tutor Bot dynamically adapts its teaching approach based on the subject:

### Math Mode - "Professor Marcus" Persona  
- **Philosophy**: Mathematics is the language of logic and patterns
- **Approach**: Systematic problem-solving with visual understanding
- **Workflow**: Assessment → Guided Solution → Practice

### Language Modes
- **Spanish Mode - "Señora Lopez" Persona**: Immersion-based learning with cultural connection
- **French Mode - "Madame Dubois" Persona**: Focus on elegance, precision, and pronunciation
- **Japanese Mode - "Tanaka-sensei" Transfer**: *Special case - actually transfers to specialized tutor with authentic Japanese voice*

### Science Mode - "Dr. Stevens" Persona
- **Philosophy**: Learning through inquiry and experimentation
- **Approach**: Socratic method, hypothesis formation
- **Workflow**: Inquiry → Hypothesis → Exploration

### History Mode - "Professor Thompson" Persona
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

**Security Note**: This demo has authentication disabled for easy testing. In production, you should enable authentication to prevent unauthorized access to your agent.

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
2. Go to **Phone Numbers** in the left sidebar
3. Click on a phone number (or purchase one if needed)
4. In the **Voice Settings** section:
   - Set **Handle Calls Using** to "SWML Script"
   - Choose **External** for the script type
   - Enter your public webhook URL: `https://abc123.ngrok-free.app/tutor`
   - Make sure the **Request Method** is set to "POST"
5. Click **Save** at the bottom of the page
6. Test by calling the phone number

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

# Note: This demo has authentication disabled by default
# The agent accepts all incoming webhook requests
# To enable authentication, modify the _check_basic_auth method in the code
```

### 🎙️ Voice Configuration

The tutor bot uses ElevenLabs voices for multilingual support:

**Default Voices:**
- **Multilingual Voice** (EN/ES/FR): `elevenlabs.bIHbv24MWmeRgasZH58o:multilingual`
- **Japanese Voice**: `elevenlabs.Mv8AjrYZCBkdsmDHNwcB`

**Why different voice setups?**
- The multilingual voice handles seamless code-switching between English, Spanish, and French
- Japanese uses a dedicated voice for authentic pronunciation and requires a different approach
- This mirrors real-world language teaching scenarios

**The Japanese Exception:**
Unlike other subjects where the tutor adapts its persona, Japanese actually transfers to a specialized "Tanaka-sensei" tutor with a dedicated Japanese voice. This is necessary because:
- Japanese pronunciation requires a native speaker voice
- Cultural nuances in Japanese teaching are unique
- The voice change creates an authentic immersion experience

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
       ├─→ Math Mode (Enhanced with "Professor Marcus" teaching style)
       ├─→ Language Selection ─┬─→ Spanish Mode ("Señora Lopez" persona)
       │                       ├─→ French Mode ("Madame Dubois" persona)
       │                       └─→ Japanese Transfer (to Tanaka-sensei)
       ├─→ Science Mode (Enhanced with "Dr. Stevens" teaching style)
       ├─→ History Mode (Enhanced with "Professor Thompson" teaching style)
       └─→ Other Mode (General tutoring capabilities)
```

### Key Concepts

1. **Context Isolation**: Each context has `.set_isolated(True)` to maintain separate teaching personalities within the same tutor
2. **Context-Level Prompts**: Teaching philosophy is defined at the context level, allowing the tutor to completely adapt its approach
3. **Step Progression**: Each subject mode has structured steps with completion criteria for optimal learning
4. **Navigation Control**: Steps define which contexts/steps can be accessed next while maintaining subject expertise

## 🛠️ Extending the Demo

### Adding Skills

To enhance the tutor with additional capabilities across all subjects:

```python
# Add web search for smarter responses in any subject
self.add_skill("web_search", {
    "api_key": os.getenv("GOOGLE_SEARCH_API_KEY"),
    "search_engine_id": os.getenv("GOOGLE_SEARCH_ENGINE_ID")
})

# Add math calculations (enhances math mode and other subjects)
self.add_skill("math")

# Add datetime for scheduling (useful for all subjects)
self.add_skill("datetime")
```

### Creating New Subject Modes

To add a new subject specialization to the tutor:

```python
# Create new context mode
programming = contexts.add_context("programming") \
    .set_isolated(True) \
    .add_section("Role", "You are now operating in Programming Mode, channeling the expertise of Professor Ada...") \
    .add_section("Teaching Philosophy", "Code is poetry that computers can understand...")

# Add steps for this mode
programming.add_step("language_choice") \
    .add_section("Current Task", "Determine which programming language to teach") \
    .set_step_criteria("Programming language selected") \
    .set_valid_steps(["concept_introduction"])
```

## 📚 Understanding the Code Structure

### Main Components

1. **TutorBotAgent Class**: The single intelligent tutor with multiple subject specializations
2. **Context Definitions**: Each subject mode with unique teaching approaches and personas
3. **Step Workflows**: Learning progression within each subject specialization
4. **Language Support**: Multi-language configuration with ElevenLabs voices

### Context vs Step Prompts

- **Context Prompts**: Define the tutor's teaching personality and approach for each subject
- **Step Prompts**: Define specific tasks within the learning process for that subject mode

Built using SignalWire AI Agent SDK 
