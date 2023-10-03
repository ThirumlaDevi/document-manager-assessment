import { useState, useEffect } from "react";

import CryptoJS from 'crypto-js';

//400Kb is a dynamodb restriction
// change file size later according to postgres standards
const chunkSize = 1024 * 1024 * 4; // 4Mb ( check braindump section "What must be each chunk size" for the reasoning)

export default function FileUpload() {
  const [counter, setCounter] = useState(1);
  const [fileToBeUpload, setFileToBeUpload] = useState({});
  const [beginingOfTheChunk, setBeginingOfTheChunk] = useState(0);
  const [endOfTheChunk, setEndOfTheChunk] = useState(chunkSize);
  const [chunkID, setChunkID] = useState("");
  const [fileSize, setFileSize] = useState(0);
  const [chunkCount, setChunkCount] = useState(0);

  const [chunkOrderMapping,setChunkOrderMapping] = useState([]);
  //   const [progress, setProgress] = useState(0);

  useEffect(() => {
    if (fileSize > 0) {
      fileUpload(counter);
    }
  }, [fileToBeUpload, endOfTheChunk]);

  const getFileContext = (e) => {
    const _file = e.target.files[0];
    setFileSize(_file.size);
    const _totalCount =
      _file.size % chunkSize == 0
        ? _file.size / chunkSize
        : Math.floor(_file.size / chunkSize) + 1; // Total count of chunks will have been upload to finish the file
    setChunkCount(_totalCount);
    setFileToBeUpload(_file);
    const _fileID = _file.name.split(".").pop();
  };

  const fileUpload = async (counter) => {
    setCounter(counter + 1);
    setChunkOrderMapping([]);
    if (counter <= chunkCount) {
      var chunk = fileToBeUpload.slice(beginingOfTheChunk, endOfTheChunk);
      chunk.hash = CryptoJS.MD5(await chunk.text()).toString(CryptoJS.enc.Hex) ;
      setChunkOrderMapping((prev) => [...prev,{chunk_id : chunk.hash,chunk_order: counter}]);
      uploadChunk(chunk);
    }
  };

  const uploadChunk = async (chunk) => {
    try {
      console.log(chunk);
      const formData = new FormData();
      formData.append('chunk', chunk);
    //   console.log(CryptoJS.MD5(formData).toString());

      console.log(chunk.hash);
       const response = await fetch(
        "http://localhost:8001/api/v1/chunks",
        // "https://mocki.io/v1/eafc15f0-6b1f-443a-a5a5-5b87329a3e41 ",
        {
          headers: {details : JSON.stringify({ userId: 1, orgId: 1, chunkId: chunk.hash }) },
          body:  formData ,
          method: "POST"
        }
      );

      const data = response.data;
      //   if (data.isSuccess) {
      setBeginingOfTheChunk(endOfTheChunk);
      setEndOfTheChunk(endOfTheChunk + chunkSize);
      if (counter == chunkCount) {
        await uploadChunkMapping();
        console.log("Process is complete, counter", counter);
        console.log(chunkOrderMapping);
        alert("File Uploaded Successfully!");
      }
      // } else {
      //   var percentage = (counter / chunkCount) * 100;
      //   setProgress(percentage);
      // // }
      //   } else {
      // console.log("Error Occurred:", data.errorMessage);
      //   }
    } catch (error) {
      console.log("error", error);
    }
  };

    const uploadChunkMapping = async () => {
      const response = await fetch("http://localhost:8001/api/v1/file_versions", {
        method: "POST",
        headers: {
          'Content-Type': 'application/json'
      },
        body: JSON.stringify({
          user_id: 1,
          org_id: 1,
          url: "",
          version_number: 0,
          created_at: new Date(),
          details: chunkOrderMapping,
        }),
      });
    };

  return (
    <div className="file-upload m-2">
      <form>
        <div class="form-group">
            <div className="fs-4">Upload File</div>
          <input
            type="file"
            onChange={getFileContext}
            className="form-control"
            id="fileupload"
            placeholder="Select file"
          />
        </div>
      </form>
    </div>
  );
}
