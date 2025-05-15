#
# Welcome to the instructions for the PivotCon 2025


# File organization

* dockerfiles/ all the files related to docker includind Dockerfile to build the environment and docker composer do download the daemons images
* env - environment shell to be used in pivotcon2025-shell.sh
* pivotcon2025-shell.sh - starts a docker image with the necessary environment
* run_all.sh - a little client to execution tasks with long command lines
* chat_test.py - a AI chat testing script to see if everything is working with the LLM side of the workshop 


# First actions

* ./run_all.sh build - this will build the pivot2025 docker image with all the necessary packages and python modules
* ./run_all.sh start - This will pull the necessary docker images and start them.
* ./run_all.sh pull_model gemma3:4b - This will ask ollama to download that model. We should run on any laptop and its what we will use for the workshop feel free to use any other 
                                      but you may need to change something on the remaining scripts
* ./run_all.sh start_model gemma3:4b - This will ask Ollama to start serving this model. This should output a JSON like information showing its running.
* ./pivot2025-shell.sh - This should open a new shell.
* ./python3 chat_test.py


# For RAG tests

* Once inside the shell, go to rag/ and run python app.py
* From your regular terminal you can now use the client to index and query the system
* for instance run: python3 rag/client.py -u http://127.0.0.1:8000 -i test_data/talos.pdf
* Navigate to http://127.0.0.1:6333/dashboard#/collections and you should see the collection with all the embeddings done. This should also be seen in the terminal where you are running the app.py ( kind of debug )
* Now you can query the system with python3 rag/client -u http://127.0.0.1:8000 -q 'Your query'
* Play around by indexing more documents and making different queries.