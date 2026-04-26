#define     CF_PSRAM_CTRL_BASE				    0x00000000

#define     CF_PSRAM_CTRL_RD_CMD_REG_ADDR        (CF_PSRAM_CTRL_BASE + 0x00800100)
#define     CF_PSRAM_CTRL_WR_CMD_REG_ADDR        (CF_PSRAM_CTRL_BASE + 0x00800200)
#define     CF_PSRAM_CTRL_EQPI_CMD_REG_ADDR      (CF_PSRAM_CTRL_BASE + 0x00800400)
#define     CF_PSRAM_CTRL_XQPI_CMD_REG_ADDR      (CF_PSRAM_CTRL_BASE + 0x00800800)
#define     CF_PSRAM_CTRL_WAIT_STATES_REG_ADDR   (CF_PSRAM_CTRL_BASE + 0x00801000)
#define     CF_PSRAM_CTRL_MODE_REG_ADDR          (CF_PSRAM_CTRL_BASE + 0x00802000)
#define     CF_PSRAM_CTRL_ENTER_QPI_REG_ADDR     (CF_PSRAM_CTRL_BASE + 0x00804000)
#define     CF_PSRAM_CTRL_EXIT_QPI_REG_ADDR      (CF_PSRAM_CTRL_BASE + 0x00808000)

volatile unsigned int * ef_psram_ctrl_rd_cmd         = (volatile unsigned int *) CF_PSRAM_CTRL_RD_CMD_REG_ADDR     ;
volatile unsigned int * ef_psram_ctrl_wr_cmd         = (volatile unsigned int *) CF_PSRAM_CTRL_WR_CMD_REG_ADDR     ;
volatile unsigned int * ef_psram_ctrl_eqpi_cmd       = (volatile unsigned int *) CF_PSRAM_CTRL_EQPI_CMD_REG_ADDR   ;
volatile unsigned int * ef_psram_ctrl_xqpi_cmd       = (volatile unsigned int *) CF_PSRAM_CTRL_XQPI_CMD_REG_ADDR   ;
volatile unsigned int * ef_psram_ctrl_wait_states    = (volatile unsigned int *) CF_PSRAM_CTRL_WAIT_STATES_REG_ADDR;
volatile unsigned int * ef_psram_ctrl_mode           = (volatile unsigned int *) CF_PSRAM_CTRL_MODE_REG_ADDR       ;
volatile unsigned int * ef_psram_ctrl_enter_qpi      = (volatile unsigned int *) CF_PSRAM_CTRL_ENTER_QPI_REG_ADDR  ;
volatile unsigned int * ef_psram_ctrl_exit_qpi       = (volatile unsigned int *) CF_PSRAM_CTRL_EXIT_QPI_REG_ADDR   ;
