
import os
import step_analysis

source_folder = r"S:\03_HiWiS\Harshith\ILSC-APP\abc_0000_step_v00\step_06"
destination_folder = "Simple_selected"

# Create the destination folder inside the source folder
destination_path = os.path.join(source_folder, destination_folder)
os.makedirs(destination_path, exist_ok=True)

#call the file selction function 
result_df = step_analysis.file_selection(source_folder, destination_folder)

# Save the CSV inside the destination folder
csv_path = os.path.join(destination_path, 'analysis_step_06.csv')
result_df.to_csv(csv_path, index=False)

#Print the results
#print(result_df)
