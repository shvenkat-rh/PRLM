"""
GitHub API client for fetching PR data including comments, changes, and responses.
"""

import requests
from github import Github
from typing import Dict, List, Any, Optional
import logging
from dataclasses import dataclass
import os

logger = logging.getLogger(__name__)

@dataclass
class Comment:
    """Represents a comment on a PR"""
    id: int
    author: str
    body: str
    created_at: str
    url: str
    type: str  # 'issue_comment', 'review_comment', 'review'

@dataclass
class PRData:
    """Complete PR data structure"""
    title: str
    description: str
    author: str
    created_at: str
    updated_at: str
    state: str
    url: str
    merged_at: Optional[str]
    closed_at: Optional[str]
    comments: List[Comment]
    changed_files: List[Dict[str, Any]]
    reviews: List[Dict[str, Any]]
    commits: List[Dict[str, Any]]

class GitHubClient:
    """GitHub API client for PR analysis"""
    
    def __init__(self, token: Optional[str] = None):
        """Initialize GitHub client with token"""
        self.token = token or os.getenv('GITHUB_TOKEN')
        if not self.token:
            raise ValueError("GitHub token is required. Set GITHUB_TOKEN env var or pass token.")
        
        self.github = Github(self.token)
        
    def parse_pr_url(self, pr_url: str) -> tuple[str, str, int]:
        """Parse GitHub PR URL to extract owner, repo, and PR number"""
        if 'github.com' not in pr_url:
            raise ValueError("Invalid GitHub URL")
            
        # Handle different URL formats
        if '/pull/' in pr_url:
            parts = pr_url.split('/pull/')
            if len(parts) != 2:
                raise ValueError("Invalid PR URL format")
            
            repo_part = parts[0].replace('https://github.com/', '').replace('http://github.com/', '')
            pr_number = int(parts[1].split('/')[0])
            
            owner, repo = repo_part.split('/')
            return owner, repo, pr_number
        else:
            raise ValueError("URL must contain '/pull/' to identify a PR")
    
    def fetch_pr_data(self, pr_url: str) -> PRData:
        """Fetch complete PR data including comments, reviews, and changes"""
        try:
            owner, repo, pr_number = self.parse_pr_url(pr_url)
            logger.info(f"Fetching PR data for {owner}/{repo}#{pr_number}")
            
            repository = self.github.get_repo(f"{owner}/{repo}")
            pr = repository.get_pull(pr_number)
            
            # Fetch all comments
            comments = self._fetch_all_comments(pr)
            
            # Fetch changed files
            changed_files = self._fetch_changed_files(pr)
            
            # Fetch reviews
            reviews = self._fetch_reviews(pr)
            
            # Fetch commits
            commits = self._fetch_commits(pr)
            
            return PRData(
                title=pr.title,
                description=pr.body or "",
                author=pr.user.login,
                created_at=pr.created_at.isoformat(),
                updated_at=pr.updated_at.isoformat(),
                state=pr.state,
                url=pr.html_url,
                merged_at=pr.merged_at.isoformat() if pr.merged_at else None,
                closed_at=pr.closed_at.isoformat() if pr.closed_at else None,
                comments=comments,
                changed_files=changed_files,
                reviews=reviews,
                commits=commits
            )
            
        except Exception as e:
            logger.error(f"Error fetching PR data: {str(e)}")
            raise
    
    def _fetch_all_comments(self, pr) -> List[Comment]:
        """Fetch all types of comments from the PR"""
        comments = []
        
        # Issue comments (general PR comments)
        for comment in pr.get_issue_comments():
            comments.append(Comment(
                id=comment.id,
                author=comment.user.login,
                body=comment.body,
                created_at=comment.created_at.isoformat(),
                url=comment.html_url,
                type='issue_comment'
            ))
        
        # Review comments (inline code comments)
        for comment in pr.get_review_comments():
            comments.append(Comment(
                id=comment.id,
                author=comment.user.login,
                body=comment.body,
                created_at=comment.created_at.isoformat(),
                url=comment.html_url,
                type='review_comment'
            ))
        
        # Review summaries
        for review in pr.get_reviews():
            if review.body:  # Only include reviews with text
                comments.append(Comment(
                    id=review.id,
                    author=review.user.login,
                    body=review.body,
                    created_at=review.submitted_at.isoformat() if review.submitted_at else "",
                    url=review.html_url,
                    type='review'
                ))
        
        return sorted(comments, key=lambda x: x.created_at)
    
    def _fetch_changed_files(self, pr) -> List[Dict[str, Any]]:
        """Fetch information about changed files"""
        files = []
        for file in pr.get_files():
            files.append({
                'filename': file.filename,
                'status': file.status,
                'additions': file.additions,
                'deletions': file.deletions,
                'changes': file.changes,
                'patch': file.patch if hasattr(file, 'patch') else None
            })
        return files
    
    def _fetch_reviews(self, pr) -> List[Dict[str, Any]]:
        """Fetch review information"""
        reviews = []
        for review in pr.get_reviews():
            reviews.append({
                'id': review.id,
                'author': review.user.login,
                'state': review.state,
                'body': review.body,
                'submitted_at': review.submitted_at.isoformat() if review.submitted_at else None,
                'html_url': review.html_url
            })
        return reviews
    
    def _fetch_commits(self, pr) -> List[Dict[str, Any]]:
        """Fetch commit information"""
        commits = []
        for commit in pr.get_commits():
            commits.append({
                'sha': commit.sha,
                'message': commit.commit.message,
                'author': commit.commit.author.name,
                'date': commit.commit.author.date.isoformat(),
                'url': commit.html_url
            })
        return commits
