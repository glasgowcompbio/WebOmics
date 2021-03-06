GraphOmics is a dashboard to integrate and explore different types of biological -omics data. 
Using this tool, you can map transcriptomics, proteomics and metabolomics data onto metabolic pathways. 
GraphOmics uses [Reactome](https://reactome.org/) as the knowledge base to map entities across different omics.
Methods to rank pathway and highlight interesting connection are also included.

**Live demo is available at [https://graphomics.glasgowcompbio.org/app/](https://graphomics.glasgowcompbio.org/app/)**

**A Python package to perform multi-omics data linking and analysis is available at [https://github.com/glasgowcompbio/pyMultiOmics](https://github.com/glasgowcompbio/pyMultiOmics)**. This is the same code used in this Web application but available for stand-alone use in your own application.

**Manuscript pre-print: [bioarxiv](https://www.biorxiv.org/content/10.1101/2021.06.24.449741v1.abstract) -- prepared for submission to BMC Bioinformatics.**

## How to install?

Refer to the [setup guide](setup_guide.md).

**Requirement**:
- Django 2.0/Python and rpy for backend.
- A local Reactome installation.
- The usual scientific python stack (Numpy/Scipy/Pandas) for analysis and running the notebooks (optional).

## Usage

The **Data Browser** tab shows all the interconnected transcripts, proteins, metabolites, reactions and pathways in your data, alongside their fold-change measurements colour-coded by their p-value significance.

![Data Explorer](graphomics/images/screenshot1.PNG?raw=true "Data Explorer")

For **interactive heatmap visualisation**, GraphOmics uses [Clustergrammer](https://amp.pharm.mssm.edu/clustergrammer/), a web-based tool for visualizing and analyzing high-dimensional data as interactive clustered heatmaps.
The heatmap is linked to the Data Browser such that anything that is clicked on one will also be selected on the other.
A cluster can also be selected from the heatmap in Clustergrammer and be used to create selection group for further analysis in GraphOmics.

![Heatmap](graphomics/images/screenshot2.PNG?raw=true "Heatmap")

A **selection group** can be created from the Data Browser or the Clustergrammer heatmap for further analysis. At the moment, users can create a boxplot or perform gene ontology analysis on a group.

![Group Analysis](graphomics/images/screenshot3.PNG?raw=true "Group Analysis")

Finally the **Inference** tab allows user to create and set-up various statistical inference such as DEseq2, t-test, PCA and pathway ranking analysis.

![Inference](graphomics/images/screenshot4.PNG?raw=true "Inference")

## Pathway Analysis

The pathway analysis functionalities used in GraphOmics have been separated into a stand-alone Python library **PALS** that can be used outside this project. This includes pathway analysis using ORA, GSEA and PLAGE on transcripts (Ensembl ID), proteins (UniProt ID)
and compound (KEGG or ChEBI IDs) from the Reactome or KEGG database. For more details, please refer to [PALS](http://pals.glasgowcompbio.org)

Integrated analysis spanning multiple omics data is also possible through [Reactome Analysis Service](https://reactome.org/dev/analysis).

## Other functionalities

Gene Ontology Analysis, PCA, heatmaps and various other plots can also be generated from GraphOmics.
