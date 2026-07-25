# Ashwas AI 2.0 - Recovery & Relapse Prevention Platform

Ashwas AI 2.0 is a multi-modal, GenAI-powered recovery and prevention platform designed to support individuals navigating substance use disorders (SUD) and their caregivers. Utilizing generative AI as its core intelligence layer, the platform provides zero-typing interventions, voice-to-voice interfaces, crisis grounding, and contextual safety tools to empower families when cognitive load is highest.

---

## 📖 Project Overview
During acute cravings or high-stress triggers, an individual's cognitive load increases, making typing or reading complex blocks of text difficult or impossible. Ashwas AI 2.0 addresses this by introducing browser-native voice dictation (speech-to-text), voice synthesis response output (text-to-speech), and one-tap zero-typing grounding scenarios. The app dynamically adapts to support either recovering individuals or their caregivers, backed by robust safety overrides.

## ⚠️ Problem Statement
Post-treatment recovery from substance use disorders is plagued by high relapse rates (40% to 60%) in the first year. Acute triggers and cravings occur unpredictably in daily life. Traditional interventions are retrospective and require active mental engagement. Recovering individuals need real-time, low-friction, safety-guided cognitive and somatic exercises to interrupt craving cycles instantly, while caregivers need rapid-response instructions during crisis alerts.

---

## 🌟 Features

* **✅ Real Voice-to-Voice Interaction:** Double-channel audio support using browser SpeechRecognition (microphone input) and SpeechSynthesis (voice response output).
* **✅ Zero-Typing Interventions:** Fast-access scenario triggers (Location Trigger, Physical Craving, Panic Spike) that bypass text input to load instant grounding scripts.
* **✅ Caregiver Portal Mode:** Separate dashboard context providing de-escalation scripts, overdose check guides, and caregiver self-care resources.
* **✅ Mindfulness & Breathing Spacer:** An interactive pacing tool running A-CHESS box-breathing cycles with visual scale animations and step trackers.
* **✅ Multilingual Engine:** Full support for English and Malayalam (മലയാളം), automatically detecting user language and responding back in the same language.
* **✅ Safety Net Overrides:** Local keyword analyzer that intercepts crisis indicators and overrides AI responses with immediate national helpline routing.
* **✅ Soothing Glassmorphic UI:** Mobile-first, calm dark theme built with Tailwind CSS, utilizing rounded interactive boundaries and responsive styling.

---

## 🏗️ Architecture & AI Workflow

### System Architecture
```
[User Browser]
   │
   ├─► SpeechRecognition (Microphone Audio -> Text)
   ├─► SpeechSynthesis (Text -> Spoken Audio Voice)
   │
   ├─► GET / (templates/index.html)
   ├─► POST /api/chat ───┐
   └─► POST /api/emergency-script
                         │
                         ▼
                  [FastAPI Backend]
                         │
        ┌────────────────┴────────────────┐
        ▼                                 ▼
 [SafetyGuardrails]               [Gemini AI Engine]
  (Crisis Detection)             (Model Fallback Chain)
        │                                 │
        ├─► Keyword Match                 ├─► gemini-1.5-flash
        │   (Fallback Override)           ├─► gemini-1.5-pro
        └─► Safe Response                 └─► gemini-pro (Fallback)
```

### Generative AI Workflow
1. **Input Capture:** Text message or microphone speech is transcribed in the browser and sent to the `/api/chat` or `/api/emergency-script` endpoint.
2. **Safety Evaluation:** The backend passes the query through `SafetyGuardrails`. If self-harm or overdose keywords are matched, it intercepts the prompt and routes to crisis contacts.
3. **Prompt Composition:** System instructions match the selected tab mode (`recovery_coach`, `caregiver_support`, `grounding`) and enforce language matching rules.
4. **Adaptive Generation:** Pushed to the Gemini Generative Model fallback chain.
5. **Acoustic Feedback:** The response JSON is rendered in the chat log and immediately spoken out loud via the browser's Web Speech engine in the corresponding language.

---

## 💻 Tech Stack
* **Backend Framework:** FastAPI (Python 3.9+)
* **AI Core Integration:** Google Gemini API (`google-generativeai` SDK)
* **Frontend Design:** Tailwind CSS & FontAwesome 6 (Responsive, Mobile-First HTML5)
* **Audio Layer:** HTML5 Web Speech API (SpeechRecognition & SpeechSynthesis)
* **Deployment Platform:** Render Cloud Application Services

---

## 🔒 Security Practices
* **No Hardcoded Secrets:** All system credentials (such as `GEMINI_API_KEY`) are fetched dynamically from Render environment configs. An `.env.example` file is included for setup.
* **Privacy-First Data Architecture:** All emotional check-in history and metric logs are persisted client-side in the browser's `localStorage`. No private recovery data is stored on backend servers.
* **Input Sanitization:** All text inputs are validated and sanitized on both client-side forms and API gateways to prevent prompt injection attacks.
* **Consent-Based Operations:** Emergency triggers prompt user consent before display, maintaining a transparent and safe environment.
* **HTTPS Enforcement:** Render automatically mounts SSL certificates, ensuring all network packets are fully encrypted in transit.

---

## ♿ Accessibility Compliance
* **Voice-First Input & Output:** Speech recognition captures mic inputs, and text-to-speech speaks AI responses back, lowering barriers for users unable to type.
* **Multilingual Coverage:** Natively supports English and Malayalam (മലയാളം) inputs/outputs.
* **AA Contrast Ratios:** Soothing high-contrast colors (white and teal text on slate backgrounds) ensure readability under glare or stress.
* **Tap Targets:** Every button, tab, and card has a minimum touch-target area of `48px` to facilitate error-free finger tapping.
* **Keyboard Navigation:** Fully navigable using standard tab focuses and submit buttons.

---

## 🧪 Testing Logs
* **Unit Verification:** Validated endpoint logic for `/api/chat` and `/api/emergency-script` using Python compilation and mock requests.
* **Manual Verification:** Tested Web Speech Recognition and Web Speech Synthesis across Chrome and Safari browsers.
* **Edge Case Error Handling:**
  - Network timeout falls back to local somatic grounding instructions to maintain crisis coverage.
  - Generative API key absence activates local offline recovery modes gracefully.
  - Invalid dictation inputs default to simulated voice logs.

---

## 🚀 Installation & Local Run

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
Create a `.env` file in the root folder using the template:
```bash
cp .env.example .env
# Edit .env and enter your GEMINI_API_KEY
```

### 3. Launch App Locally
```bash
python main.py
```
Open [http://localhost:8000](http://localhost:8000) in your web browser.

---

## 📄 License
This project is licensed under the MIT License. See [LICENSE](LICENSE) file for details.
