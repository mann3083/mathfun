import json
import random
from datetime import datetime, timedelta

def generate_dummy_data():
    data = {}
    # Start from 5 days ago
    base_time = datetime.now() - timedelta(days=5)
    
    # The new categories we added to math_utils.py
    categories = ['Algebra', 'Arithmetic', 'Number Theory', 'Fractions & %']
    
    # Simulate 5 days
    for day in range(5):
        # 3 tests per day (Morning, Afternoon, Evening)
        times = [
            (9, 30),  # 9:30 AM
            (14, 15), # 2:15 PM
            (19, 45)  # 7:45 PM
        ]
        
        for hour, minute in times:
            # 1. Create Timestamp Key (DD-MM-YY-HH-MM)
            current_date = base_time + timedelta(days=day)
            timestamp = current_date.replace(hour=hour, minute=minute)
            key = timestamp.strftime("%d-%m-%y-%H-%M")
            
            # 2. Simulate Progressive Improvement
            # Day 0: ~40% correct, Day 4: ~90% correct
            base_score = 4 + day 
            score = min(10, base_score + random.randint(0, 2)) 
            
            # 3. Generate Dummy Details
            details = []
            for q_id in range(1, 11):
                # Determine if this specific question is "correct" based on the total score
                is_correct = q_id <= score
                
                # Pick a random category to populate the Radar Chart
                cat = random.choice(categories)
                
                details.append({
                    "question_id": random.randint(100000, 999999),
                    "question_text": f"Simulated {cat} Question {q_id}",
                    "question_type": "single",
                    "category": cat,  # <--- CRITICAL UPDATE FOR RADAR CHART
                    "user_answer": "42",
                    "correct_answer": "42" if is_correct else "99",
                    "is_correct": is_correct,
                    "time_spent": random.randint(5, 45)
                })

            # 4. Construct Summary
            entry = {
                "summary": {
                    "score_obtained": score,
                    "total_questions": 10,
                    "percentage": float(score * 10),
                    "total_time_seconds": random.randint(180, 400)
                },
                "details": details
            }
            
            data[key] = entry

    # Write to file
    with open("results.json", "w") as f:
        json.dump(data, f, indent=4)
    
    print(f"Successfully generated results.json with {len(data)} entries.")
    print("Refresh your Dashboard to see the new Skill Radar!")

if __name__ == "__main__":
    generate_dummy_data()