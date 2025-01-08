#! /bin/bash

docker build -t aia-lab-mx-finance-multiagent .
echo " " 
echo " " 
echo " " 
docker container run -d --name multi-agents -p 8501:8501 aia-lab-mx-finance-multiagent
echo " " 