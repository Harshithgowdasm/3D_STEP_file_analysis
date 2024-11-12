

import step_analysis

# Define the path to the folder containing STEP files
folder_path = "All"

# Run the analysis and store the results
result_df = step_analysis.run_analysis_for_folder(folder_path)

# Save the results to a CSV file
result_df.to_csv('analysis_df.csv', index=False)

# Print the results
#print(result_df)
