docker-compose --file "$METAL_HOME/docker-compose.yml" run --volume="$PROJECT_PATH:/app" --rm \
    rails bundle install --path vendor/bundle
