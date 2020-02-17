#źródło:
#https://www.cockroachlabs.com/docs/stable/start-a-local-cluster-in-docker-mac.html

# pobranie obrazu dockera do lokalnego systemu
sudo docker pull cockroachdb/cockroach:v19.2.2
# stworzenie sieci dockerowej dla cochroachDB
sudo docker network create -d bridge roachnet
# wystartowanie klastra cockroacha, wyjaśnienie flag i parametrów w źródłach
sudo docker run -d \
--name=roach1 \
--hostname=roach1 \
--net=roachnet \
-p 26257:26257 -p 8080:8080  \
-v "${PWD}/cockroach-data/roach1:/cockroach/cockroach-data"  \
cockroachdb/cockroach:v19.2.2 start \
--insecure \
--join=roach1,roach2,roach3

sudo docker run -d \
--name=roach2 \
--hostname=roach2 \
--net=roachnet \
-v "${PWD}/cockroach-data/roach2:/cockroach/cockroach-data" \
cockroachdb/cockroach:v19.2.2 start \
--insecure \
--join=roach1,roach2,roach3

sudo docker run -d \
--name=roach3 \
--hostname=roach3 \
--net=roachnet \
-v "${PWD}/cockroach-data/roach3:/cockroach/cockroach-data" \
cockroachdb/cockroach:v19.2.2 start \
--insecure \
--join=roach1,roach2,roach3

# wylistowanie uruchomionych kontenerów
sudo docker ps

#inicjalizacja bazy danych cockroach
sudo docker exec -it roach1 ./cockroach init --insecure

# dostep do klienta psql bazy danych
sudo docker exec -it roach1 ./cockroach sql --insecure

#stworzenie bazy danych enigma
create database enigma;

#stworzenie użytkownika enigma
create user enigma;

#nadanie uprawnień użytkownikowi enigma do utworzonej bazy danych
grant all on database enigma to enigma;

# zastopowanie kontenerów cockroacha
sudo docker stop roach1 roach2 roach3

# usunięcie kontenerów cockroacha
sudo docker rm roach1 roach2 roach3

# ponowne wystartowanie kontenerów cockroacha
sudo docker start roach1 roach2 roach3

# usunięcie danych bazy cockroacha
rm -rf cockroach-data



(venv_python3.6) czarny@czarny-laptop:~/PycharmProjects/enigma$ docker tag enigma:latest czarny94/enigma:latest
(venv_python3.6) czarny@czarny-laptop:~/PycharmProjects/enigma$ docker push czarny94/enigma:latest
