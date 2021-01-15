# photo_metadata_mongodb
Store and retrieve images from MongoDB using GridFS and exif metadata.


### Usage
#### Step 1
`git clone https://github.com/sriramcu/photo_metadata_mongodb`  

#### Step 2

Install requirements:  
`pip install -r requirements.txt`

#### Step 3  
Get your Atlas-MongoDB connection string by following [these](https://docs.mongodb.com/guides/cloud/connectionstring/) steps on the website.

#### Step 4
Run the program:  
`python3 driver.py <connection_string>`  
**or**  
`python3 driver.py "$(< file.txt)"`  
Where file.txt contains the connection string.
