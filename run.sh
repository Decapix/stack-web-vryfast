#!/bin/bash

# Function to start the services in production mode
start_services_prod() {
    # Check if the supabase directory exists
    if [ ! -d "supabase" ]; then
        echo "Cloning the Supabase repository..."
        git clone --depth 1 https://github.com/supabase/supabase
    else
        echo "Supabase repository already cloned."
    fi

    cd supabase/docker

    # Check if the .env file exists
    if [ ! -f ".env" ]; then
        echo "Copying the fake env vars..."
        cp .env.example .env
    else
        echo ".env file already exists."
    fi

    echo "Pulling the latest Docker images..."
    docker compose pull

    echo "Starting the services in detached mode..."
    docker compose up -d

    cd ../..

    echo "Starting the docker-compose-project.yaml..."
    docker compose -f docker-compose-project.yaml up -d
}

# Function to start the services in development mode
start_services_dev() {
    Check if the supabase directory exists
    if [ ! -d "supabase" ]; then
        echo "Cloning the Supabase repository..."
        git clone --depth 1 https://github.com/supabase/supabase
    else
        echo "Supabase repository already cloned."
    fi

    cd supabase/docker

    # Check if the .env file exists
    if [ ! -f ".env" ]; then
        echo "Copying the fake env vars..."
        cp .env.example .env
    else
        echo ".env file already exists."
    fi

    echo "Pulling the latest Docker images..."
    docker compose pull

    echo "Starting the services in detached mode..."
    docker compose up -d

    cd ../..
    echo "Starting the docker-compose-project.yaml in attached mode..."
    docker compose -f docker-compose-project.yaml up
}

# Function to restart the docker-compose-project
restart_project() {
    echo "Restarting the docker-compose-project.yaml..."
    docker compose -f docker-compose-project.yaml down
    docker compose -f docker-compose-project.yaml build
    docker compose -f docker-compose-project.yaml up
}

# Function to stop all services
stop_all_services() {
    echo "Stopping the docker-compose-project.yaml..."
    docker compose -f docker-compose-project.yaml down
    cd supabase/docker
    echo "Stopping the Supabase services..."
    docker compose down
    cd ../..
}

# Function to stop only the docker-compose-project
stop_project() {
    echo "Stopping the docker-compose-project.yaml..."
    docker compose -f docker-compose-project.yaml down
}

# Check the command
case $1 in
    up-prod)
        start_services_prod
        ;;
    up-dev)
        start_services_dev
        ;;
    restart-project)
        restart_project
        ;;
    down-all)
        stop_all_services
        ;;
    down-project)
        stop_project
        ;;
    *)
        echo "Usage: $0 {up-prod|up-dev|restart-dev|down-all|down-project}"
        ;;
esac
