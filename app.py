import streamlit as st
import pandas as pd
from fpdf import FPDF
import os

# Function to check if the Excel file exists, and create it if not
def create_excel_file(file_path):
    if not os.path.exists(file_path):
        df = pd.DataFrame(columns=["Date", "Mileage", "Performed Tasks", "Service Costs", "Next Service Due"])
        df.loc[0] = [pd.to_datetime("today").strftime("%Y/%m/%d"), 0, "", 0, pd.to_datetime("today").strftime("%Y/%m/%d")]
        df.to_excel(file_path, index=False)
        return True
    return False

# Function to load data from Excel file into DataFrame
def load_data(file_path):
    df = pd.read_excel(file_path)
    return df

# Function to save DataFrame to Excel file
def save_data(df, file_path):
    df.to_excel(file_path, index=False)

# Function to add new vehicle log to Excel file
def add_new_vehicle_log(date, mileage, performed_tasks, service_costs, next_service_due, file_path):
    df = load_data(file_path)
    new_row_index = df.shape[0]
    df.loc[new_row_index, "Date"] = date
    df.loc[new_row_index, "Mileage"] = mileage
    df.loc[new_row_index, "Performed Tasks"] = performed_tasks
    df.loc[new_row_index, "Service Costs"] = service_costs
    df.loc[new_row_index, "Next Service Due"] = next_service_due
    save_data(df, file_path)

# Function to generate PDF document
def generate_pdf(selected_log_data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Vehicle Maintenance Log", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Date: {selected_log_data['Date']}", ln=True)
    pdf.cell(200, 10, txt=f"Mileage: {selected_log_data['Mileage']}", ln=True)
    pdf.cell(200, 10, txt=f"Performed Tasks: {selected_log_data['Performed Tasks']}", ln=True)
    pdf.cell(200, 10, txt=f"Service Costs: {selected_log_data['Service Costs']}", ln=True)
    pdf.cell(200, 10, txt=f"Next Service Due: {selected_log_data['Next Service Due']}", ln=True)
    return pdf

# Main function
def main():
    st.title("Vehicle Maintenance Log")

    # Check if Excel file exists and create it if not
    file_path = "vehicle_maintenance_log.xlsx"
    excel_created = create_excel_file(file_path)

    # Load data from Excel file
    df = load_data(file_path)

    # Initialize selected_log_date
    selected_log_date = None

    # Sidebar
    st.sidebar.header("Options")
    if df.empty or excel_created:  # Adjusted condition
        st.sidebar.write("No vehicle logs created.")
    else:
        selected_log_date = st.sidebar.selectbox("Select Log Date:", df["Date"].unique())

    # Display log details if selected_log_date is not None
    if selected_log_date is not None:
        st.subheader(f"Log Details: {selected_log_date}")
        selected_log_data = df[df["Date"] == selected_log_date].iloc[0]
        date = st.date_input("Date:", pd.to_datetime(selected_log_data["Date"]))  # Convert to datetime
        mileage = st.number_input("Mileage:", value=int(selected_log_data["Mileage"]), step=1)
        performed_tasks = st.text_area("Performed Tasks:", selected_log_data["Performed Tasks"])
        service_costs = st.number_input("Service Costs ($):", value=float(selected_log_data["Service Costs"]), step=0.01)
        next_service_due = st.date_input("Next Service Due:", pd.to_datetime(selected_log_data["Next Service Due"]))  # Convert to datetime

        # Update DataFrame with user input
        df.loc[df["Date"] == selected_log_date, "Date"] = date.strftime("%Y/%m/%d")
        df.loc[df["Date"] == date.strftime("%Y/%m/%d"), "Mileage"] = mileage
        df.loc[df["Date"] == date.strftime("%Y/%m/%d"), "Performed Tasks"] = performed_tasks
        df.loc[df["Date"] == date.strftime("%Y/%m/%d"), "Service Costs"] = service_costs
        df.loc[df["Date"] == date.strftime("%Y/%m/%d"), "Next Service Due"] = next_service_due.strftime("%Y/%m/%d")

        # Save DataFrame to Excel file
        save_data(df, file_path)

        # Button to download PDF
        pdf = generate_pdf(selected_log_data)
        st.download_button(label="Download as PDF", data=pdf.output(dest="S").encode("latin-1"), file_name="vehicle_log.pdf", mime="application/pdf")

    # Create new vehicle log button
    if st.sidebar.button("Create New Vehicle Log"):
        new_log_date = st.sidebar.date_input("Enter Log Date:", pd.to_datetime("today"))
        if new_log_date:
            add_new_vehicle_log(new_log_date.strftime("%Y/%m/%d"), 0, "", 0, new_log_date.strftime("%Y/%m/%d"), file_path)
            st.sidebar.success("New vehicle log created successfully!")

            # Reload the app to reflect the changes
            st.rerun()

if __name__ == "__main__":
    main()
