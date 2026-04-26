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


/*! \file CF_I2S.h
    \brief C header file for I2S APIs which contains the function prototypes 
    
*/

#ifndef CF_I2S_H
#define CF_I2S_H

/******************************************************************************
* Includes
******************************************************************************/
#include "CF_Driver_Common.h"

/******************************************************************************
* Macros and Constants
******************************************************************************/

#define CF_I2S_CTRL_REG_EN_BIT	                    ((uint32_t)0)
#define CF_I2S_CTRL_REG_EN_MASK	                    ((uint32_t)0x1)
#define CF_I2S_CTRL_REG_FIFO_EN_BIT	                ((uint32_t)1)
#define CF_I2S_CTRL_REG_FIFO_EN_MASK	            ((uint32_t)0x2)
#define CF_I2S_CTRL_REG_AVG_EN_BIT	                ((uint32_t)2)
#define CF_I2S_CTRL_REG_AVG_EN_MASK	                ((uint32_t)0x4)
#define CF_I2S_CTRL_REG_ZCR_EN_BIT	                ((uint32_t)3)
#define CF_I2S_CTRL_REG_ZCR_EN_MASK	                ((uint32_t)0x8)
#define CF_I2S_CFG_REG_CHANNELS_BIT	                ((uint32_t)0)
#define CF_I2S_CFG_REG_CHANNELS_MASK	            ((uint32_t)0x3)
#define CF_I2S_CFG_REG_SIGN_EXTEND_BIT	            ((uint32_t)2)
#define CF_I2S_CFG_REG_SIGN_EXTEND_MASK	            ((uint32_t)0x4)
#define CF_I2S_CFG_REG_LEFT_JUSTIFIED_BIT	        ((uint32_t)3)
#define CF_I2S_CFG_REG_LEFT_JUSTIFIED_MASK	        ((uint32_t)0x8)
#define CF_I2S_CFG_REG_SAMPLE_SIZE_BIT	            ((uint32_t)4)
#define CF_I2S_CFG_REG_SAMPLE_SIZE_MASK	            ((uint32_t)0x3f0)
#define CF_I2S_CFG_REG_AVGSEL_BIT	                ((uint32_t)10)
#define CF_I2S_CFG_REG_AVGSEL_MASK	                ((uint32_t)0x400)
#define CF_I2S_CFG_REG_ZCRSEL_BIT	                ((uint32_t)11)
#define CF_I2S_CFG_REG_ZCRSEL_MASK	                ((uint32_t)0x800)
#define CF_I2S_RX_FIFO_LEVEL_REG_LEVEL_BIT	        ((uint32_t)0)
#define CF_I2S_RX_FIFO_LEVEL_REG_LEVEL_MASK	        ((uint32_t)0xf)
#define CF_I2S_RX_FIFO_THRESHOLD_REG_THRESHOLD_BIT	((uint32_t)0)
#define CF_I2S_RX_FIFO_THRESHOLD_REG_THRESHOLD_MASK	((uint32_t)0xf)
#define CF_I2S_RX_FIFO_FLUSH_REG_FLUSH_BIT	        ((uint32_t)0)
#define CF_I2S_RX_FIFO_FLUSH_REG_FLUSH_MASK	        ((uint32_t)0x1)
#define CF_I2S_FIFOE_FLAG	                        ((uint32_t)0x1)
#define CF_I2S_FIFOA_FLAG	                        ((uint32_t)0x2)
#define CF_I2S_FIFOF_FLAG	                        ((uint32_t)0x4)
#define CF_I2S_AVGF_FLAG	                        ((uint32_t)0x8)
#define CF_I2S_ZCRF_FLAG	                        ((uint32_t)0x10)
#define CF_I2S_VADF_FLAG	                        ((uint32_t)0x20)


