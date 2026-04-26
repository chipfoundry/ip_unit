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

IP_name: CF_QSPI_XIP_CTRL
Author: Efabless
Directory Structure:

    - fw 
        - **CF_QSPI_XIP_CTRL_regs.h**: Header file containing the register definitions for the CF_QSPI_XIP_CTRL interface.

    - hdl 
        - rtl 
            - **CF_QSPI_XIP_CTRL.v**: Verilog source code for the CF_QSPI_XIP_CTRL design
            - **DMC.v**: Verilog source code for the CF_QSPI_XIP_CTRL design

            - **bus_wrappers**
                - **CF_QSPI_XIP_CTRL_AHBL.v**: Verilog wrapper to interface the CF_QSPI_XIP_CTRL with the AMBA High-performance Bus (AHB-Lite) protocol.

    - ip 
        - **dependencies.json**: Used by IPM [Do NOT EDIT OR DELETE].
    
    - **CF_QSPI_XIP_CTRL.pdf**: Comprehensive documentation for the CF_QSPI_XIP_CTRL, including its features, configuration, and usage.