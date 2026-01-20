# TOPSIS Implementation in Python

**Course:** UCS654 – Predictive Analytics using Statistics  
**Assignment:** Assignment-1 (TOPSIS)  
**Author:** Raj Gupta  
**Roll Number:** 102303324  

---

##  About the Project

This project provides a Python implementation of the  
**TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution)** method.

TOPSIS is a multi-criteria decision-making (MCDM) technique used to rank alternatives based on their distance from the ideal best and ideal worst solutions.

---
Project Website
The TOPSIS project is also deployed as a web application, allowing users to run the TOPSIS method directly through a browser interface.

🔗 Live Website: https://drfcsy7wvrrn5khq5fsgx9.streamlit.app/
---
##  Installation (User Manual)

This package requires **Python 3.7 or higher**.

### Dependencies
- pandas  
- numpy  

Package listed on PyPI:- https://pypi.org/project/topsis-rajgupta-102303324/

Install the package using pip:

```bash
pip install topsis-rajgupta-102303324
```
---

## Usage

Run the following command in the Command Prompt / Terminal:

```bash
topsis <inputFile> <weights> <impacts> <outputFile>
```
 Example

 ```bash 
 topsis sample.csv "1,1,1,1" "+,+,-,+" result.csv

```







