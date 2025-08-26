import pandas as pd
from django.core.management.base import BaseCommand
from core.models import LinkedInPost
from datetime import datetime
#https://docs.google.com/spreadsheets/d/1thMQ4ndtgzyEM6qfoA2tfrt3MEzZY2CtxhjpCTNcS0U/gviz/tq?tqx=out:csv&sheet=Content

class Command(BaseCommand):
    help = 'Load data from a CSV link into the LinkedInPost model'

    def add_arguments(self, parser):
        # The argument is now a URL
        parser.add_argument('csv_url', type=str, help='The URL of the CSV file to load.')

    def handle(self, *args, **options):
        csv_url = options['csv_url']
        self.stdout.write(f"Loading data from {csv_url}")

        try:
            df = pd.read_csv(csv_url)
            df = df[['Post title', 'Post link', 'Created date', 'Impressions', 'Clicks',
       'Click through rate (CTR)', 'Likes', 'Comments',
       'Engagement rate', 'Category',
       'Sub-Category', 'Year', 'Month', 'Day of the week',
        'Emoji', 'Type of Post', 'Interval Times']].copy()
            
            for index, row in df.iterrows():
                self.stdout.write(row)
                

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {e}"))