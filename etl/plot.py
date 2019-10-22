import matplotlib.pyplot as plt
import seaborn as sns


class PlotFactory:
    def __init__(self, analysis):
        self.mapper = {
            'tier_analysis': TierAnalysis
        }
        self.plotter = self.mapper[analysis]


class TierAnalysis:
    @ staticmethod
    def plot_tier_counts(tier_counts):
        tier_counts_form = tier_counts.pivot(
            index='donor_tier', columns='classification', values='count'
        ).fillna(0)

        # Plot setup
        fig, ax = plt.subplots(figsize=(15,10))
        sns.set(style="ticks")

        # Create the plot
        tier_counts_form.plot(ax=ax, kind='bar', stacked=True)

        # titles
        ax.set_title("Donor Tier Funnel - Number of Donors - FY20", fontsize=30)

        # axes
        ax.tick_params(axis='both', labelsize=16)
        ax.set_xlabel('Donor Tier', fontsize=20)
        ax.set_ylabel('Number of Donors', fontsize=20)

        plt.xticks(rotation=0)

        # Show plot
        plt.show()

    @staticmethod
    def plot_tier_revenue(tier_revenue):
        # Plot setup
        fig, ax = plt.subplots(figsize=(15,10))
        sns.set(style="ticks")

        # Create the plot
        ax = sns.barplot(x="donor_tier", y="transaction_amount", data=tier_revenue)

        # titles
        ax.set_title("Revenue Generated per Tier - FY20", fontsize=30)

        # axes
        ax.tick_params(axis='both', labelsize=16)
        ax.set_xlabel('Donor Tier', fontsize=20)
        ax.set_ylabel('Revenue Generated', fontsize=20)

        plt.xticks(rotation=0)

        # Show plot
        plt.show()
