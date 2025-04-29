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
