# Install Node Without Local Admin

This repo contains a python script you can run to install node on your local machine. After running the script, it will provide you with a command to copy and paste to update your environment so the "node", "npm", "npx" (etc) commands will work on your terminal.

Requires python to be already installed on your system and in your PATH

## Usage (using powershell)

Step 1: Run

`(iwr -useb "https://raw.githubusercontent.com/Carleton-BIT/install-node-noadmin/refs/heads/main/install.py").Content | python -`

FYI: It's quite dangerous to run random scripts you find on the internet. You can trust me, but don't make this a regular thing.

Step 2: Copy and paste the command to update your path from the script's output into your terminal window

Step 3: Run this as well in PowerShell: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`

Step 3: Now you'll be able to create a react project, or do whatever you want. E.g. `npm create vite@latest`