#define CF_I2S_CFG_REG_MAX_VALUE                    ((uint32_t)0x00000FFF)                      // 12 bits
#define CF_I2S_PR_REG_MAX_VALUE                     ((uint32_t)0x000000FF)                      // 8 bits
#define CF_I2S_AVGT_REG_MAX_VALUE                   ((uint32_t)0x0000FFFF)                      // 16 bits
#define CF_I2S_ZCRT_REG_MAX_VALUE                   ((uint32_t)0x0000FFFF)                      // 16 bits
#define CF_I2S_RX_FIFO_THRESHOLD_REG_MAX_VALUE      ((uint32_t)0x0000000F)                      // 4 bits
#define CF_I2S_RX_FIFO_IM_REG_MAX_VALUE             ((uint32_t)0x0000003F)                      // 6 bits
#define CF_I2S_RX_FIFO_IC_REG_MAX_VALUE             ((uint32_t)0x0000003F)                      // 6 bits



/******************************************************************************
* Typedefs and Enums
******************************************************************************/
typedef struct _CF_I2S_TYPE_ {
	__R 	RXDATA;
	__W 	PR;
	__W 	AVGT;
	__W 	ZCRT;
	__W 	CTRL;
	__W 	CFG;
	__R 	reserved_0[16250];
	__R 	RX_FIFO_LEVEL;
	__W 	RX_FIFO_THRESHOLD;
	__W 	RX_FIFO_FLUSH;
	__R 	reserved_1[61];
	__RW	IM;
	__R 	MIS;
	__R 	RIS;
	__W 	IC;
	__W 	GCLK;
} CF_I2S_TYPE;

typedef CF_I2S_TYPE*   CF_I2S_TYPE_PTR;               // CF_I2S Type Pointer


/******************************************************************************
* Function Prototypes
******************************************************************************/
//! Sets the GCLK enable bit in the I2S register to a certain value
    /*!
        \param [in] i2s An \ref CF_I2S_TYPE_PTR , which points to the base memory address of I2S registers. \ref CF_I2S_TYPE is a structure that contains the I2S registers.
        \param [in] value The value of the GCLK enable bit
        
        \return status A value of type \ref CF_DRIVER_STATUS : returns a success or error code 
    */
CF_DRIVER_STATUS CF_I2S_setGclkEnable (CF_I2S_TYPE_PTR i2s, uint32_t value);


//! Enables the I2S peripheral.
/*!
    This function enables the I2S peripheral by setting the enable bit in the control register.

    \param [in] i2s Pointer to the I2S base address structure \ref CF_I2S_TYPE_PTR.

    \return status A value of type \ref CF_DRIVER_STATUS : returns a success or error code.
*/
CF_DRIVER_STATUS CF_I2S_enable (CF_I2S_TYPE_PTR i2s);



//! Disables the I2S peripheral.
/*!
    This function disables the I2S peripheral by clearing the enable bit in the control register.

    \param [in] i2s Pointer to the I2S base address structure \ref CF_I2S_TYPE_PTR.

    \return status A value of type \ref CF_DRIVER_STATUS : returns a success or error code.
*/
CF_DRIVER_STATUS CF_I2S_disable (CF_I2S_TYPE_PTR i2s);


//! Enables the FIFO feature for the I2S peripheral.
/*!
    This function enables the FIFO feature of the I2S peripheral by setting the FIFO enable bit in the control register.

    \param [in] i2s Pointer to the I2S base address structure \ref CF_I2S_TYPE_PTR.

    \return status A value of type \ref CF_DRIVER_STATUS : returns a success or error code.
*/
CF_DRIVER_STATUS CF_I2S_enableFifo(CF_I2S_TYPE_PTR i2s);



//! Disables the FIFO feature for the I2S peripheral.
/*!
    This function disables the FIFO feature of the I2S peripheral by clearing the FIFO enable bit in the control register.

    \param [in] i2s Pointer to the I2S base address structure \ref CF_I2S_TYPE_PTR.

    \return status A value of type \ref CF_DRIVER_STATUS : returns a success or error code.
*/
CF_DRIVER_STATUS CF_I2S_disableFifo(CF_I2S_TYPE_PTR i2s);


//! Enables the AVG feature for the I2S peripheral.
/*!
    This function enables the AVG feature of the I2S peripheral by setting the AVG enable bit in the control register.

    \param [in] i2s Pointer to the I2S base address structure \ref CF_I2S_TYPE_PTR.

    \return status A value of type \ref CF_DRIVER_STATUS : returns a success or error code.
*/
CF_DRIVER_STATUS CF_I2S_enableAVG(CF_I2S_TYPE_PTR i2s);


