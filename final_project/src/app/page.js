"use client";

import styles from "./page.module.css";
import Link from "next/link";
import { useState } from "react";
import Image from "next/image";
import backgroundImage from "../../public/classroom.jpg";

export default function HomePage() {
  const [prompt, setPrompt] = useState("");
  const [responseMessage, setResponseMessage] = useState(null);
  const [pdfGenerated, setPdfGenerated] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      console.log("Sending query to backend:", prompt);

      // Trigger the Python script
      const response = await fetch("http://localhost:8000/run-script", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query: prompt }),
      });

      if (!response.ok) {
        console.error(
          "Failed to execute script. Response status:",
          response.status
        );
        throw new Error("Failed to execute script");
      }

      const data = await response.json();
      console.log("Backend response:", data);

      setPdfGenerated(true); // Mark PDF as generated
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <div
      style={{
        backgroundImage: `url('/classroom.jpg')`, // Use the public path here
        backgroundSize: "cover",
        backgroundPosition: "center",
        height: "100vh", // Ensure full page height
      }}
      className={styles.container}
    >
      <h1 className={styles.title}>Assignment Generator</h1>

      <div className={styles.mainContent}>
        {/* Images Section */}
        <div className={styles.imagesSection}>
          <div className={styles.imageCard}>
            <Image
              src="/image.png"
              width={250}
              height={250}
              alt="Picture of a happy professor holding a gift"
              className={styles.image}
            />
            <p>
              Our model analyzes assignment topics to generate creative tasks.
              Transform input ideas into structured assignments. Generate
              personalized PDFs for educational purposes.
            </p>
            <br></br>
            <p>
              <b>Side note: </b>
              This version of our project can only retrieve DSC 20 (Data Science
              20) Assignments.
            </p>
          </div>
        </div>

        {/* Form Section */}
        <div className={styles.formSection}>
          <form onSubmit={handleSubmit} className={styles.form}>
            <textarea
              className={styles.textarea}
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="Enter your topic or idea for an assignment"
              required
            />
            <button type="submit" className={styles.generateButton}>
              Generate
            </button>
          </form>

          {responseMessage && (
            <div className={styles.response}>
              <h2>AI-Generated Assignment:</h2>
              <p>{responseMessage}</p>
            </div>
          )}

          {pdfGenerated && (
            <a
              href="http://localhost:8000/public/output.pdf"
              target="_blank"
              rel="noopener noreferrer"
            >
              <button className={styles.viewButton}>View Generated PDF</button>
            </a>
          )}
        </div>
      </div>
    </div>
  );
}
