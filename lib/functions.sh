#!/bin/bash

TRUE=0
FALSE=1
DOCKER_COMPOSE="docker-compose --file=$METAL_HOME/docker-compose.yml"
ACTIVE_PROJECTS="$METAL_HOME/.projects/active"
INSTALLED_PROJECTS="$METAL_HOME/.projects/installed"

function has_active_projects() {
    if [[ $(cat $ACTIVE_PROJECTS | sed '/^\s*$/d' | wc -l) > 0 ]]; then
        return $TRUE
    else
        return $FALSE
    fi
}

function is_project_active() {
    if [ -e $ACTIVE_PROJECTS ]; then
        if [ -z "$1" ]; then
            local project="$PROJECT_NAME"
        else
            local project="$1"
        fi

        if [ `cat $ACTIVE_PROJECTS | grep -w "$project" | wc -l` -gt 0 ]; then
            return $TRUE
        fi
    fi

    return $FALSE
}

function activate_project() {
    mkdir -p "$METAL_HOME/.projects"
    echo $PROJECT_NAME >> $ACTIVE_PROJECTS

    cp "$METAL_HOME/nginx/template.conf" "$METAL_HOME/nginx/sites/$PROJECT_NAME.test.conf"
    sed "s#\[PROJECT_NAME]#$PROJECT_NAME#g" "$METAL_HOME/nginx/sites/$PROJECT_NAME.test.conf" -i

    $DOCKER_COMPOSE up -d nginx $PROJECT_NAME
    $DOCKER_COMPOSE restart nginx
}

function deactivate_project() {
    rm "$METAL_HOME/nginx/sites/$PROJECT_NAME.test.conf"
    sed "/$PROJECT_NAME/d" $ACTIVE_PROJECTS -i

    $DOCKER_COMPOSE stop $PROJECT_NAME
    $DOCKER_COMPOSE restart nginx
}

function list_installed_projects() {
    cat $INSTALLED_PROJECTS | awk '{print $1}'
}

function is_project_installed() {
    if [ -e $INSTALLED_PROJECTS ]; then
        if [ `cat $INSTALLED_PROJECTS | grep "$PROJECT_NAME " | wc -l` -gt 0 ]; then
            return $TRUE
        fi
    fi

    return $FALSE
}

function install_project() {
    mkdir -p "$METAL_HOME/.projects"
    echo "$PROJECT_NAME $PROJECT_PATH" >> $INSTALLED_PROJECTS

    rebuild_docker_compose
}

function rebuild_docker_compose() {
    cp "$METAL_HOME/docker-compose.base.yml" "$METAL_HOME/docker-compose.yml"

    cat $INSTALLED_PROJECTS | while read name path; do
        cat "$METAL_HOME/docker-compose.project.yml" >> "$METAL_HOME/docker-compose.yml"
        sed "s#\[PROJECT_NAME\]#$name#g" "$METAL_HOME/docker-compose.yml" -i
        sed "s#\[PROJECT_PATH\]#$path#g" "$METAL_HOME/docker-compose.yml" -i
        sed "s#\[ALIASES\]#- $name.test\n          [ALIASES]#g" "$METAL_HOME/docker-compose.yml" -i
    done

    sed "/\[ALIASES\]/d" "$METAL_HOME/docker-compose.yml" -i
}
