import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

# Set a premium plotting style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_context("talk")

# Curated palette for high-end look
COLORS = {
    'treated': '#E63946',     # Crimson
    'control': '#1D3557',     # Deep Blue
    'shock': '#F4A261',       # Coral orange for the shock
    'ols': '#457B9D',         # Steel Blue
    'poisson': '#2A9D8F',     # Teal
    'dark_text': '#1D3557',
    'light_bg': '#F8F9FA'
}

def plot_cancellation_trends(panel_df, segment_name="Group Bookings"):
    """
    Plots weekly cancellation trends for treated (Resort Hotel) and control (City Hotel)
    groups, highlighting the June 2017 Mega-Wildfires shock.
    """
    fig, ax = plt.subplots(figsize=(14, 7), facecolor='white')
    ax.set_facecolor(COLORS['light_bg'])
    
    # Pivot data for plotting
    plot_df = panel_df.pivot(index='week_start', columns='hotel', values='cancellations')
    
    # Plot lines with premium colors and markers
    ax.plot(plot_df.index, plot_df['Resort Hotel'], label='Resort Hotel (Treated)', 
            color=COLORS['treated'], linewidth=2.5, marker='o', markersize=4, alpha=0.9)
    ax.plot(plot_df.index, plot_df['City Hotel'], label='City Hotel (Control)', 
            color=COLORS['control'], linewidth=2.5, marker='s', markersize=4, alpha=0.7)
    
    # Highlight the wildfire shock (week starting June 12, 2017)
    shock_date = pd.Timestamp('2017-06-12')
    ax.axvline(shock_date, color=COLORS['shock'], linestyle='--', linewidth=2.5, 
               label='Wildfire Shock (June 2017)')
    
    # Add a highlighted region for post-treatment
    ax.axvspan(shock_date, plot_df.index.max(), color=COLORS['shock'], alpha=0.08)
    
    # Annotation for the wildfire
    ax.text(shock_date + pd.Timedelta(days=5), ax.get_ylim()[1] * 0.85, 
            'Portuguese\nMega-Wildfires\n(June 2017)', 
            color='#D97706', fontweight='bold', fontsize=12)

    # Titles & Labels
    ax.set_title(f'Weekly Cancellation Counts: {segment_name} Segment', 
                 fontsize=18, fontweight='bold', color=COLORS['dark_text'], pad=20)
    ax.set_xlabel('Arrival Week Start Date', fontsize=14, fontweight='bold', color=COLORS['dark_text'], labelpad=10)
    ax.set_ylabel('Number of Cancellations', fontsize=14, fontweight='bold', color=COLORS['dark_text'], labelpad=10)
    
    # Grid and legend styling
    ax.grid(True, linestyle=':', alpha=0.6)
    legend = ax.legend(frameon=True, facecolor='white', edgecolor='none', shadow=True, fontsize=12)
    legend.get_frame().set_alpha(0.9)
    
    plt.tight_layout()
    return fig

