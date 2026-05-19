from database import TicketDatabase
import sqlite3

def view_database():
    """Display database contents in a readable format"""
    db = TicketDatabase()
    
    print("\n" + "="*80)
    print("TICKET ANALYSIS DATABASE")
    print("="*80)
    
    # Get all analyses
    analyses = db.get_all_analyses()
    
    if not analyses:
        print("\nNo data in database yet!")
        return
    
    print(f"\nTotal tickets analyzed: {len(analyses)}\n")
    
    for ticket in analyses:
        ticket_id, customer, subject, urgency, sentiment, category, team, analyzed_at = ticket
        
        print(f"Ticket #{ticket_id} - {customer}")
        print(f"  Subject: {subject}")
        print(f"  Urgency: {urgency}")
        print(f"  Sentiment: {sentiment}")
        print(f"  Category: {category}")
        print(f"  Assigned to: {team}")
        print(f"  Analyzed: {analyzed_at}")
        print()
    
    # Show statistics
    print("="*80)
    print("STATISTICS")
    print("="*80)
    
    stats = db.get_stats()
    
    print("\nUrgency Distribution:")
    for urgency, count in stats['urgency'].items():
        print(f"  {urgency}: {count}")
    
    print("\nSentiment Distribution:")
    for sentiment, count in stats['sentiment'].items():
        print(f"  {sentiment}: {count}")
    
    print("\nCategory Distribution:")
    for category, count in stats['category'].items():
        print(f"  {category}: {count}")
    
    print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    view_database()