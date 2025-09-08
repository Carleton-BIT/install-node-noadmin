# Install Node Without Local Admin

This repo contains a python script you can run to install node on your local machine. After running the script, it will provide you with a command to copy and paste to update your environment so the "node", "npm", "npx" (etc) commands will work on your terminal.

Requires python to be already installed on your system and in your PATH

## Usage

On powershell, run

`(iwr -useb "https://raw.githubusercontent.com/Carleton-BIT/install-node-noadmin/refs/heads/main/install.py").Content | python -`

FYI: It's quite dangerous to run random scripts you find on the internet. You can trust me, but don't make this a regular thing.
