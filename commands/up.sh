docker-compose --file "$METAL_HOME/docker-compose.yml" up -d web

if [ -n "$METAL_DEBUG" ]
then
    docker attach metal_web_1
fi
