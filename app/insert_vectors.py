# %%

from datetime import datetime

import pandas as pd
from database.vector_store import VectorStore
from timescale_vector.client import uuid_from_time

# Initialize VectorStore
vec = VectorStore()

# Read the CSV file
# df = pd.read_csv("../data/faq_dataset.csv", sep=";")
df = pd.read_excel("../data/Datasets_R.xlsx")
df.head()


# Prepare data for insertion
def prepare_record(row):
    """Prepare a record for insertion into the vector store.

    This function creates a record with a UUID version 1 as the ID, which captures
    the current time or a specified time.

    Note:
        - By default, this function uses the current time for the UUID.
        - To use a specific time:
          1. Import the datetime module.
          2. Create a datetime object for your desired time.
          3. Use uuid_from_time(your_datetime) instead of uuid_from_time(datetime.now()).

        Example:
            from datetime import datetime
            specific_time = datetime(2023, 1, 1, 12, 0, 0)
            id = str(uuid_from_time(specific_time))

        This is useful when your content already has an associated datetime.
    """
    # content=f"Category: {row['Category']}\nJob Description: {row['Job Description']}\nAcceptance: {row['Acceptances']}\nResume: {row['Resume']}"
    content = f"JD NAME: {row['JD NAME']}\nJob Description: {row['JD']}\nRESUME: {row['RESUME']}\nInterview_Details: {row['Q AND A']}"
    # content = f"Question: {row['question']}\nAnswer: {row['answer']}"
    embedding_1 = vec.get_embedding(content)
    return pd.Series(
        {
            "id": str(uuid_from_time(datetime.now())),
            "metadata": {
                "Acceptance":row['TAG'],
                # "Laws" : row['Laws'],
                "Category": row["JD NAME"],
                "created_at": datetime.now().isoformat(),
            },
            "contents": content,
            "embedding": embedding_1,
        }
    )


records_df = df.apply(prepare_record, axis=1)

# Create tables and insert data
vec.create_tables()
vec.create_index()  # DiskAnnIndex
vec.upsert(records_df)

# %%
