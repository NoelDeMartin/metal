docker start "metal_$PROJECT_NAME"

# TODO generate config instead
cp "$METAL_HOME/nginx/$PROJECT_NAME.test.conf" "$METAL_HOME/nginx/sites"

if [ -z "`docker-compose --file "$METAL_HOME/docker-compose.yml" ps mongo | grep "metal"`" ]; then
    docker-compose --file "$METAL_HOME/docker-compose.yml" up -d mongo
fi

if [ -z "`docker-compose --file "$METAL_HOME/docker-compose.yml" ps nginx | grep "metal"`" ]; then
    docker-compose --file "$METAL_HOME/docker-compose.yml" up -d nginx
else
    docker-compose --file "$METAL_HOME/docker-compose.yml" restart nginx
fi

if [ -n "$METAL_DEBUG" ]; then
    docker attach "metal_$PROJECT_NAME"
fi
