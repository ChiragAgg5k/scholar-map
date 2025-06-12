"""Research Paper model"""
from dataclasses import dataclass


@dataclass
class Paper:
    """Data class for research papers"""

    paper_id: str
    title: str
    authors: str
    category: str
    pub_date: str
    arxiv_id: str
    journal: str
    research_field: str
    paper_type: str
    citation_count: int
    abstract: str
    relevance_score: float = 0.0
