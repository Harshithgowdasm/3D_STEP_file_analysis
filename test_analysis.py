
import os
import step_analysis

source_folder = r"S:\03_HiWiS\Harshith\ILSC-APP\abc_0000_step_v00\step_09"
destination_folder = "Selected"

# Create the destination folder inside the source folder
destination_path = os.path.join(source_folder, destination_folder)
os.makedirs(destination_path, exist_ok=True)

#call the file selction function 
result_df = step_analysis.file_selection(source_folder, destination_folder)

result_folder_path = r"S:\03_HiWiS\Harshith\ILSC-APP\abc_0000_step_v00\Results_new"
# Save the CSV inside the destination folder
csv_path = os.path.join(result_folder_path, 'selected_analysis_09.csv')
result_df.to_csv(csv_path, index=False)
print("Completed")

#Print the results
#print(result_df)
