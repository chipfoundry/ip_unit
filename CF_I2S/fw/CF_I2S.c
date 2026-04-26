/*
	Copyright 2024-2025 ChipFoundry, a DBA of Umbralogic Technologies LLC.

	Original Copyright 2024 Efabless Corp.
	Author: Efabless Corp. (ip_admin@efabless.com)

	Licensed under the Apache License, Version 2.0 (the "License");
	you may not use this file except in compliance with the License.
	You may obtain a copy of the License at

	    http://www.apache.org/licenses/LICENSE-2.0

	Unless required by applicable law or agreed to in writing, software
	distributed under the License is distributed on an "AS IS" BASIS,
	WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
	See the License for the specific language governing permissions and
	limitations under the License.

*/


/*! \file CF_I2C.c
    \brief C file for I2S APIs which contains the function implementations 
    
*/

#ifndef CF_I2S_C
#define CF_I2S_C


/******************************************************************************
* Includes
******************************************************************************/
#include "CF_I2S.h"

/******************************************************************************
* File-Specific Macros and Constants
******************************************************************************/



/******************************************************************************
* Static Variables
******************************************************************************/



/******************************************************************************
* Static Function Prototypes
******************************************************************************/



/******************************************************************************
* Function Definitions
******************************************************************************/


CF_DRIVER_STATUS CF_I2S_setGclkEnable (CF_I2S_TYPE_PTR i2s, uint32_t value){

    CF_DRIVER_STATUS status = CF_DRIVER_OK;

    if (i2s == NULL) {
        status = CF_DRIVER_ERROR_PARAMETER;     // Return CF_DRIVER_ERROR_PARAMETER if i2s is NULL
    } else if (value > (uint32_t)0x1) {  
        status = CF_DRIVER_ERROR_PARAMETER;     // Return CF_DRIVER_ERROR_PARAMETER if value is out of range
    }else {
        i2s->GCLK = value;                      // Set the GCLK enable bit to the given value
    }
    return status;
}

CF_DRIVER_STATUS CF_I2S_enable (CF_I2S_TYPE_PTR i2s){

    CF_DRIVER_STATUS status = CF_DRIVER_OK;

    if (i2s == NULL) {
        status = CF_DRIVER_ERROR_PARAMETER;     // Return CF_DRIVER_ERROR_PARAMETER if i2s is NULL
    }
    else{
        i2s->CTRL |= CF_I2S_CTRL_REG_EN_MASK;
    }
    return status;
}

CF_DRIVER_STATUS CF_I2S_disable (CF_I2S_TYPE_PTR i2s){
    
    CF_DRIVER_STATUS status = CF_DRIVER_OK;

    if (i2s == NULL) {
        status = CF_DRIVER_ERROR_PARAMETER;     // Return CF_DRIVER_ERROR_PARAMETER if i2s is NULL
    }
    else{
        i2s->CTRL &= ~CF_I2S_CTRL_REG_EN_MASK;
    }
    return status;
}


CF_DRIVER_STATUS CF_I2S_enableFifo(CF_I2S_TYPE_PTR i2s){

    CF_DRIVER_STATUS status = CF_DRIVER_OK;

    if (i2s == NULL) {
        status = CF_DRIVER_ERROR_PARAMETER;     // Return CF_DRIVER_ERROR_PARAMETER if i2s is NULL
    }
    else{
        i2s->CTRL |= CF_I2S_CTRL_REG_FIFO_EN_MASK;
    }
    return status;
}


CF_DRIVER_STATUS CF_I2S_disableFifo(CF_I2S_TYPE_PTR i2s){

    CF_DRIVER_STATUS status = CF_DRIVER_OK;

    if (i2s == NULL) {
        status = CF_DRIVER_ERROR_PARAMETER;     // Return CF_DRIVER_ERROR_PARAMETER if i2s is NULL
    }
    else{
        i2s->CTRL &= ~CF_I2S_CTRL_REG_FIFO_EN_MASK;
    }
    return status;
}