//! Disables the AVG feature for the I2S peripheral.
/*!
    This function disables the AVG feature of the I2S peripheral by clearing the AVG enable bit in the control register.

    \param [in] i2s Pointer to the I2S base address structure \ref CF_I2S_TYPE_PTR.

    \return status A value of type \ref CF_DRIVER_STATUS : returns a success or error code.
*/
CF_DRIVER_STATUS CF_I2S_disableAVG(CF_I2S_TYPE_PTR i2s);




//! Enables the ZCR feature for the I2S peripheral.
/*!
    This function enables the ZCR feature of the I2S peripheral by setting the ZCR enable bit in the control register.

    \param [in] i2s Pointer to the I2S base address structure \ref CF_I2S_TYPE_PTR.

    \return status A value of type \ref CF_DRIVER_STATUS : returns a success or error code.
*/
CF_DRIVER_STATUS CF_I2S_enableZCR(CF_I2S_TYPE_PTR i2s);



//! Disables the ZCR feature for the I2S peripheral.
/*!
    This function disables the ZCR feature of the I2S peripheral by clearing the ZCR enable bit in the control register.

    \param [in] i2s Pointer to the I2S base address structure \ref CF_I2S_TYPE_PTR.

    \return status A value of type \ref CF_DRIVER_STATUS : returns a success or error code.
*/
CF_DRIVER_STATUS CF_I2S_disableZCR(CF_I2S_TYPE_PTR i2s);



//! Sets the configuration register for the I2S peripheral.
/*!
    This function sets the configuration register of the I2S peripheral to the specified value. It validates the input parameters 
    to ensure the I2S pointer is not NULL and the configuration value is within the allowed range.

    \param [in] i2s    Pointer to the I2S base address structure \ref CF_I2S_TYPE_PTR.
    \param [in] config The configuration value to be set. Must be less than or equal to \ref CF_I2S_CFG_REG_MAX_VALUE.

    \return status A value of type \ref CF_DRIVER_STATUS : returns a success or error code.
*/
CF_DRIVER_STATUS CF_I2S_setConfigReg (CF_I2S_TYPE_PTR i2s, uint32_t config);



//! Sets the prescaler register for the I2S peripheral.
/*!
    This function configures the prescaler register of the I2S peripheral with the specified value. It ensures that 
    the I2S pointer is not NULL and that the prescaler value is within the valid range.

    \param [in] i2s       Pointer to the I2S base address structure \ref CF_I2S_TYPE_PTR.
    \param [in] prescaler The prescaler value to be set. Must be less than or equal to \ref CF_I2S_PR_REG_MAX_VALUE.

    \return status A value of type \ref CF_DRIVER_STATUS : returns a success or error code.
*/
CF_DRIVER_STATUS CF_I2S_setPrescaler(CF_I2S_TYPE_PTR i2s, uint32_t prescaler);



//! Sets the AVGT register for the I2S peripheral.
/*!
    This function sets the average threshold (AVGT) register for the I2S peripheral to the specified value. 
    It ensures that the input pointer and average value are valid.

    \param [in] i2s     Pointer to the I2S base address structure \ref CF_I2S_TYPE_PTR.
    \param [in] average The average threshold value to be set. Must be less than or equal to \ref CF_I2S_AVGT_REG_MAX_VALUE.

    \return status A value of type \ref CF_DRIVER_STATUS : returns a success or error code.
*/
CF_DRIVER_STATUS CF_I2S_setAVGT(CF_I2S_TYPE_PTR i2s, uint32_t average);


//! Sets the ZCRT register for the I2S peripheral.
/*!
    This function sets the zero-crossing threshold (ZCRT) register for the I2S peripheral to the specified value. 
    It validates the input pointer and the threshold value.

    \param [in] i2s     Pointer to the I2S base address structure \ref CF_I2S_TYPE_PTR.
    \param [in] average The zero-crossing threshold value to be set. Must be less than or equal to \ref CF_I2S_ZCRT_REG_MAX_VALUE.

    \return status A value of type \ref CF_DRIVER_STATUS : returns a success or error code.
*/
CF_DRIVER_STATUS CF_I2S_setZCRT(CF_I2S_TYPE_PTR i2s, uint32_t average);



