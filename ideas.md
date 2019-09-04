# Arguing-agents

## Ideas

- Reddit argument extraction paper (https://nestor.rug.nl/bbcswebdav/pid-9563801-dt-content-rid-19030112_2/courses/KIM.AA08.2019-2020.1A/exampleProjectReport3.pdf)
- Replace LSTM w/ different classification algorithm
- Extract and Split arguments for and against
- Extract requests for clarifications and clarifications from replies
- Pros and Cons extraction from procon.org
- Detect rhetorical questions in order to improve the performance of the existing model

### Improvements for existing solution

- Use word equivalences/explanations extracted from Wiktionary in a bag of words approach
- Detect rhetorical questions in order to improve the performance of the existing model

- Replace LTSM w/ different classification algorithm
- Extract requests for clarifications and clarifications from replies

### Extensions for visualization 

- Pros and Cons extraction from procon.org

- Extract and split arguments for and against

## Planning

1. Focus on Argument extraction
2. Implement LSTM
3. Figure out how they use Corpus
4. Scrape reddit arguments
5. Scrape procon arguments
6. Divide arguments into pros and cons from reddit and compile list
7. Compare pros and cons found by solution on reddit w/ pros and cons from procon