#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/event_groups.h"
#include "esp_log.h"
#include "mqtt_client.h"
#include "driver/gpio.h"
#include "time.h"
#include "esp_wifi.h"
#include "esp_event_loop.h"
#include "nvs_flash.h"
#include "tcpip_adapter.h"

#define KY033_GPIO_PIN GPIO_NUM_14
#define MQTT_BROKER_URI "mqtt://192.168.1.103"
#define SENSOR_ID "Nodo01"
#define FORCE_SEND_INTERVAL_MS 5000
#define WIFI_SSID "MERCURSYS_CBCE"
#define WIFI_PASS "98167494"

static const char *TAG = "MQTT_SENSOR";
static esp_mqtt_client_handle_t client;
static int stato_sensore = -1;

// === Event group per segnalare connessione Wi-Fi ===
static EventGroupHandle_t wifi_event_group;
const int WIFI_CONNECTED_BIT = BIT0;

esp_err_t event_handler(void *ctx, system_event_t *event) {
    switch(event->event_id) {
        case SYSTEM_EVENT_STA_START:
            esp_wifi_connect();
            break;
        case SYSTEM_EVENT_STA_GOT_IP:
            ESP_LOGI(TAG, "Indirizzo IP ottenuto: %s", ip4addr_ntoa(&event->event_info.got_ip.ip_info.ip));
            xEventGroupSetBits(wifi_event_group, WIFI_CONNECTED_BIT);
            break;
        case SYSTEM_EVENT_STA_DISCONNECTED:
            ESP_LOGI(TAG, "Disconnesso. Riconnessione in corso...");
            esp_wifi_connect();
            xEventGroupClearBits(wifi_event_group, WIFI_CONNECTED_BIT);
            break;
        default:
            break;
    }
    return ESP_OK;
}

void wifi_init_sta(void) {
    tcpip_adapter_init();
    wifi_event_group = xEventGroupCreate();
    esp_event_loop_init(event_handler, NULL);

    wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();
    esp_wifi_init(&cfg);

    wifi_config_t wifi_config = {
        .sta = {
            .ssid = WIFI_SSID,
            .password = WIFI_PASS,
        },
    };

    esp_wifi_set_mode(WIFI_MODE_STA);
    esp_wifi_set_config(WIFI_IF_STA, &wifi_config);
    esp_wifi_start();

    ESP_LOGI(TAG, "Connessione Wi-Fi a SSID: %s", WIFI_SSID);

    // Attende fino a che la connessione non è stabilita
    xEventGroupWaitBits(wifi_event_group, WIFI_CONNECTED_BIT, false, true, portMAX_DELAY);

    uint8_t mac[6];
    esp_wifi_get_mac(WIFI_IF_STA, mac);
    ESP_LOGI(TAG, "MAC ESP8266: %02x:%02x:%02x:%02x:%02x:%02x",
             mac[0], mac[1], mac[2], mac[3], mac[4], mac[5]);
}

void mqtt_event_handler(void *handler_args, esp_event_base_t base, int32_t event_id, void *event_data) {
    ESP_LOGI(TAG, "MQTT Event ID: %d", event_id);
}

void mqtt_app_start(void) {
    esp_mqtt_client_config_t mqtt_cfg = {
        .uri = MQTT_BROKER_URI,
    };
    client = esp_mqtt_client_init(&mqtt_cfg);
    esp_mqtt_client_register_event(client, ESP_EVENT_ANY_ID, mqtt_event_handler, NULL);
    esp_mqtt_client_start(client);
}

void task_sensore(void *param) {
    int *p_stato = (int *)param;

    gpio_config_t io_conf = {
        .pin_bit_mask = (1ULL << KY033_GPIO_PIN),
        .mode = GPIO_MODE_INPUT,
        .pull_up_en = GPIO_PULLUP_ENABLE,
        .pull_down_en = GPIO_PULLDOWN_DISABLE,
        .intr_type = GPIO_INTR_DISABLE
    };
    gpio_config(&io_conf);

    while (1) {
        int lettura = gpio_get_level(KY033_GPIO_PIN);
        ESP_LOGI(TAG, "Lettura KY033: %d", lettura);
        if (lettura != *p_stato) {
            *p_stato = lettura;
            ESP_LOGI(TAG, "Stato sensore cambiato: %d", *p_stato);
        }
        vTaskDelay(pdMS_TO_TICKS(500));
    }
}

void task_mqtt(void *param) {
    int *p_stato = (int *)param;
    char msg[128];
    char topic[] = "/binario/01";

    TickType_t last_send = xTaskGetTickCount();
    const TickType_t interval_ticks = pdMS_TO_TICKS(FORCE_SEND_INTERVAL_MS);
    int last_sent = -2;

    while (1) {
        TickType_t now = xTaskGetTickCount();
        bool time_elapsed = (now - last_send) >= interval_ticks;
        bool changed = (*p_stato != last_sent);

        if (changed || time_elapsed) {
            last_sent = *p_stato;
            last_send = now;
            time_t unix_time;
            time(&unix_time);
            snprintf(msg, sizeof(msg),
                     "{\"id\":\"%s\", \"stato\":%d, \"timestamp\":%ld}",
                     SENSOR_ID, *p_stato, unix_time);
            esp_mqtt_client_publish(client, topic, msg, 0, 1, 0);
            ESP_LOGI(TAG, "MQTT inviato: %s", msg);
        }

        vTaskDelay(pdMS_TO_TICKS(500));
    }
}

void app_main(void) {
    nvs_flash_init();
    wifi_init_sta();
    ESP_LOGI(TAG, "Avvio Applicazione Nodo %s", SENSOR_ID);
    mqtt_app_start();
    xTaskCreate(task_sensore, "task_sensore", 4096, &stato_sensore, 5, NULL);
    xTaskCreate(task_mqtt, "task_mqtt", 4096, &stato_sensore, 5, NULL);
}
