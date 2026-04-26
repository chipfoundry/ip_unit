/*
	Copyright 2025 Efabless Corp.

	Author: Efabless Corp. (ip_admin@efabless.com)

	Licensed under the Apache License, Version 2.0 (the "License");
	you may not use this file except in compliance with the License.
	You may obtain a copy of the License at

	    www.apache.org/licenses/LICENSE-2.0

	Unless required by applicable law or agreed to in writing, software
	distributed under the License is distributed on an "AS IS" BASIS,
	WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
	See the License for the specific language governing permissions and
	limitations under the License.

*/

#ifndef CF_USB_CDC_WRAPPERREGS_H
#define CF_USB_CDC_WRAPPERREGS_H

 
/******************************************************************************
* Includes
******************************************************************************/
#include <stdint.h>

/******************************************************************************
* Macros and Constants
******************************************************************************/

#ifndef IO_TYPES
#define IO_TYPES
#define   __R     volatile const uint32_t
#define   __W     volatile       uint32_t
#define   __RW    volatile       uint32_t
#endif

#define CF_USB_CDC_WRAPPER_TXDATA_REG_TXDATA_BIT	((uint32_t)0)
#define CF_USB_CDC_WRAPPER_TXDATA_REG_TXDATA_MASK	((uint32_t)0xff)
#define CF_USB_CDC_WRAPPER_TXDATA_REG_MAX_VALUE	((uint32_t)0xFF)

#define CF_USB_CDC_WRAPPER_RXDATA_REG_RXDATA_BIT	((uint32_t)0)
#define CF_USB_CDC_WRAPPER_RXDATA_REG_RXDATA_MASK	((uint32_t)0xff)
#define CF_USB_CDC_WRAPPER_RXDATA_REG_MAX_VALUE	((uint32_t)0xFF)

#define CF_USB_CDC_WRAPPER_TXFIFOLEVEL_REG_TXFIFOLEVEL_BIT	((uint32_t)0)
#define CF_USB_CDC_WRAPPER_TXFIFOLEVEL_REG_TXFIFOLEVEL_MASK	((uint32_t)0xf)
#define CF_USB_CDC_WRAPPER_TXFIFOLEVEL_REG_MAX_VALUE	((uint32_t)0xF)

#define CF_USB_CDC_WRAPPER_RXFIFOLEVEL_REG_RXFIFOLEVEL_BIT	((uint32_t)0)
#define CF_USB_CDC_WRAPPER_RXFIFOLEVEL_REG_RXFIFOLEVEL_MASK	((uint32_t)0xf)
#define CF_USB_CDC_WRAPPER_RXFIFOLEVEL_REG_MAX_VALUE	((uint32_t)0xF)

#define CF_USB_CDC_WRAPPER_TXFIFOT_REG_TXFIFOT_BIT	((uint32_t)0)
#define CF_USB_CDC_WRAPPER_TXFIFOT_REG_TXFIFOT_MASK	((uint32_t)0xf)
#define CF_USB_CDC_WRAPPER_TXFIFOT_REG_MAX_VALUE	((uint32_t)0xF)

#define CF_USB_CDC_WRAPPER_RXFIFOT_REG_RXFIFOT_BIT	((uint32_t)0)
#define CF_USB_CDC_WRAPPER_RXFIFOT_REG_RXFIFOT_MASK	((uint32_t)0xf)
#define CF_USB_CDC_WRAPPER_RXFIFOT_REG_MAX_VALUE	((uint32_t)0xF)


#define CF_USB_CDC_WRAPPER_TXE_FLAG	((uint32_t)0x1)
#define CF_USB_CDC_WRAPPER_TXB_FLAG	((uint32_t)0x2)
#define CF_USB_CDC_WRAPPER_RXF_FLAG	((uint32_t)0x4)
#define CF_USB_CDC_WRAPPER_RXA_FLAG	((uint32_t)0x8)
#define CF_USB_CDC_WRAPPER_RXE_FLAG	((uint32_t)0x10)
#define CF_USB_CDC_WRAPPER_TXF_FLAG	((uint32_t)0x20)


          
/******************************************************************************
* Typedefs and Enums
******************************************************************************/
          
typedef struct _CF_USB_CDC_WRAPPER_TYPE_ {
	__W 	TXDATA;
	__R 	RXDATA;
	__R 	TXFIFOLEVEL;
	__R 	RXFIFOLEVEL;
	__W 	TXFIFOT;
	__W 	RXFIFOT;
	__R 	reserved_0[16314];
	__RW	IM;
	__R 	MIS;
	__R 	RIS;
	__W 	IC;
} CF_USB_CDC_WRAPPER_TYPE;

typedef struct _CF_USB_CDC_WRAPPER_TYPE_ *CF_USB_CDC_WRAPPER_TYPE_PTR;     // Pointer to the register structure

  
/******************************************************************************
* Function Prototypes
******************************************************************************/



/******************************************************************************
* External Variables
******************************************************************************/




#endif

/******************************************************************************
* End of File
******************************************************************************/
          
          
