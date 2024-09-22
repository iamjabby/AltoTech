# IoT Infrastructure Deployment for Room Comfort Monitoring

## Overview
This project monitors indoor air quality (IAQ) using a simulated IoT system. Data from sensors is stored in CrateDB, and the system sends alerts to technicians when discomfort conditions are detected.

## Requirements
- Docker and Docker Compose
- CrateDB
- Python 3.x and related dependencies

## Installation

### Step 1: Clone the GitHub repository
1. Open the terminal and run the following command:
    ```bash
    git clone https://github.com/your_repo.git
    cd your_repo
    ```

### Step 2: Build and start the containers using Docker Compose
1. Run the following command to build and start the containers:
    ```bash
    docker-compose up --build
    ```

### Step 3: Check the status of CrateDB
1. Once the containers are running, you can access the CrateDB Admin Console via a browser:
    ```
    http://localhost:4200
    ```

---

### Task 1: Creating Database and Table

1. **Install CrateDB with Docker**:
   - Open the Terminal and run the following command:
     ```bash
     docker-compose up
     ```
   - Verify that CrateDB is running at `localhost:4200` by opening a browser and navigating to this URL.

2. **Create the `raw_data` table in CrateDB**:
   - You can create the `raw_data` table by running the following SQL command in the CrateDB UI:
     ```sql
     CREATE TABLE IF NOT EXISTS raw_data (
         timestamp TIMESTAMP WITH TIME ZONE,
         datetime VARCHAR(32),
         device_id VARCHAR(128),
         datapoint VARCHAR(32),
         value DOUBLE
     );
     ```
   - Verify that the table is created by using the command `DESCRIBE raw_data;` or check the CrateDB UI to ensure that the table has the required columns (`timestamp`, `datetime`, `device_id`, `datapoint`, and `value`).

---

### Task 2: Simulating IoT Devices and Uploading Data

1. **Run the Python Script to Simulate IoT Devices**:
   - Open the Terminal in the folder containing the `Simulation_iot.py` file.
   - Ensure that `mock_iaq_data.csv` is correct and contains the required data.
   - Modify the `Simulation_iot.py` file to ensure it connects to CrateDB correctly (`localhost:5433` or `cratedb:5432` depending on where it is running).
   - Run the following command:
     ```bash
     python Simulation_iot.py
     ```
   - The script will read data from the CSV and upload it to the `raw_data` table in CrateDB every 5 seconds.
   - Check CrateDB to verify that the data is being received by inspecting the `raw_data` table in the CrateDB UI.

---

### Task 3: Data Retrieval and Alerts

1. **Run the `Data-Alerts.py` Script**:
   - Ensure that the required dependencies are installed by running:
     ```bash
     pip install -r requirements.txt
     ```
   - Edit the `docker-compose.yml` file to include the correct LINE Notify Token (in the environment variables section).
   - Run the following command:
     ```bash
     python Data-Alerts.py
     ```
   - This script will check the data in CrateDB every minute to see if the temperature, humidity, or CO2 levels exceed the specified thresholds (23-26°C for temperature, 40-50% for humidity, and CO2 less than 1000 ppm).
   - If any values are out of range, the script will send alerts via LINE Notify.

2. **Verify Notifications**:
   - Check that you receive notifications in LINE when the IAQ data falls outside of the specified comfort range.

---

### Task 4: System Deployment and Scaling

1. **Check Docker and Docker Compose**:
   - Verify that the entire system is deployed using the following command:
     ```bash
     docker-compose up
     ```
   - Check the Docker logs to ensure that all services (`cratedb`, `iot_simulator`, `data_alerts`) are running correctly by using:
     ```bash
     docker-compose logs
     ```
---

### File Descriptions

- `Data-Alerts.py`: A Python script to monitor room comfort and send notifications.
- `Simulation_iot.py`: Simulates IoT devices that send air quality data to CrateDB.
- `docker-compose.yml`: Defines the services for CrateDB, IoT simulator, and data alerts.
- `Dockerfile`, `Dockerfile-alerts`: Docker configuration for building the respective containers.
- `mock_iaq_data.csv`: Simulated sensor data for the IoT system.
- `requirements.txt`: Python dependencies for the project.