CF_DRIVER_STATUS CF_I2S_enableAVG(CF_I2S_TYPE_PTR i2s){

    CF_DRIVER_STATUS status = CF_DRIVER_OK;

    if (i2s == NULL) {
        status = CF_DRIVER_ERROR_PARAMETER;     // Return CF_DRIVER_ERROR_PARAMETER if i2s is NULL
    }
    else{
        i2s->CTRL |= CF_I2S_CTRL_REG_AVG_EN_MASK;
    }
    return status;
}


CF_DRIVER_STATUS CF_I2S_disableAVG(CF_I2S_TYPE_PTR i2s){

    CF_DRIVER_STATUS status = CF_DRIVER_OK;

    if (i2s == NULL) {
        status = CF_DRIVER_ERROR_PARAMETER;     // Return CF_DRIVER_ERROR_PARAMETER if i2s is NULL
    }
    else{
        i2s->CTRL &= ~CF_I2S_CTRL_REG_AVG_EN_MASK;
    }
    return status;
}


CF_DRIVER_STATUS CF_I2S_enableZCR(CF_I2S_TYPE_PTR i2s){

    CF_DRIVER_STATUS status = CF_DRIVER_OK;

    if (i2s == NULL) {
        status = CF_DRIVER_ERROR_PARAMETER;     // Return CF_DRIVER_ERROR_PARAMETER if i2s is NULL
    }
    else{
        i2s->CTRL |= CF_I2S_CTRL_REG_ZCR_EN_MASK;
    }
    return status;
}

CF_DRIVER_STATUS CF_I2S_disableZCR(CF_I2S_TYPE_PTR i2s){

    CF_DRIVER_STATUS status = CF_DRIVER_OK;

    if (i2s == NULL) {
        status = CF_DRIVER_ERROR_PARAMETER;     // Return CF_DRIVER_ERROR_PARAMETER if i2s is NULL
    }
    else{
        i2s->CTRL &= ~CF_I2S_CTRL_REG_ZCR_EN_MASK;
    }
    return status;
}



CF_DRIVER_STATUS CF_I2S_setConfigReg (CF_I2S_TYPE_PTR i2s, uint32_t config){
    
    CF_DRIVER_STATUS status = CF_DRIVER_OK;

    if (i2s == NULL) {
        status = CF_DRIVER_ERROR_PARAMETER;     // Return CF_DRIVER_ERROR_PARAMETER if i2s is NULL
    } else if (config > CF_I2S_CFG_REG_MAX_VALUE) {
        status = CF_DRIVER_ERROR_PARAMETER;     // Return CF_DRIVER_ERROR_PARAMETER if config is out of range
    }else {
        i2s->CFG = config;                      // Set the configuration register to the given value
    }
    return status;
}


CF_DRIVER_STATUS CF_I2S_setPrescaler(CF_I2S_TYPE_PTR i2s, uint32_t prescaler){
    
    CF_DRIVER_STATUS status = CF_DRIVER_OK;

    if (i2s == NULL) {
        status = CF_DRIVER_ERROR_PARAMETER;     // Return CF_DRIVER_ERROR_PARAMETER if i2s is NULL
    } else if (prescaler > CF_I2S_PR_REG_MAX_VALUE) {
        status = CF_DRIVER_ERROR_PARAMETER;     // Return CF_DRIVER_ERROR_PARAMETER if prescaler is out of range
    }else {
        i2s->PR = prescaler;                    // Set the prescaler register to the given value
    }
    return status;
}


CF_DRIVER_STATUS CF_I2S_setAVGT(CF_I2S_TYPE_PTR i2s, uint32_t average){
    
    CF_DRIVER_STATUS status = CF_DRIVER_OK;

    if (i2s == NULL) {
        status = CF_DRIVER_ERROR_PARAMETER;     // Return CF_DRIVER_ERROR_PARAMETER if i2s is NULL
    } else if (average > CF_I2S_AVGT_REG_MAX_VALUE) {
        status = CF_DRIVER_ERROR_PARAMETER;     // Return CF_DRIVER_ERROR_PARAMETER if average is out of range
    }else {
        i2s->AVGT = average;                    // Set the AVGT register to the given value
    }
    return status;
}


