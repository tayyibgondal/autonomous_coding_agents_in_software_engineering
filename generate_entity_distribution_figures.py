"""
Generate individual figures for entity distributions by agent (Figure 3 from data_exploration.ipynb)
This replaces the 3x3 grid with 9 individual high-quality figures.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 14
plt.rcParams['axes.labelsize'] = 16
plt.rcParams['axes.titlesize'] = 18
plt.rcParams['xtick.labelsize'] = 13
plt.rcParams['ytick.labelsize'] = 13

# Create output directory
Path("figures_individual").mkdir(exist_ok=True)

print("="*80)
print("GENERATING ENTITY DISTRIBUTION FIGURES BY AGENT (9 figures)")
print("="*80)

# Load data
print("\nLoading datasets...")
pr_df = pd.read_parquet("hf://datasets/hao-li/AIDev/pull_request.parquet")
repo_df = pd.read_parquet("hf://datasets/hao-li/AIDev/repository.parquet")
user_df = pd.read_parquet("hf://datasets/hao-li/AIDev/user.parquet")
pr_comments_df = pd.read_parquet("hf://datasets/hao-li/AIDev/pr_comments.parquet")
pr_commits_df = pd.read_parquet("hf://datasets/hao-li/AIDev/pr_commits.parquet")
pr_commit_details_df = pd.read_parquet("hf://datasets/hao-li/AIDev/pr_commit_details.parquet")
issue_df = pd.read_parquet("hf://datasets/hao-li/AIDev/issue.parquet")

print(f"✓ Loaded data")

# Define agent order and colors
AGENT_ORDER = ['Claude_Code', 'Cursor', 'Copilot', 'Devin', 'OpenAI_Codex']
COLOR_MAP = {
    'Claude_Code': '#FF6B6B',
    'Cursor': '#4ECDC4', 
    'Copilot': '#45B7D1',
    'Devin': '#FFA07A',
    'OpenAI_Codex': '#98D8C8'
}

# Calculate metrics
print("Calculating metrics...")
pr_df['body_length'] = pr_df['body'].fillna('').str.len()
pr_df['created_at'] = pd.to_datetime(pr_df['created_at'])
pr_df['merged_at'] = pd.to_datetime(pr_df['merged_at'])
pr_df['closed_at'] = pd.to_datetime(pr_df['closed_at'])
pr_df['is_merged'] = pr_df['merged_at'].notna()
pr_df['time_to_merge'] = (pr_df['merged_at'] - pr_df['created_at']).dt.total_seconds() / 3600  # hours

# Commit statistics
pr_commit_stats = pr_commit_details_df.groupby('pr_id').agg({
    'additions': 'sum',
    'deletions': 'sum',
    'filename': 'count'
}).rename(columns={'filename': 'files_changed'})

pr_with_commits = pr_df.merge(pr_commit_stats, left_on='id', right_index=True, how='inner')
pr_with_commits = pr_with_commits[pr_with_commits['agent'].isin(AGENT_ORDER)]

# Comment counts
comments_per_pr = pr_comments_df.groupby('pr_id').size()
pr_with_comments = pr_df.copy()
pr_with_comments['comment_count'] = pr_with_comments['id'].map(comments_per_pr).fillna(0)
pr_with_comments = pr_with_comments[pr_with_comments['agent'].isin(AGENT_ORDER)]

print("✓ Metrics calculated\n")

# =============================================================================
# FIGURE 1: Files Changed per PR by Agent (Violin Plot)
# =============================================================================
print("Generating Figure 31: Files Changed per PR by Agent...")
fig, ax = plt.subplots(figsize=(12, 8))

data_to_plot = [pr_with_commits[pr_with_commits['agent']==agent]['files_changed'].clip(upper=50).values
                for agent in AGENT_ORDER]
data_to_plot_filtered = [d for d in data_to_plot if len(d) > 0]
positions_filtered = [i for i, d in enumerate(data_to_plot) if len(d) > 0]

if len(data_to_plot_filtered) > 0:
    parts = ax.violinplot(data_to_plot_filtered, positions=positions_filtered, 
                          showmeans=True, showmedians=True, widths=0.7)
    for i, pc in enumerate(parts['bodies']):
        agent_idx = positions_filtered[i]
        pc.set_facecolor(COLOR_MAP[AGENT_ORDER[agent_idx]])
        pc.set_alpha(0.7)
        pc.set_edgecolor('black')
        pc.set_linewidth(1.5)

ax.set_xticks(range(len(AGENT_ORDER)))
ax.set_xticklabels([a.replace('_', ' ') for a in AGENT_ORDER], rotation=45, ha='right', fontweight='bold')
ax.set_ylabel('Files Changed', fontweight='bold')
ax.set_title('Files Changed per PR by Agent', fontweight='bold', pad=20)
ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=1.2)
ax.set_ylim(0, 50)
plt.tight_layout()
plt.savefig('figures_individual/31_entity_files_changed_by_agent.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ 31_entity_files_changed_by_agent.png")

# =============================================================================
# FIGURE 2: Lines Added Distribution by Agent (Box Plot)
# =============================================================================
print("Generating Figure 32: Lines Added Distribution by Agent...")
fig, ax = plt.subplots(figsize=(12, 8))

data_to_plot = [pr_with_commits[pr_with_commits['agent']==agent]['additions'].clip(1, 10000).values
                for agent in AGENT_ORDER]
data_to_plot_filtered = [d for d in data_to_plot if len(d) > 0]
labels_filtered = [AGENT_ORDER[i].replace('_', ' ') for i, d in enumerate(data_to_plot) if len(d) > 0]

if len(data_to_plot_filtered) > 0:
    bp = ax.boxplot(data_to_plot_filtered, labels=labels_filtered, 
                    patch_artist=True, showfliers=False, widths=0.6)
    for i, patch in enumerate(bp['boxes']):
        agent_idx = [j for j, d in enumerate(data_to_plot) if len(d) > 0][i]
        patch.set_facecolor(COLOR_MAP[AGENT_ORDER[agent_idx]])
        patch.set_alpha(0.7)
        patch.set_edgecolor('black')
        patch.set_linewidth(1.5)
    # Style other elements
    for whisker in bp['whiskers']:
        whisker.set(linewidth=1.5, color='black')
    for cap in bp['caps']:
        cap.set(linewidth=1.5, color='black')
    for median in bp['medians']:
        median.set(linewidth=2, color='red')

ax.set_xticklabels(labels_filtered if len(data_to_plot_filtered) > 0 else [], 
                   rotation=45, ha='right', fontweight='bold')
ax.set_ylabel('Lines Added (log scale)', fontweight='bold')
ax.set_yscale('log')
ax.set_title('Code Additions Distribution by Agent', fontweight='bold', pad=20)
ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=1.2)
plt.tight_layout()
plt.savefig('figures_individual/32_entity_lines_added_by_agent.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ 32_entity_lines_added_by_agent.png")

# =============================================================================
# FIGURE 3: PR Description Length Distribution by Agent (Histogram Overlay)
# =============================================================================
print("Generating Figure 33: PR Description Length by Agent...")
fig, ax = plt.subplots(figsize=(12, 8))

for agent in AGENT_ORDER:
    agent_data = pr_df[pr_df['agent']==agent]['body_length'].clip(0, 5000)
    ax.hist(agent_data, bins=50, alpha=0.6, label=agent.replace('_', ' '), 
            color=COLOR_MAP[agent], edgecolor='black', linewidth=0.5)

ax.set_xlabel('PR Description Length (characters)', fontweight='bold')
ax.set_ylabel('Frequency', fontweight='bold')
ax.set_title('PR Description Length Distribution by Agent', fontweight='bold', pad=20)
ax.legend(fontsize=12, framealpha=0.9, edgecolor='black')
ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=1.2)
plt.tight_layout()
plt.savefig('figures_individual/33_entity_pr_description_length_by_agent.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ 33_entity_pr_description_length_by_agent.png")

# =============================================================================
# FIGURE 4: Review Comment Intensity by Agent (Violin Plot)
# =============================================================================
print("Generating Figure 34: Review Comment Intensity by Agent...")
fig, ax = plt.subplots(figsize=(12, 8))

data_to_plot = [pr_with_comments[pr_with_comments['agent']==agent]['comment_count'].clip(upper=30).values
                for agent in AGENT_ORDER]
data_to_plot_filtered = [d for d in data_to_plot if len(d) > 0]
positions_filtered = [i for i, d in enumerate(data_to_plot) if len(d) > 0]

if len(data_to_plot_filtered) > 0:
    parts = ax.violinplot(data_to_plot_filtered, positions=positions_filtered, 
                          showmeans=True, showmedians=True, widths=0.7)
    for i, pc in enumerate(parts['bodies']):
        agent_idx = positions_filtered[i]
        pc.set_facecolor(COLOR_MAP[AGENT_ORDER[agent_idx]])
        pc.set_alpha(0.7)
        pc.set_edgecolor('black')
        pc.set_linewidth(1.5)

ax.set_xticks(range(len(AGENT_ORDER)))
ax.set_xticklabels([a.replace('_', ' ') for a in AGENT_ORDER], rotation=45, ha='right', fontweight='bold')
ax.set_ylabel('Comments per PR', fontweight='bold')
ax.set_title('Review Comment Intensity by Agent', fontweight='bold', pad=20)
ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=1.2)
plt.tight_layout()
plt.savefig('figures_individual/34_entity_review_comment_intensity_by_agent.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ 34_entity_review_comment_intensity_by_agent.png")

# =============================================================================
# FIGURE 5: Time to Merge Distribution by Agent (Box Plot)
# =============================================================================
print("Generating Figure 35: Time to Merge by Agent...")
fig, ax = plt.subplots(figsize=(12, 8))

pr_merged = pr_df[pr_df['is_merged'] & (pr_df['time_to_merge'] > 0)]
pr_merged = pr_merged[pr_merged['agent'].isin(AGENT_ORDER)]
data_to_plot = [(pr_merged[pr_merged['agent']==agent]['time_to_merge'].clip(0, 168) / 24).values
                for agent in AGENT_ORDER]
data_to_plot_filtered = [d for d in data_to_plot if len(d) > 0]
labels_filtered = [AGENT_ORDER[i].replace('_', ' ') for i, d in enumerate(data_to_plot) if len(d) > 0]

if len(data_to_plot_filtered) > 0:
    bp = ax.boxplot(data_to_plot_filtered, labels=labels_filtered, 
                    patch_artist=True, showfliers=False, widths=0.6)
    for i, patch in enumerate(bp['boxes']):
        agent_idx = [j for j, d in enumerate(data_to_plot) if len(d) > 0][i]
        patch.set_facecolor(COLOR_MAP[AGENT_ORDER[agent_idx]])
        patch.set_alpha(0.7)
        patch.set_edgecolor('black')
        patch.set_linewidth(1.5)
    for whisker in bp['whiskers']:
        whisker.set(linewidth=1.5, color='black')
    for cap in bp['caps']:
        cap.set(linewidth=1.5, color='black')
    for median in bp['medians']:
        median.set(linewidth=2, color='red')

ax.set_xticklabels(labels_filtered if len(data_to_plot_filtered) > 0 else [], 
                   rotation=45, ha='right', fontweight='bold')
ax.set_ylabel('Time to Merge (days)', fontweight='bold')
ax.set_title('PR Merge Latency by Agent', fontweight='bold', pad=20)
ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=1.2)
plt.tight_layout()
plt.savefig('figures_individual/35_entity_time_to_merge_by_agent.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ 35_entity_time_to_merge_by_agent.png")

# =============================================================================
# FIGURE 6: Repository Popularity Distribution (Histogram)
# =============================================================================
print("Generating Figure 36: Repository Popularity Distribution...")
fig, ax = plt.subplots(figsize=(12, 8))

repo_df_clean = repo_df[repo_df['stars'] > 0]
ax.hist(repo_df_clean['stars'].clip(100, 10000), bins=50, alpha=0.75, 
        color='#3498db', edgecolor='black', linewidth=1.5)
ax.set_xlabel('Repository Stars (log scale)', fontweight='bold')
ax.set_ylabel('Frequency', fontweight='bold')
ax.set_xscale('log')
ax.set_title('Repository Popularity Distribution', fontweight='bold', pad=20)
ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=1.2)
# Add statistics
median_stars = repo_df_clean['stars'].median()
mean_stars = repo_df_clean['stars'].mean()
ax.text(0.98, 0.97, f'Median: {median_stars:.0f}\nMean: {mean_stars:.0f}', 
        transform=ax.transAxes, ha='right', va='top',
        bbox=dict(boxstyle='round', facecolor='white', edgecolor='black', alpha=0.8),
        fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig('figures_individual/36_entity_repository_popularity.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ 36_entity_repository_popularity.png")

# =============================================================================
# FIGURE 7: Commit Message Verbosity (Histogram)
# =============================================================================
print("Generating Figure 37: Commit Message Verbosity...")
fig, ax = plt.subplots(figsize=(12, 8))

pr_commits_df['message_length'] = pr_commits_df['message'].fillna('').str.len()
ax.hist(pr_commits_df['message_length'].clip(0, 500), bins=50, alpha=0.75, 
        color='#9b59b6', edgecolor='black', linewidth=1.5)
ax.set_xlabel('Commit Message Length (characters)', fontweight='bold')
ax.set_ylabel('Frequency', fontweight='bold')
ax.set_title('Commit Message Verbosity Distribution', fontweight='bold', pad=20)
ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=1.2)
# Add statistics
median_len = pr_commits_df['message_length'].median()
mean_len = pr_commits_df['message_length'].mean()
ax.text(0.98, 0.97, f'Median: {median_len:.0f}\nMean: {mean_len:.0f}', 
        transform=ax.transAxes, ha='right', va='top',
        bbox=dict(boxstyle='round', facecolor='white', edgecolor='black', alpha=0.8),
        fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig('figures_individual/37_entity_commit_message_verbosity.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ 37_entity_commit_message_verbosity.png")

# =============================================================================
# FIGURE 8: Developer Social Reach (Histogram)
# =============================================================================
print("Generating Figure 38: Developer Social Reach...")
fig, ax = plt.subplots(figsize=(12, 8))

user_df_clean = user_df[user_df['followers'] > 0]
ax.hist(user_df_clean['followers'].clip(1, 1000), bins=50, alpha=0.75, 
        color='#e67e22', edgecolor='black', linewidth=1.5)
ax.set_xlabel('User Followers (log scale)', fontweight='bold')
ax.set_ylabel('Frequency', fontweight='bold')
ax.set_xscale('log')
ax.set_title('Developer Social Reach Distribution', fontweight='bold', pad=20)
ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=1.2)
# Add statistics
median_followers = user_df_clean['followers'].median()
mean_followers = user_df_clean['followers'].mean()
ax.text(0.98, 0.97, f'Median: {median_followers:.0f}\nMean: {mean_followers:.0f}', 
        transform=ax.transAxes, ha='right', va='top',
        bbox=dict(boxstyle='round', facecolor='white', edgecolor='black', alpha=0.8),
        fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig('figures_individual/38_entity_developer_social_reach.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ 38_entity_developer_social_reach.png")

# =============================================================================
# FIGURE 9: Issue Description Detail (Histogram)
# =============================================================================
print("Generating Figure 39: Issue Description Detail...")
fig, ax = plt.subplots(figsize=(12, 8))

issue_df['body_length'] = issue_df['body'].fillna('').str.len()
ax.hist(issue_df['body_length'].clip(0, 5000), bins=50, alpha=0.75, 
        color='#16a085', edgecolor='black', linewidth=1.5)
ax.set_xlabel('Issue Body Length (characters)', fontweight='bold')
ax.set_ylabel('Frequency', fontweight='bold')
ax.set_title('Issue Description Detail Distribution', fontweight='bold', pad=20)
ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=1.2)
# Add statistics
median_len = issue_df['body_length'].median()
mean_len = issue_df['body_length'].mean()
ax.text(0.98, 0.97, f'Median: {median_len:.0f}\nMean: {mean_len:.0f}', 
        transform=ax.transAxes, ha='right', va='top',
        bbox=dict(boxstyle='round', facecolor='white', edgecolor='black', alpha=0.8),
        fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig('figures_individual/39_entity_issue_description_detail.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ 39_entity_issue_description_detail.png")

print("\n" + "="*80)
print("✅ COMPLETE! Generated 9 individual entity distribution figures")
print("="*80)
print("\nFiles saved:")
print("  31_entity_files_changed_by_agent.png")
print("  32_entity_lines_added_by_agent.png")
print("  33_entity_pr_description_length_by_agent.png")
print("  34_entity_review_comment_intensity_by_agent.png")
print("  35_entity_time_to_merge_by_agent.png")
print("  36_entity_repository_popularity.png")
print("  37_entity_commit_message_verbosity.png")
print("  38_entity_developer_social_reach.png")
print("  39_entity_issue_description_detail.png")
print("\nAll figures are 300 DPI with clear, bold text!")