//! Gets the RX FIFO level of the I2S peripheral.
/*!
    This function retrieves the current level of the RX FIFO register from the I2S peripheral 
    and stores it in the memory location pointed to by `level`.

    \param [in] i2s    Pointer to the I2S base address structure \ref CF_I2S_TYPE_PTR.
    \param [out] level Pointer to a variable where the RX FIFO level will be stored.

    \return status A value of type \ref CF_DRIVER_STATUS : returns a success or error code.
*/
CF_DRIVER_STATUS CF_I2S_getRxFifoLevel(CF_I2S_TYPE_PTR i2s, uint32_t* level);



//! Sets the RX FIFO threshold for the I2S peripheral.
/*!
    This function sets the RX FIFO threshold register for the I2S peripheral to the specified value.
    It ensures that the input pointer and threshold value are valid.

    \param [in] i2s       Pointer to the I2S base address structure \ref CF_I2S_TYPE_PTR.
    \param [in] threshold The RX FIFO threshold value to be set. Must be less than or equal to \ref CF_I2S_RX_FIFO_THRESHOLD_REG_MAX_VALUE.

    \return status A value of type \ref CF_DRIVER_STATUS : returns a success or error code.
*/
CF_DRIVER_STATUS CF_I2S_setRxFifoThreshold(CF_I2S_TYPE_PTR i2s, uint32_t threshold);



//! Reads the Raw Interrupt Status (RIS) register for the I2S peripheral.
/*!
    This function retrieves the value of the Raw Interrupt Status (RIS) register 
    for the I2S peripheral and stores it in the provided variable. The RIS register
    contains various status flags that indicate the state of the I2S peripheral.
    **RIS Register Breakdown**:
    - Bit 0:	FIFOE   - Receive FIFO is Empty
    - Bit 1:	FIFOA   - FIFO level is above the set level threshold
    - Bit 2:	FIFOF   - Receive FIFO is Full.
    - Bit 3:	AVGF    - The avg is above the threshold.
    - Bit 4:	ZCRF    - The ZCR is above the threshold.
    - Bit 5:	VADF    - The Voice Activity Detector flag; active when both ZCR & AVG flags are active.
    - Bits [6-31]: Reserved.


    \param [in]  i2s        Pointer to the I2S base address structure \ref CF_I2S_TYPE_PTR.
    \param [out] ris_value  Pointer to a variable where the RIS register value will be stored.

    \return status A value of type \ref CF_DRIVER_STATUS : returns a success or error code.

*/
CF_DRIVER_STATUS CF_I2S_getRIS(CF_I2S_TYPE_PTR i2s, uint32_t* ris_value);


//! Reads the Masked Interrupt Status (MIS) register for the I2S peripheral.
/*!
    This function retrieves the value of the Masked Interrupt Status (MIS) register 
    for the I2S peripheral and stores it in the provided variable. The MIS register 
    indicates the current interrupt status after masking.
    **RIS Register Breakdown**:
    - Bit 0:	FIFOE   - Receive FIFO is Empty
    - Bit 1:	FIFOA   - FIFO level is above the set level threshold
    - Bit 2:	FIFOF   - Receive FIFO is Full.
    - Bit 3:	AVGF    - The avg is above the threshold.
    - Bit 4:	ZCRF    - The ZCR is above the threshold.
    - Bit 5:	VADF    - The Voice Activity Detector flag; active when both ZCR & AVG flags are active.
    - Bits [6-31]: Reserved.

    \param [in]  i2s        Pointer to the I2S base address structure \ref CF_I2S_TYPE_PTR.
    \param [out] mis_value  Pointer to a variable where the MIS register value will be stored.

    \return status A value of type \ref CF_DRIVER_STATUS : returns a success or error code.

*/
CF_DRIVER_STATUS CF_I2S_getMIS(CF_I2S_TYPE_PTR i2s, uint32_t* mis_value);



