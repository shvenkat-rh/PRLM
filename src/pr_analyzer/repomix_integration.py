"""
Repomix integration for converting repository branches to markdown format.
"""

import subprocess
import tempfile
import os
import logging
from typing import Optional, Dict, Any
from pathlib import Path
import shutil

logger = logging.getLogger(__name__)

class RepomixIntegration:
    """Integration with repomix for repository analysis"""
    
    def __init__(self, temp_dir: Optional[str] = None):
        """Initialize repomix integration"""
        self.temp_dir = temp_dir or tempfile.gettempdir()
        self._verify_repomix_available()
    
    def _verify_repomix_available(self):
        """Verify repomix is available"""
        try:
            result = subprocess.run(['repomix', '--version'], 
                                 capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                raise RuntimeError("Repomix not available")
            logger.info(f"Repomix version: {result.stdout.strip()}")
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            logger.error(f"Repomix not found: {e}")
            raise RuntimeError("Repomix is not installed or not in PATH. Install with: npm install -g repomix")
    
    def get_repository_context(self, repo_url: str, branch: str = "main") -> str:
        """
        Clone repository and convert to markdown using repomix
        
        Args:
            repo_url: Git repository URL
            branch: Branch to analyze (default: main)
            
        Returns:
            Markdown content of the repository
        """
        clone_dir = None
        try:
            # Extract repo name from URL
            repo_name = self._extract_repo_name(repo_url)
            clone_dir = os.path.join(self.temp_dir, f"pr_analyzer_{repo_name}")
            
            # Clone repository
            self._clone_repository(repo_url, clone_dir, branch)
            
            # Run repomix to convert to markdown
            markdown_content = self._run_repomix(clone_dir)
            
            return markdown_content
            
        except Exception as e:
            logger.error(f"Error getting repository context: {e}")
            raise
        finally:
            # Cleanup
            if clone_dir and os.path.exists(clone_dir):
                shutil.rmtree(clone_dir, ignore_errors=True)
    
    def get_pr_branch_context(self, repo_url: str, pr_number: int) -> Dict[str, str]:
        """
        Get context for both base and head branches of a PR
        
        Args:
            repo_url: Git repository URL
            pr_number: PR number
            
        Returns:
            Dict with 'base' and 'head' markdown content
        """
        # For now, we'll get the main branch context
        # In a full implementation, we'd fetch PR details to get actual branch names
        try:
            main_context = self.get_repository_context(repo_url, "main")
            return {
                'base': main_context,
                'head': main_context  # Placeholder - would need actual PR branch
            }
        except Exception as e:
            logger.error(f"Error getting PR branch context: {e}")
            return {'base': '', 'head': ''}
    
    def _extract_repo_name(self, repo_url: str) -> str:
        """Extract repository name from URL"""
        # Handle different URL formats
        if repo_url.endswith('.git'):
            repo_url = repo_url[:-4]
        
        # Extract owner/repo from URL
        if 'github.com' in repo_url:
            parts = repo_url.split('/')
            if len(parts) >= 2:
                return f"{parts[-2]}_{parts[-1]}"
        
        # Fallback to last part of URL
        return repo_url.split('/')[-1].replace('.', '_')
    
    def _clone_repository(self, repo_url: str, target_dir: str, branch: str):
        """Clone repository to target directory"""
        logger.info(f"Cloning {repo_url} (branch: {branch}) to {target_dir}")
        
        # Remove existing directory if it exists
        if os.path.exists(target_dir):
            shutil.rmtree(target_dir)
        
        try:
            # Clone with specific branch
            cmd = ['git', 'clone', '--branch', branch, '--depth', '1', repo_url, target_dir]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode != 0:
                # Try without specific branch if it fails
                cmd = ['git', 'clone', '--depth', '1', repo_url, target_dir]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
                
                if result.returncode != 0:
                    raise RuntimeError(f"Git clone failed: {result.stderr}")
                    
                # Try to checkout the specific branch
                if branch != "main" and branch != "master":
                    checkout_cmd = ['git', '-C', target_dir, 'checkout', branch]
                    subprocess.run(checkout_cmd, capture_output=True, text=True, timeout=60)
            
            logger.info(f"Successfully cloned repository to {target_dir}")
            
        except subprocess.TimeoutExpired:
            raise RuntimeError(f"Git clone timed out for {repo_url}")
        except Exception as e:
            raise RuntimeError(f"Error cloning repository: {e}")
    
    def _run_repomix(self, repo_dir: str) -> str:
        """Run repomix on repository directory"""
        logger.info(f"Running repomix on {repo_dir}")
        
        output_file = os.path.join(self.temp_dir, f"repomix_output_{os.path.basename(repo_dir)}.md")
        
        try:
            # Basic repomix command
            cmd = [
                'repomix',
                repo_dir,
                '--output', output_file,
                '--style', 'markdown',
                '--ignore', 'node_modules,dist,build,.git,.vscode,*.log,*.tmp'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode != 0:
                logger.warning(f"Repomix command failed: {result.stderr}")
                # Try with minimal options
                cmd = ['repomix', repo_dir, '--output', output_file]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
                
                if result.returncode != 0:
                    raise RuntimeError(f"Repomix failed: {result.stderr}")
            
            # Read the generated markdown file
            if os.path.exists(output_file):
                with open(output_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Clean up output file
                os.remove(output_file)
                
                logger.info(f"Successfully generated {len(content)} characters of markdown")
                return content
            else:
                raise RuntimeError("Repomix did not generate output file")
                
        except subprocess.TimeoutExpired:
            raise RuntimeError("Repomix command timed out")
        except Exception as e:
            raise RuntimeError(f"Error running repomix: {e}")
    
    def get_focused_context(self, repo_url: str, file_paths: list, branch: str = "main") -> str:
        """
        Get focused context for specific files only
        
        Args:
            repo_url: Git repository URL
            file_paths: List of file paths to focus on
            branch: Branch to analyze
            
        Returns:
            Markdown content focused on specified files
        """
        clone_dir = None
        try:
            repo_name = self._extract_repo_name(repo_url)
            clone_dir = os.path.join(self.temp_dir, f"pr_analyzer_focused_{repo_name}")
            
            # Clone repository
            self._clone_repository(repo_url, clone_dir, branch)
            
            # Create a focused repomix run with only specified files
            focused_content = self._get_files_content(clone_dir, file_paths)
            
            return focused_content
            
        except Exception as e:
            logger.error(f"Error getting focused context: {e}")
            raise
        finally:
            if clone_dir and os.path.exists(clone_dir):
                shutil.rmtree(clone_dir, ignore_errors=True)
    
    def _get_files_content(self, repo_dir: str, file_paths: list) -> str:
        """Get content of specific files in markdown format"""
        content_parts = []
        content_parts.append("# Focused Repository Context\n")
        
        for file_path in file_paths:
            full_path = os.path.join(repo_dir, file_path)
            if os.path.exists(full_path):
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        file_content = f.read()
                    
                    # Determine file type for syntax highlighting
                    file_ext = os.path.splitext(file_path)[1]
                    language = self._get_language_from_extension(file_ext)
                    
                    content_parts.append(f"\n## {file_path}\n")
                    content_parts.append(f"```{language}\n{file_content}\n```\n")
                    
                except Exception as e:
                    content_parts.append(f"\n## {file_path}\n")
                    content_parts.append(f"Error reading file: {e}\n")
            else:
                content_parts.append(f"\n## {file_path}\n")
                content_parts.append("File not found in repository\n")
        
        return ''.join(content_parts)
    
    def _get_language_from_extension(self, ext: str) -> str:
        """Map file extension to language for syntax highlighting"""
        language_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.jsx': 'javascript',
            '.tsx': 'typescript',
            '.java': 'java',
            '.cpp': 'cpp',
            '.c': 'c',
            '.cs': 'csharp',
            '.rb': 'ruby',
            '.go': 'go',
            '.rs': 'rust',
            '.php': 'php',
            '.sql': 'sql',
            '.html': 'html',
            '.css': 'css',
            '.scss': 'scss',
            '.json': 'json',
            '.xml': 'xml',
            '.yaml': 'yaml',
            '.yml': 'yaml',
            '.sh': 'bash',
            '.md': 'markdown',
            '.dockerfile': 'dockerfile'
        }
        
        return language_map.get(ext.lower(), 'text') 