# WSL Configuration Guide for AI-Powered Development

Windows Subsystem for Linux (WSL) has become an essential development environment for Windows users, providing a seamless bridge between Windows and Linux development workflows. Beyond offering native Linux tooling, WSL enables access to powerful AI coding assistants like:

- [Amazon Q](https://aws.amazon.com/q/) – a comprehensive Generative AI Assistant that excels at automating repetitive development tasks across the entire software lifecycle. Amazon Q can perform in-depth code reviews to identify and fix [security vulnerabilities](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/understand-code-issues.html), code smells, anti-patterns, and logical errors with auto-generated patches. It generates comprehensive documentation including READMEs and data flow diagrams by analyzing your entire codebase. Amazon Q also boosts test coverage by automatically writing unit tests with boundary conditions and edge cases, while self-debugging test errors.

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview) - an Agentic Coding Tool by Anthropic that transforms development through its "Explore, plan, code, commit" workflow. According to Anthropic's [Best practices for agentic coding](https://www.anthropic.com/engineering/claude-code-best-practices), Claude Code first explores your codebase, then uses different thinking intensities ("think" to "ultrathink") to create implementation plans before writing code. This methodical approach prevents rushing to solutions for complex problems, with Claude handling everything from initial exploration to final pull requests—all through natural language commands. This workflow particularly shines when thoughtful architecture is needed rather than quick code generation.

## WSL Environment Verification

Before proceeding with setup, verify your WSL environment:

### From Windows PowerShell/CMD

```powershell
# Check default distribution and WSL version
wsl --status

# List all WSL distributions with state
wsl --list --verbose

# Update WSL to latest version
wsl --update

# Connect to specific distribution as specific user
wsl -d Ubuntu -u username
```

### From Inside WSL

```bash
# View distribution details
cat /etc/os-release

# Check distribution version
lsb_release -a

# Check user and group memberships
id
```

### Password Reset Process

If you need to reset your WSL user password:

```powershell
# From Windows, access as root
wsl -d Ubuntu -u root

# Inside WSL, reset the password
passwd username
```

Note: WSL commands like `wsl --list` work only from Windows command prompt or PowerShell, not from inside WSL.

## Setting Up WSL for AI-Assisted Development

To use AI tools like Claude Code effectively with WSL, you'll need to set up your environment properly:

