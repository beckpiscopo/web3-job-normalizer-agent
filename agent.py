from langgraph.graph import StateGraph, END
from state import JobTitleState
from nodes import analyze_title, research_title, normalize_title, route_after_analysis

def create_job_title_normalizer():
    """
    Create the job title normalizer agent graph.
    """
    # Create the graph
    workflow = StateGraph(JobTitleState)
    
    # Add nodes
    workflow.add_node("analyze", analyze_title)
    workflow.add_node("research", research_title)
    workflow.add_node("normalize", normalize_title)
    
    # Set entry point
    workflow.set_entry_point("analyze")
    
    # Add conditional routing after analysis
    workflow.add_conditional_edges(
        "analyze",
        route_after_analysis,
        {
            "research": "research",
            "normalize": "normalize"
        }
    )
    
    # After research, always normalize
    workflow.add_edge("research", "normalize")
    
    # After normalize, end
    workflow.add_edge("normalize", END)
    
    # Compile the graph
    app = workflow.compile()
    
    return app


def normalize_job_title(raw_title: str, company: str = None):
    """
    Convenience function to normalize a single job title.
    """
    app = create_job_title_normalizer()
    
    initial_state = {
        "raw_title": raw_title,
        "company": company,
        "confidence": 0.0,
        "needs_research": False,
        "search_query": None,
        "search_results": None,
        "reasoning": "",
        "normalized_title": "",
        "category": "",
        "subcategory": "",
        "confidence_score": 0.0,
        "requires_human_review": False,
        "messages": []
    }
    
    result = app.invoke(initial_state)
    
    return result


if __name__ == "__main__":
    # Test with some sample job titles
    test_titles = [
        ("Senior Solidity Engineer", "Uniswap"),
        ("DeFi Product Lead", "Aave"),
        ("Blockchain Wizard", "Unknown Startup"),
        ("Head of Growth", "Coinbase"),
        ("Smart Contract Auditor", "OpenZeppelin")
    ]
    
    print("=" * 80)
    print("JOB TITLE NORMALIZER AGENT - TEST RUN")
    print("=" * 80)
    
    for title, company in test_titles:
        print(f"\n📋 Processing: '{title}' at {company}")
        print("-" * 80)
        
        result = normalize_job_title(title, company)
        
        print(f"✅ Normalized Title: {result['normalized_title']}")
        print(f"📂 Category: {result['category']}")
        print(f"🏷️  Subcategory: {result['subcategory']}")
        print(f"📊 Confidence: {result['confidence_score']:.2f}")
        print(f"👤 Needs Review: {result['requires_human_review']}")
        print(f"\n💭 Processing Steps:")
        for msg in result['messages']:
            print(f"   - {msg}")
        print("=" * 80)