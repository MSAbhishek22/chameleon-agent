# Deployment Guide (Render.com)
This is the fastest way to get your **Deployed URL**.

### Step 1: Push Code to GitHub
1. Create a new repository on GitHub (e.g., `chameleon-agent`).
2. Run these commands in your `THE CHAMELEON AGENT` folder terminal:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   # Replace <your-repo-url> below with your actual GitHub URL
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

### Step 2: Deploy on Render
1. Go to [dashboard.render.com](https://dashboard.render.com/) and create a free account.
2. Click **"New +"** -> **"Web Service"**.
3. Connect your GitHub account and select the `chameleon-agent` repository.
4. Settings:
   - **Name**: `chameleon-agent` (or unique name)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. **Environment Variables** (Critical!):
   - Scroll down to "Environment Variables" section.
   - Key: `GEMINI_API_KEY`
   - Value: `(Paste your actual Gemini API key here)`
6. Click **"Deploy Web Service"**.

### Step 3: Get Your Info for Submission
Once the deployment shows "Live" (green):
- **Deployed URL**: Copy the URL from the top left (e.g., `https://chameleon-agent.onrender.com`).
  - *Note*: Add `/honeypot` to the end if the form asks for the specific endpoint, but usually base URL is fine. The endpoint is `POST /honeypot`.
- **API KEY**: You can enter any secure string you want, for example: `chameleon-secret-key-2025`.
  - *Explanation*: Your system is designed to accept any key provided in the header.
