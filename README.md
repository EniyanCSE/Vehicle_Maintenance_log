#Vehicle Maintenance Log
This Streamlit application allows users to maintain a log of vehicle maintenance activities. Users can input details such as date, mileage, performed tasks, service costs, and next service due date. Additionally, users can create new vehicle logs and download log details as a PDF.

##Usage
Installation: Ensure you have Python installed. Clone this repository and install the necessary dependencies using pip install -r requirements.txt.

##Running the Application: Run the Streamlit application using the
 ```streamlit run app.py ```

##Creating New Vehicle Log:

Click on the "Create New Vehicle Log" button in the sidebar.
Enter the log date and other details.
Click on "Create New Vehicle Log" button to add the new log entry.
Viewing and Editing Log Details:

Select a log date from the sidebar dropdown to view and edit the log details.
Update the details as required and click on "Update Log Details" button.
Downloading Log Details as PDF:

After selecting a log date, click on the "Download as PDF" button to download the log details as a PDF document.

##File Structure
app.py: Contains the main Streamlit application code.
vehicle_maintenance_log.xlsx: Excel file used to store vehicle maintenance log data.(will be created autometically while running the program)
##Dependencies
```
pip install Streamlit
pip install pandas
pip install fpdf
```
Contributing
Contributions are welcome! If you find any bugs or have suggestions for improvement, please open an issue or submit a pull request.

License
This project is licensed under the MIT License.
