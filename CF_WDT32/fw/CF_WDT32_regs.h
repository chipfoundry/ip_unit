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

#ifndef CF_WDT32REGS_H
#define CF_WDT32REGS_H

 
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

#define CF_WDT32_TIMER_REG_TIMER_BIT	((uint32_t)0)
#define CF_WDT32_TIMER_REG_TIMER_MASK	((uint32_t)0xffffffff)
#define CF_WDT32_TIMER_REG_MAX_VALUE	((uint32_t)0xFFFFFFFF)

#define CF_WDT32_LOAD_REG_LOAD_BIT	((uint32_t)0)
#define CF_WDT32_LOAD_REG_LOAD_MASK	((uint32_t)0xffffffff)
#define CF_WDT32_LOAD_REG_MAX_VALUE	((uint32_t)0xFFFFFFFF)

#define CF_WDT32_CONTROL_REG_CONTROL_BIT	((uint32_t)0)
#define CF_WDT32_CONTROL_REG_CONTROL_MASK	((uint32_t)0x1)
#define CF_WDT32_CONTROL_REG_MAX_VALUE	((uint32_t)0x1)


#define CF_WDT32_WDTTO_FLAG	((uint32_t)0x1)


          
/******************************************************************************
* Typedefs and Enums
******************************************************************************/
          
typedef struct _CF_WDT32_TYPE_ {
	__R 	timer;
	__W 	load;
	__W 	control;
	__R 	reserved_0[16317];
	__RW	IM;
	__R 	MIS;
	__R 	RIS;
	__W 	IC;
	__W 	GCLK;
} CF_WDT32_TYPE;

typedef struct _CF_WDT32_TYPE_ *CF_WDT32_TYPE_PTR;     // Pointer to the register structure

  
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
          
          
