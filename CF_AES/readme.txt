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

IP_name: CF_AES
Author: Efabless
Directory Structure:

    - fw 
        - **CF_AES_regs.h**: Header file containing the register definitions for the CF_AES interface.

    - hdl 
        - rtl 
            - **aes_core.v**: Verilog source code for the CF_AES design
            - **aes_decipher_block.v**: Verilog source code for the CF_AES design
            - **aes_encipher_block.v**: Verilog source code for the CF_AES design
            - **aes_inv_sbox.v**: Verilog source code for the CF_AES design
            - **aes_key_mem.v**: Verilog source code for the CF_AES design
            - **aes_sbox.v**: Verilog source code for the CF_AES design
            - **aes.v**: Verilog source code for the CF_AES design

            - **bus_wrappers**
                - **CF_AES_AHBL.v**: Verilog wrapper to interface the CF_AES with the AMBA High-performance Bus (AHB-Lite) protocol.
                - **CF_AES_APB.v**: Verilog wrapper to interface the CF_AES with the Advanced Peripheral Bus (APB) protocol.
                - **CF_AES_WB.v**: Verilog wrapper to interface the CF_AES with the Wishbone bus protocol.
            - **dft**
                - **CF_AES_AHBL_DFT.v**: Verilog wrapper with Design for Test (DFT) support specific to the AHB-Lite interface of the CF_AES .
                - **CF_AES_APB_DFT.v**: Verilog wrapper with DFT support specific to the APB interface of the CF_AES.
                - **CF_AES_WB_DFT.v**: Verilog wrapper with DFT support specific to the Wishbone interface of the CF_AES.

    - ip 
        - **dependencies.json**: Used by IPM [Do NOT EDIT OR DELETE].
    
    - **CF_AES.pdf**: Comprehensive documentation for the CF_AES, including its features, configuration, and usage.