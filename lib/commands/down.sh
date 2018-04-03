source $METAL_HOME/lib/functions.sh

if is_project_active; then
    rm "$METAL_HOME/nginx/sites/$PROJECT_NAME.test.conf"
    $DOCKER_COMPOSE stop $PROJECT_NAME
    $DOCKER_COMPOSE restart nginx

    sed "/$PROJECT_NAME/d" "$METAL_HOME/projects/active" -i

    if ! has_active_projects; then
        $DOCKER_COMPOSE down
        docker network rm metal_network
    fi

fi
