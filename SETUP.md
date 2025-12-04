# Setup Guide

## Prerequisites

- Python 3.9+
- Node.js 18+
- npm or yarn

## Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment:**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Create `.env` file:**
   Create a `.env` file in the `backend` directory with:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   REPLICATE_API_TOKEN=your_replicate_api_token_here
   CORS_ORIGINS=http://localhost:3000
   BACKEND_PORT=8000
   ```

6. **Run the backend:**
   ```bash
   # From backend directory
   uvicorn main:app --reload
   ```
   Or:
   ```bash
   python main.py
   ```

   The backend will run on `http://localhost:8000`

## Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Run the frontend:**
   ```bash
   npm run dev
   ```

   The frontend will run on `http://localhost:3000`

## Getting API Keys

### OpenAI API Key
1. Go to https://platform.openai.com/
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy and add to `.env` file

### Replicate API Token
1. Go to https://replicate.com/
2. Sign up or log in
3. Navigate to Account Settings → API Tokens
4. Create a new token
5. Copy and add to `.env` file

## Usage

1. Start the backend server (port 8000)
2. Start the frontend server (port 3000)
3. Open `http://localhost:3000` in your browser
4. Enter a prompt and generate an image
5. Watch the agentic workflow in action!

## Architecture Overview

### Agentic Workflow
1. **Prompt Enhancement Agent**: Enhances user prompts with technical details
2. **Image Generation Agent**: Generates images using AI models
3. **Validation Agent**: Validates anatomical correctness and quality

### How It Works
- User enters a prompt
- System enhances the prompt automatically
- Image is generated using the enhanced prompt
- Image is validated for quality and anatomical correctness
- Results are displayed with validation scores

## Troubleshooting

### Backend Issues
- Ensure Python 3.9+ is installed
- Check that all dependencies are installed
- Verify `.env` file has correct API keys
- Check that port 8000 is not in use

### Frontend Issues
- Ensure Node.js 18+ is installed
- Delete `node_modules` and `package-lock.json`, then run `npm install` again
- Check that port 3000 is not in use
- Verify backend is running on port 8000

### API Issues
- Verify API keys are correct
- Check API rate limits
- Ensure you have sufficient API credits

