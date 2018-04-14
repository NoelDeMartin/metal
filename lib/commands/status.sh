source $METAL_HOME/lib/functions.sh

list_installed_projects | while read project; do
    printf $project
    if is_project_active $project; then
        echo " [running @ http://$project.test]"
    else
        echo " [stopped]"
    fi
done
