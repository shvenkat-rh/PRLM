"""
Timeline analysis for PR lifecycle metrics.
"""

from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class TimelineMetrics:
    """PR timeline metrics"""
    created_at: datetime
    first_review_at: Optional[datetime]
    last_activity_at: datetime
    merged_at: Optional[datetime]
    closed_at: Optional[datetime]
    
    # Calculated metrics
    time_to_first_review: Optional[float]  # hours
    time_to_merge: Optional[float]  # hours
    total_lifecycle: float  # hours
    review_cycles: int
    comment_frequency: float  # comments per day

@dataclass
class ActivityPeriod:
    """Represents a period of activity on the PR"""
    start: datetime
    end: datetime
    activity_type: str  # 'review', 'discussion', 'revision'
    participants: List[str]

class TimelineAnalyzer:
    """Analyzes PR timeline and lifecycle metrics"""
    
    def analyze_timeline(self, pr_data) -> TimelineMetrics:
        """Analyze the complete timeline of a PR"""
        created_at = datetime.fromisoformat(pr_data.created_at.replace('Z', '+00:00'))
        
        # Find first review
        first_review_at = self._find_first_review(pr_data)
        
        # Find merge/close time
        merged_at = None
        closed_at = None
        
        if hasattr(pr_data, 'merged_at') and pr_data.merged_at:
            merged_at = datetime.fromisoformat(pr_data.merged_at.replace('Z', '+00:00'))
        if hasattr(pr_data, 'closed_at') and pr_data.closed_at:
            closed_at = datetime.fromisoformat(pr_data.closed_at.replace('Z', '+00:00'))
            
        # Use updated_at as fallback for last activity
        last_activity_at = datetime.fromisoformat(pr_data.updated_at.replace('Z', '+00:00'))
        
        # Calculate metrics
        time_to_first_review = None
        if first_review_at:
            time_to_first_review = (first_review_at - created_at).total_seconds() / 3600
            
        time_to_merge = None
        if merged_at:
            time_to_merge = (merged_at - created_at).total_seconds() / 3600
            
        total_lifecycle = (last_activity_at - created_at).total_seconds() / 3600
        
        # Count review cycles and comments
        review_cycles = self._count_review_cycles(pr_data)
        comment_frequency = self._calculate_comment_frequency(pr_data, created_at, last_activity_at)
        
        return TimelineMetrics(
            created_at=created_at,
            first_review_at=first_review_at,
            last_activity_at=last_activity_at,
            merged_at=merged_at,
            closed_at=closed_at,
            time_to_first_review=time_to_first_review,
            time_to_merge=time_to_merge,
            total_lifecycle=total_lifecycle,
            review_cycles=review_cycles,
            comment_frequency=comment_frequency
        )
    
    def _find_first_review(self, pr_data) -> Optional[datetime]:
        """Find the timestamp of the first review"""
        earliest_review = None
        
        # Check review comments
        for comment in pr_data.comments:
            if comment.type in ['review_comment', 'review']:
                comment_time = datetime.fromisoformat(comment.created_at.replace('Z', '+00:00'))
                if earliest_review is None or comment_time < earliest_review:
                    earliest_review = comment_time
                    
        # Check formal reviews
        for review in pr_data.reviews:
            if review.get('submitted_at'):
                review_time = datetime.fromisoformat(review['submitted_at'].replace('Z', '+00:00'))
                if earliest_review is None or review_time < earliest_review:
                    earliest_review = review_time
                    
        return earliest_review
    
    def _count_review_cycles(self, pr_data) -> int:
        """Count the number of review cycles"""
        # A review cycle is defined as a period of feedback followed by changes
        cycles = 0
        
        # Group activities by day to identify cycles
        activities_by_day = {}
        
        # Add comments
        for comment in pr_data.comments:
            if comment.type in ['review_comment', 'review']:
                date = datetime.fromisoformat(comment.created_at.replace('Z', '+00:00')).date()
                if date not in activities_by_day:
                    activities_by_day[date] = {'reviews': 0, 'commits': 0}
                activities_by_day[date]['reviews'] += 1
        
        # Add commits
        for commit in pr_data.commits:
            date = datetime.fromisoformat(commit['date'].replace('Z', '+00:00')).date()
            if date not in activities_by_day:
                activities_by_day[date] = {'reviews': 0, 'commits': 0}
            activities_by_day[date]['commits'] += 1
        
        # Count cycles (days with both reviews and subsequent commits)
        sorted_dates = sorted(activities_by_day.keys())
        for i in range(len(sorted_dates) - 1):
            current_day = activities_by_day[sorted_dates[i]]
            next_day = activities_by_day[sorted_dates[i + 1]]
            
            if current_day['reviews'] > 0 and next_day['commits'] > 0:
                cycles += 1
                
        return max(1, cycles)  # At least 1 cycle
    
    def _calculate_comment_frequency(self, pr_data, start_time: datetime, end_time: datetime) -> float:
        """Calculate comments per day"""
        total_days = max(1, (end_time - start_time).days)
        total_comments = len(pr_data.comments)
        return total_comments / total_days
    
    def analyze_activity_periods(self, pr_data) -> List[ActivityPeriod]:
        """Identify distinct periods of activity"""
        periods = []
        
        # Combine all timestamped activities
        activities = []
        
        # Add comments
        for comment in pr_data.comments:
            activities.append({
                'timestamp': datetime.fromisoformat(comment.created_at.replace('Z', '+00:00')),
                'type': 'comment',
                'author': comment.author,
                'activity': comment.type
            })
        
        # Add commits
        for commit in pr_data.commits:
            activities.append({
                'timestamp': datetime.fromisoformat(commit['date'].replace('Z', '+00:00')),
                'type': 'commit',
                'author': commit['author'],
                'activity': 'commit'
            })
        
        # Sort by timestamp
        activities.sort(key=lambda x: x['timestamp'])
        
        # Group into periods (gap of more than 1 day = new period)
        if not activities:
            return periods
            
        current_period_start = activities[0]['timestamp']
        current_period_activities = [activities[0]]
        
        for activity in activities[1:]:
            time_gap = (activity['timestamp'] - current_period_activities[-1]['timestamp']).total_seconds() / 3600
            
            if time_gap > 24:  # More than 24 hours gap
                # End current period
                period_type = self._determine_period_type(current_period_activities)
                participants = list(set(act['author'] for act in current_period_activities))
                
                periods.append(ActivityPeriod(
                    start=current_period_start,
                    end=current_period_activities[-1]['timestamp'],
                    activity_type=period_type,
                    participants=participants
                ))
                
                # Start new period
                current_period_start = activity['timestamp']
                current_period_activities = [activity]
            else:
                current_period_activities.append(activity)
        
        # Add final period
        if current_period_activities:
            period_type = self._determine_period_type(current_period_activities)
            participants = list(set(act['author'] for act in current_period_activities))
            
            periods.append(ActivityPeriod(
                start=current_period_start,
                end=current_period_activities[-1]['timestamp'],
                activity_type=period_type,
                participants=participants
            ))
        
        return periods
    
    def _determine_period_type(self, activities: List[Dict]) -> str:
        """Determine the type of activity period"""
        commit_count = sum(1 for act in activities if act['type'] == 'commit')
        comment_count = sum(1 for act in activities if act['type'] == 'comment')
        
        if commit_count > comment_count:
            return 'revision'
        elif comment_count > 0:
            return 'review'
        else:
            return 'discussion' 