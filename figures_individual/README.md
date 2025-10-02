# Individual Figure Documentation

This directory contains **30 high-quality individual figures** generated from the AIDev dataset analysis. Each figure is saved separately with clear, readable text at 300 DPI resolution.

## Why Individual Figures?

The original analysis notebooks (`data_exploration.ipynb` and `more_exploration.ipynb`) created multi-subfigure plots (e.g., 3x3, 2x3 grids) which made individual plots hard to read. These individual figures provide:

✅ **Larger text** - Font sizes: 14-18pt (vs 10-12pt in subfigures)  
✅ **Bold labels** - All axis labels and titles are bold for clarity  
✅ **Clear titles** - Each figure has a descriptive, standalone title  
✅ **Better resolution** - 12x8 inch figures at 300 DPI  
✅ **Meaningful names** - Files are numbered and named descriptively  
✅ **Value annotations** - Bar charts include numeric labels  

## Figure Organization

### Section 1: PR Metrics Distributions (Files 01-09)

*From `more_exploration.ipynb` - Basic distribution analysis*

| File | Description | Metrics |
|------|-------------|---------|
| `01_pr_files_changed_histogram.png` | Files changed per PR (histogram) | Median: varied |
| `02_pr_files_changed_boxplot.png` | Files changed per PR (box plot) | Shows outliers |
| `03_pr_files_changed_violinplot.png` | Files changed per PR (violin plot) | Distribution shape |
| `04_pr_lines_added_histogram.png` | Lines added per PR | Code growth |
| `05_pr_lines_deleted_histogram.png` | Lines deleted per PR | Code reduction |
| `06_pr_total_changes_histogram.png` | Total changes per PR | Overall activity |
| `07_pr_title_length_histogram.png` | PR title length distribution | Text metrics |
| `08_pr_body_length_histogram.png` | PR body length distribution | Description detail |
| `09_pr_state_distribution.png` | PR state (merged/closed/open) | Acceptance rates |

### Section 2: Commit, Review, and Timeline Distributions (Files 10-18)

| File | Description | Metrics |
|------|-------------|---------|
| `10_commits_per_pr_histogram.png` | Commits per PR (histogram) | Development activity |
| `11_commits_per_pr_boxplot.png` | Commits per PR (box plot) | Outlier detection |
| `12_commit_message_length_histogram.png` | Commit message length | Documentation quality |
| `13_reviews_per_pr_histogram.png` | Reviews per PR | Review engagement |
| `14_review_body_length_histogram.png` | Review comment length | Feedback detail |
| `15_review_state_distribution.png` | Review states (approved/commented) | Review outcomes |
| `16_comments_per_pr_histogram.png` | Comments per PR | Discussion level |
| `17_comment_body_length_histogram.png` | Comment length distribution | Comment detail |
| `18_timeline_events_per_pr_histogram.png` | Timeline events per PR | PR lifecycle |

### Section 3: User and Repository Distributions (Files 19-24)

| File | Description | Metrics |
|------|-------------|---------|
| `19_prs_per_user_histogram.png` | PRs per user | User activity |
| `20_prs_per_repo_histogram.png` | PRs per repository | Repo activity |
| `21_user_followers_histogram.png` | User followers distribution | Developer influence |
| `22_repo_stars_histogram.png` | Repository stars | Project popularity |
| `23_repo_forks_histogram.png` | Repository forks | Community engagement |
| `24_programming_languages_barplot.png` | Top 15 programming languages | Language distribution |

### Section 4: File-Level Change Distributions (Files 25-30)

*From `more_exploration.ipynb` - File-level granularity*

| File | Description | Metrics |
|------|-------------|---------|
| `25_file_additions_histogram.png` | Lines added per file | File-level growth |
| `26_file_deletions_histogram.png` | Lines deleted per file | File-level reduction |
| `27_file_status_distribution.png` | File statuses (modified/added/deleted) | Change types |
| `28_file_additions_boxplot.png` | File additions (box plot) | Addition outliers |
| `29_file_deletions_boxplot.png` | File deletions (box plot) | Deletion outliers |
| `30_timeline_event_types_barplot.png` | Top 15 timeline event types | Event categories |

