# GitHub Push Instructions

## Step 1: Install Git

**Windows:**
- Download from: https://git-scm.com/download/win
- Run the installer and follow default options
- Restart your terminal after installation

**Verify installation:**
```bash
git --version
```

---

## Step 2: Configure Git (First Time Only)

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

---

## Step 3: Create GitHub Repository

1. Go to https://github.com/new
2. **Repository name**: `safety-equipment-detection` (or your choice)
3. **Description**: Safety Equipment Detection using YOLOv8 (optional)
4. Select **Public** (if you want others to see it)
5. **DO NOT** initialize with README (we already have one)
6. Click **Create repository**
7. Copy the repository URL (looks like `https://github.com/yourusername/safety-equipment-detection.git`)

---

## Step 4: Initialize Git & Push

Open PowerShell in your project directory and run:

```bash
cd c:\Users\hafiz\OneDrive\Desktop\Hackthon

# Initialize git
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Safety Equipment Detection System"

# Add remote (replace URL with your repo URL)
git remote add origin https://github.com/yourusername/safety-equipment-detection.git

# Push to GitHub
git branch -M main
git push -u origin main
```

---

## Step 5: Verify on GitHub

- Go to your repository URL on GitHub
- Check that all files are uploaded
- Verify README is displayed

---

## Step 6: Future Updates

To update your repository with new changes:

```bash
# Add changes
git add .

# Commit
git commit -m "Description of changes"

# Push
git push origin main
```

---

## Useful Git Commands

```bash
# Check status
git status

# See commit history
git log --oneline

# See what files changed
git diff

# Undo last commit (keep files)
git reset --soft HEAD~1

# View remote
git remote -v
```

---

## Notes

- ✅ `.gitignore` is already created - it will exclude model files, uploads, and cache
- ✅ `README.md` is ready with full documentation
- ⚠️ `best.pt` model file WON'T be pushed (too large - 100MB+)
  - Users will need to download or train the model themselves
  - Add instructions in README for downloading the model

---

## If You Get Authentication Issues

**Using HTTPS (Easiest):**
- GitHub will ask for username/password OR personal access token
- Create token at: https://github.com/settings/tokens
- When prompted, use token as password

**Using SSH (Advanced):**
```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your.email@example.com"

# Add to GitHub: https://github.com/settings/keys
# Use SSH URL: git@github.com:yourusername/repo.git
```

---

## Quick Copy-Paste (All Commands)

```bash
cd c:\Users\hafiz\OneDrive\Desktop\Hackthon
git init
git add .
git commit -m "Initial commit: Safety Equipment Detection System"
git remote add origin https://github.com/YOUR_USERNAME/safety-equipment-detection.git
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username!

---

**Done! 🚀**
