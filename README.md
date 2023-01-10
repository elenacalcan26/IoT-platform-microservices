# IoT-platform-microservices

#### Calcan Elena-Claudia
#### 343C3

## Synopsys
------------

- este implementata o platforma pentru colectarea, stocarea si vizualizarea datelor provenite de la IoT.

## Strucrura proiectului si implementare
----------------------------------------

- in radacina proiectului se afla fisierele **stack.yml** si **run.sh**
- **stack.yml** contine descrierea componentelor folosite in realizarea
platformei:
    - mqqt - broker-ul de MQTT
    - adapter - adaptorul care primeste datele si le adauga in baza de date
    - influxdb - baza de date InfuxDB
    - grafana - tool-ul de vizualizare Grafana
- **run.sh** este folosit pentru buildarea imaginilor si pornirea aplicatiei folosind Docker Swarm
- retele Docker definite sunt urmatoarele:
  - mqtt-network - conexiune intre borker si adaptor
  - db-network - conexiune intre InfluxDB si adaptor
  - grafana-network - conexiune intre InfluxDB si Grafana

### mosquitto
---------------
- contine fisierul **mosquitto.conf** care este folosit pentru configurarea borker-ului de MQTT.

### adapter
------------
- fisierul **main.py** contine implemenatrea componentei adaptor
  - are rol de client al borker-ului MQTT si server a bazei de date folosita
  - acesta este subscibed la topicul '#', parseaza mesajele primite si le adauga in baza de date
  - de asemenea, acesta afiseaza mesaje de looging atunci cand variabila **DEBUG_DATA_FLOW=True** in componenta corespunzatoare

### grafana
-----------
- contine configuratiile pentru tool-ul de vizualizare folosit
- in **dashboards** se afla configuratiile celor 2 Dashboard-uri folosite: UPB IoT Data & Battery Dashboard
- in **datasources** contine configurarea sursei de date, baza de date InfluxDB, pentru vizualizarea datelor

### publisher
-------------
- contine un scriptul **publisher.py** folosit pentru testarea platformei
- publisher-ul trimite mesaje catre broker-ul MQTT la topicul corespunzator statiei careia i s-au facut masuratorile

## Rulare si Testare
- pentru rularea proiectului:

        ./run.sh

- ca si o mica observatie in legatura cu buildarea si rularea platformei:
  - se presupune ca inainte s-a dat comanda

         docker swarm init

- pentru testare, in interiorul directorului **publisher**

         python3 publisher.py

## Referinte
- https://www.homeautomationguy.io/docker-tips/configuring-the-mosquitto-mqtt-docker-container-for-use-with-home-assistant/
- https://influxdb-python.readthedocs.io/en/latest/examples.html
- https://grafana.com/docs/grafana/latest/datasources/influxdb/

