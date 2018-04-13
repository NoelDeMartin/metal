source $METAL_HOME/lib/functions.sh

$DOCKER_COMPOSE run --volume="$PROJECT_PATH:/app" --rm rails bundle install --path vendor/bundle
