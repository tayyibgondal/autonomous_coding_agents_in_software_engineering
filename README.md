# Autonomous Coding Agents in Software Engineering

A comprehensive empirical analysis of AI coding agents' performance and behavior in real-world software development using the AIDev dataset.

## 📊 Overview

This project analyzes the adoption, performance, and collaboration patterns of autonomous coding agents (Claude Code, Cursor, Copilot, Devin, OpenAI Codex) in software engineering. Through extensive data analysis and visualization, we explore how these AI agents contribute to open-source repositories, interact with human developers, and evolve over time.

## 🎯 Research Questions

1. **Agent Adoption**: How are different AI coding agents being adopted across repositories?
2. **PR Acceptance Rates**: What are the success rates of PRs submitted by different agents?
3. **Entity Distributions**: How do code contributions vary across agents in terms of size and complexity?
4. **Temporal Evolution**: How have agent behaviors and performance changed over time?
5. **Human-Bot Collaboration**: How do human reviewers engage with AI-generated code?
6. **Learning Curves**: Do AI agents improve their performance within the same repository?
7. **Review Conversation Depth**: What role do code review discussions play in PR outcomes?

## 📁 Dataset

**AIDev Dataset** - A large-scale dataset of AI-generated pull requests from GitHub
- **Pull Requests**: 33,596 agentic PRs
- **Repositories**: 2,807 repositories
- **Developers**: 1,796 users
- **Reviews**: 28,875 PR reviews
- **Comments**: 39,122 PR comments
- **Commits**: 88,576 commits with 711,923 file-level changes
- **Timeline Events**: 325,500 events
- **Duration**: December 2024 - July 2025 (218 days)

