
# Connecting Google BigQuery to Grafana Cloud

## Step 1: Prepare Google Cloud Project

### At Service Account
**Assign the following roles**:
    `BigQuery Data Viewer` and `BigQuery Job User`

### Create and Download a Key

1. Go to the **"Keys"** tab.
2. Click **“Add Key → Create new key”**.
3. Select **JSON** and download the `.json` key file.
4. Save this to upload to Grafana Cloud later.

## Step 2: Enable Required APIs

### Required APIs

    BigQuery API                                
    BigQuery Storage API 
    Cloud Resource Manager API

### Enable via Console

Visit and enable each of the following:
- https://console.cloud.google.com/marketplace/product/google/bigquery.googleapis.com
- https://console.cloud.google.com/marketplace/product/google/bigquerystorage.googleapis.com
- https://console.cloud.google.com/marketplace/product/google/cloudresourcemanager.googleapis.com


---

## Step 3: Configure Grafana Cloud

1. Log into your Grafana Cloud instance.
2. Go to **Connections → Data Sources**.
3. Click **"Add data source"**, search for **BigQuery**, and select it.
4. Upload the JSON key file.
5. Click **"Save & Test"**.

---

### Now the datasource is ready and from that, we can now build dashboards and panels in Grafana using SQL queries directly on BigQuery.
