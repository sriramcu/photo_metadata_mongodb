# photo_metadata_mongodb
Store and retrieve images from MongoDB using GridFS and exif metadata.


### Usage
#### Step 1
`git clone https://github.com/sriramcu/photo_metadata_mongodb`  

#### Step 2

Install requirements:  
`pip install -r requirements.txt`

#### Step 3  
Get your Atlas-MongoDB connection string by following the steps on the website. Modify lines 24,26,27 in driver.py to match the values entered by you when creating your cluster.

#### Step 4
Run the program:  
`python3 driver.py <connection_string>`  
**or**  
`python3 driver.py "$(< file.txt)"`  
Where file.txt contains the connection string.
