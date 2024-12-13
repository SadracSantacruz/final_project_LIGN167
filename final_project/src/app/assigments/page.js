import styles from "./page.module.css";
import Link from "next/link";

// Fetch assignments from the backend (or Python script)
async function fetchAssignments() {
  const response = await fetch("http://localhost:8000/assignments"); // Adjust the API endpoint
  return response.json();
}

export default async function AssignmentsPage() {
  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Generated PDF Assignment</h1>
      <div className={styles.pdfContainer}>
        <iframe
          src="/scripts/output.pdf"
          width="100%"
          height="800px"
          style={{ border: "none" }}
          title="Generated Assignment PDF"
        ></iframe>
      </div>
    </div>
  );
}
