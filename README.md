# Formula 1 Data Semantic Modeling

## Project Overview

This project, part of the "Knowledge and Data Engineering" course at Utrecht University, demonstrates the practical application of Semantic Web technologies. It involves the conversion of Formula 1 datasets (CSV files) into RDF triples, utilizing data from Kaggle and incorporating it into a semantic framework using Blazegraph.

## Goals and Objectives

The aim is to use Semantic Web technologies to enhance data integration and interoperability within the domain of motor sports, particularly Formula 1. By transforming structured data into RDF, I created a semantically enriched data model that facilitates advanced data querying and knowledge extraction.

## Methodology

- Reviewed the `student_project_details.pdf` for comprehensive understanding of the project requirements.  
- Downloaded structured [Formula 1 datasets from Kaggle](https://www.kaggle.com/datasets/rohanrao/formula-1-world-championship-1950-2020).
- Transformed CSV data into RDF triples using Python scripts detailed in `project1.ipynb`.
- Uploaded the resulting RDF data (`f1_data.rdf`) to Blazegraph, a powerful triplestore.
- Developed an interactive user interface with HTML and JavaScript that sends SPARQL queries to Blazegraph and displays the results.

## Project Structure

- `server.js`:  This is the main server script for the application. It is responsible for setting up an Express.js server that serves static files from a specified directory. It also sets up a proxy middleware for handling requests to a Blazegraph instance. The script configures the server to listen on a specific port and logs a message when the server is running. The proxy middleware is configured to rewrite paths for requests to the Blazegraph namespace and to add CORS headers to the responses. The server is designed to handle SPARQL queries sent to the Blazegraph instance.
- `index.html` & `index.js`: Frontend files for the web-based user interface.
- `f1_data.rdf`: The RDF data file containing semantically modeled Formula 1 data.
- `main.py`: This Python script, which mirrors the `project1.ipynb` file, is designed for general use. It is responsible for transforming data into semantically rich RDF triples. It serves as a convenient alternative to the Jupyter notebook for users who prefer working with standalone scripts.

## Installation and Usage

1. Clone the repository:
- git clone https://github.com/masoud112229/Formula1_web_semantic.git

2. Set up Blazegraph and load the RDF data:
 - Follow the instructions from Blazegraph to upload the `f1_data.rdf` file.
3. Start Blazegraph:
 - Open the command prompt and navigate to the directory where `Blazegraph.jar` is located.
 - Run the following command to start Blazegraph:

    ```bash 
    java -server -Xmx4g -jar blazegraph.jar
    ```

4. Launch the Node Server:
 - In the command prompt, navigate to the project directory.
 - Run the following command to start the Node server:

    ```bash 
    node server.js
    ```

4. Open `index.html` in a web browser to interact with the user interface.

## Semantic Web Technologies Utilization

- RDF Schema and OWL for ontological axioms.
- SPARQL queries for data retrieval and manipulation.
- Data integration with external sources like DBpedia and Wikidata.

## Challenges and Future Prospects

This section includes reflections on the challenges of Semantic Web, its future in the era of generative AI, and the impact on data modeling efficiency.

## Acknowledgements

Special thanks to the instructor of the "Knowledge and Data Engineering" course at Utrecht University for providing guidance and resources throughout this project.

## License

This project is licensed under the terms of the [MIT License](LICENSE).

## Contact

For inquiries or further collaboration, feel free to contact me at [masoud.aghayan@students.uu.nl](mailto:masoud.aghayan@students.uu.nl) or [masoud.aghayan64@gmail.com](mailto:masoud.aghayan64@gmail.com).

---

_Masoud Aghayan_

