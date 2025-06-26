#include <Arduino.h>
#include "sensing.h"
#include "mqtt.h"
#include "logutil.h"
#include "config.h"

void setup() {
    logInit();
    logInfo("MAIN", "Avvio sistema NodeMCU %s", CLIENT_ID);
    setupMQTT(CLIENT_ID);
    setupSensing();
}

void loop() {
    mqttLoop();
    sensingLoop();
    delay(10);
}
