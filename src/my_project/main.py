import os
import json
from my_project.crew import MyProjectCrew

def run():
    #getting the path to the root directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    #my_project/src/my_project/main.py
    root_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))
    data_path = os.path.join(root_dir, 'data', 'test_review_subset.json')
    
    print(f"Loading test case from: {data_path}")

    #extracting the first case from the test file
    try:
        with open(data_path, 'r', encoding='utf-8') as f:
            line = f.readline()
            if not line:
                print("Error: The test file is empty.")
                return
            first_case = json.loads(line)
            
    except FileNotFoundError:
        print(f"Error: Cannot find file at {data_path}")
        return
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON. Check if the file format is correct.")
        return

    #preparing inputs for the Crew
    inputs = {
        'user_id': first_case.get('user_id'),
        'item_id': first_case.get('business_id') or first_case.get('item_id')
    }
    
    print("="*30)
    print(f"KICKING OFF YELP PREDICTION CREW")
    print(f"Target User: {inputs['user_id']}")
    print(f"Target Item: {inputs['item_id']}")
    print("="*30)

    #kickoff the crew
    try:
        result = MyProjectCrew().crew().kickoff(inputs=inputs)
        
        print("\n" + "="*30)
        print("FINAL PREDICTION RESULT:")
        print(result)
        print("="*30)
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    run()