Source: [HuggingFace - AIDev Dataset](https://huggingface.co/datasets/hao-li/AIDev)

## 🔧 Requirements

```bash
Python 3.8+
pandas
numpy
matplotlib
seaborn
scipy
```

Install dependencies:
```bash
pip install pandas numpy matplotlib seaborn scipy
```

## 📈 Analyses & Visualizations

### Figure 1: Agent Adoption Landscape
Three-panel analysis showing:
- PR volume distribution by agent
- Repository reach across agents
- Intensity of usage (PRs per repository)

**Key Finding**: OpenAI Codex dominates with 21,799 PRs (64.89%), with the highest intensity of 17.5 PRs/repo.

### Figure 2: PR Acceptance Rates
- PR status distribution by agent (merged, closed unmerged, open)
- Temporal trends in merge rates

**Key Finding**: OpenAI Codex has the highest merge rate (82.6%), while Copilot has the lowest (43.0%).

### Figure 3: Entity Distribution Analysis
Nine-panel comprehensive analysis including:
- Files changed per PR
- Code additions distribution
- PR description lengths
- Review comment intensity
- Time to merge latency
- Repository popularity
- Commit message verbosity
- Developer social reach
- Issue description detail

### Figure 4: Temporal Evolution
Four-panel time-series analysis:
- Monthly PR activity by agent
- Cumulative repository adoption
- Code churn evolution (median lines added)
- Monthly review activity

### Figure 5: Human vs Bot Reviewer Engagement
Six-panel analysis of review patterns:
- Reviewer type distribution (human vs bot)
- Review verbosity comparison
- Review decision distribution
- Comment frequency
- Top 10 human reviewers
- Top 10 bot reviewers

**Key Finding**: 58.5% of reviews are from humans, 41.5% from bots.

### Figure 6: Learning Curves
Agent-specific analysis of performance improvement over time within the same repository.

**Key Finding**: Claude Code shows improvement (+3.2%), while Devin and Cursor show slight declines.

### Figure 7: Conversation Depth Analysis
Impact of review discussions on PR outcomes.

**Key Finding**: PRs with no discussion have 80.6% merge rate vs 59.0% for heavily discussed PRs, suggesting discussions often arise from problematic code.

## 📊 Key Statistics

### Dataset Metrics
- **Total Lines Added**: 26,137,647
- **Total Lines Deleted**: 12,610,026
- **Net Lines of Code**: 13,527,621
- **Unique Files Modified**: 196,073
- **Total Text Content**: 105.78 MB

### Programming Languages
- **Top Language**: TypeScript (650 repos, 23.16%)
- **Second**: Python (530 repos, 18.88%)
- **Third**: Go (242 repos, 8.62%)

### Multi-Language PRs
- **Single-language PRs**: 43.9%
- **Multi-language PRs**: 35.2%
- **Average languages per PR**: 1.39
- **Most versatile agent**: Claude Code (59.2% multi-language, avg 2.57 langs/PR)

### Traceability Analysis
- **Total URLs found**: 159,095
- **Unique URLs**: 86,798
- **Top domain**: github.com (15.47%)
- **External URLs**: 81.0%

## 🚀 Usage

1. **Load the dataset**:
```python
import pandas as pd

# Load core datasets
pr_df = pd.read_parquet("hf://datasets/hao-li/AIDev/pull_request.parquet")
repo_df = pd.read_parquet("hf://datasets/hao-li/AIDev/repository.parquet")
user_df = pd.read_parquet("hf://datasets/hao-li/AIDev/user.parquet")
```

2. **Run the analysis**:
Open `ASSIGNMENT.ipynb` in Jupyter Notebook and execute cells sequentially.

3. **Generate figures**:
All figures are automatically saved to the `figures/` directory in both PDF and PNG formats.

## 📂 Project Structure

```
autonomous_coding_agents_in_software_engineering/
├── ASSIGNMENT.ipynb          # Main analysis notebook
├── README.md                  # This file
├── figures/                   # Generated visualizations
│   ├── fig1_agent_adoption_landscape.png
│   ├── fig2_pr_acceptance_rates.png
│   ├── fig3_entity_distributions.png
│   ├── fig4_temporal_evolution.png
│   ├── fig5_human_vs_bot_engagement.png
│   ├── fig6_learning_curves.png
│   └── fig7_conversation_depth.png
├── analysis/                  # Additional analysis notebooks
│   ├── dataset_overview.ipynb
│   ├── language_usage.ipynb
│   ├── productivity.ipynb
│   └── reviewers.ipynb
└── backup/                    # Backup files
```

## 🔍 Novel Insights

### 1. Learning Effects
Most AI agents maintain consistent performance over time within repositories, with Claude Code showing modest improvement (+3.2%) and others remaining stable or slightly declining.

### 2. Review Discussion Paradox
Heavy review discussions correlate with 21.5% lower merge rates, indicating that discussions typically arise from problematic code rather than healthy collaboration.

### 3. Agent Specialization
- **OpenAI Codex**: Highest volume, best merge rate, most repositories
- **Claude Code**: Most versatile, handles multi-language projects
- **Cursor**: Strong repository diversity
- **Devin**: Moderate performance across metrics
- **Copilot**: Lowest merge rate, unique usage pattern

### 4. Human-Bot Review Dynamics
- Bots write longer reviews (avg 11,700 chars) compared to humans (avg 200 chars)
- Human reviewers are more critical, with higher rates of change requests
- Bot reviewers dominate certain agents' PRs

## 📝 Citation

If you use this analysis or the AIDev dataset in your research, please cite:

```bibtex
@dataset{aidev2025,
  title={AIDev: A Dataset of AI-Generated Pull Requests},
  author={Li, Hao and others},
  year={2025},
  publisher={HuggingFace}
}
```

## 🙏 Acknowledgments

- **AIDev Dataset**: Hao Li and contributors
- **HuggingFace**: For hosting the dataset
- **AI Coding Agents**: Claude Code, Cursor, GitHub Copilot, Devin, OpenAI Codex

## 📧 Contact

For questions or collaborations, please open an issue in this repository.

## 📄 License

This analysis is provided for educational and research purposes. Please refer to the original AIDev dataset license for data usage terms.

---

**Last Updated**: October 2025

