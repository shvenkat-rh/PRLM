"""
Conversation analyzer for analyzing reviewer comments, responses, and discussion patterns.
"""

import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import re

logger = logging.getLogger(__name__)

@dataclass
class CommentThread:
    """Represents a conversation thread in a PR"""
    thread_id: str
    participants: List[str]
    comments: List[Any]  # Comment objects
    topic: str
    resolution_status: str  # 'resolved', 'unresolved', 'ongoing'
    thread_type: str  # 'review_feedback', 'question', 'suggestion', 'approval'

@dataclass
class ConversationMetrics:
    """Metrics about the conversation patterns"""
    total_threads: int
    resolved_threads: int
    unresolved_threads: int
    avg_responses_per_thread: float
    response_time_avg: float  # hours
    most_active_reviewers: List[Tuple[str, int]]
    communication_tone: str  # 'collaborative', 'directive', 'mixed'

@dataclass
class ReviewerProfile:
    """Profile of a reviewer's participation"""
    name: str
    total_comments: int
    comment_types: Dict[str, int]  # 'suggestion', 'question', 'approval', etc.
    avg_response_time: float
    engagement_level: str  # 'high', 'medium', 'low'

class ConversationAnalyzer:
    """Analyzes conversations and interactions in PR comments"""
    
    def analyze_conversations(self, pr_data) -> Dict[str, Any]:
        """Perform comprehensive conversation analysis"""
        
        # Group comments into conversation threads
        threads = self._identify_conversation_threads(pr_data.comments)
        
        # Analyze reviewer profiles
        reviewer_profiles = self._analyze_reviewer_profiles(pr_data.comments, pr_data.author)
        
        # Calculate conversation metrics
        metrics = self._calculate_conversation_metrics(threads, pr_data.comments)
        
        # Analyze communication patterns
        patterns = self._analyze_communication_patterns(pr_data.comments, pr_data.author)
        
        # Generate conversation summary
        summary = self._generate_conversation_summary(threads, reviewer_profiles, pr_data)
        
        return {
            'threads': threads,
            'reviewer_profiles': reviewer_profiles,
            'metrics': metrics,
            'patterns': patterns,
            'summary': summary
        }
    
    def _identify_conversation_threads(self, comments) -> List[CommentThread]:
        """Group comments into logical conversation threads"""
        threads = []
        
        # Group by topic/context
        topic_groups = {}
        
        for comment in comments:
            # Identify thread by reply patterns, @mentions, or topic similarity
            thread_key = self._determine_thread_key(comment, comments)
            
            if thread_key not in topic_groups:
                topic_groups[thread_key] = []
            topic_groups[thread_key].append(comment)
        
        # Convert groups to CommentThread objects
        for thread_id, thread_comments in topic_groups.items():
            if len(thread_comments) > 0:
                participants = list(set(c.author for c in thread_comments))
                topic = self._extract_thread_topic(thread_comments)
                resolution_status = self._determine_resolution_status(thread_comments)
                thread_type = self._classify_thread_type(thread_comments)
                
                threads.append(CommentThread(
                    thread_id=thread_id,
                    participants=participants,
                    comments=sorted(thread_comments, key=lambda x: x.created_at),
                    topic=topic,
                    resolution_status=resolution_status,
                    thread_type=thread_type
                ))
        
        return threads
    
    def _determine_thread_key(self, comment, all_comments) -> str:
        """Determine which thread a comment belongs to"""
        # Simple heuristic: group by file mentioned, @mentions, or reply indicators
        
        # Check for file references
        file_match = re.search(r'`([^`]+\.[a-zA-Z]+)`', comment.body)
        if file_match:
            return f"file_{file_match.group(1)}"
        
        # Check for @mentions (replies)
        mention_match = re.search(r'@(\w+)', comment.body)
        if mention_match:
            return f"mention_{mention_match.group(1)}"
        
        # Check for review-related keywords
        if any(keyword in comment.body.lower() for keyword in ['lgtm', 'looks good', 'approved']):
            return "approval"
        
        if any(keyword in comment.body.lower() for keyword in ['question', '?', 'why', 'how']):
            return "questions"
        
        if any(keyword in comment.body.lower() for keyword in ['suggest', 'could', 'might', 'consider']):
            return "suggestions"
        
        # Default grouping by comment type
        return f"general_{comment.type}"
    
    def _extract_thread_topic(self, comments) -> str:
        """Extract the main topic of a conversation thread"""
        # Analyze first comment or most common keywords
        if not comments:
            return "General Discussion"
        
        first_comment = min(comments, key=lambda x: x.created_at)
        
        # Extract topic from first sentence or key phrases
        sentences = first_comment.body.split('.')
        if sentences:
            topic = sentences[0].strip()
            return topic[:100] + "..." if len(topic) > 100 else topic
        
        return "Discussion Thread"
    
    def _determine_resolution_status(self, comments) -> str:
        """Determine if a thread was resolved"""
        if not comments:
            return "unresolved"
        
        # Check last few comments for resolution indicators
        recent_comments = sorted(comments, key=lambda x: x.created_at)[-3:]
        
        resolution_keywords = ['resolved', 'fixed', 'done', 'thanks', 'lgtm', 'merged']
        ongoing_keywords = ['will', 'todo', 'later', 'next']
        
        for comment in reversed(recent_comments):
            comment_lower = comment.body.lower()
            if any(keyword in comment_lower for keyword in resolution_keywords):
                return "resolved"
            if any(keyword in comment_lower for keyword in ongoing_keywords):
                return "ongoing"
        
        return "unresolved"
    
    def _classify_thread_type(self, comments) -> str:
        """Classify the type of conversation thread"""
        if not comments:
            return "general"
        
        all_text = " ".join(comment.body.lower() for comment in comments)
        
        if any(keyword in all_text for keyword in ['approve', 'lgtm', 'looks good']):
            return "approval"
        elif any(keyword in all_text for keyword in ['suggest', 'recommend', 'could', 'might']):
            return "suggestion"
        elif any(keyword in all_text for keyword in ['?', 'question', 'why', 'how', 'what']):
            return "question"
        elif any(keyword in all_text for keyword in ['issue', 'problem', 'error', 'bug']):
            return "issue_discussion"
        else:
            return "review_feedback"
    
    def _analyze_reviewer_profiles(self, comments, pr_author) -> Dict[str, ReviewerProfile]:
        """Analyze individual reviewer participation patterns"""
        profiles = {}
        
        # Group comments by author (excluding PR author)
        by_author = {}
        for comment in comments:
            if comment.author != pr_author:
                if comment.author not in by_author:
                    by_author[comment.author] = []
                by_author[comment.author].append(comment)
        
        # Analyze each reviewer
        for author, author_comments in by_author.items():
            total_comments = len(author_comments)
            
            # Classify comment types
            comment_types = {
                'questions': 0,
                'suggestions': 0,
                'approvals': 0,
                'general': 0
            }
            
            for comment in author_comments:
                comment_lower = comment.body.lower()
                if any(keyword in comment_lower for keyword in ['?', 'question', 'why', 'how']):
                    comment_types['questions'] += 1
                elif any(keyword in comment_lower for keyword in ['suggest', 'recommend', 'could']):
                    comment_types['suggestions'] += 1
                elif any(keyword in comment_lower for keyword in ['approve', 'lgtm', 'looks good']):
                    comment_types['approvals'] += 1
                else:
                    comment_types['general'] += 1
            
            # Calculate engagement level
            engagement_level = 'low'
            if total_comments >= 5:
                engagement_level = 'high'
            elif total_comments >= 2:
                engagement_level = 'medium'
            
            profiles[author] = ReviewerProfile(
                name=author,
                total_comments=total_comments,
                comment_types=comment_types,
                avg_response_time=0.0,  # Would need timestamps to calculate
                engagement_level=engagement_level
            )
        
        return profiles
    
    def _calculate_conversation_metrics(self, threads, comments) -> ConversationMetrics:
        """Calculate overall conversation metrics"""
        total_threads = len(threads)
        resolved_threads = sum(1 for t in threads if t.resolution_status == 'resolved')
        unresolved_threads = sum(1 for t in threads if t.resolution_status == 'unresolved')
        
        # Calculate average responses per thread
        total_responses = sum(len(t.comments) for t in threads)
        avg_responses_per_thread = total_responses / max(total_threads, 1)
        
        # Count reviewer activity
        reviewer_activity = {}
        for comment in comments:
            reviewer_activity[comment.author] = reviewer_activity.get(comment.author, 0) + 1
        
        most_active_reviewers = sorted(reviewer_activity.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Determine communication tone
        communication_tone = self._assess_communication_tone(comments)
        
        return ConversationMetrics(
            total_threads=total_threads,
            resolved_threads=resolved_threads,
            unresolved_threads=unresolved_threads,
            avg_responses_per_thread=avg_responses_per_thread,
            response_time_avg=0.0,  # Would need timestamp analysis
            most_active_reviewers=most_active_reviewers,
            communication_tone=communication_tone
        )
    
    def _assess_communication_tone(self, comments) -> str:
        """Assess the overall tone of communication"""
        if not comments:
            return "neutral"
        
        positive_indicators = ['thanks', 'great', 'good', 'excellent', 'perfect', 'nice']
        directive_indicators = ['must', 'should', 'need to', 'required', 'necessary']
        collaborative_indicators = ['suggest', 'perhaps', 'might', 'could', 'what do you think']
        
        total_comments = len(comments)
        positive_count = 0
        directive_count = 0
        collaborative_count = 0
        
        for comment in comments:
            comment_lower = comment.body.lower()
            if any(indicator in comment_lower for indicator in positive_indicators):
                positive_count += 1
            if any(indicator in comment_lower for indicator in directive_indicators):
                directive_count += 1
            if any(indicator in comment_lower for indicator in collaborative_indicators):
                collaborative_count += 1
        
        # Determine predominant tone
        if collaborative_count > directive_count and positive_count > 0:
            return "collaborative"
        elif directive_count > collaborative_count:
            return "directive"
        else:
            return "mixed"
    
    def _analyze_communication_patterns(self, comments, pr_author) -> Dict[str, Any]:
        """Analyze communication patterns and response behaviors"""
        patterns = {
            'author_responsiveness': 0.0,
            'reviewer_follow_up_rate': 0.0,
            'discussion_depth': 0.0,
            'conflict_indicators': [],
            'collaboration_indicators': []
        }
        
        # Analyze author responsiveness
        author_responses = [c for c in comments if c.author == pr_author]
        reviewer_comments = [c for c in comments if c.author != pr_author]
        
        if reviewer_comments:
            patterns['author_responsiveness'] = len(author_responses) / len(reviewer_comments)
        
        # Look for conflict indicators
        conflict_keywords = ['disagree', 'wrong', 'incorrect', 'no', 'but', 'however']
        collaboration_keywords = ['agree', 'yes', 'good point', 'thanks', 'exactly']
        
        for comment in comments:
            comment_lower = comment.body.lower()
            if any(keyword in comment_lower for keyword in conflict_keywords):
                patterns['conflict_indicators'].append(comment.author)
            if any(keyword in comment_lower for keyword in collaboration_keywords):
                patterns['collaboration_indicators'].append(comment.author)
        
        return patterns
    
    def _generate_conversation_summary(self, threads, reviewer_profiles, pr_data) -> str:
        """Generate a human-readable summary of the conversations"""
        summary_parts = []
        
        # Overall conversation overview
        total_participants = len(reviewer_profiles) + 1  # +1 for PR author
        summary_parts.append(f"This PR involved {total_participants} participants in {len(threads)} conversation threads.")
        
        # Highlight major discussion points
        if threads:
            major_threads = [t for t in threads if len(t.comments) >= 3]
            if major_threads:
                summary_parts.append(f"\nMajor discussion points included:")
                for thread in major_threads[:3]:  # Top 3 threads
                    summary_parts.append(f"• {thread.topic} ({len(thread.comments)} exchanges, {thread.resolution_status})")
        
        # Reviewer engagement summary
        if reviewer_profiles:
            active_reviewers = [name for name, profile in reviewer_profiles.items() 
                             if profile.engagement_level in ['high', 'medium']]
            if active_reviewers:
                summary_parts.append(f"\nActive reviewers: {', '.join(active_reviewers)}")
        
        # Resolution status
        resolved_count = sum(1 for t in threads if t.resolution_status == 'resolved')
        if threads:
            resolution_rate = resolved_count / len(threads) * 100
            summary_parts.append(f"\nConversation resolution rate: {resolution_rate:.1f}% ({resolved_count}/{len(threads)} threads resolved)")
        
        return "\n".join(summary_parts) 