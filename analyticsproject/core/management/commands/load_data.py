import pandas as pd
from django.core.management.base import BaseCommand
from core.models import LinkedInPost
from datetime import datetime
from overall.models import Followers

# https://docs.google.com/spreadsheets/d/1thMQ4ndtgzyEM6qfoA2tfrt3MEzZY2CtxhjpCTNcS0U/gviz/tq?tqx=out:csv&sheet=Content
# https://docs.google.com/spreadsheets/d/1thMQ4ndtgzyEM6qfoA2tfrt3MEzZY2CtxhjpCTNcS0U/gviz/tq?tqx=out:csv&sheet=Sheet24
# https://docs.google.com/spreadsheets/d/1thMQ4ndtgzyEM6qfoA2tfrt3MEzZY2CtxhjpCTNcS0U/gviz/tq?tqx=out:csv&sheet=Sheet25
# https://docs.google.com/spreadsheets/d/1thMQ4ndtgzyEM6qfoA2tfrt3MEzZY2CtxhjpCTNcS0U/gviz/tq?tqx=out:csv&sheet=Sheet26
# https://docs.google.com/spreadsheets/d/1thMQ4ndtgzyEM6qfoA2tfrt3MEzZY2CtxhjpCTNcS0U/gviz/tq?tqx=out:csv&sheet=Sheet27
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
        
            df = df[['Date', 'Total followers', 'Follower Count', 'Month/Yr']].copy()
            
            
            for index, row in df.iterrows():
           
                date_obj = datetime.strptime(row['Date'], '%m/%d/%Y').date()

                month_year_obj = datetime.strptime(row['Month/Yr'], '%b %Y').date()

                post, created = Followers.objects.update_or_create(
                    date= date_obj,
                    defaults={
                        'follower_increase' : pd.to_numeric(row['Total followers']),
                        'total_follower_count' : pd.to_numeric(row['Follower Count']),
                        'month_year' : month_year_obj
                    }
                )
                

                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created new post: "{post.date}"'))
                else:
                    self.stdout.write(f'Updated existing post: "{post.date}"')

            self.stdout.write(self.style.SUCCESS('Successfully loaded all data.'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {e}"))

    # help = 'Load data from a CSV link into the LinkedInPost model'

    # def add_arguments(self, parser):
    #     # The argument is now a URL
    #     parser.add_argument('csv_url', type=str, help='The URL of the CSV file to load.')

    # def handle(self, *args, **options):
    #     csv_url = options['csv_url']
    #     self.stdout.write(f"Loading data from {csv_url}")

    #     try:
    #         df = pd.read_csv(csv_url)
    #         df = df[['Post title', 'Post link', 'Created date', 'Impressions', 'Clicks',
    #    'Click through rate (CTR)', 'Likes', 'Comments',
    #    'Engagement rate', 'Category',
    #    'Sub-Category', 'Year', 'Month', 'Day of the week',
    #     'Emoji', 'Type of Post', 'Interval Times']].copy()
            
    #         for index, row in df.iterrows():
    #             created_date_obj = datetime.strptime(row['Created date'], '%m/%d/%Y').date()
    #             time_of_posting_obj = datetime.strptime(row['Interval Times'], '%I:%M %p').time()

    #             emoji_bool = str(row['Emoji']).upper() == 'TRUE'

    #             post, created = LinkedInPost.objects.update_or_create(
    #                 post_link = row['Post link'],
    #                 defaults={
    #                     'post_title' : row['Post title'],
    #                     'created_date' : created_date_obj,
    #                     'impressions': pd.to_numeric(row['Impressions'], errors='coerce'),
    #                     'clicks' : pd.to_numeric(row['Clicks'], errors='coerce'),
    #                     'ctr' : pd.to_numeric(row['Click through rate (CTR)'], errors='coerce'),
    #                     'likes' : pd.to_numeric(row['Likes'], errors='coerce'),
    #                     'comments': pd.to_numeric(row['Comments'], errors='coerce'),
    #                     'engagement_rate': pd.to_numeric(row['Engagement rate'], errors='coerce'),
    #                     'category': row['Category'],
    #                     'sub_category': row['Sub-Category'],
    #                     'year': row['Year'],
    #                     'month': row['Month'],
    #                     'day_of_week': row['Day of the week'],
    #                     'time_of_posting': time_of_posting_obj,
    #                     'emoji': emoji_bool,
    #                     'type_of_post': row['Type of Post'],
    #                 }
    #             )

    #             if created:
    #                 self.stdout.write(self.style.SUCCESS(f'Created new post: "{post.post_title}"'))
    #             else:
    #                 self.stdout.write(f'Updated existing post: "{post.post_title}"')

    #         self.stdout.write(self.style.SUCCESS('Successfully loaded all data.'))
                
    #     except Exception as e:
    #         self.stdout.write(self.style.ERROR(f"An error occurred: {e}"))