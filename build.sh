docker compose up -d
sleep 5
docker exec -i postgres_db psql -U admin -d leads_management < ./database/createdatabase.sql