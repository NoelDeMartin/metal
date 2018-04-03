function active_projects() {
    if [ -e "$METAL_HOME/projects/active" ]; then
        cat "$METAL_HOME/projects/active"
    fi
}

function has_active_projects() {
    if [[ $(cat "$METAL_HOME/projects/active" | sed '/^\s*$/d' | wc -l) > 0 ]]; then
        return 0
    else
        return 1
    fi
}

function is_project_active() {
    if [ -e "$METAL_HOME/projects/active" ]; then
        # TODO this matches partial existance (like "foobar would be active if foo was active")
        if [ `cat "$METAL_HOME/projects/active" | grep $PROJECT_NAME` ]; then
            return 0
        fi
    fi

    return 1
}

function project_exists() {
    # TODO this matches partial existance (like "foobar would be active if foo was active")
    if [ -d "$METAL_HOME/projects/$PROJECT_NAME" ]; then
        return 0
    else
        return 1
    fi
}

function network_created() {
    if [ "$(docker network ls | grep metal_network)" ]; then
        return 0
    else
        return 1
    fi
}

DOCKER_COMPOSE="docker-compose --file $METAL_HOME/docker-compose.yml"
for PROJECT in `active_projects`
do
    DOCKER_COMPOSE="$DOCKER_COMPOSE --file $METAL_HOME/projects/$PROJECT/docker-compose.yml"
done
