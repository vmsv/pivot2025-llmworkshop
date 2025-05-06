#!/bin/zsh
export DOCKERFILES_PATH="./dockerfiles"
export NETWORK_NAME="pivot2025-nw"

if [[ $HOSTNAME == "pivot2025-shell" ]]; then
  export OLLAMA_URL="http://ollama-pivot2025:11434"
  export ARANGODB_URL="http://arangodb-pivot2025:8529"
  export QDRANT_URL="http://qdrant-pivot2025:8333"
fi

if [[ ! -d "./data" ]]; then
  mkdir data
fi

if ! docker network inspect "$NETWORK_NAME" &>/dev/null; then
  docker network create $NETWORK_NAME
  echo "Created docker network \"$NETWORK_NAME\"."
fi

if [[ $1 == "refresh" ]]; then
  docker compose -f ${DOCKERFILES_PATH}/docker-compose.yml stop
  docker compose -f ${DOCKERFILES_PATH}/docker-compose.yml rm
  docker compose -f ${DOCKERFILES_PATH}/docker-compose.yml pull
  docker compose -f ${DOCKERFILES_PATH}/docker-compose.yml up -d
  sleep 2
  docker compose ps
  docker compose logs
  
fi

if [[ $1 == "remove_all_for_sure" ]]; then
  docker compose -f ${DOCKERFILES_PATH}/docker-compose.yml stop 
  docker compose -f ${DOCKERFILES_PATH}/docker-compose.yml rm
  echo "Need ROOT do remove all files!!!! ARE YOU SURE??!!!"
  sudo rm -rf ${DOCKERFILES_PATH}/data
  exit 1
fi

if [[ $1 == "build" ]]; then
  cd ${DOCKERFILES_PATH}
  docker build -t pivot2025:latest .
  cd ..
fi

if [[ $1 == "start" ]]; then
  docker compose -f ${DOCKERFILES_PATH}/docker-compose.yml up -d
  docker compose -f ${DOCKERFILES_PATH}/docker-compose.yml ps
  exit 1
fi

if [[ $1 == "status" ]]; then
  docker compose -f ${DOCKERFILES_PATH}/docker-compose.yml ps
  exit 1
fi


if [[ $1 == "pull_model" ]]; then
  curl http://localhost:11434/api/pull -d '{"model": "'${2}'"}'
fi

if [[ $1 == "start_model" ]]; then
  docker compose -f ${DOCKERFILES_PATH}/docker-compose.yml exec ollama run $2
  sleep 2
  curl http://0.0.0.0:11434/api/ps | jq
fi

if [[ $1 == "list_running_models" ]]; then
  curl http://0.0.0.0:11434/api/ps | jq
fi
