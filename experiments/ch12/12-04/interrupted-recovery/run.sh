#!/bin/bash
set -euo pipefail
cd /home/ubuntu/ai-infra-book-experiments/ch12/12-04/interrupted-recovery
if docker ps -a --format '{{.Names}}' | grep -qx book-window1204; then
  echo 'Window benchmark container still exists; recovery not started.' >&2
  exit 2
fi
mkdir results
docker image inspect ai-infra-book-net1204:local > results/image-inspect.json
docker run -d --name book-recovery1204 --network none --cap-add NET_ADMIN --cpus 2 --memory 2g -v "$(dirname "$PWD"):/work" -w /work/interrupted-recovery ai-infra-book-net1204:local sleep infinity > results/container-id.txt
trap 'docker rm -f book-recovery1204 > results/container-removed.txt' EXIT
docker inspect book-recovery1204 > results/container-inspect.json
docker exec book-recovery1204 tc qdisc add dev lo root netem delay 40ms rate 20mbit loss 0.1%
docker exec book-recovery1204 tc -s -j qdisc show dev lo > results/before.json
docker exec book-recovery1204 python run.py --output results/loss0.1
sleep 1
docker exec book-recovery1204 tc -s -j qdisc show dev lo > results/after.json
