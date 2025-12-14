cat > /Users/beckpiscopo/Desktop/dev/agents/job-title-normalizer/README.md << 'EOF'
# Web3 Job Normalizer Agent

An AI-powered agent built with LangGraph that normalizes messy web3/crypto job titles into standardized categories.

## Features

- Intelligent job title analysis using Claude
- Conditional routing based on confidence levels
- Automatic categorization into standard web3 roles
- Flags ambiguous titles for human review
- High accuracy on common web3 positions

## How It Works
```
START → Analyze Title → [Decision Point]
                          ├→ High Confidence → Normalize → END
                          └→ Low Confidence → Research → Normalize → END
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/beckpiscopo/web3-job-normalizer-agent.git
cd web3-job-normalizer-agent
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your API key:
```bash
ANTHROPIC_API_KEY=your_api_key_here
```

## Usage

Run the test suite:
```bash
python agent.py
```

Use in your own code:
```python
from agent import normalize_job_title

result = normalize_job_title("Blockchain Wizard", "Cool Startup")
print(f"Normalized: {result['normalized_title']}")
print(f"Category: {result['category']}")
print(f"Confidence: {result['confidence_score']}")
```

## Example Output
```
Processing: 'Senior Solidity Engineer' at Uniswap
Normalized Title: Senior Smart Contract Engineer
Category: Engineering
Subcategory: Smart Contract
Confidence: 0.95
Needs Review: False
```

## Categories

- **Engineering**: Frontend, Backend, Full Stack, Smart Contract, Protocol, DevOps, Security, Data
- **Design**: Product Design, UI/UX, Visual Design, Brand Design
- **Product**: Product Manager, Product Owner, Technical PM
- **Marketing**: Growth, Content, Community, Social Media, Brand
- **Operations**: Operations Manager, Program Manager, Project Manager
- **Business Development**: Partnerships, Sales, Strategy
- **Research**: Research Analyst, Data Analyst, Researcher
- **Leadership**: C-Level, Director, VP, Head of
- **Community**: Community Manager, Developer Relations, Moderator
- **Legal**: Legal Counsel, Compliance, Regulatory

## Tech Stack

- [LangGraph](https://github.com/langchain-ai/langgraph) - Agent orchestration
- [LangChain](https://github.com/langchain-ai/langchain) - LLM framework
- [Anthropic Claude](https://www.anthropic.com/) - Language model
- Python 3.11+

## Project Structure
```
web3-job-normalizer-agent/
├── state.py          # State schema definition
├── nodes.py          # Node processing functions
├── agent.py          # Main graph & test runner
├── requirements.txt  # Dependencies
└── .env             # API keys (not committed)
```

## Future Enhancements

- [ ] Real web search integration (Tavily)
- [ ] Batch processing from CSV
- [ ] Database storage for learning
- [ ] Human-in-the-loop review workflow
- [ ] Streamlit UI

## License

MIT

## Contributing

Contributions welcome! Please feel free to submit a Pull Request.
EOF