CF_DRIVER_STATUS CF_I2S_setZCRT(CF_I2S_TYPE_PTR i2s, uint32_t average){
    
    CF_DRIVER_STATUS status = CF_DRIVER_OK;

    if (i2s == NULL) {
        status = CF_DRIVER_ERROR_PARAMETER;     // Return CF_DRIVER_ERROR_PARAMETER if i2s is NULL
    } else if (average > CF_I2S_ZCRT_REG_MAX_VALUE) {
        status = CF_DRIVER_ERROR_PARAMETER;     // Return CF_DRIVER_ERROR_PARAMETER if average is out of range
    }else {
        i2s->ZCRT = average;                    // Set the ZCRT register to the given value
    }
    return status;
}

CF_DRIVER_STATUS CF_I2S_getRxFifoLevel(CF_I2S_TYPE_PTR i2s, uint32_t* level){
    
    CF_DRIVER_STATUS status = CF_DRIVER_OK;

    if (i2s == NULL) {
        status = CF_DRIVER_ERROR_PARAMETER;     // Return CF_DRIVER_ERROR_PARAMETER if i2s is NULL
    } else if (level == NULL) {
        status = CF_DRIVER_ERROR_PARAMETER;     // Return CF_DRIVER_ERROR_PARAMETER if level is NULL
    } else {
        *level = i2s->RX_FIFO_LEVEL;            // Get the RX FIFO level
    }
    return status;
}

CF_DRIVER_STATUS CF_I2S_setRxFifoThreshold(CF_I2S_TYPE_PTR i2s, uint32_t threshold){

    CF_DRIVER_STATUS status = CF_DRIVER_OK;

    if (i2s == NULL) {
        status = CF_DRIVER_ERROR_PARAMETER;     // Return CF_DRIVER_ERROR_PARAMETER if i2s is NULL
    } else if (threshold > CF_I2S_RX_FIFO_THRESHOLD_REG_MAX_VALUE) {
        status = CF_DRIVER_ERROR_PARAMETER;     // Return CF_DRIVER_ERROR_PARAMETER if average is out of range
    } else {
        i2s->RX_FIFO_THRESHOLD = threshold;
    }
    return status;

}


CF_DRIVER_STATUS CF_I2S_getRIS(CF_I2S_TYPE_PTR i2s, uint32_t* ris_value){

    CF_DRIVER_STATUS status = CF_DRIVER_OK;

    if (i2s == NULL) {
        status = CF_DRIVER_ERROR_PARAMETER;     // Return CF_DRIVER_ERROR_PARAMETER if i2s is NULL
    } else if (ris_value == NULL){
        status = CF_DRIVER_ERROR_PARAMETER;     // Return CF_DRIVER_ERROR_PARAMETER if ris_value is NULL
    } else {
        *ris_value = i2s->RIS;
    }
    return status;
}


CF_DRIVER_STATUS CF_I2S_getMIS(CF_I2S_TYPE_PTR i2s, uint32_t* mis_value){

    CF_DRIVER_STATUS status = CF_DRIVER_OK;

    if (i2s == NULL) {
        status = CF_DRIVER_ERROR_PARAMETER;     // Return CF_DRIVER_ERROR_PARAMETER if i2s is NULL
    } else if (mis_value == NULL){
        status = CF_DRIVER_ERROR_PARAMETER;     // Return CF_DRIVER_ERROR_PARAMETER if mis_value is NULL
    } else {
        *mis_value = i2s->MIS;
    }
    return status;
}



CF_DRIVER_STATUS CF_I2S_setIM(CF_I2S_TYPE_PTR i2s, uint32_t mask){
    
    CF_DRIVER_STATUS status = CF_DRIVER_OK;

    if (i2s == NULL) {
        status = CF_DRIVER_ERROR_PARAMETER;     // Return CF_DRIVER_ERROR_PARAMETER if i2s is NULL
    }else if (mask > CF_I2S_RX_FIFO_IM_REG_MAX_VALUE){
        status = CF_DRIVER_ERROR_PARAMETER;     // Return CF_DRIVER_ERROR_PARAMETER if mask is out of range
    } else {
        i2s->IM = mask;
    }
    return status;
}


