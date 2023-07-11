# Markov Chain Text Generator

This was a final project for my "Analysis of Algorithms" Class. This Python script generates random sentences using a Markov chain based on input files. It leverages Markov matrices to analyze word sequences and generate random semi-coherent sentences. The script provides options to generate random sentences, run tests, and perform time tests.

## Features

- Markov matrix generation: The script creates a Markov matrix from some open source input files from the web, capturing word sequences and their probabilities.
- Random sentence generation: Using the Markov matrix, the script generates random sentences by selecting the next word based on the probabilities.
- Tests: The script includes tests to verify the correctness of regular expressions, Markov matrix generation, sentence generation, and file combination functionality.
- Time tests: The script provides timing measurements for Markov matrix creation and the generation of a large number of random sentences.

## Usage

1. To generate random sentences, select option 1 in the menu.
2. To run tests, select option 2 in the menu.
3. To perform time tests, select option 3 in the menu.
4. Enter 'q' to exit the program.

## Input Files

The input files should be placed in the `inputFiles` directory. Each file will contribute to the Markov matrix generation, allowing the generator to produce more diverse sentences.

## Requirements

- Python 3.x

## Running the Script

Execute the script by running the command:

``` python
python Markov_Chain.py
```
