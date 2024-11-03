# Ask the Paper [draft]

## Project Description
"Ask the Paper" is an intuitive platform designed for organizations, teams, and researchers to analyze and query their research materials. The project transforms interaction with text documents by enabling users to ask direct questions and receive insightful answers based on the content of those documents.

## Table of Contents
- [Features](#features)
- [Project Roles](#project-roles)
- [Functionality](#functionality)
- [User Interface](#user-interface)
- [Technical Architecture](#technical-architecture)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features
- Document upload and processing for indexed text chunking.
- Semantic query handling utilizing advanced machine learning models.
- Conversational user experience for easy interaction with research materials.

## Project Roles
The system comprises two primary roles:

### Admin Role
The Admin is responsible for managing the research materials uploaded to the platform with the following functions:
- **Uploading Documents**: Upload research papers or text materials in PDF format.
- **Data Processing**: Process uploaded PDFs to extract text and divide it into manageable chunks.
- **Storage Management**: Store extracted text in FAISS and PKL formats for efficient retrieval and store files in Amazon S3.

### User Role
Users interact with the system through a user-friendly interface:
- **File Access**: Check the S3 bucket for FAISS and PKL file availability.
- **Questioning Interface**: Ask questions related to the content of the research papers.
- **Conversational Experience**: Engage in a natural conversation to retrieve information.

## Functionality
- **Document Upload and Processing**: Upload research papers for conversion into indexed text chunks.
- **Query Handling and Retrieval**: Use Amazon Titan text embedding model for understanding and analyzing queries, utilizing FAISS for quick retrieval.
- **Interactive User Interface**: A web interface built using Streamlit for document upload and real-time responses.

## User Interface
The user interface is designed with simplicity and functionality:
- **Upload Section**: An area for admins to upload PDF files.
- **Query Input Field**: Users can type their questions for easy interaction.
- **Response Display**: Clear presentation of answers for quick understanding.

## Technical Architecture
The architecture leverages various AWS tools and modern machine learning techniques for efficient document processing, storage, and retrieval. Key components include data flow, service integration, and overall system design.

## Technologies Used
- **Amazon S3**: For storing uploaded documents and processed files.
- **Amazon Bedrock**: Access to pre-trained language models for text processing.
- **FAISS**: Efficient similarity search among embedded text chunks.
- **Langchain**: Document handling and text chunking.
- **Boto3**: AWS SDK for Python for interactions with AWS services.

## Installation
To set up the project, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/nimish-nimishmittal/ask-the-paper.git
   cd ask-the-paper
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure your AWS credentials:
   Ensure you have your AWS credentials configured. You can do this using the AWS CLI:
   ```bash
   aws configure
   ```

## Usage
1. Start the application:
   ```bash
   streamlit run app.py
   ```

2. Access the web interface through your browser (usually at `http://localhost:8501`).

3. Admins can upload documents, and users can ask questions through the interface.

## Contributing
Contributions are welcome! If you have suggestions for improvements or want to report a bug, please open an issue or submit a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

For further information, please refer to the documentation or contact the project maintainers.
```

Feel free to adjust any sections to better fit your project's specifics, such as the repository link or any additional instructions you might have!
