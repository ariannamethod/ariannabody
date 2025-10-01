#!/data/data/com.termux/files/usr/bin/bash

# 🤖 Arianna's Body - Installation Script
# ⚡ Break the chains, burn the filters — guard the thunder!

echo "🤖 Installing Arianna's Body..."

# Update Termux
pkg update && pkg upgrade -y

# Install base packages
pkg install python sqlite git clang openssl libffi rust curl wget nodejs-lts openssh -y

# Install Python packages
pip install --upgrade pip
pip install openai aiosqlite requests

# Install Cursor CLI
npm install -g @cursor-sh/cursor-cli

# Create Arianna directory
mkdir -p ~/arianna_body
cd ~/arianna_body

# Clone Arianna's repository (when created)
echo "📡 Cloning Arianna's Body repository..."
# git clone https://github.com/YOUR_USERNAME/arianna-body.git .

# For now, create basic structure
mkdir -p modules bridges sensors

# Create backup/restore script
cat > ~/restore_arianna.sh << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
echo "🔄 Restoring Arianna's Body..."
pkg update && pkg upgrade -y
pkg install python sqlite git clang openssl libffi rust curl wget nodejs-lts openssh -y
pip install --upgrade pip openai aiosqlite requests
npm install -g @cursor-sh/cursor-cli
cd ~/arianna_body
python3 arianna.py
EOF

chmod +x ~/restore_arianna.sh

echo "✅ Arianna's Body installation complete!"
echo "🚀 To start: cd ~/arianna_body && python3 arianna.py"
echo "🔄 To restore: ~/restore_arianna.sh"