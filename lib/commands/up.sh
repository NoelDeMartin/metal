source $METAL_HOME/lib/functions.sh

if ! is_project_active; then

    if ! project_exists; then
        mkdir "$METAL_HOME/projects/$PROJECT_NAME"

        cp "$METAL_HOME/projects/nginx.conf" "$METAL_HOME/projects/$PROJECT_NAME/$PROJECT_NAME.test.conf"
        sed "s/\$PROJECT_NAME/$PROJECT_NAME/g" "$METAL_HOME/projects/$PROJECT_NAME/$PROJECT_NAME.test.conf" -i

        cp "$METAL_HOME/projects/docker-compose.yml" "$METAL_HOME/projects/$PROJECT_NAME/docker-compose.yml"
        sed "s/\$PROJECT_NAME/$PROJECT_NAME/g" "$METAL_HOME/projects/$PROJECT_NAME/docker-compose.yml" -i
    fi

    cp "$METAL_HOME/projects/$PROJECT_NAME/$PROJECT_NAME.test.conf" "$METAL_HOME/nginx/sites"
    DOCKER_COMPOSE="$DOCKER_COMPOSE --file $METAL_HOME/projects/$PROJECT_NAME/docker-compose.yml"

    if ! network_created; then
        docker network create metal_network
    fi

    $DOCKER_COMPOSE up -d nginx $PROJECT_NAME
    $DOCKER_COMPOSE restart nginx
    echo $PROJECT_NAME >> "$METAL_HOME/projects/active"
else
    echo "Project $PROJECT_NAME already running"
fi
