# RAG Application

This is a RAG (Retrieval-Augmented Generation) application built using NextJS and NodeJS for the frontend and backend, with Python handling the RAG execution and OpenAI API integration.

## Prerequisites

Before setting up the application, ensure you have the following:

1. **Node.js**: You can download and install Node.js from [nodejs.org](https://nodejs.org/en). After installation, restart your computer to ensure all files are correctly installed.
2. **OpenAI API Key**: Obtain your API key from OpenAI.

## Setup Instructions

### 1. Clone or Fork the Repository
First, commit to the repository and then clone or fork it to your local machine:
```bash
git clone <repository_url>
```

### 2. Add OpenAI API Key
Navigate to the `scripts` folder and locate the `sk.py` file. Paste your OpenAI API key into this file to enable the application to communicate with the OpenAI API.

### 3. Install Node.js Dependencies
Navigate to the project directory and install the necessary Node.js packages:
```bash
npm install
```

### 4. Start the Application

Open two terminals and execute the following commands:

#### Terminal 1:
```bash
node server.js
```
This starts the backend server.

#### Terminal 2:
```bash
npm run dev
```
This starts the Next.js development server.

### 5. Access the Application
Once both servers are running, the application should be available locally. Open your browser and navigate to:
```
http://localhost:3000
```

## Notes
- Ensure you have all dependencies installed before starting the application.
- Make sure the API key is correctly set up in the `sk.py` file.
- Restart your computer after installing Node.js to avoid any potential issues with the environment setup.

Enjoy using the RAG application!

