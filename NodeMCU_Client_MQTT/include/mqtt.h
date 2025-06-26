#pragma once

void setupMQTT(const char* client_id);
void mqttLoop();
void mqttPublish(const char* payload);
bool mqttAckRicevuto();
void mqttResetAck();