CF_DRIVER_STATUS CF_I2S_setIC(CF_I2S_TYPE_PTR i2s, uint32_t mask){
    
    CF_DRIVER_STATUS status = CF_DRIVER_OK;

    if (i2s == NULL) {
        status = CF_DRIVER_ERROR_PARAMETER;     // Return CF_DRIVER_ERROR_PARAMETER if i2s is NULL
    }else if (mask > CF_I2S_RX_FIFO_IC_REG_MAX_VALUE){
        status = CF_DRIVER_ERROR_PARAMETER;     // Return CF_DRIVER_ERROR_PARAMETER if mask is out of range
    } else {
        i2s->IC = mask;
    }
    return status;
}



CF_DRIVER_STATUS CF_I2S_getIM(CF_I2S_TYPE_PTR i2s, uint32_t* im_value){
    
    CF_DRIVER_STATUS status = CF_DRIVER_OK;

    if (i2s == NULL) {
        status = CF_DRIVER_ERROR_PARAMETER;     // Return CF_DRIVER_ERROR_PARAMETER if i2s is NULL
    }else if (im_value == NULL){
        status = CF_DRIVER_ERROR_PARAMETER;     // Return CF_DRIVER_ERROR_PARAMETER if im_value is NULL
    } else {
        *im_value = i2s->IM;
    }
    return status;
}

CF_DRIVER_STATUS CF_I2S_readData(CF_I2S_TYPE_PTR i2s, uint32_t* data){
    
    CF_DRIVER_STATUS status = CF_DRIVER_OK;

    if (i2s == NULL) {
        status = CF_DRIVER_ERROR_PARAMETER;     // Return CF_DRIVER_ERROR_PARAMETER if i2s is NULL
    }
    else if (data == NULL){
        status = CF_DRIVER_ERROR_PARAMETER;     // Return CF_DRIVER_ERROR_PARAMETER if data is NULL
    } else {
        uint32_t ris_value;
        do {
            // wait until RX FIFO is not empty
            status = CF_I2S_getRIS(i2s, &ris_value);
        }
        while((status == CF_DRIVER_OK)&&((ris_value & CF_I2S_FIFOA_FLAG) == (uint32_t)0x0)); // wait over RX fifo is above Flag to unset  

        if (status==CF_DRIVER_OK){
            *data = i2s->RXDATA;
            status = CF_I2S_clearIrqRxLevel(i2s);
        }else{}
    }
    return status;
}


CF_DRIVER_STATUS CF_I2S_clearIrqRxempty(CF_I2S_TYPE_PTR i2s){

    CF_DRIVER_STATUS status = CF_DRIVER_OK;

    if (i2s == NULL) {
        status = CF_DRIVER_ERROR_PARAMETER;     // Return CF_DRIVER_ERROR_PARAMETER if i2s is NULL
    }else{
        status = CF_I2S_setIC(i2s, CF_I2S_FIFOE_FLAG);
    }
    return status;
}


CF_DRIVER_STATUS CF_I2S_clearIrqRxLevel(CF_I2S_TYPE_PTR i2s){

    CF_DRIVER_STATUS status = CF_DRIVER_OK;

    if (i2s == NULL) {
        status = CF_DRIVER_ERROR_PARAMETER;     // Return CF_DRIVER_ERROR_PARAMETER if i2s is NULL
    }else{
        status = CF_I2S_setIC(i2s, CF_I2S_FIFOA_FLAG);
    }
    return status;
}


CF_DRIVER_STATUS CF_I2S_clearIrqRxFull(CF_I2S_TYPE_PTR i2s){
    
    CF_DRIVER_STATUS status = CF_DRIVER_OK;

    if (i2s == NULL) {
        status = CF_DRIVER_ERROR_PARAMETER;     // Return CF_DRIVER_ERROR_PARAMETER if i2s is NULL
    }else{
        status = CF_I2S_setIC(i2s, CF_I2S_FIFOF_FLAG);
    }
    return status;
}


