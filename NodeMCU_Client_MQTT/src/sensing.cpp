#include <Arduino.h>
#include "mqtt.h"
#include "config.h"
#include "logutil.h"

// Stato del sensore e variabili di controllo
//int current_state = -1;
int last_physical_state = 1;  // 1: alto (libero), 0: basso (occupato)
int last_state_sent = -2;

unsigned long last_idle_sent = 0;
unsigned long last_event_sent = 0;
unsigned long last_transition_time = 0;

bool waiting_for_ack = false;
bool evento_in_gestione = false;
bool attesa_rilascio = false;




void setupSensing() {
    pinMode(KY033_PIN, INPUT_PULLUP);
    logInfo("SENSING", "Pin KY-033 configurato in ingresso.");
}
void sensingLoop() {
    int read_state = digitalRead(KY033_PIN);
    unsigned long now = millis();

    // Evento: passaggio a occupato (fronte 1→0) e non già in gestione
    if (read_state == 0 && last_physical_state == 1 &&
       !waiting_for_ack && !evento_in_gestione && 
        now - last_transition_time > DEBOUNCE_DELAY) {
        
        last_transition_time = now;        
        waiting_for_ack = true;
        evento_in_gestione = true;
        last_event_sent = now;
        last_state_sent = 0;        
        last_physical_state = 0;

        mqttResetAck();

        char payload[128];
        snprintf(payload, sizeof(payload),
                 "{\"id\":\"%s\", \"stato\":0, \"timestamp\":%lu}",
                 CLIENT_ID, now / 1000);
        mqttPublish(payload);
        return;
    }

    // Ricevuto ack → pubblica rilascio (stato 1)
    if (waiting_for_ack && mqttAckRicevuto()) {
        waiting_for_ack = false;
        mqttResetAck();
        last_state_sent = 1;

        char payload[128];
        snprintf(payload, sizeof(payload),
                 "{\"id\":\"%s\", \"stato\":1, \"timestamp\":%lu}",
                 CLIENT_ID, now / 1000);
        mqttPublish(payload);
        return;
    }

    // Retry MQTT se ack non arriva in tempo
    if (waiting_for_ack && (now - last_event_sent > RETRY_ACK_MS)) {
        last_event_sent = now;
        
        char payload[128];
        snprintf(payload, sizeof(payload),
                 "{\"id\":\"%s\", \"stato\":0, \"retry\":true, \"timestamp\":%lu}",
                 CLIENT_ID, now / 1000);
        mqttPublish(payload);        
        logWarn("SENSING", "Retry MQTT per evento=0.");
        return;
    }

    // Rilascio del sensore (fronte 0→1) → resetta permesso a nuovi eventi
    if (read_state == 1 && last_physical_state == 0) {
        last_physical_state = 1;
        evento_in_gestione = false;  // Ora posso accettare un nuovo evento
    }

    // Stato idle
    if (!waiting_for_ack && read_state == 1 && (now - last_idle_sent > INTERVAL_IDLE_MS)) {

        last_idle_sent = now;
        last_state_sent = 1;

        char payload[128];
        snprintf(payload, sizeof(payload),
                 "{\"id\":\"%s\", \"stato\":1, \"idle\":true, \"timestamp\":%lu}",
                 CLIENT_ID, now / 1000);
        mqttPublish(payload);
    }
}
