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
5. Determine polarity of arguments
6. Scrape procon arguments
7. Divide arguments into pros and cons from reddit and compile list
8. Compare pros and cons found by solution on reddit w/ pros and cons from procon

### Feedback

Search for argumentation mining papers + other website apart from reddit.

Keep it simple.

Concretely define the approach

## Steps

### Reddit data extraction https://www.reddit.com/r/changemyview

1. Install PRAW API
2. Learn PRAW API
3. Extract X amount of posts
4. Detect sentences and deltas.
5. Determine quality of arguments. (corpus + LSTM)
6. Determine the polarity of arguments (how to test their polarity? should be known prior to it: It's fine to just have two lists)

Extract subject from reddit post. Insert subject to procon. Extract words from both pros and cons from Procon and use said words to determine polairty of a sentence on reddit.



## Proposal

The prime goal of our assignment is to be able to extract arguments from a Reddit board called [ChangeMyView](https://www.reddit.com/r/changemyview/). In this subreddit, a person submits their view on a particular topic and people reply to them in natural language in an attempt to convince them to change their stance. The idea is based on two papers and a project given as an example on Nestor. In their example, an LSTM neural network coupled with a Corpus is used in order to determine whether sentences are arguments and establish the quality of the arguments. 

### What is the problem addressed?

The purpose of the project is to achieve argument extraction and classification into Pros and Cons from natural language. Typically, websites that classify arguments into pros and cons use structured essays to gather their data. Whilst these arguments are valid, they are extracted by users who carefully analyze structured text. Extracting arguments from an online discussion poses a much more difficult task, since the text is usually unstructured and features an abundance of language nuances and subtleties, rhetorical questions and implications to name a few.  

The source for our argument extraction task comes from Reddit, a website on which people can create posts on an array of topics. The website is segmented into different `subreddits`, each one having a certain topic. 
One such subreddit, named `changemyview`, consists of an original poster (OP) who posts his view on a particular topic. People may then post comments in an attempt to convince the OP to change his original stance of the topic. Although comments towards the OP's address are usually  counter-arguments to their view, people may defend the view of the OP by replying to comments attacking it. This results in an environment in which both pro and against arguments are formed on a particular view in a natural way, and it is the extraction of these arguments that is of interest to this project.

### What is the state of the art concerning this problem?

Argument extraction from unstructured texts has been attempted before and serves as a key inspiration for our project. The idea came from a project created in the scope of this course which attempted to extract arguments from the same subreddit and judge the quality of the arguments. The project used Long-short term memory neural networks to learn and determine whether sentences were arguments. Moreover, a corpus was used that contained annotations describing different language features, such as the quality of an argument. In such an approach, the results show a good performance in terms of distinguishing between argumentative and non-argumentative sentences.