//! Writes a value to the Interrupt Mask (IM) register for the I2S peripheral.
/*!
    This function sets the value of the Interrupt Mask (IM) register for the I2S peripheral. 
    The IM register determines which interrupts are enabled or disabled.
    **RIS Register Breakdown**:
    - Bit 0:	FIFOE   - Receive FIFO is Empty
    - Bit 1:	FIFOA   - FIFO level is above the set level threshold
    - Bit 2:	FIFOF   - Receive FIFO is Full.
    - Bit 3:	AVGF    - The avg is above the threshold.
    - Bit 4:	ZCRF    - The ZCR is above the threshold.
    - Bit 5:	VADF    - The Voice Activity Detector flag; active when both ZCR & AVG flags are active.
    - Bits [6-31]: Reserved.

    \param [in] i2s   Pointer to the I2S base address structure \ref CF_I2S_TYPE_PTR.
    \param [in] mask  The value to be written to the IM register. Must be within 
                      the valid range \ref CF_I2S_RX_FIFO_IM_REG_MAX_VALUE.

    \return status A value of type \ref CF_DRIVER_STATUS : returns a success or error code.
*/
CF_DRIVER_STATUS CF_I2S_setIM(CF_I2S_TYPE_PTR i2s, uint32_t mask);


//! Writes a value to the Interrupt Clear (IC) register for the I2S peripheral.
/*!
    This function clears specific interrupts in the I2S peripheral by writing to 
    the Interrupt Clear (IC) register.
    **RIS Register Breakdown**:
    - Bit 0:	FIFOE   - Receive FIFO is Empty
    - Bit 1:	FIFOA   - FIFO level is above the set level threshold
    - Bit 2:	FIFOF   - Receive FIFO is Full.
    - Bit 3:	AVGF    - The avg is above the threshold.
    - Bit 4:	ZCRF    - The ZCR is above the threshold.
    - Bit 5:	VADF    - The Voice Activity Detector flag; active when both ZCR & AVG flags are active.
    - Bits [6-31]: Reserved.

    \param [in] i2s   Pointer to the I2S base address structure \ref CF_I2S_TYPE_PTR.
    \param [in] mask  The value to be written to the IC register. Must be within 
                      the valid range \ref CF_I2S_RX_FIFO_IC_REG_MAX_VALUE.

    \return status A value of type \ref CF_DRIVER_STATUS : returns a success or error code.
*/
CF_DRIVER_STATUS CF_I2S_setIC(CF_I2S_TYPE_PTR i2s, uint32_t mask);


//! Reads the Interrupt Mask (IM) register for the I2S peripheral.
/*!
    This function retrieves the value of the Interrupt Mask (IM) register for the 
    I2S peripheral and stores it in the provided variable. The IM register indicates 
    which interrupts are enabled.
    **RIS Register Breakdown**:
    - Bit 0:	FIFOE   - Receive FIFO is Empty
    - Bit 1:	FIFOA   - FIFO level is above the set level threshold
    - Bit 2:	FIFOF   - Receive FIFO is Full.
    - Bit 3:	AVGF    - The avg is above the threshold.
    - Bit 4:	ZCRF    - The ZCR is above the threshold.
    - Bit 5:	VADF    - The Voice Activity Detector flag; active when both ZCR & AVG flags are active.
    - Bits [6-31]: Reserved.

    \param [in]  i2s       Pointer to the I2S base address structure \ref CF_I2S_TYPE_PTR.
    \param [out] im_value  Pointer to a variable where the IM register value will be stored.

    \return status A value of type \ref CF_DRIVER_STATUS : returns a success or error code.
*/
CF_DRIVER_STATUS CF_I2S_getIM(CF_I2S_TYPE_PTR i2s, uint32_t* im_value);


//! Reads data from the RX FIFO of the I2S peripheral.
/*!
    This function retrieves a data word from the RX FIFO of the specified I2S peripheral.
    It waits until the RX FIFO has data available before performing the read operation.
    After reading the data, the RX level interrupt is cleared.

    \param [in] i2s    Pointer to the I2S base address structure \ref CF_I2S_TYPE_PTR.
    \param [out] data  Pointer to a variable where the read data will be stored.

    \return status A value of type \ref CF_DRIVER_STATUS : returns a success or error code.

    \note The function uses a busy-wait loop to check the RX FIFO status. Ensure proper system design 
          to avoid potential blocking or infinite loops in case of hardware issues.
*/
CF_DRIVER_STATUS CF_I2S_readData(CF_I2S_TYPE_PTR i2s, uint32_t* data);



