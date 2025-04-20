
#URL: https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet
#Ingest all data for a given year 
#

import requests
import sys
from google.cloud import storage

def download_parquet_file(url, file_name): 
    print(f"Attempting to download {url}")
    try:
        response = requests.get(url, stream=True)
        if response.status_code==200:
            with open(file_name, 'wb') as f: 
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"Successfully downloaded {file_name}")
            return True
        elif response.status_code==404:
            print(f"file not found 404 at {url}. skipping")
            return False
        else:
            response.raise_for_status()
            print(f"downloaded {file_name}(unexpected status { respone.status_code})")
            return False
    except requests.exceptions.RequestException as e:
        print(f"error downloading {url}: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occured while processing {url}: {e}")
        return False

def upload_to_gcs(bucket_name, file_name, gcs_blob_name):
    
    storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024  # 5 MB
    storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(gcs_blob_name)
    blob.upload_from_filename(file_name)
    print(f"Uploaded {file_name} to gs://{bucket_name}/{gcs_blob_name}")
    
def main():
    dataset_name = "yellow_tripdata"
    dataset_year = "2024"
    bucket_name = "de-learning-project-bucket"
    

    
    print(f"Starting download process for {dataset_name} in {dataset_year}")

    for month_number in range(1,13):
        month_string = f"{month_number:02d}"

        url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/{dataset_name}_{dataset_year}-{month_string}.parquet"
        file_name = f"{dataset_name}_{dataset_year}-{month_string}.parquet"
        downloaded = download_parquet_file(url, file_name)

        if downloaded: 
            gcs_blob_name = f"{dataset_year}/{file_name}"
            upload_to_gcs(bucket_name, file_name, gcs_blob_name)
    print("Upload Complete")
    

    
    


if __name__ == "__main__":
    main()

    