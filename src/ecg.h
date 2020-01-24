#ifndef ECG_H
#define ECG_H

#include <bcm2835.h>
#include <stdio.h>
#include <unistd.h>
#include <time.h>
#include <pthread.h>
#include <iostream>
#include "waves.h"
#include <string>

#define lowByte(w)((w)&0xff)
#define highByte(w)((w)>>8)

#define NSR 1
#define ARRHYTYMIA 2
#define SQUARE 3

struct serder_args
{
    int plot;
    __useconds_t interval;
    __useconds_t idle_time;
    int waveLen;
    unsigned short wave[10000];
    
};

void *sender(void *args);
void sendData(unsigned short value);

class ecg
{
    public:
        ecg();
        void setBPM(int);
        void start();
        void setCurve(const unsigned char curve);
        virtual ~ecg();
        int getBPM();
        void setArrhythmia(int arrthmiaId);
        void setSquare(int period, int highValue, int lowValue);
        void setNSR(int bpm);
        int getSquarePeriod();
        int getMode();
    protected:
    private:
        int bpm;
        int msquareperiod;
        int mode;
        void setCurve(const unsigned short *curve, int size, int pointInterval = DEFAULT_ECG_INTERVAL);
        serder_args senderParams;
        pthread_t senderThread;
};

#endif // ECG_H