/*!
    This function clears the interrupt corresponding to the receive FIFO empty condition 
    in the I2S peripheral by writing to the Interrupt Clear (IC) register.

    \param [in] i2s  Pointer to the I2S base address structure \ref CF_I2S_TYPE_PTR.

    \return status A value of type \ref CF_DRIVER_STATUS : returns a success or error code.
*/
CF_DRIVER_STATUS CF_I2S_clearIrqRxempty(CF_I2S_TYPE_PTR i2s);




//! Clears the receive FIFO level interrupt for the I2S peripheral.
/*!
    This function clears the interrupt corresponding to the receive FIFO level condition 
    in the I2S peripheral by writing to the Interrupt Clear (IC) register.

    \param [in] i2s  Pointer to the I2S base address structure \ref CF_I2S_TYPE_PTR.

    \return status A value of type \ref CF_DRIVER_STATUS : returns a success or error code.
*/
CF_DRIVER_STATUS CF_I2S_clearIrqRxLevel(CF_I2S_TYPE_PTR i2s);



//! Clears the receive FIFO full interrupt for the I2S peripheral.
/*!
    This function clears the interrupt corresponding to the receive FIFO full condition 
    in the I2S peripheral by writing to the Interrupt Clear (IC) register.

    \param [in] i2s  Pointer to the I2S base address structure \ref CF_I2S_TYPE_PTR.

    \return status A value of type \ref CF_DRIVER_STATUS : returns a success or error code.
*/
CF_DRIVER_STATUS CF_I2S_clearIrqRxFull(CF_I2S_TYPE_PTR i2s);


//! Clears the average above threshold interrupt for the I2S peripheral.
/*!
    This function clears the interrupt corresponding to the average (AVG) being above the 
    threshold in the I2S peripheral by writing to the Interrupt Clear (IC) register.

    \param [in] i2s  Pointer to the I2S base address structure \ref CF_I2S_TYPE_PTR.

    \return status A value of type \ref CF_DRIVER_STATUS : returns a success or error code.
*/
CF_DRIVER_STATUS CF_I2S_clearIrqAVGAboveThreshold(CF_I2S_TYPE_PTR i2s);





//! Clears the zero-crossing rate above threshold interrupt for the I2S peripheral.
/*!
    This function clears the interrupt corresponding to the zero-crossing rate (ZCR) being 
    above the threshold in the I2S peripheral by writing to the Interrupt Clear (IC) register.

    \param [in] i2s  Pointer to the I2S base address structure \ref CF_I2S_TYPE_PTR.

    \return status A value of type \ref CF_DRIVER_STATUS : returns a success or error code.

*/
CF_DRIVER_STATUS CF_I2S_clearIrqZCRAboveThreshold(CF_I2S_TYPE_PTR i2s);


//! Clears the Voice Activity Detector (VAD) flag interrupt for the I2S peripheral.
/*!
    This function clears the interrupt corresponding to the Voice Activity Detector (VAD) flag 
    in the I2S peripheral by writing to the Interrupt Clear (IC) register.

    \param [in] i2s  Pointer to the I2S base address structure \ref CF_I2S_TYPE_PTR.

    \return status A value of type \ref CF_DRIVER_STATUS : returns a success or error code.
*/
CF_DRIVER_STATUS CF_I2S_clearIrqVADFlag(CF_I2S_TYPE_PTR i2s);



//! Checks if the RX FIFO has available space in the I2S peripheral.
/*!
    This function checks whether the RX FIFO of the I2S peripheral has available space.

    \param [in] i2s          Pointer to the I2S base address structure \ref CF_I2S_TYPE_PTR.
    \param [out] isAvailable Pointer to a boolean variable that will be set to true if the RX FIFO 
                             has available space, or false if it is full.

    \return status A value of type \ref CF_DRIVER_STATUS : returns a success or error code.

*/

