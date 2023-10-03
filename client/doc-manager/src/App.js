import "./App.css";
import FileVersions from "./FileVersions";
import FileUpload from "./FileUpload";

import "bootstrap/dist/css/bootstrap.css";

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <FileUpload />
        <hr/>
        <FileVersions />
      </header>
    </div>
  );
}

export default App;
