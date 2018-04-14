source $METAL_HOME/lib/functions.sh

if is_project_active; then
    deactivate_project

    if ! has_active_projects; then
        $DOCKER_COMPOSE down
    fi
fi
