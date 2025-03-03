We use two Docker Compose configurations:
- A pre-made Supabase project
- Our project (backend and frontend)


to run :

1. make the run.sh executable :
chmod +x run.sh
2. run :
./run.sh up-prod


Documentation des commandes run.sh :

  up-prod: Démarre tous les services en mode production (détaché).
  up-dev: Démarre uniquement docker-compose-project.yaml en mode attaché pour le développement.
  restart-project: Redémarre uniquement docker-compose-project.yaml (en mode devellopement)
  down-all: Arrête tous les services, y compris Supabase.
  down-project: Arrête uniquement docker-compose-project.yaml.