CF_DRIVER_STATUS CF_I2S_RxFIFOAvailable(CF_I2S_TYPE_PTR i2s, bool* isAvailable);



//! Checks if the RX FIFO is empty in the I2S peripheral.
/*!
    This function checks whether the RX FIFO of the I2S peripheral is empty.

    \param [in] i2s      Pointer to the I2S base address structure \ref CF_I2S_TYPE_PTR.
    \param [out] isEmpty Pointer to a boolean variable that will be set to true if the RX FIFO is empty, 
                         or false otherwise.

    \return status A value of type \ref CF_DRIVER_STATUS : returns a success or error code.
*/
CF_DRIVER_STATUS CF_I2S_RxFIFOEmpty(CF_I2S_TYPE_PTR i2s, bool* isEmpty);




//! Checks if the RX FIFO is full in the I2S peripheral.
/*!
    This function checks whether the RX FIFO of the I2S peripheral is full.

    \param [in] i2s     Pointer to the I2S base address structure \ref CF_I2S_TYPE_PTR.
    \param [out] isFull Pointer to a boolean variable that will be set to true if the RX FIFO is full, 
                        or false otherwise.

    \return status A value of type \ref CF_DRIVER_STATUS : returns a success or error code.

*/
CF_DRIVER_STATUS CF_I2S_RxFIFOFull(CF_I2S_TYPE_PTR i2s, bool* isFull);




//! Checks if the I2S peripheral is busy.
/*!
    This function checks whether the I2S peripheral is currently busy.

    \param [in] i2s     Pointer to the I2S base address structure \ref CF_I2S_TYPE_PTR.
    \param [out] isBusy Pointer to a boolean variable that will be set to true if the peripheral is busy, 
                        or false otherwise.

    \return status A value of type \ref CF_DRIVER_STATUS : returns a success or error code.
*/
CF_DRIVER_STATUS CF_I2S_Busy(CF_I2S_TYPE_PTR i2s, bool* isBusy);




//! Checks if the RX FIFO level is over the threshold in the I2S peripheral.
/*!
    This function checks whether the RX FIFO level has exceeded the threshold in the I2S peripheral.

    \param [in] i2s               Pointer to the I2S base address structure \ref CF_I2S_TYPE_PTR.
    \param [out] isOverThreshold  Pointer to a boolean variable that will be set to true if the RX FIFO 
                                  level is over the threshold, or false otherwise.

    \return status A value of type \ref CF_DRIVER_STATUS : returns a success or error code.

*/
CF_DRIVER_STATUS CF_I2S_FIFOOverThreshold(CF_I2S_TYPE_PTR i2s, bool* isOverThreshold);


//! Checks if the zero-crossing rate exceeds the threshold in the I2S peripheral.
/*!
    This function checks whether the zero-crossing rate (ZCR) has exceeded the threshold in the I2S peripheral.

    \param [in] i2s               Pointer to the I2S base address structure \ref CF_I2S_TYPE_PTR.
    \param [out] isOverThreshold  Pointer to a boolean variable that will be set to true if the ZCR 
                                  exceeds the threshold, or false otherwise.

    \return status A value of type \ref CF_DRIVER_STATUS : returns a success or error code.

*/
CF_DRIVER_STATUS CF_I2S_ZCROverThreshold(CF_I2S_TYPE_PTR i2s, bool* isOverThreshold);



//! Checks if the Voice Activity Detector (VAD) flag is set in the I2S peripheral.
/*!
    This function checks whether the Voice Activity Detector (VAD) flag is set in the I2S peripheral.

    \param [in] i2s               Pointer to the I2S base address structure \ref CF_I2S_TYPE_PTR.
    \param [out] isOverThreshold  Pointer to a boolean variable that will be set to true if the VAD flag 
                                  is set, or false otherwise.

    \return status A value of type \ref CF_DRIVER_STATUS : returns a success or error code.

*/
CF_DRIVER_STATUS CF_I2S_VADFlag(CF_I2S_TYPE_PTR i2s, bool* isOverThreshold);


/******************************************************************************
* External Variables
******************************************************************************/


#endif // CF_I2S_H

/******************************************************************************
* End of File
******************************************************************************/