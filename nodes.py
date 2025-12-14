from state import JobTitleState
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize the LLM
llm = ChatAnthropic(model="claude-sonnet-4-20250514", api_key=os.getenv("ANTHROPIC_API_KEY"))

# Common web3 job categories
WEB3_CATEGORIES = {
    "Engineering": ["Frontend", "Backend", "Full Stack", "Smart Contract", "Protocol", "DevOps", "Security", "Data"],
    "Design": ["Product Design", "UI/UX", "Visual Design", "Brand Design"],
    "Product": ["Product Manager", "Product Owner", "Technical PM"],
    "Marketing": ["Growth", "Content", "Community", "Social Media", "Brand"],
    "Operations": ["Operations Manager", "Program Manager", "Project Manager"],
    "Business Development": ["Partnerships", "Sales", "Strategy"],
    "Research": ["Research Analyst", "Data Analyst", "Researcher"],
    "Leadership": ["C-Level", "Director", "VP", "Head of"],
    "Community": ["Community Manager", "Developer Relations", "Moderator"],
    "Legal": ["Legal Counsel", "Compliance", "Regulatory"]
}

def analyze_title(state: JobTitleState) -> JobTitleState:
    """
    Initial analysis of the job title to determine confidence and if research is needed.
    """
    raw_title = state["raw_title"]
    company = state.get("company", "Unknown")
    
    system_prompt = """You are an expert at analyzing and categorizing web3/crypto job titles.

Analyze the job title and determine:
1. Your confidence level (0.0 to 1.0) in categorizing it
2. Whether you need web research to understand it better
3. Initial reasoning

Respond in this format:
CONFIDENCE: <float>
NEEDS_RESEARCH: <true/false>
REASONING: <your reasoning>"""

    user_prompt = f"""Available categories: {list(WEB3_CATEGORIES.keys())}

Job Title: {raw_title}
Company: {company}"""

    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ])
    content = response.content
    
    # Parse response
    lines = content.split('\n')
    confidence = 0.5
    needs_research = False
    reasoning = ""
    
    for line in lines:
        if line.startswith("CONFIDENCE:"):
            try:
                confidence = float(line.split(":")[1].strip())
            except:
                confidence = 0.5
        elif line.startswith("NEEDS_RESEARCH:"):
            needs_research = "true" in line.lower()
        elif line.startswith("REASONING:"):
            reasoning = line.split(":", 1)[1].strip()
    
    return {
        **state,
        "confidence": confidence,
        "needs_research": needs_research,
        "reasoning": reasoning,
        "messages": [f"Analyzed '{raw_title}' - Confidence: {confidence}, Needs Research: {needs_research}"]
    }


def research_title(state: JobTitleState) -> JobTitleState:
    """
    Research the job title using web search for additional context.
    """
    raw_title = state["raw_title"]
    company = state.get("company", "")
    
    # Create a search query
    search_query = f"{raw_title} {company} web3 crypto job responsibilities".strip()
    
    # For now, we'll simulate search results
    # In production, you'd use Tavily or another search tool
    search_results = f"Simulated search results for: {search_query}"
    
    return {
        **state,
        "search_query": search_query,
        "search_results": search_results,
        "messages": [f"Researched title with query: {search_query}"]
    }


def normalize_title(state: JobTitleState) -> JobTitleState:
    """
    Normalize the job title into standard category and subcategory.
    """
    raw_title = state["raw_title"]
    company = state.get("company", "Unknown")
    search_results = state.get("search_results", "No additional research")
    
    system_prompt = """You are an expert at normalizing web3/crypto job titles into standard categories.

Provide:
1. A normalized, standard job title
2. The primary category
3. The subcategory
4. A confidence score (0.0 to 1.0)
5. Whether this needs human review (if confidence < 0.7)

Respond EXACTLY in this format:
NORMALIZED_TITLE: <title>
CATEGORY: <category>
SUBCATEGORY: <subcategory>
CONFIDENCE: <float>
HUMAN_REVIEW: <true/false>"""

    user_prompt = f"""Available categories and subcategories:
{WEB3_CATEGORIES}

Given the following information, normalize the job title:

Original Title: {raw_title}
Company: {company}
Research Context: {search_results}"""

    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ])
    content = response.content
    
    # Parse response
    normalized_title = raw_title
    category = "Unknown"
    subcategory = "Unknown"
    confidence_score = 0.5
    requires_human_review = True
    
    for line in content.split('\n'):
        if line.startswith("NORMALIZED_TITLE:"):
            normalized_title = line.split(":", 1)[1].strip()
        elif line.startswith("CATEGORY:"):
            category = line.split(":", 1)[1].strip()
        elif line.startswith("SUBCATEGORY:"):
            subcategory = line.split(":", 1)[1].strip()
        elif line.startswith("CONFIDENCE:"):
            try:
                confidence_score = float(line.split(":", 1)[1].strip())
            except:
                confidence_score = 0.5
        elif line.startswith("HUMAN_REVIEW:"):
            requires_human_review = "true" in line.lower()
    
    return {
        **state,
        "normalized_title": normalized_title,
        "category": category,
        "subcategory": subcategory,
        "confidence_score": confidence_score,
        "requires_human_review": requires_human_review,
        "messages": [f"Normalized to: {normalized_title} ({category} - {subcategory})"]
    }


def route_after_analysis(state: JobTitleState) -> str:
    """
    Routing function to decide next step after analysis.
    """
    if state["needs_research"] or state["confidence"] < 0.7:
        return "research"
    else:
        return "normalize"
