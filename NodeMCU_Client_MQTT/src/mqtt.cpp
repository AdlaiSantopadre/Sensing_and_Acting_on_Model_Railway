#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include "mqtt.h"
#include "config.h"
#include "logutil.h"

WiFiClient espClient;
PubSubClient client(espClient);

static volatile bool ackRicevuto = false;

void mqttCallback(char* topic, byte* payload, unsigned int length) {
    payload[length] = '\0';
    logInfo("MQTT", "Ricevuto messaggio su topic: %s => %s", topic, (char*)payload);
    if (strcmp(topic, MQTT_ACK_TOPIC) == 0) {
        ackRicevuto = true;
        logInfo("MQTT", "ACK ricevuto.");
    }
}

void setupMQTT(const char* client_id) {
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    logInfo("MQTT", "Connessione a SSID: %s ...", WIFI_SSID);

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        logInfo("MQTT", ".");
    }

    logInfo("MQTT", "WiFi connesso. IP: %s", WiFi.localIP().toString().c_str());

    client.setServer(MQTT_BROKER, MQTT_PORT);
    client.setCallback(mqttCallback);

    while (!client.connected()) {
        logInfo("MQTT", "Connessione al broker %s ...", MQTT_BROKER);
        if (client.connect(client_id, MQTT_USERNAME, MQTT_PASSWORD)) {
            logInfo("MQTT", "Connesso al broker MQTT.");
        } else {
            logError("MQTT", "Connessione fallita (rc=%d). Riprovo...", client.state());
            delay(1000);
        }
    }

    client.subscribe(MQTT_ACK_TOPIC, 1);
    logInfo("MQTT", "Sottoscritto a topic: %s", MQTT_ACK_TOPIC);
}

void mqttLoop() {
    client.loop();
}

void mqttPublish(const char* payload) {
    logInfo("MQTT", "Pubblico messaggio: %s", payload);
    client.publish(MQTT_TOPIC_DATA, payload, false);
}

bool mqttAckRicevuto() {
    return ackRicevuto;
}

void mqttResetAck() {
    ackRicevuto = false;
}
