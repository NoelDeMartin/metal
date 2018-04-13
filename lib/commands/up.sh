source $METAL_HOME/lib/functions.sh

if ! is_project_active; then
    if ! is_project_installed; then
        install_project
    fi

    activate_project
else
    echo "Project $PROJECT_NAME already running"
fi
