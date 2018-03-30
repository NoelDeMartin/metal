if [ ! "$(docker network ls | grep metal_network)" ]; then
    docker network create metal_network
fi

docker-compose --file "$METAL_HOME/docker-compose.yml" build

if [ `docker ps -q --all -f name="metal_$PROJECT_NAME"` ]; then
    if [ `docker ps -q -f name="metal_$PROJECT_NAME"` ]; then
        docker stop "metal_$PROJECT_NAME"
    fi
    docker rm "metal_$PROJECT_NAME"
fi

docker create \
    --name="metal_$PROJECT_NAME" \
    --env="BUNDLE_APP_CONFIG=/app/.bundle" \
    --expose="3000" \
    --expose="28080" \
    --volume="$PROJECT_PATH:/app" \
    --network="metal_network" \
    --network-alias="$PROJECT_NAME" \
    -t metal_rails bin/rails server
