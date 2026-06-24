Pathway of things to do from scratch:

## AI Part of it:

### Core processing
#### LLM & Hosting:
- Choose the correct model, choices of model to choose from:
    - `qwen2.5:14b-instruct-q4_K_M` - it is faster than qwen3 as it takes up lesser space but it is not as smart and runs out of context very fast 
    - `qwen3:14b` - it *is* slower - but it is a very good model - I can try to find more optimised versions of it - might have to run GGUF instead of Ollama
        - Can try VLMM's memory quant and use that to host this locally
            - I see that it has small but valid improvements over ollama, no MoE bug for 30b a3b (not that it matters for my usecase)
            - qwen 14b AWQ (with AWQ(_recommended_) / FP8 )
                - 
                ```
                VLLM_ATTENTION_BACKEND=XFORMERS \
                VLLM_MEMORY_PROFILER_ESTIMATE_CUDAGRAPHS=0 \
                TORCH_CUDA_ARCH_LIST=12.0 \
                CUDA_VISIBLE_DEVICES=0 \
                vllm serve ~/models/Qwen3-14B-AWQ \
                --max-model-len 3500 \
                --gpu-memory-utilization 0.90 \
                --dtype float16 \
                --enforce-eager \
                --port 8000
                ```
                - do Ollama and VLLM really slow down inference that much ?
        - Can try the q4_K_M
            - that IS a valid Ollama route
- I need to get the model up and running, configure via VLLM / Ollama / etc - plug it up with langchain
    - Use the most updated version of langchain, no deprecared versioning
    - Make a slot to place prompt templates - read from JSON / txt
- Add a stop to prevent looping
    - Add a max iteration loop and then force LLM to give response

#### RAG:
- Set up a basic RAG
    - Make sure to keep it as precise + modular + as efficient as possible
    - Add end points for document upload as well reading text, tables, all that as well different types of files
    - optimise:
        - chunking
        - retreivers / retreival
        - reranking
- Set up proper Chain Of Thought (COT) logic and implementation
- Integrate Web Search (DDGS) into the RAG as well as the LLM
- Set up RAG feedback loop (quality of answers, using recall@ / RAGAS)

##### VDB:
- temp VDB to be used for normal calls:
    - see if it's possible for a temp VDB to be made for longer context conversations without breaking the back of the model
        - try using async alongside inference so that the user never knows about it
            - backend endpoints will be useful here
- Use chroma for testing
- Move to pinecone / weaviate for faster and more prod-ready VDB's
    - Need faster and more precise answers

#### Agents:
- Add a place to add agents into the loop
- Have a few pre-fixed agentic routes / lanes for the user to select based on their use-case
    - Allow customisation for this (B.AI)
- Implement MCP
- Add more agentic protocols:
    - .
- Need to add a stop for infinite iteration
    - Make a tool that does this
- COT Agent

#### Outputting:
- Make way for structured outputs (JSON)
    - User can give the type of output they want, the way the answer needs to be given (via examples / few shot)
- Implement prompt-compression engine

### Security:
- Add custom input and output guardrails
    - use a pre-trained model (I will train it) to see if the input it malicious or not (_Recommended_)
        - see what exists in the market currently and if there's an industry standard for it
            - if not - make it + publish findings / datasources / databases for the same
        - can add a folder for the user to add custom guardrails 
    - use an agent to check if the input is malicious or not
    - use the library
- This entire instance is run inside a Docker environment
    - add kubernetes if that is needed
    - "uptime-kuma" - https://www.youtube.com/watch?v=FvdlwyMwrzg
    - containers I think i'll need:
        - Core AI code
        - Model Storage (should I keep it inside of a container, will it slow it down ?)
        - Data Storage (chat, settings, etc)
        - VDB Storage
        - FrontEnd
        - Backend
- Add encryption to the chats that is used on setup
    - the chat / system un-encrypts it on start based on a _5 letter string followed by a 4 number long sequence_
        - try AES
    - there should be a way on how the computer generates a string that is unique to this iteration only (true random) and that is combined with the user's password to create a key/lock system

## FrontEnd Part of it:
- Make a basic frontend applet
    - Use basic FE (JS/HTML/CSS) to make it (_Recommended_)
        - Use Auth thanks
    - Use Chainlit
    - Use StreamLit

## BackEnd / UpKeep Part of it:
- restAPI, SwaggerUI, fastAPI endpoints for basic AI functions to route things through
    - Make a good documentation for this
- valid retry logic and fallback plans
- model versioning, deployment pipelines, lifecycle management
    - adding an option to version models trained and label them, as well as seeing which one is being used currently along with their stats shown in the side
- Add progress tracking and make it verbose enough to be well understood
- cron jobs checking the health of the model / re-testing their scores / etc
- need to do threading / pooling

## Testing and others:
- Implement a checker / endpoint for checking telemetry (tokens sent / received / etc)
- SDLC part of it
    - need to write tests
    - unit testing
    - technical testing
    - functional testing
- playwright / selenium
    - section for the user to add their own custom testing scenarios / user stories
- Automated testing via LLM to look for holes / report back in a log file
    - pen-testing and reporting with an agentic loop 
        - fetch API spec > analyze it > generate test cases (happy, end, negative) > write test file > execute > capture output > analyze failures/repeated failures > report w/improvements

# Storage:
- use parquet files over CSV files
- setup postgreSQL / Apache Spark (if it's free) for storage