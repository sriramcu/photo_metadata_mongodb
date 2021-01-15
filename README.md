# photo_metadata_mongodb
Store and retrieve images from MongoDB using GridFS and exif metadata.


### Usage

#### Step 1

Install requirements:  
`pip install -r requirements.txt`

#### Step 2  
Get your Atlas-MongoDB connection string by following the steps on the website.

#### Step 3
Run the program:  
`python3 driver.py <connection_string>`  
**or**  
`python3 driver.py "$(< file.txt)"`  
Where file.txt contains the connection string.
