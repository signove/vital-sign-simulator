/**
 * \file ecg.cpp
 * \brief ECG class implementation.
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

#include "ecg.h"

ecg::ecg()
{
    bcm2835_init();
    senderParams.plot = 1;
    this->setNSR(60);
    msquareperiod = 0;
}

ecg::~ecg()
{

}

void ecg::setNSR(int bpm){
   mode = NSR;
   this->setCurve(1);   
   this->setBPM(bpm);
}

void ecg::setArrhythmia(int arrythmiaId){
   mode = ARRHYTYMIA;
   senderParams.idle_time = 0;
   this->setCurve(arrythmiaId);
}

void ecg::setSquare(int period, int highValue, int lowValue){
   mode = SQUARE;
   msquareperiod = period;
   int count =0;
   for(; count < period; count++){
      senderParams.wave[count] = highValue;
   }
   
   for(period = period*2; count < period; count++){
      senderParams.wave[count] = lowValue;
   }
   senderParams.waveLen = period;
   senderParams.idle_time = 0;
}

void ecg::setBPM(int value)
{
   bpm = value;
   if(value == 0){
      value = 1;
   }
   int idleInterval = (60000/value) - senderParams.waveLen;
   if(idleInterval < 0){
      senderParams.idle_time = 0;
   } else{
       senderParams.idle_time = idleInterval;
   }
}

int ecg::getBPM(){
   return bpm;
}

void ecg::setCurve(const unsigned short *curve, int size, int pointInterval)
{
    for(int i =0; i < size; i++){
        senderParams.wave[i] = curve[i];
    }
    senderParams.waveLen = size;
    senderParams.interval = pointInterval;
}

void ecg::setCurve(const unsigned char curve)
{
    switch(curve)
    {
         case 1:
            this->setCurve(NORMAL_ECG_1, NORMAL_ECG_1_SIZE);
            senderParams.idle_time = 0;
            break;
         case 2:
            this->setCurve(VTACH_1, VTACH_1_SIZE, VTACH_1_INTERVAL);
            senderParams.idle_time = 0;
            break;
         case 3:
            this->setCurve(IRREGULAR_HR, IRREGULAR_HR_SIZE, IRREGULAR_HR_INTERVAL);
            senderParams.idle_time = 0;
            break;
         case 4:
            this->setCurve(NORMAL_ECG_1, NORMAL_ECG_1_SIZE);
            setBPM(40);
            break;
         case 5:
            this->setCurve(NORMAL_ECG_1, NORMAL_ECG_1_SIZE);
            setBPM(25);
            break;
         case 6:
            this->setCurve(NORMAL_ECG_1, NORMAL_ECG_1_SIZE);
            setBPM(25);
            usleep(15000000);
            setBPM(40);
            usleep(15000000);
            this->setCurve(IRREGULAR_HR, IRREGULAR_HR_SIZE, IRREGULAR_HR_INTERVAL);
            break;
         case 7:
            this->setCurve(NORMAL_ECG_1, NORMAL_ECG_1_SIZE, 0);
            break;
         case 8:
            this->setCurve(VFIB_1, VFIB_1_SIZE, VFIB_1_INTERVAL);
            senderParams.idle_time = 0;
            break;

         case 9:
            this->setCurve(VENT_RHYTHM, VENT_RHYTHM_SIZE, VENT_RHYTHM_INTERVAL);
            senderParams.idle_time = 0;
            break;
            
         default:
            this->setCurve(NORMAL_ECG_1, NORMAL_ECG_1_SIZE);
            break;
    }
}

void ecg::start()
{
   pthread_create(&senderThread, NULL, sender, &senderParams);
}

void sendData(unsigned short value)
{
   char buffer[2];
   char Data=0;
   Data = highByte(value);
   Data = 0b00001111 & Data;
   Data = 0b00110000 | Data;
   buffer[0] = Data;
   buffer[1] = lowByte(value);
   bcm2835_spi_chipSelect(BCM2835_SPI_CS0);
   bcm2835_spi_writenb(&buffer[0], 2);
}
void *sender(void *args)
{
   struct serder_args *params = (serder_args *)args;
   int i, idlec, idletime;
   bcm2835_spi_begin();
   bcm2835_spi_setChipSelectPolarity(BCM2835_SPI_CS0, 0);
   bcm2835_spi_setClockDivider(BCM2835_SPI_CLOCK_DIVIDER_32);

   while(params -> plot){
       i = 0;
       idlec = 0;
       idletime = params-> idle_time;
       while(i < params-> waveLen){
          sendData(params-> wave[i++]);
          usleep(params-> interval);
       }
       while(idlec++ < idletime){
          usleep(params-> interval);
       }

   }
   bcm2835_spi_end();
}

int ecg::getSquarePeriod(){
    return msquareperiod;
}
int ecg::getMode(){
    return mode;
}

extern "C" {
     ecg* ecg_new(){ return new ecg();}
     void ecg_setBPM(ecg* ecg, int bpm){ecg ->setBPM(bpm);}
     void ecg_start(ecg* ecg){ ecg -> start();}
     void ecg_setCurve(ecg* ecg, const unsigned char curve){ ecg ->setCurve(curve);}
     int  ecg_getBPM(ecg* ecg){return ecg->getBPM();}
     int  ecg_getSquarePeriod(ecg* ecg){return ecg->getSquarePeriod();}
     int  ecg_getMode(ecg* ecg){return ecg->getMode();}
     void ecg_setNSR(ecg* ecg, int bpm){ecg->setNSR(bpm);}
     void ecg_setArrhythmia(ecg* ecg, int arrythmiaId){ecg->setArrhythmia(arrythmiaId);}
     void ecg_setSquare(ecg* ecg, int period, int highValue, int lowValue){ecg->setSquare(period, highValue, lowValue);}
}