def plot_model_comparison(panel_df, ols_pred, poisson_pred, segment_name="Group Bookings"):
    """
    Plots the actual vs. predicted values for OLS and Poisson, showing how
    OLS predicts negative counts.
    """
    # Create the visualization
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7), facecolor='white')
    
    # Left subplot: Actual vs. Predicted Time-series (Treated Hotel only)
    ax1.set_facecolor(COLORS['light_bg'])
    resort_df = panel_df[panel_df['hotel'] == 'Resort Hotel'].copy()
    resort_idx = resort_df.index
    
    ax1.plot(resort_df['week_start'], resort_df['cancellations'], label='Actual Cancellations', 
            color=COLORS['treated'], linewidth=2.0, alpha=0.6, marker='o', markersize=3)
    ax1.plot(resort_df['week_start'], ols_pred[resort_idx], label='OLS Predictions', 
            color=COLORS['ols'], linewidth=2.5, linestyle='-')
    ax1.plot(resort_df['week_start'], poisson_pred[resort_idx], label='Poisson Predictions', 
            color=COLORS['poisson'], linewidth=2.5, linestyle='--')
    
    # Highlight the wildfire shock
    shock_date = pd.Timestamp('2017-06-12')
    ax1.axvline(shock_date, color=COLORS['shock'], linestyle=':', linewidth=2)
    
    ax1.set_title('Treated Group (Resort Hotel): Actual vs. Predictions', 
                 fontsize=16, fontweight='bold', color=COLORS['dark_text'], pad=15)
    ax1.set_xlabel('Week Start Date', fontsize=12, color=COLORS['dark_text'])
    ax1.set_ylabel('Cancellations', fontsize=12, color=COLORS['dark_text'])
    ax1.grid(True, linestyle=':', alpha=0.6)
    ax1.legend(frameon=True, fontsize=11)
    
    # Right subplot: Highlight Negative OLS Predictions
    ax2.set_facecolor(COLORS['light_bg'])
    
    # Plot histogram or scatter of predictions in chronological order to highlight negative bounds
    ax2.scatter(panel_df['week_start'], ols_pred, color=COLORS['ols'], alpha=0.5, label='OLS Predictions', s=25)
    ax2.scatter(panel_df['week_start'], poisson_pred, color=COLORS['poisson'], alpha=0.7, label='Poisson Predictions', s=25)
    
    # Zero line
    ax2.axhline(0, color='black', linestyle='-', linewidth=1.5, alpha=0.7)
    
    # Highlight the negative prediction region
    min_ols = min(ols_pred)
    if min_ols < 0:
        ax2.axhspan(min_ols - 0.5, 0, color='#fee2e2', alpha=0.5, label='Physical Nonsense (Negative Counts)')
    
    ax2.set_title('Distribution of Predictions: Linear vs. Exponential link', 
                 fontsize=16, fontweight='bold', color=COLORS['dark_text'], pad=15)
    ax2.set_xlabel('Week Start Date', fontsize=12, color=COLORS['dark_text'])
    ax2.set_ylabel('Predicted Counts', fontsize=12, color=COLORS['dark_text'])
    ax2.grid(True, linestyle=':', alpha=0.6)
    ax2.legend(frameon=True, fontsize=11, loc='upper left')
    
    plt.tight_layout()
    return fig

def plot_log_offset_sensitivity(offsets, coefficients, std_errors):
    """
    Plots treatment effect coefficients and confidence intervals across different log offsets,
    visualizing the log(1+Y) landmine.
    """
    fig, ax = plt.subplots(figsize=(12, 6.5), facecolor='white')
    ax.set_facecolor(COLORS['light_bg'])
    
    # Convert inputs to numpy arrays
    offsets = np.array(offsets)
    coefficients = np.array(coefficients)
    std_errors = np.array(std_errors)
    
    # Compute 95% confidence intervals
    ci_lower = coefficients - 1.96 * std_errors
    ci_upper = coefficients + 1.96 * std_errors
    
    # Plot coefficients and CI bands
    ax.plot(offsets, coefficients, marker='o', color=COLORS['ols'], linewidth=2.5, 
            label='Estimated Treatment Effect (OLS Coefficient)')
    ax.fill_between(offsets, ci_lower, ci_upper, color=COLORS['ols'], alpha=0.15, 
                    label='95% Confidence Interval')
    
    # Add labels on x-axis
    ax.set_xscale('log')
    ax.set_xticks(offsets)
    ax.set_xticklabels([str(o) for o in offsets])
    
    # Labels & Title
    ax.set_title('The log(Y + ε) Landmine: Treatment Effect Sensitivity to Offset ε', 
                 fontsize=18, fontweight='bold', color=COLORS['dark_text'], pad=20)
    ax.set_xlabel('Offset Value (ε) on Log Scale', fontsize=14, fontweight='bold', color=COLORS['dark_text'], labelpad=10)
    ax.set_ylabel('Treatment Effect (OLS Coeff)', fontsize=14, fontweight='bold', color=COLORS['dark_text'], labelpad=10)
    
    ax.grid(True, which="both", linestyle=':', alpha=0.6)
    ax.legend(frameon=True, facecolor='white', shadow=True, fontsize=12)
    
    # Add a text callout on how the treatment effect wildly shifts
    range_coeff = coefficients.max() - coefficients.min()
    ax.text(offsets[len(offsets)//2], coefficients.min() + range_coeff*0.2, 
            '⚠️ Warning:\nChanging the offset shifts\nthe treatment effect & significance!', 
            bbox=dict(facecolor='white', edgecolor='red', boxstyle='round,pad=0.5', alpha=0.9),
            color='red', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    return fig
