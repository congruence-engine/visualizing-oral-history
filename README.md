# Visualizing Oral History

## Short summary
Since its origins, Oral History has provided key insights into the human dimension of the past, expanding the variety of individual experiences that can inform the interpretative work of historians and museum curators. And yet, despite recent efforts to digitalize audio recordings, most of the oral history repositories are still not easily accessible, and the discovery, navigation and sense-making of this material is still a challenge. Consequently, the potential contribution of these repositories of human knowledge to enrich historical and museum practice, in a world of increasingly interoperable data, remains limited. 

This investigation explored how AI, in close dialogue with the critical expertise of historians and museum curators, might offer the key to unlocking the knowledge enclosed in oral history archives and enable their connection with heritage collections and other historical sources. The overall aim of the investigation was to explore how recent advancements in Large Language Models (LLMs), speech-to-text and visual analytics can automate parts of the curatorial process, provide an innovative way to access and explore the complexities of recorded life stories, and connect them with museum objects.

This experimental work was developed within three major iterations between July 2022 and December 2024, bringing together an interdisciplinary group of digital heritage researchers, oral historians, museum curators, computer scientists and interaction design specialists. The insights as well as the tools and interfaces developed in the project have shown how a responsible use of Artificial Intelligence can introduce new possibilities not only for the use of oral histories in museums and historical research, but also for envisioning innovative, diverse and creative ways to engage with recorded life stories.

## Research questions

## 1)Overarching question
Can the advancements in Natural Language Processing help to unlock the knowledge enclosed in Oral History archives and connect them with other sources?

## 2)Secondary questions

### First iteration
•	How useful are oral histories in linking heritage collections?

### Second iteration
•	Can we meaningfully deploy Large Language Models (LLMs) with oral history archives?
•	Are new Speech-to-Text tools good enough for automated transcriptions?
•	Can visual analytics enable a different perspective on archives and their curatorial processes?



## People

### First iteration

**Stefania Zardini Lacedelli**: Conceptualization, Methodology, Investigation, Data Curation, Project administration, Visualization, Writing

**Tim Smith**: Investigation, Data Curation, Visualization, Resources

**Simon Popple**: Investigation, Data Curation, Visualization

**Paul Craddock**; Investigation, Data Curation, Visualization

**Maggie Smith**: Resources

**Elizabeth Llabres**: Resources

**John Ashton**: Resources


### Second iteration

**Stef De Sabbata**: Conceptualization, Methodology, Investigation, Data Curation, Formal analysis, Visualization, Software, Writing

**Stefania Zardini Lacedelli**: Conceptualization, Methodology, Investigation, Data Curation, Project administration, Visualization, Writing

**Alex Butterworth**: Methodology, Investigation, Data Curation, Writing

**Andrew Richardson**: Methodology, Investigation

**Colin Hyde**: Resources, Data Curation

**Sally Horrocks**: Data Curation, Validation

**Daniel Belteki**: Investigation, Data Curation

**Neslihan Suzen**: Software

**Felix Needham-Simpson**: Data Curation

**Alison Clague**: Resources

**Julia Ankenbrand**: Resources




## Data sources

### First iteration
### The Saltaire Collection of life stories
A group of stories of living and working in Saltaire, collected, recorded and transcribed by Collection volunteers. For the purpose of the investigation, one transcribed life story was used.

### Bradford Heritage Recording Unit
A major project set up by Bradford Museums, Galleries and Libraries from 1983 to 2006 with the aim of capturing the memories, reflections, contemporary attitudes and images of Bradford people of all ages, classes and races. For the purpose of this investigation, 800 audio interviews (available as digital audio files) were collected, including a consistent corpus of life stories of individuals of European, Asian and Afro Caribbean origins who came to work in the textile industry.

### Second iteration: Mines of Memory
A corpus of 23 mining interviews with mining workers at Snibston and Whitwick collieries, aimed at enhancing the interpretation of the mining collections of the Snibston Museum. Once the museum closed in 2016, the interviews - comprising both digital audio files and digitized transcripts – were made available as part of the East Midlands Oral History Archive. As part of the investigation, the museum collection data was also collected from Leicestershire County Council.

## Investigation methods/ tools/ code/ software (used or developed)

### First iteration: Exploring the connective potential of life stories
Named Entity Recognition, Fuzzy Matching, Manual Annotation, Digital Curatorial Platforms (Omeka and Yarn)

### Second iteration: The Visualizing Oral History pipeline 
Speech to Text (OpenAI Whisper), Topic Modelling (LLM-based), Visual Analytics (Plotly and Dash python libraries)

### Third iteration: Towards an explorable, scalable Data Visualization Interface
Trained Named Entity Extraction, Entity Relation Extraction, SpaCyFishing and QCode Linkage, Geoparsing, Token probability analysis

A full description of each stage of the pipeline (and related code developed) is available in the repository.


## Outputs


### First iteration
Two digital narratives were created on two digital platforms – Omeka and Yarn – with the aim to visualize the connections with museum objects, historical sources and online repositories which are enclosed in a life story. 

### Second iteration
A proof-of-concept interactive dashboard which allows users to explore a web of automatic-generated topics from the Mines of Memory and visualize the connections of specific sections of the interviews with museum objects from the Snibston Museum. In a first visualization, the interviews are represented as bars, each splitted into one section per paragraph. Clicking on a bar section activates a side section where the transcription and a suggested matched object from the museum collection is shown. In a second visualization, the sentences are represented as dots, which are arranged on the screen based on their similarity, thus allowing the user to manually identify interesting groupings.


  
## Licence 
This work is licensed under a [Creative Commons Attribution 4.0 License - CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

