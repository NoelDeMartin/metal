source $METAL_HOME/lib/functions.sh

if ! network_created; then
    docker network create metal_network
fi

docker-compose --file "$METAL_HOME/docker-compose.yml" run \
    --volume="$PROJECT_PATH:/app" --rm \
    rails bundle install --path vendor/bundle

if ! has_active_projects; then
    docker network rm metal_network
fi
