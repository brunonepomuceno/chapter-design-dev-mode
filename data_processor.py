import csv
import os
from collections import Counter
from datetime import datetime

class SurveyDataProcessor:
    def __init__(self):
        self.csv_file = 'data/survey_responses.csv'
        self.responses = []
        self.load_data()
    
    def load_data(self):
        """Load and parse CSV data"""
        try:
            if os.path.exists(self.csv_file):
                with open(self.csv_file, 'r', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    self.responses = list(reader)
            else:
                self.responses = []
        except Exception as e:
            print(f"Error loading CSV data: {e}")
            self.responses = []
    
    def get_ide_preferences(self):
        """Extract IDE usage data"""
        ide_counts = Counter()
        for response in self.responses:
            ide = response.get('Com quais IDEs você trabalha na frete?', '').strip()
            if ide:
                ide_counts[ide] += 1
        return dict(ide_counts)
    
    def get_satisfaction_ratings(self):
        """Extract Dev Mode satisfaction ratings"""
        ratings = []
        for response in self.responses:
            rating = response.get('O Dev Mode do Figma facilita o entendimento dos fluxos?', '').strip()
            if rating and rating.isdigit():
                ratings.append(int(rating))
        
        # Count ratings distribution
        rating_counts = Counter(ratings)
        return {
            'ratings': dict(rating_counts),
            'average': sum(ratings) / len(ratings) if ratings else 0,
            'total_responses': len(ratings)
        }
    
    def get_feedback_themes(self):
        """Analyze what developers like and dislike"""
        likes = []
        dislikes = []
        
        for response in self.responses:
            like = response.get('Do que você MAIS GOSTA nos Handoffs?', '').strip()
            dislike = response.get('Do que você MENOS GOSTA nos Handoffs?', '').strip()
            
            if like:
                # Split by commas and clean up
                like_items = [item.strip() for item in like.split(',')]
                likes.extend(like_items)
            
            if dislike:
                dislike_items = [item.strip() for item in dislike.split(',')]
                dislikes.extend(dislike_items)
        
        return {
            'likes': dict(Counter(likes).most_common(5)),
            'dislikes': dict(Counter(dislikes).most_common(5))
        }
    
    def get_developer_quotes(self):
        """Extract meaningful developer quotes"""
        quotes = []
        for response in self.responses:
            name = response.get('Nome', '').strip()
            feedback = response.get('Fala que eu te escuto', '').strip()
            suggestions = response.get('Você tem alguma sugestões de melhorias para o handoff?', '').strip()
            
            if name and (feedback or suggestions):
                quote_text = feedback if len(feedback) > len(suggestions) else suggestions
                if quote_text and len(quote_text) > 20:  # Only meaningful quotes
                    quotes.append({
                        'name': name,
                        'text': quote_text[:200] + '...' if len(quote_text) > 200 else quote_text,
                        'avatar': f"https://ui-avatars.com/api/?name={name.replace(' ', '+')}&background=2563EB&color=fff"
                    })
        
        return quotes[:3]  # Return top 3 quotes
    
    def get_survey_insights(self):
        """Get all survey insights for the dashboard"""
        ide_data = self.get_ide_preferences()
        satisfaction_data = self.get_satisfaction_ratings()
        feedback_themes = self.get_feedback_themes()
        quotes = self.get_developer_quotes()
        
        # Calculate key statistics
        total_responses = len(self.responses)
        avg_satisfaction = satisfaction_data.get('average', 0)
        
        # Top insights based on data
        top_ide = max(ide_data.items(), key=lambda x: x[1]) if ide_data else ('Visual Studio Code', 0)
        top_like = max(feedback_themes['likes'].items(), key=lambda x: x[1]) if feedback_themes['likes'] else ('Clareza nos fluxos', 0)
        top_dislike = max(feedback_themes['dislikes'].items(), key=lambda x: x[1]) if feedback_themes['dislikes'] else ('Edge cases', 0)
        
        return {
            'total_responses': total_responses,
            'survey_date': 'Março-Abril 2025',
            'avg_satisfaction': round(avg_satisfaction, 1),
            'top_ide': top_ide,
            'top_like': top_like,
            'top_dislike': top_dislike,
            'quotes': quotes,
            'report_date': datetime.now().strftime('%d de %B de %Y')
        }
    
    def get_chart_data(self):
        """Get data formatted for Chart.js"""
        ide_data = self.get_ide_preferences()
        satisfaction_data = self.get_satisfaction_ratings()
        feedback_themes = self.get_feedback_themes()
        
        return {
            'ide_chart': {
                'labels': list(ide_data.keys()),
                'data': list(ide_data.values()),
                'backgroundColor': ['#2563EB', '#3B82F6', '#60A5FA', '#93C5FD']
            },
            'satisfaction_chart': {
                'labels': [f'Rating {k}' for k in satisfaction_data['ratings'].keys()],
                'data': list(satisfaction_data['ratings'].values()),
                'backgroundColor': ['#EF4444', '#F97316', '#EAB308', '#22C55E', '#10B981']
            },
            'feedback_chart': {
                'likes': {
                    'labels': list(feedback_themes['likes'].keys())[:5],
                    'data': list(feedback_themes['likes'].values())[:5]
                },
                'dislikes': {
                    'labels': list(feedback_themes['dislikes'].keys())[:5],
                    'data': list(feedback_themes['dislikes'].values())[:5]
                }
            }
        }
