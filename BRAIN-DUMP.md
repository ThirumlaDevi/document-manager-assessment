### Issues planned to tackle and how?
#### How to not make the uploading of the whole file everytime, even though it's just revisions of the same file?
  
  _Reason : everytime pushing whole file uses a whole lot of cloud storage space and request bandwidth_ 
  
_**File chunking process on file upload**_
  1. Check if file is more than 400Kb

  2. If yes, then divide it into 400Kb chunks

    Note: initially these file size limits were decided with respect to the dynamodb S3 size limits
  
  3. Create a unique identifier for the file chunk to user unique identifier
      - Reason being : if same hash function is used to uniquely identify same file alone but for different users, then that might cause a issue.

  4. For each chunk, check if chunkid already exists

  5. If not, upload each chunk to an external blob storage, identified by the unique chunk id either through an sdk or server

    Note: efficiently spawning threads to do process 4 and 5 will make the process much faster

  6. Generate a metadata on the stored file with the user, file id, revision, url location, list of chunk information (each having chunk order & chunk id info ) metastore

    Note: on new file upload, make sure to update the cache of file name, user name and revison version with newest revision number

#### How to make upload faster
  - The meta data file that has information on chunk index

**Metadata file as source of truth for revision**_
  1. Check if latest file revision information exisits in cache(assume redis cache for time being).
      
      1.1 Update the cache with this information

  2.  Get the revision of file form the file metadata store db

  3. Then make the file chunking process checks, only chunkids that have been changed is uploaded.

_Note: Since metadata file acts as source of truth for file this information needs to be stored in a consistent db. Hence, RDBMS must be preferred_

#### How to serve/download data at scale?

One good thing on get if revision number is not given, latest revision number is taken from cache

ACTUALLY NEED TO CHECK HOW TO COMBINE CHUNKS ON ACCESS/DOWNLOAD
#### How to make querying faster in metadastore
Introducing indexing on filename to username

### Issues not tackled
- Not making a backup for the data storage or any sort of disaster recovery was simulated in the local development
- when meta data store is filled, horizontal addition of datastore is required
  - sharding of data within metadata store is not done for now
- Caching for metadata store as everytime to get data we query the datastore
- Caching for the chunks itself
 - What needs to be cached is a complete another logic to tackle 
- All of the chunking logic makes the frontend heavy. However moving it to backend just consumes more bandwidth especially if big files needs to be transferred to backend. 
  - The metadata file generation logic needs to be tackled before moving part of chunking logic to backend.
  - Post this how to make upload happen with less bandwidth (chunking can happen in frontend itself and send information on how many more chunks on the same to be expected) 
- The current build is assumed as if all services are up