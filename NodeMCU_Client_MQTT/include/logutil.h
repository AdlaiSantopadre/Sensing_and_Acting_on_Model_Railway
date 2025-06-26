#pragma once

void logInit();
void logInfo(const char* tag, const char* fmt, ...);
void logWarn(const char* tag, const char* fmt, ...);
void logError(const char* tag, const char* fmt, ...);
