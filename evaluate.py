import sqlite3
from database import TicketDatabase

def evaluate_ticket():
    """Interactive tool to evaluate AI predictions"""
    db = TicketDatabase()
    conn = sqlite3.connect('tickets.db')
    cursor = conn.cursor()
    
    # Get tickets that haven't been evaluated yet
    cursor.execute('''
        SELECT t.id, t.ticket_id, t.customer, t.subject, t.message,
               a.urgency, a.sentiment, a.category, a.suggested_team
        FROM tickets t
        JOIN analysis a ON t.id = a.ticket_id
        WHERE t.id NOT IN (SELECT DISTINCT ticket_id FROM evaluations)
        LIMIT 1
    ''')
    
    result = cursor.fetchone()
    
    if not result:
        print("\n✓ All tickets have been evaluated!")
        show_accuracy_report()
        conn.close()
        return
    
    db_id, ticket_id, customer, subject, message, urgency, sentiment, category, team = result
    
    print("\n" + "="*80)
    print(f"TICKET #{ticket_id} - {customer}")
    print("="*80)
    print(f"Subject: {subject}")
    print(f"Message: {message}")
    print("\n" + "-"*80)
    print("AI PREDICTIONS:")
    print(f"  Urgency: {urgency}")
    print(f"  Sentiment: {sentiment}")
    print(f"  Category: {category}")
    print(f"  Team: {team}")
    print("-"*80 + "\n")
    
    # Evaluate each field
    evaluations = []
    
    # Urgency
    print("Is URGENCY correct? (high/medium/low)")
    print(f"AI said: {urgency}")
    correct = input("Correct? (y/n or type correct value): ").strip().lower()
    if correct == 'y':
        evaluations.append(('urgency', urgency, urgency, True))
    else:
        human_label = correct if correct != 'n' else input("What should it be?: ")
        evaluations.append(('urgency', urgency, human_label, False))
    
    # Sentiment
    print(f"\nIs SENTIMENT correct? AI said: {sentiment}")
    correct = input("Correct? (y/n or type correct value): ").strip().lower()
    if correct == 'y':
        evaluations.append(('sentiment', sentiment, sentiment, True))
    else:
        human_label = correct if correct != 'n' else input("What should it be?: ")
        evaluations.append(('sentiment', sentiment, human_label, False))
    
    # Category
    print(f"\nIs CATEGORY correct? AI said: {category}")
    correct = input("Correct? (y/n or type correct value): ").strip().lower()
    if correct == 'y':
        evaluations.append(('category', category, category, True))
    else:
        human_label = correct if correct != 'n' else input("What should it be?: ")
        evaluations.append(('category', category, human_label, False))
    
    # Save evaluations
    for field, ai_pred, human_label, is_correct in evaluations:
        cursor.execute('''
            INSERT INTO evaluations (ticket_id, field, ai_prediction, human_label, is_correct)
            VALUES (?, ?, ?, ?, ?)
        ''', (db_id, field, ai_pred, human_label, is_correct))
    
    conn.commit()
    conn.close()
    
    print("\n✓ Evaluation saved!\n")
    
    # Ask if they want to continue
    another = input("Evaluate another ticket? (y/n): ").strip().lower()
    if another == 'y':
        evaluate_ticket()
    else:
        show_accuracy_report()

def show_accuracy_report():
    """Show overall accuracy statistics"""
    conn = sqlite3.connect('tickets.db')
    cursor = conn.cursor()
    
    print("\n" + "="*80)
    print("ACCURACY REPORT")
    print("="*80 + "\n")
    
    # Overall accuracy
    cursor.execute('SELECT COUNT(*) FROM evaluations WHERE is_correct = 1')
    correct = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM evaluations')
    total = cursor.fetchone()[0]
    
    if total == 0:
        print("No evaluations yet!")
        conn.close()
        return
    
    accuracy = (correct / total) * 100
    print(f"Overall Accuracy: {accuracy:.1f}% ({correct}/{total} correct)")
    
    # Per-field accuracy
    for field in ['urgency', 'sentiment', 'category']:
        cursor.execute('''
            SELECT COUNT(*) FROM evaluations 
            WHERE field = ? AND is_correct = 1
        ''', (field,))
        field_correct = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM evaluations WHERE field = ?', (field,))
        field_total = cursor.fetchone()[0]
        
        if field_total > 0:
            field_accuracy = (field_correct / field_total) * 100
            print(f"{field.capitalize()} Accuracy: {field_accuracy:.1f}% ({field_correct}/{field_total})")
    
    conn.close()
    print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    print("TICKET EVALUATION TOOL")
    print("This helps you track AI accuracy by labeling tickets as correct/incorrect\n")
    evaluate_ticket()

