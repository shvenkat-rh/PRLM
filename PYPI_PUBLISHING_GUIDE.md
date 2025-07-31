# 🚀 PyPI Publishing Guide

This guide explains how to publish your PR Analyzer package to PyPI automatically when you create GitHub releases.

## 📦 Package Setup (Already Completed)

Your project is now configured for automated PyPI publishing with:

- ✅ `pyproject.toml` - Modern Python packaging configuration
- ✅ `MANIFEST.in` - Specifies additional files to include in the package
- ✅ `LICENSE` - MIT license for open source distribution
- ✅ GitHub Actions workflow (`.github/workflows/publish-pypi.yml`)
- ✅ Proper package structure with entry points
- ✅ CLI commands: `pr-analyzer` and `pr-analyzer-gui`

## 🔐 Setting Up PyPI Publishing

### Step 1: Set Up PyPI Trusted Publishing (Recommended)

1. **Create a PyPI account** at https://pypi.org/account/register/
2. **Go to Publishing** at https://pypi.org/manage/account/publishing/
3. **Add a new pending publisher** with these details:
   - **PyPI project name**: `pr-analyzer`
   - **Owner**: `shvenkat-rh`
   - **Repository name**: `PRLM`
   - **Workflow name**: `publish-pypi.yml`
   - **Environment name**: `release`

### Step 2: Set Up GitHub Environments

1. Go to your GitHub repository: https://github.com/shvenkat-rh/PRLM
2. Click **Settings** → **Environments**
3. Create two environments:

#### Environment: `release` (for PyPI)
- **Name**: `release`
- **Protection Rules**:
  - ✅ Required reviewers (optional, for extra safety)
  - ✅ Wait timer: 0 minutes
  - ✅ Deployment branches: Selected branches → `main`

#### Environment: `test-release` (for TestPyPI)
- **Name**: `test-release`
- **Protection Rules**: None needed (for testing)

### Step 3: Alternative - API Token Method (if trusted publishing doesn't work)

If you prefer to use API tokens instead of trusted publishing:

1. **Generate PyPI API token**:
   - Go to https://pypi.org/manage/account/
   - Create a new API token with scope "Entire account"
   - Copy the token (starts with `pypi-`)

2. **Add to GitHub Secrets**:
   - Go to repository **Settings** → **Secrets and variables** → **Actions**
   - Add repository secret:
     - **Name**: `PYPI_API_TOKEN`
     - **Value**: Your PyPI API token

3. **Update workflow** to use token instead of trusted publishing (modify `.github/workflows/publish-pypi.yml`):
   ```yaml
   - name: Publish to PyPI
     uses: pypa/gh-action-pypi-publish@release/v1
     with:
       password: ${{ secrets.PYPI_API_TOKEN }}
   ```

## 🏷️ Creating Releases for Automatic Publishing

### Method 1: GitHub Web Interface (Recommended)

1. **Go to your repository**: https://github.com/shvenkat-rh/PRLM
2. **Click "Releases"** in the right sidebar
3. **Click "Create a new release"**
4. **Fill in the release form**:
   - **Tag version**: `v1.0.0` (or `1.0.0`)
   - **Release title**: `PR Analyzer v1.0.0`
   - **Description**: 
     ```markdown
     ## 🎉 Initial Release - PR Analyzer v1.0.0
     
     ### 🌟 Features
     - AI-powered GitHub Pull Request analysis
     - Professional Streamlit GUI interface
     - Command-line interface with `pr-analyzer` command
     - Comprehensive timeline and conversation analysis
     - Word document report generation
     - Enterprise-grade security with local processing
     
     ### 🚀 Installation
     ```bash
     pip install pr-analyzer
     ```
     
     ### 📖 Usage
     ```bash
     # Launch GUI
     pr-analyzer-gui
     
     # CLI analysis
     pr-analyzer https://github.com/owner/repo/pull/123
     ```
     
     ### 📊 What's Included
     - Advanced PR metrics and timeline analysis
     - AI-powered insights using local LLM models
     - Interactive dashboards and visualizations
     - Secure, privacy-focused architecture
     ```
5. **Click "Publish release"**

### Method 2: Command Line with GitHub CLI

```bash
# Install GitHub CLI if you haven't already
# brew install gh (macOS) or see https://cli.github.com/

# Login to GitHub
gh auth login

# Create and publish a release
gh release create v1.0.0 \
  --title "PR Analyzer v1.0.0" \
  --notes "Initial release with AI-powered PR analysis and professional GUI"
```

### Method 3: Git Tags + GitHub Release

```bash
# Create and push a tag
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# Then create a release from the tag in GitHub web interface
```

## 🤖 What Happens When You Create a Release

1. **GitHub detects the release** and triggers the workflow
2. **Tests run** across Python 3.8-3.12 to ensure compatibility
3. **Package is built** (both wheel and source distribution)
4. **Package is validated** with `twine check`
5. **Package is published** to PyPI automatically
6. **Users can install** with `pip install pr-analyzer`

## 📊 Monitoring the Publishing Process

### Check GitHub Actions
1. Go to **Actions** tab in your repository
2. Look for "Publish to PyPI" workflow
3. Click on the run to see detailed logs

### Check PyPI
1. Visit https://pypi.org/project/pr-analyzer/
2. Verify your package appears with the correct version
3. Check that the description and metadata look correct

## 🛠️ Package Installation and Usage

Once published, users can install your package:

```bash
# Install the package
pip install pr-analyzer

# Launch the professional GUI
pr-analyzer-gui

# Use the CLI for analysis
pr-analyzer https://github.com/microsoft/vscode/pull/12345

# Get help
pr-analyzer --help
```

## 🔄 Updating Versions

For future releases:

1. **Update version** in `src/pr_analyzer/__init__.py`:
   ```python
   __version__ = "1.1.0"
   ```

2. **Update version** in `pyproject.toml`:
   ```toml
   version = "1.1.0"
   ```

3. **Commit and create a new release** following the steps above

## 📋 Version Numbering Guidelines

Follow semantic versioning (semver):
- **Major** (X.0.0): Breaking changes
- **Minor** (1.X.0): New features, backwards compatible
- **Patch** (1.1.X): Bug fixes, backwards compatible

Examples:
- `1.0.0` - Initial release
- `1.0.1` - Bug fix release
- `1.1.0` - New features added
- `2.0.0` - Breaking changes

## 🐛 Troubleshooting

### Build Fails
- Check the Actions logs for specific error messages
- Ensure all dependencies are correctly specified in `pyproject.toml`
- Verify the package structure hasn't changed

### Publishing Fails
- Check PyPI trusted publishing configuration
- Verify environment names match exactly
- Ensure the package name isn't already taken

### Import Errors After Installation
- Check that all entry points are correctly defined
- Verify the package structure in `pyproject.toml`
- Test locally with `pip install -e .` first

## 🎯 Best Practices

1. **Test locally first**: Always run `python -m build` and `twine check dist/*` before creating a release
2. **Use pre-releases**: For testing, create releases with names like `v1.0.0-rc1`
3. **Write good release notes**: Users appreciate knowing what changed
4. **Monitor downloads**: Check PyPI stats to see how your package is being used
5. **Keep dependencies updated**: Regularly update version requirements

## 🚀 Success!

Your PR Analyzer package is now ready for automatic PyPI publishing! 🎉

Every time you create a GitHub release, your package will be automatically:
- ✅ Tested across multiple Python versions
- ✅ Built into proper distribution packages
- ✅ Published to PyPI
- ✅ Available for installation with `pip install pr-analyzer`

Happy publishing! 🚀 