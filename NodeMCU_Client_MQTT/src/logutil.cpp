#include "logutil.h"
#include <Arduino.h>
#include <stdarg.h>

void logInit() {
    Serial.begin(115200);
    while (!Serial);  // Attende apertura seriale
    delay(1000);
    Serial.println("--- Logger inizializzato ---");
}

void logFormatted(const char* level, const char* tag, const char* fmt, va_list args) {
    char buffer[256];
    vsnprintf(buffer, sizeof(buffer), fmt, args);
    unsigned long now = millis();
    Serial.printf("[%lu ms] [%s] [%s] %s\n", now, level, tag, buffer);
}

void logInfo(const char* tag, const char* fmt, ...) {
    va_list args;
    va_start(args, fmt);
    logFormatted("INFO", tag, fmt, args);
    va_end(args);
}

void logWarn(const char* tag, const char* fmt, ...) {
    va_list args;
    va_start(args, fmt);
    logFormatted("WARN", tag, fmt, args);
    va_end(args);
}

void logError(const char* tag, const char* fmt, ...) {
    va_list args;
    va_start(args, fmt);
    logFormatted("ERROR", tag, fmt, args);
    va_end(args);
}
