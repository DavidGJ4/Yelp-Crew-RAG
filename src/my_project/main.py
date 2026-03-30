import os
import json
from my_project.crew import MyProjectCrew

def run():
    #paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))
    data_path = os.path.join(root_dir, 'data', 'test_review_subset.json')
    
    print(f"Loading test case from: {data_path}")

    #extracting ground truth
    try:
        with open(data_path, 'r', encoding='utf-8') as f:
            line = f.readline()
            if not line:
                return
            ground_truth = json.loads(line)
            
    except Exception as e:
        print(f"Error loading test file: {e}")
        return

    #preparing inputs
    inputs = {
        'user_id': ground_truth.get('user_id'),
        'item_id': ground_truth.get('business_id') or ground_truth.get('item_id')
    }
    
    print("="*30)
    print(f"KICKING OFF YELP PREDICTION CREW")
    print(f"Target User: {inputs['user_id']}")
    print(f"Target Item: {inputs['item_id']}")
    print("="*30)

    #kickoff and saving Result
    try:
        result = MyProjectCrew().crew().kickoff(inputs=inputs)
        prediction_data = result.pydantic.dict() if hasattr(result, 'pydantic') else str(result)

        #creating the comparison Report
        report = {
            "target_user": inputs['user_id'],
            "target_item": inputs['item_id'],
            "ground_truth": {
                "stars": ground_truth.get('stars'),
                "review": ground_truth.get('text')
            },
            "prediction": prediction_data
        }

        #saving to report.json in the root directory
        report_path = os.path.join(root_dir, 'report.json')
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=4)

        print(f"\nPrediction Finished! Report saved to: {report_path}")
        print("\n" + "="*30)
        print("QUICK COMPARISON:")
        print(f"Actual Stars: {ground_truth.get('stars')}")
        print(f"Predicted Stars: {prediction_data.get('stars') if isinstance(prediction_data, dict) else 'Check report'}")
        print("="*30)
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    run()