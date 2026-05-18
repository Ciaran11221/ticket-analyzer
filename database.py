import sqlite3
import json
from datetime import datetime

class TicketDatabase:
    def __init__(self, db_path='tickets.db'):
        self.db_path = db_path
        self.setup_database()
    
    def setup_database(self):
        """Create tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tickets table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id TEXT,
                customer TEXT,
                subject TEXT,
                message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Analysis results table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id INTEGER,
                urgency TEXT,
                sentiment TEXT,
                category TEXT,
                suggested_team TEXT,
                summary TEXT,
                analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (ticket_id) REFERENCES tickets(id)
            )
        ''')
        
        # Evaluation table (for tracking accuracy)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS evaluations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id INTEGER,
                field TEXT,
                ai_prediction TEXT,
                human_label TEXT,
                is_correct BOOLEAN,
                evaluated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (ticket_id) REFERENCES tickets(id)
            )
        ''')
        
        conn.commit()
        conn.close()
        print("Database setup complete!")
    
    def insert_ticket(self, ticket_id, customer, subject, message):
        """Insert a new ticket"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO tickets (ticket_id, customer, subject, message)
            VALUES (?, ?, ?, ?)
        ''', (ticket_id, customer, subject, message))
        
        conn.commit()
        db_ticket_id = cursor.lastrowid
        conn.close()
        return db_ticket_id
    
    def insert_analysis(self, ticket_id, analysis):
        """Insert analysis results"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO analysis (ticket_id, urgency, sentiment, category, suggested_team, summary)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            ticket_id,
            analysis['urgency'],
            analysis['sentiment'],
            analysis['category'],
            analysis['suggested_team'],
            analysis['summary']
        ))
        
        conn.commit()
        conn.close()
    
    def get_all_analyses(self):
        """Get all analyses with ticket info"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                t.ticket_id, t.customer, t.subject,
                a.urgency, a.sentiment, a.category, a.suggested_team,
                a.analyzed_at
            FROM tickets t
            JOIN analysis a ON t.id = a.ticket_id
            ORDER BY a.analyzed_at DESC
        ''')
        
        results = cursor.fetchall()
        conn.close()
        return results
    
    def get_stats(self):
        """Get summary statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Count by urgency
        cursor.execute('SELECT urgency, COUNT(*) FROM analysis GROUP BY urgency')
        urgency_stats = dict(cursor.fetchall())
        
        # Count by sentiment
        cursor.execute('SELECT sentiment, COUNT(*) FROM analysis GROUP BY sentiment')
        sentiment_stats = dict(cursor.fetchall())
        
        # Count by category
        cursor.execute('SELECT category, COUNT(*) FROM analysis GROUP BY category')
        category_stats = dict(cursor.fetchall())
        
        conn.close()
        
        return {
            'urgency': urgency_stats,
            'sentiment': sentiment_stats,
            'category': category_stats
        }

if __name__ == "__main__":
    # Test the database
    db = TicketDatabase()
    print("Database ready!")