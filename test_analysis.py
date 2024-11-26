
import os
import step_analysis

source_folder = "Selected"
destination_folder = "selected_automation_1"
os.makedirs(destination_folder, exist_ok=True)
result_df = step_analysis.file_selection(source_folder, destination_folder)
result_df.to_csv('analysis_df.csv', index=False)

#Print the results
#print(result_df)