1. **Install Windows Subsystem for Linux (WSL)**
   - Follow the [official Microsoft WSL setup guide](https://learn.microsoft.com/en-us/windows/wsl/setup/environment)
   - We recommend Ubuntu as the Linux distribution for compatibility

2. **Install Python with Proper Aliases**
   - Install Python from the Ubuntu repositories:

     ```bash
     sudo apt update
     sudo apt install python3 python3-pip python3-venv python3-full
     ```

   - Create the Python alias so both `python` and `python3` commands work:

     ```bash
     sudo apt install python-is-python3
     ```

   - Verify installation:

     ```bash
     python --version   # Should show Python 3.x.x
     python3 --version  # Same version as above
     pip --version
     pip3 --version
     ```

   - See also: [Microsoft's Python in WSL guide](https://learn.microsoft.com/en-us/windows/python/web-frameworks#install-windows-subsystem-for-linux)

3. **Python Virtual Environment Setup**
   - Ubuntu uses an "externally managed environment" for Python packages to prevent system package conflicts
   - Always create a virtual environment for your projects:

     ```bash
     # Navigate to your project directory
     cd /path/to/project
     
     # Create a virtual environment
     python3 -m venv .venv
     
     # Activate the environment
     source .venv/bin/activate
     
     # Install packages (now inside the virtual environment)
     pip install -r requirements.txt
     ```

   - When finished, deactivate the environment:

     ```bash
     deactivate
     ```

4. **Install Node.js via NVM**
   - Install NVM (Node Version Manager):

     ```bash
     curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/master/install.sh | bash
     ```

   - Start a new terminal or source your profile:

     ```bash
     source ~/.bashrc
     ```

   - **IMPORTANT**: Newer versions of Node.js (e.g., v24) may cause compatibility issues with Claude Code, so install Node.js v18:

     ```bash
     # Install Node.js 18 (recommended for Claude Code)
     nvm install 18

     # Make Node.js 18 your default
     nvm use 18
     nvm alias default 18

     # List all installed Node.js versions
     nvm ls

     # Verify installation
     node -v  # Should show v18.x.x
     npm -v
     ```

   - See also: [Microsoft Node.js on WSL guide](https://learn.microsoft.com/en-us/windows/dev-environment/javascript/nodejs-on-wsl)

5. **Access Windows Environment Variables**
   - Add this to your `~/.bashrc` to import the ANTHROPIC_API_KEY:

     ```bash
     # Import ANTHROPIC_API_KEY from Windows environment
     export ANTHROPIC_API_KEY=$(powershell.exe -Command "\$env:ANTHROPIC_API_KEY" | tr -d '\r')
     ```

   - Apply the changes:

     ```bash
     source ~/.bashrc
     
     # Verify the API key is available
     echo $ANTHROPIC_API_KEY
     env | grep ANTH
     ```

6. **Install Claude Code CLI**
   - With Node.js 18 active, install Claude Code:

     ```bash
     npm install -g @anthropic-ai/claude-code
     ```

   - Start Claude Code:

     ```bash
     claude
     ```

   - See also: [Claude Code overview](https://docs.anthropic.com/en/docs/claude-code/overview)

   - If you encounter connectivity issues, verify you can reach Anthropic's API:

     ```bash
     curl -I https://api.anthropic.com
     ```

     and consult the [Troubleshooting guide](https://docs.anthropic.com/en/docs/claude-code/troubleshooting) for common issues.

7. **Configure VS Code for WSL**
   - Follow the [VS Code with WSL tutorial](https://learn.microsoft.com/en-us/windows/wsl/tutorials/wsl-vscode)
   - This enables VS Code to seamlessly work with your WSL environment

These setup steps create the foundation needed for AI-powered development tools to effectively analyze and modify your codebase.

## Setting Up Git for WSL Development

This section addresses common Git issues when working with repositories in WSL and provides solutions for a streamlined development experience.

### Git User Configuration

When working with Git in WSL, you can automatically sync your Windows Git user configuration:

```bash
# Import Git user email and name from Windows
WIN_GIT_EMAIL=$(powershell.exe -Command "git config --global user.email" | tr -d '\r')
WIN_GIT_NAME=$(powershell.exe -Command "git config --global user.name" | tr -d '\r')

# Apply Windows Git configuration to WSL
git config --global user.email "$WIN_GIT_EMAIL"
git config --global user.name "$WIN_GIT_NAME"
```

If you have authentication issues when pushing to repositories, configure Git to use the Windows credential manager:

```bash
# Configure Git to use Windows credential manager
git config --global credential.helper "/mnt/c/Program\ Files/Git/mingw64/bin/git-credential-manager.exe"
```

This allows you to use your Windows-stored credentials and identity for Git operations in WSL.

### Common Issue: False "Modified Files"

When accessing Windows-based repositories through WSL's `/mnt/` paths, Git may incorrectly show numerous files as modified even when no changes have been made. This occurs due to:

1. **Line endings**: Windows uses CRLF (`\r\n`) while Linux uses LF (`\n`)
2. **File permissions**: WSL tracks executable bits that Windows Git ignores

#### Quick Fix

Execute the following commands in your WSL terminal to resolve these issues:

```bash
# Configure line ending behavior (only convert to LF when committing)
git config core.autocrlf input

# Ensure consistent line endings
git config core.eol lf

# Ignore file permission changes between Windows and WSL
git config core.fileMode false

# Reset the working directory to match the index (if needed)
# WARNING: This discards uncommitted changes!
git reset --hard
```

#### Recommended `.gitattributes` File

For optimal cross-platform compatibility, add this `.gitattributes` file to your repository:

```bash
# Set default behavior to automatically normalize line endings
* text=auto

# Explicitly declare text files you want to always be normalized and converted
# to native line endings on checkout
*.js text
*.ts text
*.json text
*.md text
*.html text
*.css text
*.scss text
*.yml text
*.yaml text
*.xml text
*.txt text

# Declare files that will always have CRLF line endings on checkout
*.{cmd,[cC][mM][dD]} text eol=crlf
*.{bat,[bB][aA][tT]} text eol=crlf

# Declare files that will always have LF line endings on checkout
*.sh text eol=lf

# Denote all files that are truly binary and should not be modified
*.png binary
*.jpg binary
*.jpeg binary
*.gif binary
*.ico binary
*.zip binary
*.pdf binary
*.vsix binary
*.exe binary
```

This file helps maintain consistent line endings across platforms and should remain in your repository.

## VSCode Integration

For the best experience with VSCode and WSL:

1. Install the "Remote - WSL" extension in VSCode
2. Open your project through WSL by:
   - Clicking the green remote button in the bottom-left corner
   - Selecting "Remote-WSL: Open Folder in WSL..."
   - Navigating to your project folder

3. Add these settings to your VSCode `settings.json`:

```json
{
    "files.eol": "\n",
    "remote.WSL.fileWatcher.polling": true
}
```
