## Analyzing and managing traffic in 5G wireless networks

### Description of the project

The beyond fifth generation (5G) wireless networks necessitates the understanding of the traffic dynamics and has already attracted significant research attention. By understanding the traffic, we can facilitate traffic predictions, detections of changes and anomalies in Radio Access Networks (RANs), which can improve resource utilization. Namely, we can achieve a more optimized use of network resources concerning energy, cost and also a better user service.

In this project, we aim to investigate techniques that can analyze and manage such traffic datasets (as to predict traffic, detect anomalies, etc.). This is a challenging task since our datasets consist of data streams of ultra-high volume, velocity, and variety. For this purpose, we will focus on feasible and efficient techniques towards analysis and management of such data and we will investigate tailored techniques that can summarize such data.

### Project Implementation - Overview
The project is organized under 3 different main axes:
1. Data Synopsis Methods
	* Sampling
		* Reservoir
		* Concise
		* StreamSamp
	* Equi-depth histograms
2. Change Detection
3. Implementation in Azure

### Repository Structure
* sampling notebooks: Main notebooks used for the project.
	* clustering_validation_jenks_method: Apply and validate jenks method in concise sampling
	* equi_depth_histograms: Implementation of equi-depth histograms
	* data_exploration: Basic investigation of the dataset 
	* traffic_simulation: Implementation of stream simulator.
	* change_detection: Implementation of change detection method.

* send_receive_code: Python scripts for sending the data in a streaming format to an Azure Event Hub.
* concise_sampling_trigger: Implementation of concise sampling as an Azure Function. The function is triggered when there are incoming records at the Azure Event Hub.
* blob_storage: Python script for downloading the blobs created after the concise sampling in the Azure Blob Storage.
* scientific_papers_and_books_used: Literature used for the project.
* host.json: Configuration file for Azure Event Hub.
* requirements.txt: Libraries required for the Azure Function.

### Dataset
Due to size limitations, the dataset is not included in the repository and can be found [here](https://drive.google.com/file/d/1DIRWTjKaOgFzOdl33rxezloYSQQAel10/view?usp=share_link).