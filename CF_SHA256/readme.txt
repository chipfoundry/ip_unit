/*
	Copyright 2024 ChipFoundry Corp.

	Author: ChipFoundry Corp. (ip_admin@chipfoundry.com)

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

IP_name: CF_SHA256
Author: ChipFoundry
Directory Structure:

    - fw 
        - **CF_SHA256_regs.h**: Header file containing the register definitions for the CF_SHA256 interface.

    - hdl 
        - rtl 
            - **sha256_core.v**: Verilog source code for the CF_SHA256 design
            - **sha256_k_constants.v**: Verilog source code for the CF_SHA256 design
            - **sha256_w_mem.v**: Verilog source code for the CF_SHA256 design
            - **bus_wrappers**
                - **CF_SHA256_AHBL.v**: Verilog wrapper to interface the CF_SHA256 with the AMBA High-performance Bus (AHB-Lite) protocol.
                - **CF_SHA256_APB.v**: Verilog wrapper to interface the CF_SHA256 with the Advanced Peripheral Bus (APB) protocol.
                - **CF_SHA256_WB.v**: Verilog wrapper to interface the CF_SHA256 with the Wishbone bus protocol.
            - **dft**
                - **CF_SHA256_AHBL_DFT.v**: Verilog wrapper with Design for Test (DFT) support specific to the AHB-Lite interface of the CF_SHA256 .
                - **CF_SHA256_APB_DFT.v**: Verilog wrapper with DFT support specific to the APB interface of the CF_SHA256.
                - **CF_SHA256_WB_DFT.v**: Verilog wrapper with DFT support specific to the Wishbone interface of the CF_SHA256.

    - ip 
        - **dependencies.json**: Used by IPM [Do NOT EDIT OR DELETE].
    
    - **CF_SHA256.pdf**: Comprehensive documentation for the CF_SHA256, including its features, configuration, and usage.