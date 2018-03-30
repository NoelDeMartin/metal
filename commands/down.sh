# TODO only stop compose containers if no app is running
docker-compose --file "$METAL_HOME/docker-compose.yml" down

docker stop "metal_$PROJECT_NAME"
rm "$METAL_HOME/nginx/sites/$PROJECT_NAME.test.conf"

# TODO if containers were not stopped, restart nginx
