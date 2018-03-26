if [ -z "$METAL_DEBUG" ]
then
    docker-compose --file "$METAL_HOME/docker-compose.yml" up -d web mongo
else
    docker-compose --file "$METAL_HOME/docker-compose.yml" up -d mongo
    docker-compose --file "$METAL_HOME/docker-compose.yml" up web
fi