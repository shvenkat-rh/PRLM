"""
Local LLM client for analyzing PR data using ollama with llama3:latest.
"""

import ollama
import json
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class AnalysisResult:
    """Result from LLM analysis"""
    summary: str
    key_changes: List[str]
    comment_analysis: str
    developer_mistakes: List[str]
    code_quality_issues: List[str]
    suggestions: List[str]
    overall_assessment: str

class LLMClient:
    """Client for local LLM analysis using ollama"""
    
    def __init__(self, model_name: str = "llama3:latest"):
        """Initialize LLM client"""
        self.model_name = model_name
        self._verify_model_available()
    
    def _verify_model_available(self):
        """Verify the model is available in ollama"""
        try:
            models = ollama.list()
            if 'models' in models:
                model_names = []
                for model in models['models']:
                    # Handle different response formats
                    if hasattr(model, 'model'):
                        # Model objects with .model attribute
                        name = model.model
                    elif isinstance(model, dict):
                        name = model.get('name') or model.get('model') or str(model)
                    else:
                        name = str(model)
                    model_names.append(name)
            else:
                model_names = []
            
            if self.model_name not in model_names:
                logger.warning(f"Model {self.model_name} not found. Available models: {model_names}")
                raise ValueError(f"Model {self.model_name} not available. Please install it with: ollama pull {self.model_name}")
        except Exception as e:
            logger.error(f"Error checking ollama models: {e}")
            raise
    
    def analyze_pr_comprehensive(self, pr_data, timeline_metrics, repo_context: str = "") -> AnalysisResult:
        """Perform comprehensive PR analysis"""
        
        # Prepare the analysis prompt
        prompt = self._create_comprehensive_analysis_prompt(pr_data, timeline_metrics, repo_context)
        
        try:
            response = ollama.chat(
                model=self.model_name,
                messages=[{
                    'role': 'user',
                    'content': prompt
                }],
                options={
                    'temperature': 0.1,  # Low temperature for more consistent analysis
                    'top_p': 0.9,
                    'num_predict': 2048
                }
            )
            
            analysis_text = response['message']['content']
            return self._parse_analysis_response(analysis_text)
            
        except Exception as e:
            logger.error(f"Error during LLM analysis: {e}")
            raise
    
    def _create_comprehensive_analysis_prompt(self, pr_data, timeline_metrics, repo_context: str) -> str:
        """Create a comprehensive analysis prompt for the LLM"""
        
        # Prepare PR data summary
        pr_summary = f"""
        PR Title: {pr_data.title}
        Author: {pr_data.author}
        State: {pr_data.state}
        Created: {pr_data.created_at}
        Updated: {pr_data.updated_at}
        
        Description:
        {pr_data.description[:1000]}...
        
        Files Changed: {len(pr_data.changed_files)}
        Total Comments: {len(pr_data.comments)}
        Reviews: {len(pr_data.reviews)}
        Commits: {len(pr_data.commits)}
        """
        
        # Prepare timeline summary
        time_to_merge = f"{timeline_metrics.time_to_merge:.1f} hours" if timeline_metrics.time_to_merge else "Not merged"
        timeline_summary = f"""
        Timeline Metrics:
        - Time to first review: {timeline_metrics.time_to_first_review:.1f} hours
        - Time to merge: {time_to_merge}
        - Total lifecycle: {timeline_metrics.total_lifecycle:.1f} hours
        - Review cycles: {timeline_metrics.review_cycles}
        - Comment frequency: {timeline_metrics.comment_frequency:.1f} comments/day
        """
        
        # Prepare comments summary
        comments_summary = ""
        for i, comment in enumerate(pr_data.comments[:10]):  # Limit to first 10 comments
            comments_summary += f"\n{i+1}. [{comment.type}] {comment.author}: {comment.body[:200]}..."
        
        # Prepare file changes summary
        changes_summary = ""
        for file_info in pr_data.changed_files[:15]:  # Limit to first 15 files
            changes_summary += f"\n- {file_info['filename']}: {file_info['status']} (+{file_info['additions']} -{file_info['deletions']})"
        
        prompt = f"""
        You are an expert code reviewer and software engineering analyst. Please analyze this GitHub Pull Request comprehensively and provide structured insights.

        ## PULL REQUEST DATA:
        {pr_summary}

        ## TIMELINE ANALYSIS:
        {timeline_summary}

        ## REPOSITORY CONTEXT:
        {repo_context[:1000] if repo_context else 'No additional context provided'}

        ## COMMENTS AND DISCUSSIONS:
        {comments_summary}

        ## FILE CHANGES:
        {changes_summary}

        ## ANALYSIS REQUIREMENTS:
        Please provide a comprehensive analysis in the following structured format:

        ### SUMMARY
        [Provide a concise overview of what this PR accomplishes, its scope, and significance]

        ### KEY CHANGES
        [List the 5-10 most important changes made in this PR]

        ### COMMENT ANALYSIS
        [Analyze the comment patterns, reviewer concerns, and how the author responded to feedback]

        ### DEVELOPER MISTAKES
        [Identify any mistakes, oversights, or issues that were caught during review]

        ### CODE QUALITY ISSUES
        [Highlight any code quality, performance, security, or maintainability concerns]

        ### SUGGESTIONS
        [Provide suggestions for improvement or lessons learned]

        ### OVERALL ASSESSMENT
        [Give an overall assessment of the PR quality, review process, and development practices]

        Please be specific, actionable, and focus on learning opportunities. Consider the timeline metrics when assessing the efficiency of the review process.
        """
        
        return prompt
    
    def _parse_analysis_response(self, analysis_text: str) -> AnalysisResult:
        """Parse the LLM response into structured data"""
        sections = {
            'summary': '',
            'key_changes': [],
            'comment_analysis': '',
            'developer_mistakes': [],
            'code_quality_issues': [],
            'suggestions': [],
            'overall_assessment': ''
        }
        
        current_section = None
        lines = analysis_text.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Detect section headers
            if '### SUMMARY' in line.upper():
                current_section = 'summary'
                continue
            elif '### KEY CHANGES' in line.upper():
                current_section = 'key_changes'
                continue
            elif '### COMMENT ANALYSIS' in line.upper():
                current_section = 'comment_analysis'
                continue
            elif '### DEVELOPER MISTAKES' in line.upper():
                current_section = 'developer_mistakes'
                continue
            elif '### CODE QUALITY ISSUES' in line.upper():
                current_section = 'code_quality_issues'
                continue
            elif '### SUGGESTIONS' in line.upper():
                current_section = 'suggestions'
                continue
            elif '### OVERALL ASSESSMENT' in line.upper():
                current_section = 'overall_assessment'
                continue
            
            # Add content to current section
            if current_section and line:
                if current_section in ['key_changes', 'developer_mistakes', 'code_quality_issues', 'suggestions']:
                    # List items
                    if line.startswith('-') or line.startswith('*') or line.startswith('•'):
                        sections[current_section].append(line[1:].strip())
                    elif line and not line.startswith('#'):
                        sections[current_section].append(line)
                else:
                    # Text sections
                    if sections[current_section]:
                        sections[current_section] += '\n'
                    sections[current_section] += line
        
        return AnalysisResult(
            summary=sections['summary'],
            key_changes=sections['key_changes'],
            comment_analysis=sections['comment_analysis'],
            developer_mistakes=sections['developer_mistakes'],
            code_quality_issues=sections['code_quality_issues'],
            suggestions=sections['suggestions'],
            overall_assessment=sections['overall_assessment']
        )
    
    def analyze_code_changes(self, changed_files: List[Dict], pr_context: str) -> Dict[str, Any]:
        """Analyze specific code changes in detail"""
        
        # Focus on the most significant files
        significant_files = sorted(changed_files, key=lambda x: x['changes'], reverse=True)[:5]
        
        analysis = {}
        
        for file_info in significant_files:
            if file_info.get('patch'):
                file_analysis = self._analyze_single_file(file_info, pr_context)
                analysis[file_info['filename']] = file_analysis
        
        return analysis
    
    def _analyze_single_file(self, file_info: Dict, pr_context: str) -> Dict[str, Any]:
        """Analyze a single file's changes"""
        
        prompt = f"""
        Analyze this specific file change from a pull request:
        
        File: {file_info['filename']}
        Status: {file_info['status']}
        Additions: {file_info['additions']}
        Deletions: {file_info['deletions']}
        
        PR Context: {pr_context[:500]}
        
        Code Changes:
        {file_info['patch'][:2000]}
        
        Please analyze:
        1. What is the purpose of these changes?
        2. Are there any potential issues or improvements?
        3. How does this fit into the overall PR goal?
        4. Any security, performance, or maintainability concerns?
        
        Provide a concise analysis (2-3 paragraphs max).
        """
        
        try:
            response = ollama.chat(
                model=self.model_name,
                messages=[{'role': 'user', 'content': prompt}],
                options={'temperature': 0.1, 'num_predict': 512}
            )
            
            return {
                'analysis': response['message']['content'],
                'complexity_score': min(file_info['changes'] / 50, 10),  # Simple complexity metric
                'risk_level': self._assess_risk_level(file_info)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing file {file_info['filename']}: {e}")
            return {
                'analysis': f"Error analyzing file: {str(e)}",
                'complexity_score': 0,
                'risk_level': 'unknown'
            }
    
    def _assess_risk_level(self, file_info: Dict) -> str:
        """Assess risk level of file changes"""
        filename = file_info['filename'].lower()
        changes = file_info['changes']
        
        # High risk indicators
        if any(pattern in filename for pattern in ['auth', 'security', 'payment', 'config', 'sql']):
            return 'high'
        elif filename.endswith(('.sql', '.env', '.config')):
            return 'high'
        elif changes > 100:
            return 'medium'
        elif changes > 20:
            return 'low'
        else:
            return 'minimal' 