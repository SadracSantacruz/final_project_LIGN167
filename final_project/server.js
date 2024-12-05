const express = require("express");
const { exec } = require("child_process");
const path = require("path");
const cors = require("cors"); // Import the CORS package

const app = express();
app.use(cors()); // Enable CORS for all origins
app.use(express.json());

// Health check endpoint
app.get("/", (req, res) => {
  res.send("Server is running");
});

// Endpoint to run the Python script
app.post("/run-script", (req, res) => {
  const query = req.body.query;

  console.log("Received query:", query);

  if (!query || typeof query !== "string" || query.trim() === "") {
    console.error("Invalid query received");
    return res.status(400).json({ error: "Query must be a non-empty string" });
  }

  const env = { ...process.env, QUERY: query };
  const scriptPath = path.resolve(__dirname, "src/scripts/main.py");

  console.log("Running script with query:", query);
  const pythonPath = "/Users/sadrac/miniforge3/bin/python"; // Replace this path if different

  exec(
    `${pythonPath} /Users/sadrac/Documents/classes/LIGN167/final_project_LIGN167/final_project/src/scripts/main.py`,
    { env },
    (error, stdout, stderr) => {
      if (error) {
        console.error(`Error: ${error.message}`);
        console.error(`Stderr: ${stderr}`);
        return res.status(500).json({
          error: "Failed to execute script",
          details: error.message,
          stderr,
        });
      }
      if (stderr) {
        console.error(`Stderr: ${stderr}`);
      }
      console.log(`Stdout: ${stdout}`);
      res.json({ message: "Script executed successfully", output: stdout });
    }
  );
});

// Serve the PDF
app.use("/public", express.static(path.join(__dirname, "src/scripts")));

// Start the server
const PORT = 8000;
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