### Section 5: Entity Distributions by Agent (Files 31-39)

*From `data_exploration.ipynb` - Agent-specific behavioral analysis*

| File | Description | Plot Type | Metrics |
|------|-------------|-----------|---------|
| `31_entity_files_changed_by_agent.png` | Files changed per PR by agent | Violin plot | Agent comparison |
| `32_entity_lines_added_by_agent.png` | Lines added distribution by agent | Box plot (log scale) | Code volume |
| `33_entity_pr_description_length_by_agent.png` | PR description length by agent | Histogram overlay | Documentation detail |
| `34_entity_review_comment_intensity_by_agent.png` | Review comment intensity by agent | Violin plot | Engagement levels |
| `35_entity_time_to_merge_by_agent.png` | Time to merge by agent | Box plot | Merge velocity |
| `36_entity_repository_popularity.png` | Repository popularity distribution | Histogram (log scale) | Star counts |
| `37_entity_commit_message_verbosity.png` | Commit message verbosity | Histogram | Message lengths |
| `38_entity_developer_social_reach.png` | Developer social reach | Histogram (log scale) | Follower counts |
| `39_entity_issue_description_detail.png` | Issue description detail | Histogram | Issue body lengths |

## Technical Specifications

### Figure Properties
- **Size**: 12x8 inches (10x8 for box plots, 12x10 for horizontal bar plots)
- **Resolution**: 300 DPI
- **Format**: PNG with transparent backgrounds where applicable
- **Font Sizes**:
  - Main text: 14pt
  - Axis labels: 16pt (bold)
  - Titles: 18pt (bold)
  - Tick labels: 13pt
  - Legend: 13pt

### Visual Features
- **Grid lines**: Dashed horizontal/vertical grids (alpha=0.3)
- **Edge colors**: Black borders on bars/histograms (linewidth=1.5)
- **Alpha values**: 0.75 for histograms, 0.8 for bar charts
- **Color schemes**:
  - Histograms: Domain-specific colors (blue for files, green for additions, red for deletions)
  - Bar charts: Colormap-based (tab10, tab20, Set3, Paired)
  - Box plots: Themed colors matching histogram counterparts

### Data Filtering
Many figures filter extreme outliers for better visualization:
- Files changed: ≤50 files
- Lines added/deleted: ≤1000 lines
- PR title: ≤200 characters
- PR body: ≤5000 characters
- Commits: ≤20 per PR
- Reviews: ≤10 per PR
- Comments: ≤20 per PR
- Timeline events: ≤30 per PR

*Note: Full data ranges are preserved in the calculations; filtering only affects visualization.*

## Generation

These figures were generated using `regenerate_individual_figures.py` script, which:
1. Loads all AIDev dataset tables
2. Calculates metrics and aggregations
3. Creates individual high-quality figures
4. Saves to `figures_individual/` directory

To regenerate all figures:
```bash
python regenerate_individual_figures.py
```

## Usage in Reports

These figures are ideal for:
- **Academic papers** - High DPI suitable for publication
- **Presentations** - Clear text readable on projectors
- **Reports** - Professional appearance with meaningful titles
- **Web content** - High quality with good compression

### LaTeX Integration
```latex
\begin{figure}[H]
\centering
\includegraphics[width=0.8\textwidth]{figures_individual/01_pr_files_changed_histogram.png}
\caption{Files changed per pull request distribution}
\label{fig:pr_files_changed}
\end{figure}
```

### Markdown Integration
```markdown
![Files Changed per PR](figures_individual/01_pr_files_changed_histogram.png)
```

## Dataset Statistics

- **Pull Requests**: 33,596
- **Repositories**: 2,807
- **Users**: 1,796
- **Comments**: 39,122
- **Reviews**: 28,875
- **Commits**: 88,576
- **File Changes**: 711,923
- **Timeline Events**: 325,500

## Notes

- All statistics include median and mean values in titles
- Bar charts include value labels for exact counts
- Box plots show outliers as red circles
- Violin plots show distribution density
- Horizontal bar plots are inverted (highest at top)

---

**Generated**: October 2025  
**Source**: AIDev Dataset (hf://datasets/hao-li/AIDev)  
**Script**: `regenerate_individual_figures.py`

