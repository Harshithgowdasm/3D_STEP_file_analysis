
import os
from scripts.step_analysis import file_selection
# from scripts.step_analysis import *

source_folder = r"S:\03_HiWiS\Harshith\ILSC-APP\3D_STEP_file_analysis\data\Selected_Manually\Combined\Complex"
# destination_folder = "Simple_selected"

# Create the destination folder inside the source folder
destination_path = os.path.join(source_folder, destination_folder)
os.makedirs(destination_path, exist_ok=True)

#call the file selction function 
result_df = file_selection(source_folder, destination_folder)

result_folder_path = r"S:\03_HiWiS\Harshith\ILSC-APP\3D_STEP_file_analysis\data\Selected_Manually\Combined\Complex\Complex_selected"
# Save the CSV inside the destination folder
csv_path = os.path.join(result_folder_path, 'Complex_selected_analysis_result_V06.csv')
result_df.to_csv(csv_path, index=False)
print("Completed")

#Print the results
#print(result_df)
