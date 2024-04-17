# Formula 1 Data Semantic Modeling

## Project Overview

This project, part of the "Knowledge and Data Engineering" course at Utrecht University, demonstrates the practical application of Semantic Web technologies. It involves the conversion of Formula 1 datasets into RDF triples, utilizing data from Kaggle and incorporating it into a semantic framework using Blazegraph.

## Goals and Objectives

The aim is to leverage Semantic Web technologies to enhance data integration and interoperability within the domain of motor sports, particularly Formula 1. By transforming structured data into RDF, we create a semantically enriched data model that facilitates advanced data querying and knowledge extraction.

## Methodology

- Downloaded structured Formula 1 datasets from Kaggle.
- Transformed CSV data into RDF triples using Python scripts detailed in `project1.ipynb`.
- Uploaded the resulting RDF data (`f1_data.rdf`) to Blazegraph, a powerful triplestore.
- Developed an interactive user interface with HTML and JavaScript that sends SPARQL queries to Blazegraph and displays the results.

## Project Structure

- `main.py`: Python backend for handling server requests and SPARQL queries.
- `index.html` & `index.js`: Frontend files for the web-based user interface.
- `f1_data.rdf`: The RDF data file containing semantically modeled Formula 1 data.

## Installation and Usage

1. Clone the repository:
- git clone https://github.com/masoud112229/Formula1_web_semantic.git

2. Set up Blazegraph and load the RDF data:
- Follow the instructions from Blazegraph to upload the `f1_data.rdf` file.
3. Run the Python server:
- python main.py

4. Open `index.html` in a web browser to interact with the user interface.

## Semantic Web Technologies Utilization

- RDF Schema and OWL for ontological axioms.
- SPARQL queries for data retrieval and manipulation.
- Data integration with external sources like DBpedia and Wikidata.

## Challenges and Future Prospects

This section includes reflections on the challenges of Semantic Web, its future in the era of generative AI, and the impact on data modeling efficiency.

## Acknowledgements

Special thanks to the instructors and contributors of the "Knowledge and Data Engineering" course at Utrecht University for providing guidance and resources throughout this project.

## License

This project is licensed under the terms of the [MIT License](LICENSE).

## Contact

For inquiries or further collaboration, feel free to contact me at [masoud.aghayan@students.uu.nl](mailto:masoud.aghayan@students.uu.nl).

---

_Masoud Aghayan_

