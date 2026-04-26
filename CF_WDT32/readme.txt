/*
	Copyright 2024 Efabless Corp.

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

IP_name: CF_WDT32
Author: Efabless
Directory Structure:

    - fw 
        - **CF_WDT32_regs.h**: Header file containing the register definitions for the CF_WDT32 interface.

    - hdl 
        - rtl 
            - **CF_WDT32.v**: Verilog source code for the CF_WDT32 design
            - **bus_wrappers**
                - **CF_WDT32_AHBL.v**: Verilog wrapper to interface the CF_WDT32 with the AMBA High-performance Bus (AHB-Lite) protocol.
                - **CF_WDT32_APB.v**: Verilog wrapper to interface the CF_WDT32 with the Advanced Peripheral Bus (APB) protocol.
                - **CF_WDT32_WB.v**: Verilog wrapper to interface the CF_WDT32 with the Wishbone bus protocol.
            - **dft**
                - **CF_WDT32_AHBL_DFT.v**: Verilog wrapper with Design for Test (DFT) support specific to the AHB-Lite interface of the CF_WDT32 .
                - **CF_WDT32_APB_DFT.v**: Verilog wrapper with DFT support specific to the APB interface of the CF_WDT32.
                - **CF_WDT32_WB_DFT.v**: Verilog wrapper with DFT support specific to the Wishbone interface of the CF_WDT32.

    - ip 
        - **dependencies.json**: Used by IPM [Do NOT EDIT OR DELETE].
    
    - **CF_WDT32.pdf**: Comprehensive documentation for the CF_WDT32, including its features, configuration, and usage.