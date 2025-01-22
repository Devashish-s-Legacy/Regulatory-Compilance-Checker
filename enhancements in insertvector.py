import streamlit as st
import pandas as pd
import io

# Helper function to process the blank Excel file and fill data
def process_blank_file(blank_file):
    # Load the blank Excel file into a DataFrame
    try:
        df = pd.read_excel(blank_file, engine='openpyxl')
    except Exception as e:
        st.error(f"Error reading the file: {e}")
        return None

    # Example logic to fill the blank Excel file (replace this with your actual logic)
    # Adding a sample column with filled data
    df['Filled Data'] = ['Sample Data' for _ in range(len(df))]

    return df

# Streamlit app
def main():
    st.title("AI-Powered Regulatory Compliance Checker")

    st.sidebar.header("Upload Options")

    # Option 1: Upload filled Excel file
    st.subheader("Upload Filled Excel File")
    filled_file = st.file_uploader("Upload your filled Excel file", type=['xlsx'])

    if filled_file:
        try:
            filled_df = pd.read_excel(filled_file, engine='openpyxl')
            st.write("Preview of the uploaded filled file:")
            st.dataframe(filled_df)
        except Exception as e:
            st.error(f"Error reading the file: {e}")

    # Option 2: Upload blank Excel file
    st.subheader("Upload Blank Excel File")
    blank_file = st.file_uploader("Upload your blank Excel file", type=['xlsx'], key="blank")

    if blank_file:
        st.write("Processing the blank file...")
        filled_data = process_blank_file(blank_file)

        if filled_data is not None:
            st.write("Preview of the filled file:")
            st.dataframe(filled_data)

            # Download button for the filled file
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                filled_data.to_excel(writer, index=False, sheet_name='Sheet1')
            output.seek(0)

            st.download_button(
                label="Download Filled Excel File",
                data=output,
                file_name="filled_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

if __name__ == "__main__":
    main()
