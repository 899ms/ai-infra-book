#!/bin/bash
set -euo pipefail
cd /home/ubuntu/ai-infra-book-experiments/ch12/12-04/computer-use
mkdir network-results
docker image inspect ai-infra-book-net1204:local > network-results/image-inspect.json
docker run -d --name book-computer1204 --network none --cap-add NET_ADMIN --cpus 2 --memory 2g -v "$PWD:/work" -w /work ai-infra-book-net1204:local sleep infinity > network-results/container-id.txt
trap 'docker rm -f book-computer1204 > network-results/container-removed.txt' EXIT
docker inspect book-computer1204 > network-results/container-inspect.json
docker exec book-computer1204 tc qdisc add dev lo root netem delay 40ms rate 20mbit loss 0.1%
docker exec book-computer1204 tc -s -j qdisc show dev lo > network-results/before.json
docker exec book-computer1204 python run_network.py --output network-results/loss0.1
sleep 1
docker exec book-computer1204 tc -s -j qdisc show dev lo > network-results/after.json
