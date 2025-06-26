#pragma once

// === Wi-Fi ===
#define WIFI_SSID         "MERCUSYS_CBCE"
#define WIFI_PASSWORD     "98167494"

// === MQTT ===
#define MQTT_BROKER       "192.168.1.153"
#define MQTT_PORT         1883
#define MQTT_USERNAME     "esp03"
#define MQTT_PASSWORD     "esp2025"
#define MQTT_TOPIC_DATA   "/binario/03"
#define MQTT_ACK_TOPIC    "ack/Nodo03"
#define CLIENT_ID         "Nodo03"

// === Sensore ===
#define KY033_PIN         D5 // oppure GPIO14
#define INTERVAL_IDLE_MS  5000
#define RETRY_ACK_MS      2000
#define DEBOUNCE_DELAY 600 //ms