CF_DRIVER_STATUS CF_I2S_clearIrqAVGAboveThreshold(CF_I2S_TYPE_PTR i2s){
    
    CF_DRIVER_STATUS status = CF_DRIVER_OK;

    if (i2s == NULL) {
        status = CF_DRIVER_ERROR_PARAMETER;     // Return CF_DRIVER_ERROR_PARAMETER if i2s is NULL
    }else{
        status = CF_I2S_setIC(i2s, CF_I2S_AVGF_FLAG);
    }
    return status;
}



CF_DRIVER_STATUS CF_I2S_clearIrqZCRAboveThreshold(CF_I2S_TYPE_PTR i2s){
    
    CF_DRIVER_STATUS status = CF_DRIVER_OK;

    if (i2s == NULL) {
        status = CF_DRIVER_ERROR_PARAMETER;     // Return CF_DRIVER_ERROR_PARAMETER if i2s is NULL
    }else{
        status = CF_I2S_setIC(i2s, CF_I2S_ZCRF_FLAG);       
    }
    return status;
}



CF_DRIVER_STATUS CF_I2S_clearIrqVADFlag(CF_I2S_TYPE_PTR i2s){
    
    CF_DRIVER_STATUS status = CF_DRIVER_OK;

    if (i2s == NULL) {
        status = CF_DRIVER_ERROR_PARAMETER;     // Return CF_DRIVER_ERROR_PARAMETER if i2s is NULL
    }else{
        status = CF_I2S_setIC(i2s, CF_I2S_VADF_FLAG);
    }
    return status;
}

CF_DRIVER_STATUS CF_I2S_RxFIFOAvailable(CF_I2S_TYPE_PTR i2s, bool* isAvailable){
    CF_DRIVER_STATUS status = CF_DRIVER_OK;
    uint32_t ris_value;
    if (i2s == NULL) {
        status = CF_DRIVER_ERROR_PARAMETER;     // Return CF_DRIVER_ERROR_PARAMETER if i2s is NULL
    }else if (isAvailable == NULL){
        status = CF_DRIVER_ERROR_PARAMETER;     // Return CF_DRIVER_ERROR_PARAMETER if isAvailable is NULL
    } else {
        status = CF_I2S_getRIS(i2s, &ris_value);
        if((ris_value & CF_I2S_FIFOF_FLAG) != (uint32_t)0x0){   // check if RX FIFO is full
            *isAvailable = false;
        }else{
            *isAvailable = true;
        }
    }
    return status;
}



CF_DRIVER_STATUS CF_I2S_RxFIFOEmpty(CF_I2S_TYPE_PTR i2s, bool* isEmpty){
    CF_DRIVER_STATUS status = CF_DRIVER_OK;
    uint32_t ris_value;
    if (i2s == NULL) {
        status = CF_DRIVER_ERROR_PARAMETER;     // Return CF_DRIVER_ERROR_PARAMETER if i2s is NULL
    }else if (isEmpty == NULL){
        status = CF_DRIVER_ERROR_PARAMETER;     // Return CF_DRIVER_ERROR_PARAMETER if isEmpty is NULL
    } else {
        status = CF_I2S_getRIS(i2s, &ris_value);
        if((ris_value & CF_I2S_FIFOE_FLAG)!= (uint32_t)0x0){   // check if RX FIFO is empty
            *isEmpty = true;
        }else{
            *isEmpty = false;
        }
    }
    return status;
}



CF_DRIVER_STATUS CF_I2S_RxFIFOFull(CF_I2S_TYPE_PTR i2s, bool* isFull){
    CF_DRIVER_STATUS status = CF_DRIVER_OK;
    uint32_t ris_value;
    if (i2s == NULL) {
        status = CF_DRIVER_ERROR_PARAMETER;     // Return CF_DRIVER_ERROR_PARAMETER if i2s is NULL
    }else if (isFull == NULL){
        status = CF_DRIVER_ERROR_PARAMETER;     // Return CF_DRIVER_ERROR_PARAMETER if isFull is NULL
    } else {
        status = CF_I2S_getRIS(i2s, &ris_value);
        if((ris_value & CF_I2S_FIFOF_FLAG)!= (uint32_t)0x0){   // check if RX FIFO is full
            *isFull = true;
        }else{
            *isFull = false;
        }
    }
    return status;
}


