from app.classes.dbconfig import technicians_info, tickets_data
from app.classes.technicians_info import TechniciansInfo
from scipy.stats import linregress
from io import BytesIO

import base64
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


class DataVizualizer(TechniciansInfo):
    def __init__(self) -> None:
        pass

    def get_all_tickets(self):
        tickets = list(tickets_data.find({}))
        for ticket in tickets:
            ticket['_id'] = str(ticket['_id'])
            user_id = ticket.get('assigned_to')
            if user_id:
                ticket['assigned_to'] = str(user_id)
            ticket['created_at'] = ticket['created_at'].strftime("%Y-%m-%d %H:%M:%S")
        return tickets

    def get_infographics_technicians(self):
        all_technicians = self.get_all_technicians()

        df = pd.DataFrame(all_technicians)

        plt.figure(figsize=(10, 6))
        df.groupby('skill_set')['rating'].mean().plot(kind='bar', color='skyblue')
        plt.title('Average Rating by Skill Set')
        plt.xlabel('Skill Set')
        plt.ylabel('Average Rating')
        plt.xticks(rotation=45)
        plt.tight_layout()
        buf = BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        plt.close()
        buf_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")

        # Example: Pie chart of feedback sentiment distribution
        plt.figure(figsize=(8, 8))
        df['feedback_sentiment'].value_counts().plot(kind='pie', autopct='%1.1f%%', colors=['lightcoral', 'lightskyblue', 'lightgreen'])
        plt.title('Feedback Sentiment Distribution')
        plt.ylabel('')
        plt.tight_layout()
        buf2 = BytesIO()
        plt.savefig(buf2, format="png")
        buf2.seek(0)
        plt.close()
        buf2_base64 = base64.b64encode(buf2.getvalue()).decode("utf-8")

        plt.figure(figsize=(10, 6))
        plt.scatter(df['experience_years'], df['rating'], color='orange', alpha=0.6, s=100, edgecolor='black')
        plt.title('Rating vs. Experience Years')
        plt.xlabel('Experience Years')
        plt.ylabel('Rating')
        
        # Add a trendline
        slope, intercept, r_value, p_value, std_err = linregress(df['experience_years'], df['rating'])
        x_vals = np.array([min(df['experience_years']), max(df['experience_years'])])
        y_vals = slope * x_vals + intercept
        plt.plot(x_vals, y_vals, color='blue', linestyle='--')
        
        plt.grid(True)
        plt.tight_layout()
        buf3 = BytesIO()
        plt.savefig(buf3, format="png")
        buf3.seek(0)
        plt.close()
        buf3_base64 = base64.b64encode(buf3.getvalue()).decode("utf-8")

        # Histogram of experience years
        plt.figure(figsize=(12, 8))
        counts, bins, _ = plt.hist(df['experience_years'], bins=20, color='lightblue', edgecolor='black', alpha=0.7, label='Experience Years')

        # Add count above each bar
        for count, (left_edge, right_edge) in zip(counts, zip(bins[:-1], bins[1:])):
            x = (left_edge + right_edge) / 2  # Calculate the center of the bin
            plt.text(x, count + 0.2, str(int(count)), ha='center', va='bottom')

        # Add vertical lines for mean, median, and quartiles
        mean_exp = df['experience_years'].mean()
        median_exp = df['experience_years'].median()
        q1_exp = df['experience_years'].quantile(0.25)
        q3_exp = df['experience_years'].quantile(0.75)

        plt.axvline(mean_exp, color='red', linestyle='--', linewidth=2, label='Mean: {:.2f}'.format(mean_exp))
        plt.axvline(median_exp, color='green', linestyle='--', linewidth=2, label='Median: {:.2f}'.format(median_exp))
        plt.axvline(q1_exp, color='purple', linestyle='--', linewidth=2, label='Q1: {:.2f}'.format(q1_exp))
        plt.axvline(q3_exp, color='orange', linestyle='--', linewidth=2, label='Q3: {:.2f}'.format(q3_exp))

        # Box plot overlay
        plt.boxplot(df['experience_years'], vert=False, patch_artist=True, widths=0.7, boxprops=dict(facecolor='lightgrey'))
        plt.title('Distribution of Experience Years')
        plt.xlabel('Experience Years')
        plt.ylabel('Frequency')
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.xticks(fontsize=10)
        plt.yticks(fontsize=10)
        plt.legend()

        # Set ylim to ensure the grey box is not included
        plt.ylim(bottom=0)

        plt.tight_layout()

        buf4 = BytesIO()
        plt.savefig(buf4, format="png")
        buf4.seek(0)
        plt.close()
        buf4_base64 = base64.b64encode(buf4.getvalue()).decode("utf-8")

        return [
            {"Average_Rating_by_Skill_Set": buf_base64},
            {"Feedback_Sentiment_Distribution": buf2_base64},
            {"Rating_vs_Experience_Years": buf3_base64},
            {"Experience_Distribution": buf4_base64}
        ]

    def get_infographics_tickets(self):
        tickets_data = self.get_all_tickets()

        df = pd.DataFrame(tickets_data)

        # Count the number of tasks in each status
        status_counts = df['status'].value_counts()

        # Create a pie chart
        plt.figure(figsize=(8, 8))
        plt.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%', colors=['lightcoral', 'lightskyblue', 'lightgreen'])
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        
        # Add title at the center with a box around it
        title_text = 'Task Status Distribution'
        plt.title(title_text, loc='center', bbox=dict(facecolor='lightgrey', alpha=0.5, edgecolor='black', boxstyle='round,pad=0.5'), pad=20)

        plt.tight_layout()

        # Save the plot to a BytesIO object
        buf = BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        plt.close()

        # Convert the plot to base64
        buf_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")


        # Convert 'created_at' column to datetime format
        df['created_at'] = pd.to_datetime(df['created_at'])

        # Group tasks by day and count the number of tasks created each day
        tasks_created_per_day = df.groupby(df['created_at'].dt.date).size()

        # Create a line chart
        plt.figure(figsize=(10, 6))
        tasks_created_per_day.plot(marker='o', color='blue', linestyle='-')
        
        # Set labels and title
        plt.title('Tickets Created Over Time')
        plt.xlabel('Date')
        plt.ylabel('Number of Tickets Created')
        plt.grid(True)
        plt.tight_layout()

        # Save the plot to a BytesIO object
        buf = BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        plt.close()

        # Convert the plot to base64
        buf2_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")

        return [
            {"Count_Tickets_In_Each_Status": buf_base64},
            {"Tickets_Created_Over_Time": buf2_base64}
        ]