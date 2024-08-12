import csv

def save_all(input_text, first_handle_result, target_result, trajectory_result, location_result, original_steps, detailed_steps, thetas):
    with open('record.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([input_text, first_handle_result, target_result, trajectory_result, location_result, original_steps, detailed_steps, thetas])
