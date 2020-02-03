/**
 * \file ecg.h
 * \brief ECG class definition.
 * \author William Silva
 * \author Marcos Pereira
 * \date Feb 3, 2020
 *
 * \internal
 * Copyright (C) 2020 Signove Tecnologia Corporation.
 * All rights reserved.
 * Contact: Signove Tecnologia Corporation (contact@signove.com)
 *
 * $LICENSE_TEXT:BEGIN$
 * MIT License
 * 
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 * 
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 * $LICENSE_TEXT:END$
 */

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
