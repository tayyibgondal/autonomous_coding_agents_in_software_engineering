"""
Script to regenerate all visualization figures as individual plots with clear, readable text.
This replaces the multi-subfigure plots with individual high-quality figures.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Create figures directory
Path("figures_individual").mkdir(exist_ok=True)

print("="*80)
print("REGENERATING ALL FIGURES AS INDIVIDUAL PLOTS")
print("="*80)

# Set publication-quality defaults
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 14
plt.rcParams['axes.labelsize'] = 16
plt.rcParams['axes.titlesize'] = 18
plt.rcParams['xtick.labelsize'] = 13
plt.rcParams['ytick.labelsize'] = 13
plt.rcParams['legend.fontsize'] = 13

# Load data
print("\nLoading datasets...")
pr_df = pd.read_parquet("hf://datasets/hao-li/AIDev/pull_request.parquet")
repo_df = pd.read_parquet("hf://datasets/hao-li/AIDev/repository.parquet")
user_df = pd.read_parquet("hf://datasets/hao-li/AIDev/user.parquet")
pr_comments_df = pd.read_parquet("hf://datasets/hao-li/AIDev/pr_comments.parquet")
pr_reviews_df = pd.read_parquet("hf://datasets/hao-li/AIDev/pr_reviews.parquet")
pr_commits_df = pd.read_parquet("hf://datasets/hao-li/AIDev/pr_commits.parquet")
pr_commit_details_df = pd.read_parquet("hf://datasets/hao-li/AIDev/pr_commit_details.parquet")
pr_timeline_df = pd.read_parquet("hf://datasets/hao-li/AIDev/pr_timeline.parquet")

print(f"✓ Loaded {len(pr_df):,} PRs, {len(repo_df):,} repos, {len(user_df):,} users")

# Calculate metrics
print("\nCalculating metrics...")
pr_df['title_length'] = pr_df['title'].apply(lambda x: len(str(x)) if pd.notna(x) else 0)
pr_df['body_length'] = pr_df['body'].apply(lambda x: len(str(x)) if pd.notna(x) else 0)

files_per_pr = pr_commit_details_df.groupby('pr_id').size()
additions_per_pr = pr_commit_details_df.groupby('pr_id')['additions'].sum()
deletions_per_pr = pr_commit_details_df.groupby('pr_id')['deletions'].sum()
changes_per_pr = additions_per_pr + deletions_per_pr

commits_per_pr = pr_commits_df.groupby('pr_id').size()
reviews_per_pr = pr_reviews_df.groupby('pr_id').size()
comments_per_pr = pr_comments_df.groupby('pr_id').size()
timeline_events_per_pr = pr_timeline_df.groupby('pr_id').size()

pr_commits_df['message_length'] = pr_commits_df['message'].apply(lambda x: len(str(x)) if pd.notna(x) else 0)
pr_comments_df['body_length'] = pr_comments_df['body'].apply(lambda x: len(str(x)) if pd.notna(x) else 0)
pr_reviews_df['body_length'] = pr_reviews_df['body'].apply(lambda x: len(str(x)) if pd.notna(x) else 0)

prs_per_user = pr_df.groupby('user').size()
prs_per_repo = pr_df.groupby('repo_url').size() if 'repo_url' in pr_df.columns else pr_df.groupby('repo_id').size()

print("✓ Metrics calculated")

# =============================================================================
# SECTION 1: PR METRICS DISTRIBUTIONS
# =============================================================================
print("\n" + "="*80)
print("SECTION 1: PR METRICS DISTRIBUTIONS (9 figures)")
print("="*80)

# 1.1 Files changed per PR - Histogram
fig, ax = plt.subplots(figsize=(12, 8))
data = files_per_pr[files_per_pr <= 50]
ax.hist(data, bins=50, color='steelblue', edgecolor='black', alpha=0.75, linewidth=1.5)
ax.set_xlabel('Number of Files Changed', fontweight='bold')
ax.set_ylabel('Frequency', fontweight='bold')
ax.set_title(f'Files Changed per Pull Request\nMedian: {files_per_pr.median():.1f} | Mean: {files_per_pr.mean():.1f}', 
             fontweight='bold', pad=20)
ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=1.2)
plt.tight_layout()
plt.savefig('figures_individual/01_pr_files_changed_histogram.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ 01_pr_files_changed_histogram.png")

# 1.2 Files changed per PR - Boxplot
fig, ax = plt.subplots(figsize=(10, 8))
bp = ax.boxplot([files_per_pr], vert=True, patch_artist=True, widths=0.6)
bp['boxes'][0].set_facecolor('lightblue')
bp['boxes'][0].set_edgecolor('steelblue')
bp['boxes'][0].set_linewidth(2.5)
bp['medians'][0].set_color('red')
bp['medians'][0].set_linewidth(3)
for whisker in bp['whiskers']:
    whisker.set(linewidth=2.5, color='steelblue')
for cap in bp['caps']:
    cap.set(linewidth=2.5, color='steelblue')
for flier in bp['fliers']:
    flier.set(marker='o', markerfacecolor='red', markersize=4, alpha=0.5)
ax.set_ylabel('Number of Files Changed', fontweight='bold')
ax.set_title('Files Changed per Pull Request - Box Plot', fontweight='bold', pad=20)
ax.set_xticklabels(['Files Changed'], fontweight='bold')
ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=1.2)
plt.tight_layout()
plt.savefig('figures_individual/02_pr_files_changed_boxplot.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ 02_pr_files_changed_boxplot.png")

# 1.3 Files changed per PR - Violin Plot
fig, ax = plt.subplots(figsize=(10, 8))
parts = ax.violinplot([files_per_pr], vert=True, showmeans=True, showmedians=True, showextrema=True)
for pc in parts['bodies']:
    pc.set_facecolor('lightblue')
    pc.set_edgecolor('steelblue')
    pc.set_linewidth(2)
    pc.set_alpha(0.7)
ax.set_ylabel('Number of Files Changed', fontweight='bold')
ax.set_title('Files Changed per Pull Request - Violin Plot', fontweight='bold', pad=20)
ax.set_xticks([1])
ax.set_xticklabels(['Files Changed'], fontweight='bold')
ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=1.2)
plt.tight_layout()
plt.savefig('figures_individual/03_pr_files_changed_violinplot.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ 03_pr_files_changed_violinplot.png")

# 1.4 Lines added per PR - Histogram
fig, ax = plt.subplots(figsize=(12, 8))
data = additions_per_pr[additions_per_pr <= 1000]
ax.hist(data, bins=50, color='green', edgecolor='black', alpha=0.75, linewidth=1.5)
ax.set_xlabel('Lines Added', fontweight='bold')
ax.set_ylabel('Frequency', fontweight='bold')
ax.set_title(f'Lines Added per Pull Request\nMedian: {additions_per_pr.median():.0f} | Mean: {additions_per_pr.mean():.0f}', 
             fontweight='bold', pad=20)
ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=1.2)
plt.tight_layout()
plt.savefig('figures_individual/04_pr_lines_added_histogram.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ 04_pr_lines_added_histogram.png")

# 1.5 Lines deleted per PR - Histogram
fig, ax = plt.subplots(figsize=(12, 8))
data = deletions_per_pr[deletions_per_pr <= 1000]
ax.hist(data, bins=50, color='red', edgecolor='black', alpha=0.75, linewidth=1.5)
ax.set_xlabel('Lines Deleted', fontweight='bold')
ax.set_ylabel('Frequency', fontweight='bold')
ax.set_title(f'Lines Deleted per Pull Request\nMedian: {deletions_per_pr.median():.0f} | Mean: {deletions_per_pr.mean():.0f}', 
             fontweight='bold', pad=20)
ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=1.2)
plt.tight_layout()
plt.savefig('figures_individual/05_pr_lines_deleted_histogram.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ 05_pr_lines_deleted_histogram.png")

# 1.6 Total changes per PR - Histogram
fig, ax = plt.subplots(figsize=(12, 8))
data = changes_per_pr[changes_per_pr <= 2000]
ax.hist(data, bins=50, color='purple', edgecolor='black', alpha=0.75, linewidth=1.5)
ax.set_xlabel('Total Lines Changed', fontweight='bold')
ax.set_ylabel('Frequency', fontweight='bold')
ax.set_title(f'Total Changes per Pull Request\nMedian: {changes_per_pr.median():.0f} | Mean: {changes_per_pr.mean():.0f}', 
             fontweight='bold', pad=20)
ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=1.2)
plt.tight_layout()
plt.savefig('figures_individual/06_pr_total_changes_histogram.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ 06_pr_total_changes_histogram.png")

# 1.7 PR Title Length - Histogram
fig, ax = plt.subplots(figsize=(12, 8))
data = pr_df['title_length'][pr_df['title_length'] <= 200]
ax.hist(data, bins=50, color='orange', edgecolor='black', alpha=0.75, linewidth=1.5)
ax.set_xlabel('Title Length (characters)', fontweight='bold')
ax.set_ylabel('Frequency', fontweight='bold')
ax.set_title(f'PR Title Length Distribution\nMedian: {pr_df["title_length"].median():.0f} | Mean: {pr_df["title_length"].mean():.0f}', 
             fontweight='bold', pad=20)
ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=1.2)
plt.tight_layout()
plt.savefig('figures_individual/07_pr_title_length_histogram.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ 07_pr_title_length_histogram.png")

# 1.8 PR Body Length - Histogram
fig, ax = plt.subplots(figsize=(12, 8))
data = pr_df['body_length'][pr_df['body_length'] <= 5000]
ax.hist(data, bins=50, color='brown', edgecolor='black', alpha=0.75, linewidth=1.5)
ax.set_xlabel('Body Length (characters)', fontweight='bold')
ax.set_ylabel('Frequency', fontweight='bold')
ax.set_title(f'PR Body Length Distribution\nMedian: {pr_df["body_length"].median():.0f} | Mean: {pr_df["body_length"].mean():.0f}', 
             fontweight='bold', pad=20)
ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=1.2)
plt.tight_layout()
plt.savefig('figures_individual/08_pr_body_length_histogram.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ 08_pr_body_length_histogram.png")

# 1.9 PR State Distribution - Bar Chart
if 'state' in pr_df.columns:
    fig, ax = plt.subplots(figsize=(12, 8))
    state_counts = pr_df['state'].value_counts()
    colors_state = ['#2ecc71' if 'merge' in str(s).lower() else '#e74c3c' if 'close' in str(s).lower() else '#3498db' 
                    for s in state_counts.index]
    bars = ax.bar(range(len(state_counts)), state_counts.values, color=colors_state, 
                   edgecolor='black', alpha=0.8, linewidth=1.5)
    ax.set_xticks(range(len(state_counts)))
    ax.set_xticklabels(state_counts.index, rotation=45, ha='right', fontweight='bold')
    ax.set_ylabel('Count', fontweight='bold')
    ax.set_title('PR State Distribution', fontweight='bold', pad=20)
    ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=1.2)
    # Add value labels
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height):,}',
                ha='center', va='bottom', fontweight='bold', fontsize=12)
    plt.tight_layout()
    plt.savefig('figures_individual/09_pr_state_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ 09_pr_state_distribution.png")

# =============================================================================
# SECTION 2: COMMIT, REVIEW, AND TIMELINE DISTRIBUTIONS
# =============================================================================
print("\n" + "="*80)
print("SECTION 2: COMMIT, REVIEW, AND TIMELINE DISTRIBUTIONS (9 figures)")
print("="*80)

# 2.1 Commits per PR - Histogram
fig, ax = plt.subplots(figsize=(12, 8))
data = commits_per_pr[commits_per_pr <= 20]
ax.hist(data, bins=20, color='steelblue', edgecolor='black', alpha=0.75, linewidth=1.5)
ax.set_xlabel('Number of Commits', fontweight='bold')
ax.set_ylabel('Frequency', fontweight='bold')
ax.set_title(f'Commits per Pull Request\nMedian: {commits_per_pr.median():.1f} | Mean: {commits_per_pr.mean():.1f}', 
             fontweight='bold', pad=20)
ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=1.2)
plt.tight_layout()
plt.savefig('figures_individual/10_commits_per_pr_histogram.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ 10_commits_per_pr_histogram.png")

# 2.2 Commits per PR - Boxplot
fig, ax = plt.subplots(figsize=(10, 8))
bp = ax.boxplot([commits_per_pr], vert=True, patch_artist=True, widths=0.6)
bp['boxes'][0].set_facecolor('lightblue')
bp['boxes'][0].set_edgecolor('steelblue')
bp['boxes'][0].set_linewidth(2.5)
bp['medians'][0].set_color('red')
bp['medians'][0].set_linewidth(3)
for whisker in bp['whiskers']:
    whisker.set(linewidth=2.5, color='steelblue')
for cap in bp['caps']:
    cap.set(linewidth=2.5, color='steelblue')
ax.set_ylabel('Number of Commits', fontweight='bold')
ax.set_title('Commits per Pull Request - Box Plot', fontweight='bold', pad=20)
ax.set_xticklabels(['Commits'], fontweight='bold')
ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=1.2)
plt.tight_layout()
plt.savefig('figures_individual/11_commits_per_pr_boxplot.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ 11_commits_per_pr_boxplot.png")

# 2.3 Commit Message Length - Histogram
fig, ax = plt.subplots(figsize=(12, 8))
data = pr_commits_df['message_length'][pr_commits_df['message_length'] <= 500]
ax.hist(data, bins=50, color='darkblue', edgecolor='black', alpha=0.75, linewidth=1.5)
ax.set_xlabel('Message Length (characters)', fontweight='bold')
ax.set_ylabel('Frequency', fontweight='bold')
ax.set_title(f'Commit Message Length Distribution\nMedian: {pr_commits_df["message_length"].median():.0f} | Mean: {pr_commits_df["message_length"].mean():.0f}', 
             fontweight='bold', pad=20)
ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=1.2)
plt.tight_layout()
plt.savefig('figures_individual/12_commit_message_length_histogram.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ 12_commit_message_length_histogram.png")

# 2.4 Reviews per PR - Histogram
fig, ax = plt.subplots(figsize=(12, 8))
data = reviews_per_pr[reviews_per_pr <= 10]
ax.hist(data, bins=10, color='green', edgecolor='black', alpha=0.75, linewidth=1.5)
ax.set_xlabel('Number of Reviews', fontweight='bold')
ax.set_ylabel('Frequency', fontweight='bold')
ax.set_title(f'Reviews per Pull Request\nMedian: {reviews_per_pr.median():.1f} | Mean: {reviews_per_pr.mean():.1f}', 
             fontweight='bold', pad=20)
ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=1.2)
plt.tight_layout()
plt.savefig('figures_individual/13_reviews_per_pr_histogram.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ 13_reviews_per_pr_histogram.png")

# 2.5 Review Body Length - Histogram
fig, ax = plt.subplots(figsize=(12, 8))
data = pr_reviews_df['body_length'][pr_reviews_df['body_length'] <= 2000]
ax.hist(data, bins=50, color='darkgreen', edgecolor='black', alpha=0.75, linewidth=1.5)
ax.set_xlabel('Body Length (characters)', fontweight='bold')
ax.set_ylabel('Frequency', fontweight='bold')
ax.set_title(f'Review Body Length Distribution\nMedian: {pr_reviews_df["body_length"].median():.0f} | Mean: {pr_reviews_df["body_length"].mean():.0f}', 
             fontweight='bold', pad=20)
ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=1.2)
plt.tight_layout()
plt.savefig('figures_individual/14_review_body_length_histogram.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ 14_review_body_length_histogram.png")

# 2.6 Review State Distribution - Bar Chart
if 'state' in pr_reviews_df.columns:
    fig, ax = plt.subplots(figsize=(12, 8))
    state_counts = pr_reviews_df['state'].value_counts().head(10)
    colors_review = plt.cm.Set3(np.linspace(0, 1, len(state_counts)))
    bars = ax.bar(range(len(state_counts)), state_counts.values, color=colors_review, 
                   edgecolor='black', alpha=0.8, linewidth=1.5)
    ax.set_xticks(range(len(state_counts)))
    ax.set_xticklabels(state_counts.index, rotation=45, ha='right', fontweight='bold')
    ax.set_ylabel('Count', fontweight='bold')
    ax.set_title('Review State Distribution (Top 10)', fontweight='bold', pad=20)
    ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=1.2)
    # Add value labels
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height):,}',
                ha='center', va='bottom', fontweight='bold', fontsize=11)
    plt.tight_layout()
    plt.savefig('figures_individual/15_review_state_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ 15_review_state_distribution.png")

# 2.7 Comments per PR - Histogram
fig, ax = plt.subplots(figsize=(12, 8))
data = comments_per_pr[comments_per_pr <= 20]
ax.hist(data, bins=20, color='orange', edgecolor='black', alpha=0.75, linewidth=1.5)
ax.set_xlabel('Number of Comments', fontweight='bold')
ax.set_ylabel('Frequency', fontweight='bold')
ax.set_title(f'Comments per Pull Request\nMedian: {comments_per_pr.median():.1f} | Mean: {comments_per_pr.mean():.1f}', 
             fontweight='bold', pad=20)
ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=1.2)
plt.tight_layout()
plt.savefig('figures_individual/16_comments_per_pr_histogram.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ 16_comments_per_pr_histogram.png")

# 2.8 Comment Body Length - Histogram
fig, ax = plt.subplots(figsize=(12, 8))
data = pr_comments_df['body_length'][pr_comments_df['body_length'] <= 1000]
ax.hist(data, bins=50, color='darkorange', edgecolor='black', alpha=0.75, linewidth=1.5)
ax.set_xlabel('Body Length (characters)', fontweight='bold')
ax.set_ylabel('Frequency', fontweight='bold')
ax.set_title(f'Comment Body Length Distribution\nMedian: {pr_comments_df["body_length"].median():.0f} | Mean: {pr_comments_df["body_length"].mean():.0f}', 
             fontweight='bold', pad=20)
ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=1.2)
plt.tight_layout()
plt.savefig('figures_individual/17_comment_body_length_histogram.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ 17_comment_body_length_histogram.png")

# 2.9 Timeline Events per PR - Histogram
fig, ax = plt.subplots(figsize=(12, 8))
data = timeline_events_per_pr[timeline_events_per_pr <= 30]
ax.hist(data, bins=30, color='purple', edgecolor='black', alpha=0.75, linewidth=1.5)
ax.set_xlabel('Number of Timeline Events', fontweight='bold')
ax.set_ylabel('Frequency', fontweight='bold')
ax.set_title(f'Timeline Events per Pull Request\nMedian: {timeline_events_per_pr.median():.1f} | Mean: {timeline_events_per_pr.mean():.1f}', 
             fontweight='bold', pad=20)
ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=1.2)
plt.tight_layout()
plt.savefig('figures_individual/18_timeline_events_per_pr_histogram.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ 18_timeline_events_per_pr_histogram.png")

# =============================================================================
# SECTION 3: USER AND REPOSITORY DISTRIBUTIONS
# =============================================================================
print("\n" + "="*80)
print("SECTION 3: USER AND REPOSITORY DISTRIBUTIONS (6 figures)")
print("="*80)

# 3.1 PRs per User - Histogram
fig, ax = plt.subplots(figsize=(12, 8))
data = prs_per_user[prs_per_user <= 50]
ax.hist(data, bins=50, color='teal', edgecolor='black', alpha=0.75, linewidth=1.5)
ax.set_xlabel('Number of PRs', fontweight='bold')
ax.set_ylabel('Frequency', fontweight='bold')
ax.set_title(f'Pull Requests per User\nMedian: {prs_per_user.median():.1f} | Mean: {prs_per_user.mean():.1f}', 
             fontweight='bold', pad=20)
ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=1.2)
plt.tight_layout()
plt.savefig('figures_individual/19_prs_per_user_histogram.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ 19_prs_per_user_histogram.png")

# 3.2 PRs per Repository - Histogram
fig, ax = plt.subplots(figsize=(12, 8))
data = prs_per_repo[prs_per_repo <= 50]
ax.hist(data, bins=50, color='coral', edgecolor='black', alpha=0.75, linewidth=1.5)
ax.set_xlabel('Number of PRs', fontweight='bold')
ax.set_ylabel('Frequency', fontweight='bold')
ax.set_title(f'Pull Requests per Repository\nMedian: {prs_per_repo.median():.1f} | Mean: {prs_per_repo.mean():.1f}', 
             fontweight='bold', pad=20)
ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=1.2)
plt.tight_layout()
plt.savefig('figures_individual/20_prs_per_repo_histogram.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ 20_prs_per_repo_histogram.png")

# 3.3 User Followers Distribution
if 'followers' in user_df.columns:
    fig, ax = plt.subplots(figsize=(12, 8))
    data = user_df['followers'][user_df['followers'] <= 500]
    ax.hist(data, bins=50, color='mediumpurple', edgecolor='black', alpha=0.75, linewidth=1.5)
    ax.set_xlabel('Number of Followers', fontweight='bold')
    ax.set_ylabel('Frequency', fontweight='bold')
    ax.set_title(f'User Followers Distribution\nMedian: {user_df["followers"].median():.0f} | Mean: {user_df["followers"].mean():.0f}', 
                 fontweight='bold', pad=20)
    ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=1.2)
    plt.tight_layout()
    plt.savefig('figures_individual/21_user_followers_histogram.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ 21_user_followers_histogram.png")

# 3.4 Repository Stars Distribution
if 'stars' in repo_df.columns:
    fig, ax = plt.subplots(figsize=(12, 8))
    data = repo_df['stars'][repo_df['stars'] <= 10000]
    ax.hist(data, bins=50, color='gold', edgecolor='black', alpha=0.75, linewidth=1.5)
    ax.set_xlabel('Number of Stars', fontweight='bold')
    ax.set_ylabel('Frequency', fontweight='bold')
    ax.set_title(f'Repository Stars Distribution\nMedian: {repo_df["stars"].median():.0f} | Mean: {repo_df["stars"].mean():.0f}', 
                 fontweight='bold', pad=20)
    ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=1.2)
    plt.tight_layout()
    plt.savefig('figures_individual/22_repo_stars_histogram.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ 22_repo_stars_histogram.png")

# 3.5 Repository Forks Distribution
if 'forks' in repo_df.columns:
    fig, ax = plt.subplots(figsize=(12, 8))
    data = repo_df['forks'][repo_df['forks'] <= 1000]
    ax.hist(data, bins=50, color='lightcoral', edgecolor='black', alpha=0.75, linewidth=1.5)
    ax.set_xlabel('Number of Forks', fontweight='bold')
    ax.set_ylabel('Frequency', fontweight='bold')
    ax.set_title(f'Repository Forks Distribution\nMedian: {repo_df["forks"].median():.0f} | Mean: {repo_df["forks"].mean():.0f}', 
                 fontweight='bold', pad=20)
    ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=1.2)
    plt.tight_layout()
    plt.savefig('figures_individual/23_repo_forks_histogram.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ 23_repo_forks_histogram.png")

# 3.6 Programming Language Distribution
if 'language' in repo_df.columns:
    fig, ax = plt.subplots(figsize=(12, 10))
    lang_counts = repo_df['language'].value_counts().head(15)
    colors_lang = plt.cm.tab20(np.linspace(0, 1, len(lang_counts)))
    bars = ax.barh(range(len(lang_counts)), lang_counts.values, color=colors_lang, 
                    edgecolor='black', alpha=0.8, linewidth=1.5)
    ax.set_yticks(range(len(lang_counts)))
    ax.set_yticklabels(lang_counts.index, fontweight='bold')
    ax.set_xlabel('Number of Repositories', fontweight='bold')
    ax.set_title('Top 15 Programming Languages', fontweight='bold', pad=20)
    ax.grid(axis='x', alpha=0.3, linestyle='--', linewidth=1.2)
    ax.invert_yaxis()
    # Add value labels
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height()/2.,
                f'{int(width):,}',
                ha='left', va='center', fontweight='bold', fontsize=11, 
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='gray', alpha=0.8))
    plt.tight_layout()
    plt.savefig('figures_individual/24_programming_languages_barplot.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ 24_programming_languages_barplot.png")

# =============================================================================
# SECTION 4: FILE-LEVEL CHANGE DISTRIBUTIONS
# =============================================================================
print("\n" + "="*80)
print("SECTION 4: FILE-LEVEL CHANGE DISTRIBUTIONS (6 figures)")
print("="*80)

# 4.1 File Additions Distribution - Histogram
fig, ax = plt.subplots(figsize=(12, 8))
data = pr_commit_details_df['additions'][pr_commit_details_df['additions'] <= 500]
ax.hist(data, bins=50, color='green', edgecolor='black', alpha=0.75, linewidth=1.5)
ax.set_xlabel('Lines Added per File', fontweight='bold')
ax.set_ylabel('Frequency', fontweight='bold')
ax.set_title(f'File Additions Distribution\nMedian: {pr_commit_details_df["additions"].median():.1f} | Mean: {pr_commit_details_df["additions"].mean():.1f}', 
             fontweight='bold', pad=20)
ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=1.2)
plt.tight_layout()
plt.savefig('figures_individual/25_file_additions_histogram.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ 25_file_additions_histogram.png")

# 4.2 File Deletions Distribution - Histogram
fig, ax = plt.subplots(figsize=(12, 8))
data = pr_commit_details_df['deletions'][pr_commit_details_df['deletions'] <= 500]
ax.hist(data, bins=50, color='red', edgecolor='black', alpha=0.75, linewidth=1.5)
ax.set_xlabel('Lines Deleted per File', fontweight='bold')
ax.set_ylabel('Frequency', fontweight='bold')
ax.set_title(f'File Deletions Distribution\nMedian: {pr_commit_details_df["deletions"].median():.1f} | Mean: {pr_commit_details_df["deletions"].mean():.1f}', 
             fontweight='bold', pad=20)
ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=1.2)
plt.tight_layout()
plt.savefig('figures_individual/26_file_deletions_histogram.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ 26_file_deletions_histogram.png")

# 4.3 File Status Distribution - Bar Chart
if 'status' in pr_commit_details_df.columns:
    fig, ax = plt.subplots(figsize=(12, 8))
    status_counts = pr_commit_details_df['status'].value_counts().head(10)
    colors_status = ['#2ecc71', '#3498db', '#e74c3c', '#f39c12', '#9b59b6'][:len(status_counts)]
    bars = ax.bar(range(len(status_counts)), status_counts.values, color=colors_status, 
                   edgecolor='black', alpha=0.8, linewidth=1.5)
    ax.set_xticks(range(len(status_counts)))
    ax.set_xticklabels(status_counts.index, rotation=45, ha='right', fontweight='bold')
    ax.set_ylabel('Count', fontweight='bold')
    ax.set_title('File Status Distribution (Top 10)', fontweight='bold', pad=20)
    ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=1.2)
    # Add value labels
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height):,}',
                ha='center', va='bottom', fontweight='bold', fontsize=11)
    plt.tight_layout()
    plt.savefig('figures_individual/27_file_status_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ 27_file_status_distribution.png")

# 4.4 File Additions Boxplot
fig, ax = plt.subplots(figsize=(10, 8))
bp = ax.boxplot([pr_commit_details_df['additions']], vert=True, patch_artist=True, widths=0.6)
bp['boxes'][0].set_facecolor('lightgreen')
bp['boxes'][0].set_edgecolor('green')
bp['boxes'][0].set_linewidth(2.5)
bp['medians'][0].set_color('red')
bp['medians'][0].set_linewidth(3)
for whisker in bp['whiskers']:
    whisker.set(linewidth=2.5, color='green')
for cap in bp['caps']:
    cap.set(linewidth=2.5, color='green')
ax.set_ylabel('Lines Added per File', fontweight='bold')
ax.set_title('File Additions - Box Plot', fontweight='bold', pad=20)
ax.set_xticklabels(['Additions'], fontweight='bold')
ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=1.2)
plt.tight_layout()
plt.savefig('figures_individual/28_file_additions_boxplot.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ 28_file_additions_boxplot.png")

# 4.5 File Deletions Boxplot
fig, ax = plt.subplots(figsize=(10, 8))
bp = ax.boxplot([pr_commit_details_df['deletions']], vert=True, patch_artist=True, widths=0.6)
bp['boxes'][0].set_facecolor('lightcoral')
bp['boxes'][0].set_edgecolor('red')
bp['boxes'][0].set_linewidth(2.5)
bp['medians'][0].set_color('blue')
bp['medians'][0].set_linewidth(3)
for whisker in bp['whiskers']:
    whisker.set(linewidth=2.5, color='red')
for cap in bp['caps']:
    cap.set(linewidth=2.5, color='red')
ax.set_ylabel('Lines Deleted per File', fontweight='bold')
ax.set_title('File Deletions - Box Plot', fontweight='bold', pad=20)
ax.set_xticklabels(['Deletions'], fontweight='bold')
ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=1.2)
plt.tight_layout()
plt.savefig('figures_individual/29_file_deletions_boxplot.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ 29_file_deletions_boxplot.png")

# 4.6 Timeline Event Types Distribution - Bar Chart
if 'event' in pr_timeline_df.columns:
    fig, ax = plt.subplots(figsize=(12, 10))
    event_counts = pr_timeline_df['event'].value_counts().head(15)
    colors_event = plt.cm.Paired(np.linspace(0, 1, len(event_counts)))
    bars = ax.barh(range(len(event_counts)), event_counts.values, color=colors_event, 
                    edgecolor='black', alpha=0.8, linewidth=1.5)
    ax.set_yticks(range(len(event_counts)))
    ax.set_yticklabels(event_counts.index, fontweight='bold')
    ax.set_xlabel('Count', fontweight='bold')
    ax.set_title('Top 15 Timeline Event Types', fontweight='bold', pad=20)
    ax.grid(axis='x', alpha=0.3, linestyle='--', linewidth=1.2)
    ax.invert_yaxis()
    # Add value labels
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height()/2.,
                f'{int(width):,}',
                ha='left', va='center', fontweight='bold', fontsize=11,
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='gray', alpha=0.8))
    plt.tight_layout()
    plt.savefig('figures_individual/30_timeline_event_types_barplot.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ 30_timeline_event_types_barplot.png")

# =============================================================================
# COMPLETION
# =============================================================================
print("\n" + "="*80)
print("COMPLETE! All figures have been saved to: figures_individual/")
print("="*80)
print(f"\n✓ Generated 30+ individual high-quality figures")
print("✓ All figures saved with meaningful names")
print("✓ Text is clear and readable at 300 DPI")
print("✓ Figures use larger fonts and bold labels")
print("\nFigures are organized by category:")
print("  01-09:  PR Metrics Distributions")
print("  10-18:  Commit, Review, and Timeline Distributions")
print("  19-24:  User and Repository Distributions")
print("  25-30:  File-Level Change Distributions")
print("\nYou can now use these individual figures in your report!")

