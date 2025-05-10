#include <stdio.h>             //Include funzioni standard di input/output
#include "freertos/FreeRTOS.h" //Include il core di FreeRTOS e le API per creare task
#include "freertos/task.h"     //Includono  le API per creare task
#include "esp_log.h"           //Permette di stampare log sulla console seriale (ESP_LOGI).
#include "mqtt_client.h"       //Includi le API del client MQTT dell’ESP-IDF.
#include "driver/gpio.h"        //Permette di usare i GPIO (input/output digitali)
#include "time.h"               //Serve per ottenere il timestamp UNIX (time_t) 

//Definizioni macro e configurazioni
#define KY033_GPIO_PIN GPIO_NUM_14 //Il pin GPIO14 (sul NodeMCU è D5) è collegato al segnale del sensore.
#define MQTT_BROKER_URI "mqtt://192.168.1.103" //Indirizzo IP del broker MQTT (su raspberrypi01).
#define SENSOR_ID "Nodo01" //Etichetta univoca del nodo sensore
#define FORCE_SEND_INTERVAL_MS 5000 //Intervallo in millisecondi per l’invio sincrono periodico (ogni 5 secondi).

//Variabili globali
static const char *TAG = "MQTT_SENSOR"; //Etichetta usata nei messaggi di log seriale
static esp_mqtt_client_handle_t client;  //Gestore (handle) per il client MQTT
static int stato_sensore = -1;  // Variabile condivisa tra i task che rappresenta lo stato del sensore (0 = libero, 1 = occupato).

//Callback che stampa ogni evento MQTT ricevuto (es. connessione, pubblicazione, errore).
void mqtt_event_handler(void *handler_args, esp_event_base_t base, int32_t event_id, void *event_data) {
    ESP_LOGI(TAG, "MQTT Event ID: %d", event_id);
}

//Inizializzazione del client MQTT
void mqtt_app_start(void) {
    esp_mqtt_client_config_t mqtt_cfg = {
        .uri = MQTT_BROKER_URI,
    };//Configura l’URI del broker MQTT
    client = esp_mqtt_client_init(&mqtt_cfg); //Inizializza il client MQTT
    esp_mqtt_client_register_event(client, ESP_EVENT_ANY_ID, mqtt_event_handler, NULL); //Registra la callback.
    esp_mqtt_client_start(client); //Avvia la connessione
}

//Task FreeRTOS: lettura sensore 
void task_sensore(void *param) { //Riceve un puntatore a intero (indirizzo di stato_sensore).
    int *p_stato = (int *)param; //*p_stato consente di accedere/modificare il valore globale condiviso
    gpio_set_direction(KY033_GPIO_PIN, GPIO_MODE_INPUT);//Imposta il pin collegato al sensore come input digitale

    while (1) {
        int lettura = gpio_get_level(KY033_GPIO_PIN); //Legge periodicamente lo stato del sensore.
        if (lettura != *p_stato) { //Se è cambiato rispetto a *p_stato, lo aggiorna e stampa un log.
            *p_stato = lettura;
            ESP_LOGI(TAG, "Stato sensore cambiato: %d", *p_stato);
        }
        vTaskDelay(pdMS_TO_TICKS(500));//Ciclo ogni 500ms.
    }
}
//Task_mqtt
void task_mqtt(void *param) {
    int *p_stato = (int *)param;//Anche questo task riceve il puntatore alla stessa variabile stato_sensore
    char msg[128]; //buffer per il messaggio JSON e per il topic dedicato al sensore #01.
    char topic[] = "/binario/01";

    TickType_t last_send = xTaskGetTickCount();//serve per gestire invio sincrono ogni N secondi
    const TickType_t interval_ticks = pdMS_TO_TICKS(FORCE_SEND_INTERVAL_MS);//converte i millisecondi in tick FreeRTOS.
    int last_sent = -2;  // Valore iniziale impossibile per forzare primo invio
    //last_sent memorizza l’ultimo valore inviato per verificare se è cambiato
    while (1) { //Verifica se il tempo è passato o se il valore è cambiato
        TickType_t now = xTaskGetTickCount(); //legge il tempo attuale in tick
        bool time_elapsed = (now - last_send) >= interval_ticks;
        bool changed = (*p_stato != last_sent);
        //Verifica: se lo stato è cambiato (evento asincrono) o se è passato il tempo stabilito (evento sincrono)
        if (changed || time_elapsed) { //Se almeno una condizione è vera, aggiorna last_sent e last_send
            last_sent = *p_stato;
            last_send = now;
            time_t unix_time;
            time(&unix_time);//Ottiene il tempo corrente in formato UNIX (secondi da 1970)
            //Crea un messaggio JSON formattato
            snprintf(msg, sizeof(msg),
                     "{\"id\":\"%s\", \"stato\":%d, \"timestamp\":%ld}",
                     SENSOR_ID, *p_stato, unix_time);
            esp_mqtt_client_publish(client, topic, msg, 0, 1, 0); //Lo invia via MQTT (QoS 1, non retained).
            ESP_LOGI(TAG, "MQTT inviato: %s", msg);
        }

        vTaskDelay(pdMS_TO_TICKS(500)); //Attende 500ms per il prossimo ciclo
    }
}
// Avvio della app e creazione dei due task con stack di 4 KB e priorità 5
void app_main(void) {
    ESP_LOGI(TAG, "Avvio Applicazione Nodo %s", SENSOR_ID);
    mqtt_app_start();
    xTaskCreate(task_sensore, "task_sensore", 4096, &stato_sensore, 5, NULL);
    xTaskCreate(task_mqtt, "task_mqtt", 4096, &stato_sensore, 5, NULL);
}