CF_DRIVER_STATUS CF_I2S_Busy(CF_I2S_TYPE_PTR i2s, bool* isBusy){
    CF_DRIVER_STATUS status = CF_DRIVER_OK;
    uint32_t ris_value;
    if (i2s == NULL) {
        status = CF_DRIVER_ERROR_PARAMETER;     // Return CF_DRIVER_ERROR_PARAMETER if i2s is NULL
    }else if (isBusy == NULL){
        status = CF_DRIVER_ERROR_PARAMETER;     // Return CF_DRIVER_ERROR_PARAMETER if isBusy is NULL
    } else {
        status = CF_I2S_getRIS(i2s, &ris_value);
        if((ris_value & CF_I2S_FIFOE_FLAG)!= (uint32_t)0x0){   // check if RX FIFO is full
            *isBusy = false;
        }else{
            *isBusy = true;
        }
    }
    return status;
}


CF_DRIVER_STATUS CF_I2S_FIFOOverThreshold(CF_I2S_TYPE_PTR i2s, bool* isOverThreshold){
    CF_DRIVER_STATUS status = CF_DRIVER_OK;
    uint32_t ris_value;
    if (i2s == NULL) {
        status = CF_DRIVER_ERROR_PARAMETER;     // Return CF_DRIVER_ERROR_PARAMETER if i2s is NULL
    }else if (isOverThreshold == NULL){
        status = CF_DRIVER_ERROR_PARAMETER;     // Return CF_DRIVER_ERROR_PARAMETER if isOverThreshold is NULL
    } else {
        status = CF_I2S_getRIS(i2s, &ris_value);
        if((ris_value & CF_I2S_FIFOA_FLAG)!= (uint32_t)0x0){   // check if RX FIFO is full
            *isOverThreshold = true;
        }else{
            *isOverThreshold = false;
        }
    }
    return status;
}


CF_DRIVER_STATUS CF_I2S_ZCROverThreshold(CF_I2S_TYPE_PTR i2s, bool* isOverThreshold){
    CF_DRIVER_STATUS status = CF_DRIVER_OK;
    uint32_t ris_value;
    if (i2s == NULL) {
        status = CF_DRIVER_ERROR_PARAMETER;     // Return CF_DRIVER_ERROR_PARAMETER if i2s is NULL
    }else if (isOverThreshold == NULL){
        status = CF_DRIVER_ERROR_PARAMETER;     // Return CF_DRIVER_ERROR_PARAMETER if isOverThreshold is NULL
    } else {
        status = CF_I2S_getRIS(i2s, &ris_value);
        if((ris_value & CF_I2S_ZCRF_FLAG)!= (uint32_t)0x0){   // check if RX FIFO is full
            *isOverThreshold = true;
        }else{
            *isOverThreshold = false;
        }
    }
    return status;
}


CF_DRIVER_STATUS CF_I2S_VADFlag(CF_I2S_TYPE_PTR i2s, bool* isOverThreshold){
    CF_DRIVER_STATUS status = CF_DRIVER_OK;
    uint32_t ris_value;
    if (i2s == NULL) {
        status = CF_DRIVER_ERROR_PARAMETER;     // Return CF_DRIVER_ERROR_PARAMETER if i2s is NULL
    }else if (isOverThreshold == NULL){
        status = CF_DRIVER_ERROR_PARAMETER;     // Return CF_DRIVER_ERROR_PARAMETER if isOverThreshold is NULL
    } else {
        status = CF_I2S_getRIS(i2s, &ris_value);
        if((ris_value & CF_I2S_VADF_FLAG)!= (uint32_t)0x0){     // check if RX FIFO is full
            *isOverThreshold = true;
        }else{
            *isOverThreshold = false;
        }
    }
    return status;
}


/******************************************************************************
* Static Function Definitions
******************************************************************************/



#endif // CF_I2S_C

/******************************************************************************
* End of File
******************************************************************************/