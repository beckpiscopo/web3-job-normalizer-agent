from typing import TypedDict, Optional, List
from typing_extensions import Annotated

class JobTitleState(TypedDict):
    """State that flows through the job title normalizer agent."""
    
    # Input
    raw_title: str
    company: Optional[str]
    
    # Processing
    confidence: float
    needs_research: bool
    search_query: Optional[str]
    search_results: Optional[str]
    reasoning: str
    
    # Output
    normalized_title: str
    category: str  # e.g., "Engineering", "Design", "Marketing", "Operations"
    subcategory: str  # e.g., "Frontend", "Backend", "Full Stack", "DevOps"
    confidence_score: float
    requires_human_review: bool
    
    # Messages for tracking
    messages: Annotated[List[str], "append"]