# I WROTE EVERYTHING - NO AI WAS USED IN THE CODING OF THIS PROJECT

Pathway of things to do from scratch:

## AI Part of it:

### Core processing
- Choose the correct model, choices of model to choose from:
    - `qwen2.5:14b-instruct-q4_K_M` - it is faster than qwen3 as it takes up lesser space but it is not as smart and runs out of context very fast 
    - `qwen3:14b` - it is way slower - but it is a very good model - I can try to find more optimised versions of it - might have to run GGUF instead of Ollama
        - Can try VLMM's memory quant and use that to host this locally
        - Can try the q4_K_M
- I need to get the model up and running, configure via VLLM / Ollama / etc - plug it up with langchain
    - Use the most updated version of langchain, no deprecared versioning
    - Make a slot to place prompt templates - read from JSON / txt
- Set up a basic RAG
    - Make sure to keep it as precise + modular + as efficient as possible
    - Add end points for document upload as well reading text, tables, all that as well different types of files
    - optimise chunking
    - use optimised retreivers and rerankers
- Set up proper Chain Of Thought logic and implementation
- Integrate Web Search (DDGS) into the RAG as well as the LLM
- temp VDB to be used for normal calls:
    - see if it's possible for a temp VDB to be made for longer context conversations without breaking the back of the model
        - try using async alongside inference so that the user never knows about it
            - backend endpoints will be useful here
- Agents
    - Add a place to add agents into the loop
    - Have a few pre-fixed agentic routes / lanes for the user to select based on their use-case
        - Allow customisation for this (B.AI)

### Security
- Add custom input and output guardrails
    - use a pre-trained model (I will train it) to see if the input it malicious or not (_Recommended_)
        - see what exists in the market currently and if there's an industry standard for it
            - if not - make it + publish findings / datasources / databases for the same
        - can add a folder for the user to add custom guardrails 
    - use an agent to check if the input is malicious or not
    - use the library
- This entire instance is run inside a Docker environment
    - add kubernetes if that is needed
- Add encryption to the chats that is used on setup
    - the chat / system un-encrypts it on start based on a _5 letter string followed by a 4 number long sequence_
    - there should be a way on how the computer generates a string that is unique to this iteration only (true random) and that is combined with the user's password to create a key/lock system

## FrontEnd Part of it:
- Make a basic frontend applet
    - Use basic FE (JS/HTML/CSS) to make it (_Recommended_)
        - Use Auth thanks
    - Use Chainlit

## BackEnd / UpKeep Part of it:
- restAPI, SwaggerUI, fastAPI endpoints for basic AI functions to route things through
    - Make a good documentation for this
- valid retry logic and fallback plans
- model versioning, deployment pipelines, lifecycle management
    - adding an option to version models trained and label them, as well as seeing which one is being used currently along with their stats shown in the side
- Add progress tracking and make it verbose enough to be well understood
- cron jobs checking the health of the model / re-testing their scores / etc
- a checker / endpoint for checking telemetry (tokens sent / received / etc)

# Storage:
- use parquet files over CSV files
- setup postgreSQL / Apache Spark (if it's free) for storage