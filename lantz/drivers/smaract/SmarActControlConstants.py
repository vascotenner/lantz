######
#
# Based on SmarActControlConstants.h provided by SmarAct 2018
#
# Author V. T. Tenner 2019
#
#########

#/**********************************************************/
#/* GLOBAL DEFINITIONS                                     */
#/**********************************************************/

SA_CTL_INFINITE                                     = 0xffffffff

SA_CTL_DISABLED                                     = 0x00
SA_CTL_ENABLED                                      = 0x01
SA_CTL_NON_INVERTED                                 = 0x00
SA_CTL_INVERTED                                     = 0x01
SA_CTL_FORWARD_DIRECTION                            = 0x00
SA_CTL_BACKWARD_DIRECTION                           = 0x01
SA_CTL_EITHER_DIRECTION                             = 0x02

SA_CTL_STRING_MAX_LENGTH                            = 63
SA_CTL_REQUEST_ID_MAX_COUNT                         = 240

#/**********************************************************/
#/* EVENT TYPES                                            */
#/**********************************************************/

SA_CTL_EVENT_NONE                                   = 0x0000

#  channel events (0x0001 - 0x3fff)
SA_CTL_EVENT_MOVEMENT_FINISHED                      = 0x0001
SA_CTL_EVENT_SENSOR_STATE_CHANGED                   = 0x0002
SA_CTL_EVENT_REFERENCE_FOUND                        = 0x0003
SA_CTL_EVENT_FOLLOWING_ERR_LIMIT                    = 0x0004
SA_CTL_EVENT_HOLDING_ABORTED                        = 0x0005
SA_CTL_EVENT_POSITIONER_TYPE_CHANGED                = 0x0006

#  module events (0x4000 - 0x7fff)
SA_CTL_EVENT_SM_STATE_CHANGED                       = 0x4000
SA_CTL_EVENT_OVER_TEMPERATURE                       = 0x4001
SA_CTL_EVENT_HIGH_VOLTAGE_OVERLOAD                  = 0x4002
SA_CTL_EVENT_ADJUSTMENT_FINISHED                    = 0x4010
SA_CTL_EVENT_ADJUSTMENT_STATE_CHANGED               = 0x4011
SA_CTL_EVENT_ADJUSTMENT_UPDATE                      = 0x4012
SA_CTL_EVENT_DIGITAL_INPUT_CHANGED                  = 0x4040

#  device events (0x8000 - 0xbfff)
SA_CTL_EVENT_STREAM_FINISHED                        = 0x8000
SA_CTL_EVENT_STREAM_READY                           = 0x8001
SA_CTL_EVENT_STREAM_TRIGGERED                       = 0x8002
SA_CTL_EVENT_CMD_GROUP_TRIGGERED                    = 0x8010
SA_CTL_EVENT_HM_STATE_CHANGED                       = 0x8020
SA_CTL_EVENT_EMERGENCY_STOP_TRIGGERED               = 0x8030
SA_CTL_EVENT_EXT_INPUT_TRIGGERED                    = 0x8040
SA_CTL_EVENT_BUS_RESYNC_TRIGGERED                   = 0x8050

#  api events (0xf000 - 0xffff)
SA_CTL_EVENT_REQUEST_READY                          = 0xf000
SA_CTL_EVENT_CONNECTION_LOST                        = 0xf001

#/**********************************************************/
#/* EVENT PARAMETERS                                       */
#/**********************************************************/

SA_CTL_EVENT_PARAM_DETACHED                         = 0x00000000
SA_CTL_EVENT_PARAM_ATTACHED                         = 0x00000001

SA_CTL_EVENT_REQ_READY_TYPE_READ                    = 0x00
SA_CTL_EVENT_REQ_READY_TYPE_WRITE                   = 0x01

#  event parameter decoding
SA_CTL_EVENT_PARAM_RESULT_MASK                      = 0x0000ffff
SA_CTL_EVENT_PARAM_INDEX_MASK                       = 0x00ff0000
SA_CTL_EVENT_PARAM_HANDLE_MASK                      = 0xff000000
#SA_CTL_EVENT_PARAM_RESULT(param)                    (((param) & SA_CTL_EVENT_PARAM_RESULT_MASK) >> = 0)
#SA_CTL_EVENT_PARAM_INDEX(param)                     (((param) & SA_CTL_EVENT_PARAM_INDEX_MASK) >> = 16)
#SA_CTL_EVENT_PARAM_HANDLE(param)                    (((param) & SA_CTL_EVENT_PARAM_HANDLE_MASK) >> = 24)

SA_CTL_EVENT_REQ_READY_ID_MASK                      = 0x00000000000000ff
SA_CTL_EVENT_REQ_READY_TYPE_MASK                    = 0x000000000000ff00
SA_CTL_EVENT_REQ_READY_DATA_TYPE_MASK               = 0x0000000000ff0000
SA_CTL_EVENT_REQ_READY_ARRAY_SIZE_MASK              = 0x00000000ff000000
SA_CTL_EVENT_REQ_READY_PROPERTY_KEY_MASK            = 0xffffffff00000000
#SA_CTL_EVENT_REQ_READY_ID(param)                    (((param) & SA_CTL_EVENT_REQ_READY_ID_MASK) >> = 0)
#SA_CTL_EVENT_REQ_READY_TYPE(param)                  (((param) & SA_CTL_EVENT_REQ_READY_TYPE_MASK) >> = 8)
#SA_CTL_EVENT_REQ_READY_DATA_TYPE(param)             (((param) & SA_CTL_EVENT_REQ_READY_DATA_TYPE_MASK) >> = 16)
#SA_CTL_EVENT_REQ_READY_ARRAY_SIZE(param)            (((param) & SA_CTL_EVENT_REQ_READY_ARRAY_SIZE_MASK) >> = 24)
#SA_CTL_EVENT_REQ_READY_PROPERTY_KEY(param)          (((param) & SA_CTL_EVENT_REQ_READY_PROPERTY_KEY_MASK) >> = 32)

# /*********************************************************/
# /* ERROR CODES                                           */
# /*********************************************************/

SA_CTL_ERROR_NONE                                   = 0x0000
SA_CTL_ERROR_UNKNOWN_COMMAND                        = 0x0001
SA_CTL_ERROR_INVALID_PACKET_SIZE                    = 0x0002
SA_CTL_ERROR_TIMEOUT                                = 0x0004
SA_CTL_ERROR_INVALID_PROTOCOL                       = 0x0005
SA_CTL_ERROR_BUFFER_UNDERFLOW                       = 0x000c
SA_CTL_ERROR_BUFFER_OVERFLOW                        = 0x000d
SA_CTL_ERROR_INVALID_FRAME_SIZE                     = 0x000e
SA_CTL_ERROR_INVALID_PACKET                         = 0x0010
SA_CTL_ERROR_INVALID_KEY                            = 0x0012
SA_CTL_ERROR_INVALID_PARAMETER                      = 0x0013
SA_CTL_ERROR_INVALID_DATA_TYPE                      = 0x0016
SA_CTL_ERROR_INVALID_DATA                           = 0x0017
SA_CTL_ERROR_HANDLE_LIMIT_REACHED                   = 0x0018
SA_CTL_ERROR_ABORTED                                = 0x0019

SA_CTL_ERROR_INVALID_DEVICE_INDEX                   = 0x0020
SA_CTL_ERROR_INVALID_MODULE_INDEX                   = 0x0021
SA_CTL_ERROR_INVALID_CHANNEL_INDEX                  = 0x0022

SA_CTL_ERROR_PERMISSION_DENIED                      = 0x0023
SA_CTL_ERROR_COMMAND_NOT_GROUPABLE                  = 0x0024
SA_CTL_ERROR_MOVEMENT_LOCKED                        = 0x0025
SA_CTL_ERROR_SYNC_FAILED                            = 0x0026
SA_CTL_ERROR_INVALID_ARRAY_SIZE                     = 0x0027
SA_CTL_ERROR_OVERRANGE                              = 0x0028
SA_CTL_ERROR_INVALID_CONFIGURATION                  = 0x0029

SA_CTL_ERROR_NO_HM_PRESENT                          = 0x0100
SA_CTL_ERROR_NO_IOM_PRESENT                         = 0x0101
SA_CTL_ERROR_NO_SM_PRESENT                          = 0x0102
SA_CTL_ERROR_NO_SENSOR_PRESENT                      = 0x0103
SA_CTL_ERROR_SENSOR_DISABLED                        = 0x0104
SA_CTL_ERROR_POWER_SUPPLY_DISABLED                  = 0x0105
SA_CTL_ERROR_AMPLIFIER_DISABLED                     = 0x0106
SA_CTL_ERROR_INVALID_SENSOR_MODE                    = 0x0107
SA_CTL_ERROR_INVALID_ACTUATOR_MODE                  = 0x0108
SA_CTL_ERROR_INVALID_INPUT_TRIG_MODE                = 0x0109
SA_CTL_ERROR_INVALID_CONTROL_OPTIONS                = 0x010a
SA_CTL_ERROR_INVALID_REFERENCE_TYPE                 = 0x010b
SA_CTL_ERROR_INVALID_ADJUSTMENT_STATE               = 0x010c
SA_CTL_ERROR_INVALID_INFO_TYPE                      = 0x010d
SA_CTL_ERROR_NO_FULL_ACCESS                         = 0x010e
SA_CTL_ERROR_ADJUSTMENT_FAILED                      = 0x010f
SA_CTL_ERROR_MOVEMENT_OVERRIDDEN                    = 0x0110
SA_CTL_ERROR_NOT_CALIBRATED                         = 0x0111
SA_CTL_ERROR_NOT_REFERENCED                         = 0x0112
SA_CTL_ERROR_NOT_ADJUSTED                           = 0x0113
SA_CTL_ERROR_SENSOR_TYPE_NOT_SUPPORTED              = 0x0114
SA_CTL_ERROR_CONTROL_LOOP_INPUT_DISABLED            = 0x0115
SA_CTL_ERROR_INVALID_CONTROL_LOOP_INPUT             = 0x0116
SA_CTL_ERROR_UNEXPECTED_SENSOR_DATA                 = 0x0117

SA_CTL_ERROR_BUSY_MOVING                            = 0x0150
SA_CTL_ERROR_BUSY_CALIBRATING                       = 0x0151
SA_CTL_ERROR_BUSY_REFERENCING                       = 0x0152
SA_CTL_ERROR_BUSY_ADJUSTING                         = 0x0153

SA_CTL_ERROR_END_STOP_REACHED                       = 0x0200
SA_CTL_ERROR_FOLLOWING_ERR_LIMIT                    = 0x0201
SA_CTL_ERROR_RANGE_LIMIT_REACHED                    = 0x0202
SA_CTL_ERROR_OVER_TEMPERATURE                       = 0x0206

SA_CTL_ERROR_INVALID_STREAM_HANDLE                  = 0x0300
SA_CTL_ERROR_INVALID_STREAM_CONFIGURATION           = 0x0301
SA_CTL_ERROR_INSUFFICIENT_FRAMES                    = 0x0302
SA_CTL_ERROR_BUSY_STREAMING                         = 0x0303

SA_CTL_ERROR_HM_INVALID_SLOT_INDEX                  = 0x0400
SA_CTL_ERROR_HM_INVALID_CHANNEL_INDEX               = 0x0401
SA_CTL_ERROR_HM_INVALID_GROUP_INDEX                 = 0x0402
SA_CTL_ERROR_HM_INVALID_CH_GRP_INDEX                = 0x0403

SA_CTL_ERROR_INTERNAL_COMMUNICATION                 = 0x0500

SA_CTL_ERROR_FEATURE_NOT_SUPPORTED                  = 0x7ffd
SA_CTL_ERROR_FEATURE_NOT_IMPLEMENTED                = 0x7ffe

#  api error codes
SA_CTL_ERROR_DEVICE_LIMIT_REACHED                   = 0xf000
SA_CTL_ERROR_INVALID_LOCATOR                        = 0xf001
SA_CTL_ERROR_INITIALIZATION_FAILED                  = 0xf002
SA_CTL_ERROR_NOT_INITIALIZED                        = 0xf003
SA_CTL_ERROR_COMMUNICATION_FAILED                   = 0xf004
SA_CTL_ERROR_INVALID_QUERYBUFFER_SIZE               = 0xf006
SA_CTL_ERROR_INVALID_DEVICE_HANDLE                  = 0xf007
SA_CTL_ERROR_INVALID_TRANSMIT_HANDLE                = 0xf008
SA_CTL_ERROR_UNEXPECTED_PACKET_RECEIVED             = 0xf00f
SA_CTL_ERROR_CANCELED                               = 0xf010
SA_CTL_ERROR_DRIVER_FAILED                          = 0xf013
SA_CTL_ERROR_BUFFER_LIMIT_REACHED                   = 0xf016
SA_CTL_ERROR_INVALID_PROTOCOL_VERSION               = 0xf017
SA_CTL_ERROR_DEVICE_RESET_FAILED                    = 0xf018
SA_CTL_ERROR_BUFFER_EMPTY                           = 0xf019
SA_CTL_ERROR_DEVICE_NOT_FOUND                       = 0xf01a
SA_CTL_ERROR_THREAD_LIMIT_REACHED                   = 0xf01b

#/**********************************************************/
#/* DATA TYPES                                             */
#/**********************************************************/

SA_CTL_DTYPE_UINT16                                 = 0x03
SA_CTL_DTYPE_INT32                                  = 0x06
SA_CTL_DTYPE_INT64                                  = 0x0e
SA_CTL_DTYPE_FLOAT32                                = 0x10
SA_CTL_DTYPE_FLOAT64                                = 0x11
SA_CTL_DTYPE_STRING                                 = 0x12
SA_CTL_DTYPE_NONE                                   = 0xff

#/**********************************************************/
#/* BASE UNIT TYPES                                        */
#/**********************************************************/

SA_CTL_UNIT_NONE                                    = 0x00000000
SA_CTL_UNIT_PERCENT                                 = 0x00000001
SA_CTL_UNIT_METER                                   = 0x00000002
SA_CTL_UNIT_DEGREE                                  = 0x00000003
SA_CTL_UNIT_SECOND                                  = 0x00000004
SA_CTL_UNIT_HERTZ                                   = 0x00000005

#/**********************************************************/
#/* PROPERTY KEYS                                          */
#/**********************************************************/
#  device
SA_CTL_PKEY_NUMBER_OF_CHANNELS                      = 0x020F0017
SA_CTL_PKEY_NUMBER_OF_BUS_MODULES                   = 0x020F0016
SA_CTL_PKEY_DEVICE_STATE                            = 0x020F000F
SA_CTL_PKEY_DEVICE_SERIAL_NUMBER                    = 0x020F005E
SA_CTL_PKEY_DEVICE_NAME                             = 0x020F003D
SA_CTL_PKEY_EMERGENCY_STOP_MODE                     = 0x020F0088
SA_CTL_PKEY_NETWORK_DISCOVER_MODE                   = 0x020F0159
#  module
SA_CTL_PKEY_POWER_SUPPLY_ENABLED                    = 0x02030010
SA_CTL_PKEY_MODULE_STATE                            = 0x0203000F
SA_CTL_PKEY_NUMBER_OF_BUS_MODULE_CHANNELS           = 0x02030017
#  positioner
SA_CTL_PKEY_AMPLIFIER_ENABLED                       = 0x0302000D
SA_CTL_PKEY_POSITIONER_CONTROL_OPTIONS              = 0x0302005D
SA_CTL_PKEY_ACTUATOR_MODE                           = 0x03020019
SA_CTL_PKEY_CONTROL_LOOP_INPUT                      = 0x03020018
SA_CTL_PKEY_SENSOR_INPUT_SELECT                     = 0x0302009D
SA_CTL_PKEY_POSITIONER_TYPE                         = 0x0302003C
SA_CTL_PKEY_POSITIONER_TYPE_NAME                    = 0x0302003D
SA_CTL_PKEY_MOVE_MODE                               = 0x03050087
SA_CTL_PKEY_CHANNEL_STATE                           = 0x0305000F
SA_CTL_PKEY_POSITION                                = 0x0305001D
SA_CTL_PKEY_TARGET_POSITION                         = 0x0305001E
SA_CTL_PKEY_SCAN_POSITION                           = 0x0305001F
SA_CTL_PKEY_SCAN_VELOCITY                           = 0x0305002A
SA_CTL_PKEY_HOLD_TIME                               = 0x03050028
SA_CTL_PKEY_MOVE_VELOCITY                           = 0x03050029
SA_CTL_PKEY_MOVE_ACCELERATION                       = 0x0305002B
SA_CTL_PKEY_MAX_CL_FREQUENCY                        = 0x0305002F
SA_CTL_PKEY_DEFAULT_MAX_CL_FREQUENCY                = 0x03050057
SA_CTL_PKEY_STEP_FREQUENCY                          = 0x0305002E
SA_CTL_PKEY_STEP_AMPLITUDE                          = 0x03050030
SA_CTL_PKEY_FOLLOWING_ERROR_LIMIT                   = 0x03050055
SA_CTL_PKEY_FOLLOWING_ERROR                         = 0x03020055
SA_CTL_PKEY_BROADCAST_STOP_OPTIONS                  = 0x0305005D
SA_CTL_PKEY_SENSOR_POWER_MODE                       = 0x03080019
SA_CTL_PKEY_SENSOR_POWER_SAVE_DELAY                 = 0x03080054
SA_CTL_PKEY_POSITION_MEAN_SHIFT                     = 0x03090022
SA_CTL_PKEY_SAFE_DIRECTION                          = 0x03090027
SA_CTL_PKEY_CL_INPUT_SENSOR_VALUE                   = 0x0302001D
SA_CTL_PKEY_CL_INPUT_AUX_VALUE                      = 0x030200B2
SA_CTL_PKEY_TARGET_TO_ZERO_VOLTAGE_HOLD_TH          = 0x030200B9
#  scale
SA_CTL_PKEY_LOGICAL_SCALE_OFFSET                    = 0x02040024
SA_CTL_PKEY_LOGICAL_SCALE_INVERSION                 = 0x02040025
SA_CTL_PKEY_RANGE_LIMIT_MIN                         = 0x02040020
SA_CTL_PKEY_RANGE_LIMIT_MAX                         = 0x02040021
#  calibration
SA_CTL_PKEY_CALIBRATION_OPTIONS                     = 0x0306005D
SA_CTL_PKEY_SIGNAL_CORRECTION_OPTIONS               = 0x0306001C
#  referencing
SA_CTL_PKEY_REFERENCING_OPTIONS                     = 0x0307005D
SA_CTL_PKEY_DIST_CODE_INVERTED                      = 0x0307000E
SA_CTL_PKEY_DISTANCE_TO_REF_MARK                    = 0x030700A2
#  tuning and customizing
SA_CTL_PKEY_POS_MOVEMENT_TYPE                       = 0x0309003F
SA_CTL_PKEY_POS_IS_CUSTOM_TYPE                      = 0x03090041
SA_CTL_PKEY_POS_BASE_UNIT                           = 0x03090042
SA_CTL_PKEY_POS_BASE_RESOLUTION                     = 0x03090043
SA_CTL_PKEY_POS_HEAD_TYPE                           = 0x0309008E
SA_CTL_PKEY_POS_REF_TYPE                            = 0x03090048
SA_CTL_PKEY_POS_P_GAIN                              = 0x0309004B
SA_CTL_PKEY_POS_I_GAIN                              = 0x0309004C
SA_CTL_PKEY_POS_D_GAIN                              = 0x0309004D
SA_CTL_PKEY_POS_PID_SHIFT                           = 0x0309004E
SA_CTL_PKEY_POS_ANTI_WINDUP                         = 0x0309004F
SA_CTL_PKEY_POS_ESD_DIST_TH                         = 0x03090050
SA_CTL_PKEY_POS_ESD_COUNTER_TH                      = 0x03090051
SA_CTL_PKEY_POS_TARGET_REACHED_TH                   = 0x03090052
SA_CTL_PKEY_POS_TARGET_HOLD_TH                      = 0x03090053
SA_CTL_PKEY_POS_SAVE                                = 0x0309000A
SA_CTL_PKEY_POS_WRITE_PROTECTION                    = 0x0309000D
#  streaming
SA_CTL_PKEY_STREAM_BASE_RATE                        = 0x040F002C
SA_CTL_PKEY_STREAM_EXT_SYNC_RATE                    = 0x040F002D
SA_CTL_PKEY_STREAM_OPTIONS                          = 0x040F005D
SA_CTL_PKEY_STREAM_LOAD_MAX                         = 0x040F0301
#  diagnostic
SA_CTL_PKEY_CHANNEL_ERROR                           = 0x0502007A
SA_CTL_PKEY_CHANNEL_TEMPERATURE                     = 0x05020034
SA_CTL_PKEY_BUS_MODULE_TEMPERATURE                  = 0x05030034
#  io module
SA_CTL_PKEY_IO_MODULE_OPTIONS                       = 0x0603005D
SA_CTL_PKEY_IO_MODULE_VOLTAGE                       = 0x06030031
SA_CTL_PKEY_IO_MODULE_ANALOG_INPUT_RANGE            = 0x060300A0
#  auxiliary
SA_CTL_PKEY_AUX_POSITIONER_TYPE                     = 0x0802003C
SA_CTL_PKEY_AUX_POSITIONER_TYPE_NAME                = 0x0802003D
SA_CTL_PKEY_AUX_INPUT_SELECT                        = 0x08020018
SA_CTL_PKEY_AUX_IO_MODULE_INPUT_INDEX               = 0x081100AA
SA_CTL_PKEY_AUX_SENSOR_MODULE_INPUT_INDEX           = 0x080B00AA
SA_CTL_PKEY_AUX_IO_MODULE_INPUT0_VALUE              = 0x08110000
SA_CTL_PKEY_AUX_IO_MODULE_INPUT1_VALUE              = 0x08110001
SA_CTL_PKEY_AUX_SENSOR_MODULE_INPUT0_VALUE          = 0x080B0000
SA_CTL_PKEY_AUX_SENSOR_MODULE_INPUT1_VALUE          = 0x080B0001
SA_CTL_PKEY_AUX_DIRECTION_INVERSION                 = 0x0809000E
SA_CTL_PKEY_AUX_DIGITAL_INPUT_VALUE                 = 0x080300AD
SA_CTL_PKEY_AUX_DIGITAL_OUTPUT_VALUE                = 0x080300AE
SA_CTL_PKEY_AUX_DIGITAL_OUTPUT_SET                  = 0x080300B0
SA_CTL_PKEY_AUX_DIGITAL_OUTPUT_CLEAR                = 0x080300B1
SA_CTL_PKEY_AUX_ANALOG_OUTPUT_VALUE0                = 0x08030000
SA_CTL_PKEY_AUX_ANALOG_OUTPUT_VALUE1                = 0x08030001
#  threshold detector
SA_CTL_PKEY_THD_INPUT_SELECT                        = 0x09020018
SA_CTL_PKEY_THD_IO_MODULE_INPUT_INDEX               = 0x091100AA
SA_CTL_PKEY_THD_SENSOR_MODULE_INPUT_INDEX           = 0x090B00AA
SA_CTL_PKEY_THD_THRESHOLD_HIGH                      = 0x090200B4
SA_CTL_PKEY_THD_THRESHOLD_LOW                       = 0x090200B5
SA_CTL_PKEY_THD_INVERSION                           = 0x0902000E
#  input trigger
SA_CTL_PKEY_DEV_INPUT_TRIG_MODE                     = 0x060D0087
SA_CTL_PKEY_DEV_INPUT_TRIG_CONDITION                = 0x060D005A
#  output trigger
SA_CTL_PKEY_CH_OUTPUT_TRIG_MODE                     = 0x060E0087
SA_CTL_PKEY_CH_OUTPUT_TRIG_POLARITY                 = 0x060E005B
SA_CTL_PKEY_CH_OUTPUT_TRIG_PULSE_WIDTH              = 0x060E005C
SA_CTL_PKEY_CH_POS_COMP_START_THRESHOLD             = 0x060E0058
SA_CTL_PKEY_CH_POS_COMP_INCREMENT                   = 0x060E0059
SA_CTL_PKEY_CH_POS_COMP_DIRECTION                   = 0x060E0026
SA_CTL_PKEY_CH_POS_COMP_LIMIT_MIN                   = 0x060E0020
SA_CTL_PKEY_CH_POS_COMP_LIMIT_MAX                   = 0x060E0021
#  hand control module
SA_CTL_PKEY_HM_STATE                                = 0x020C000F
SA_CTL_PKEY_HM_LOCK_OPTIONS                         = 0x020C0083
SA_CTL_PKEY_HM_DEFAULT_LOCK_OPTIONS                 = 0x020C0084
#  api
SA_CTL_PKEY_EVENT_NOTIFICATION_OPTIONS              = 0xF010005D
SA_CTL_PKEY_AUTO_RECONNECT                          = 0xF01000A1

#/**********************************************************/
#/* STATE BITS                                             */
#/**********************************************************/

#  device states
SA_CTL_DEV_STATE_BIT_HM_PRESENT                     = 0x0001
SA_CTL_DEV_STATE_BIT_MOVEMENT_LOCKED                = 0x0002
SA_CTL_DEV_STATE_BIT_INTERNAL_COMM_FAILURE          = 0x0100
SA_CTL_DEV_STATE_BIT_IS_STREAMING                   = 0x1000

#  module states
SA_CTL_MOD_STATE_BIT_SM_PRESENT                     = 0x0001
SA_CTL_MOD_STATE_BIT_BOOSTER_PRESENT                = 0x0002
SA_CTL_MOD_STATE_BIT_ADJUSTMENT_ACTIVE              = 0x0004
SA_CTL_MOD_STATE_BIT_IOM_PRESENT                    = 0x0008
SA_CTL_MOD_STATE_BIT_INTERNAL_COMM_FAILURE          = 0x0100
SA_CTL_MOD_STATE_BIT_HIGH_VOLTAGE_FAILURE           = 0x1000
SA_CTL_MOD_STATE_BIT_HIGH_VOLTAGE_OVERLOAD          = 0x2000
SA_CTL_MOD_STATE_BIT_OVER_TEMPERATURE               = 0x4000

#  channel states
SA_CTL_CH_STATE_BIT_ACTIVELY_MOVING                 = 0x0001
SA_CTL_CH_STATE_BIT_CLOSED_LOOP_ACTIVE              = 0x0002
SA_CTL_CH_STATE_BIT_CALIBRATING                     = 0x0004
SA_CTL_CH_STATE_BIT_REFERENCING                     = 0x0008
SA_CTL_CH_STATE_BIT_MOVE_DELAYED                    = 0x0010
SA_CTL_CH_STATE_BIT_SENSOR_PRESENT                  = 0x0020
SA_CTL_CH_STATE_BIT_IS_CALIBRATED                   = 0x0040
SA_CTL_CH_STATE_BIT_IS_REFERENCED                   = 0x0080
SA_CTL_CH_STATE_BIT_END_STOP_REACHED                = 0x0100
SA_CTL_CH_STATE_BIT_RANGE_LIMIT_REACHED             = 0x0200
SA_CTL_CH_STATE_BIT_FOLLOWING_LIMIT_REACHED         = 0x0400
SA_CTL_CH_STATE_BIT_MOVEMENT_FAILED                 = 0x0800
SA_CTL_CH_STATE_BIT_IS_STREAMING                    = 0x1000

SA_CTL_CH_STATE_BIT_OVER_TEMPERATURE                = 0x4000
SA_CTL_CH_STATE_BIT_REFERENCE_MARK                  = 0x8000

#  hand control module states
SA_CTL_HM_STATE_BIT_INTERNAL_COMM_FAILURE           = 0x0100
SA_CTL_HM_STATE_BIT_IS_INTERNAL                     = 0x0200

#/**********************************************************/
#/* MOVEMENT MODES                                         */
#/**********************************************************/

SA_CTL_MOVE_MODE_CL_ABSOLUTE                        = 0
SA_CTL_MOVE_MODE_CL_RELATIVE                        = 1
SA_CTL_MOVE_MODE_SCAN_ABSOLUTE                      = 2
SA_CTL_MOVE_MODE_SCAN_RELATIVE                      = 3
SA_CTL_MOVE_MODE_STEP                               = 4

#/**********************************************************/
#/* ACTUATOR MODES                                         */
#/**********************************************************/

SA_CTL_ACTUATOR_MODE_NORMAL                         = 0
SA_CTL_ACTUATOR_MODE_QUIET                          = 1
SA_CTL_ACTUATOR_MODE_LOW_VIBRATION                  = 2

#/**********************************************************/
#/* CONTROL LOOP INPUT                                     */
#/**********************************************************/

SA_CTL_CONTROL_LOOP_INPUT_DISABLED                  = 0
SA_CTL_CONTROL_LOOP_INPUT_SENSOR                    = 1
SA_CTL_CONTROL_LOOP_INPUT_POSITION                  = 1  # deprecated
SA_CTL_CONTROL_LOOP_INPUT_AUX_IN                    = 2

#/**********************************************************/
#/* SENSOR INPUT SELECT                                    */
#/**********************************************************/

SA_CTL_SENSOR_INPUT_SELECT_POSITION                 = 0
SA_CTL_SENSOR_INPUT_SELECT_CALC_SYS                 = 1

#/**********************************************************/
#/* AUX INPUT SELECT                                       */
#/**********************************************************/

SA_CTL_AUX_INPUT_SELECT_IO_MODULE                   = 0
SA_CTL_AUX_INPUT_SELECT_SENSOR_MODULE               = 1

#/**********************************************************/
#/* THRESHOLD DETECTOR INPUT SELECT                        */
#/**********************************************************/

SA_CTL_THD_INPUT_SELECT_IO_MODULE                   = 0
SA_CTL_THD_INPUT_SELECT_SENSOR_MODULE               = 1

#/**********************************************************/
#/* EMERGENCY STOP TRIGGER MODES                           */
#/**********************************************************/

SA_CTL_EMERGENCY_STOP_MODE_NORMAL                   = 0
SA_CTL_EMERGENCY_STOP_MODE_RESTRICTED               = 1
SA_CTL_EMERGENCY_STOP_MODE_AUTO_RELEASE             = 2

#/**********************************************************/
#/* COMMAND GROUP TRIGGER MODES                            */
#/**********************************************************/

SA_CTL_CMD_GROUP_TRIGGER_MODE_DIRECT                = 0
SA_CTL_CMD_GROUP_TRIGGER_MODE_EXTERNAL              = 1

#/**********************************************************/
#/* STREAM TRIGGER MODES                                   */
#/**********************************************************/

SA_CTL_STREAM_TRIGGER_MODE_DIRECT                   = 0
SA_CTL_STREAM_TRIGGER_MODE_EXTERNAL_ONCE            = 1
SA_CTL_STREAM_TRIGGER_MODE_EXTERNAL_SYNC            = 2

#/**********************************************************/
#/* STREAM OPTIONS                                         */
#/**********************************************************/

SA_CTL_STREAM_OPT_BIT_INTERPOLATION_DIS             = 0x00000001

#/**********************************************************/
#/* POSITIONER CONTROL OPTIONS                             */
#/**********************************************************/

SA_CTL_POS_CTRL_OPT_BIT_ACC_REL_POS_DIS             = 0x00000001
SA_CTL_POS_CTRL_OPT_BIT_NO_SLIP                     = 0x00000002
SA_CTL_POS_CTRL_OPT_BIT_NO_SLIP_WHILE_HOLDING       = 0x00000004
SA_CTL_POS_CTRL_OPT_BIT_FORCED_SLIP_DIS             = 0x00000008
SA_CTL_POS_CTRL_OPT_BIT_STOP_ON_FOLLOWING_ERR       = 0x00000010
SA_CTL_POS_CTRL_OPT_BIT_TARGET_TO_ZERO_VOLTAGE      = 0x00000020

#/**********************************************************/
#/* CALIBRATION OPTIONS                                    */
#/**********************************************************/

SA_CTL_CALIB_OPT_BIT_DIRECTION                      = 0x00000001
SA_CTL_CALIB_OPT_BIT_DIST_CODE_INV_DETECT           = 0x00000002
SA_CTL_CALIB_OPT_BIT_ASC_CALIBRATION                = 0x00000004
SA_CTL_CALIB_OPT_BIT_REF_MARK_TEST                  = 0x00000008
SA_CTL_CALIB_OPT_BIT_LIMITED_TRAVEL_RANGE           = 0x00000100

#/**********************************************************/
#/* REFERENCING OPTIONS                                    */
#/**********************************************************/

SA_CTL_REF_OPT_BIT_START_DIR                        = 0x00000001
SA_CTL_REF_OPT_BIT_REVERSE_DIR                      = 0x00000002
SA_CTL_REF_OPT_BIT_AUTO_ZERO                        = 0x00000004
SA_CTL_REF_OPT_BIT_ABORT_ON_ENDSTOP                 = 0x00000008
SA_CTL_REF_OPT_BIT_CONTINUE_ON_REF_FOUND            = 0x00000010
SA_CTL_REF_OPT_BIT_STOP_ON_REF_FOUND                = 0x00000020

#/**********************************************************/
#/* SENSOR POWER MODES                                     */
#/**********************************************************/

SA_CTL_SENSOR_MODE_DISABLED                         = 0
SA_CTL_SENSOR_MODE_ENABLED                          = 1
SA_CTL_SENSOR_MODE_POWER_SAVE                       = 2

#/**********************************************************/
#/* BROADCAST STOP OPTIONS                                 */
#/**********************************************************/

SA_CTL_STOP_OPT_BIT_END_STOP_REACHED                = 0x00000001
SA_CTL_STOP_OPT_BIT_RANGE_LIMIT_REACHED             = 0x00000002
SA_CTL_STOP_OPT_BIT_FOLLOWING_LIMIT_REACHED         = 0x00000004

#/**********************************************************/
#/* INPUT/OUTPUT TRIGGER                                   */
#/**********************************************************/

#  device input trigger modes
SA_CTL_DEV_INPUT_TRIG_MODE_DISABLED                 = 0
SA_CTL_DEV_INPUT_TRIG_MODE_EMERGENCY_STOP           = 1
SA_CTL_DEV_INPUT_TRIG_MODE_STREAM                   = 2
SA_CTL_DEV_INPUT_TRIG_MODE_CMD_GROUP                = 3
SA_CTL_DEV_INPUT_TRIG_MODE_EVENT                    = 4

#  output trigger modes
SA_CTL_CH_OUTPUT_TRIG_MODE_CONSTANT                 = 0
SA_CTL_CH_OUTPUT_TRIG_MODE_POSITION_COMPARE         = 1
SA_CTL_CH_OUTPUT_TRIG_MODE_TARGET_REACHED           = 2
SA_CTL_CH_OUTPUT_TRIG_MODE_ACTIVELY_MOVING          = 3

#  trigger conditions
SA_CTL_TRIGGER_CONDITION_RISING                     = 0
SA_CTL_TRIGGER_CONDITION_FALLING                    = 1
SA_CTL_TRIGGER_CONDITION_EITHER                     = 2

#  trigger polarities
SA_CTL_TRIGGER_POLARITY_ACTIVE_LOW                  = 0
SA_CTL_TRIGGER_POLARITY_ACTIVE_HIGH                 = 1

#/**********************************************************/
#/* HM LOCK OPTIONS                                        */
#/**********************************************************/

SA_CTL_HM1_LOCK_OPT_BIT_GLOBAL                      = 0x00000001
SA_CTL_HM1_LOCK_OPT_BIT_CONTROL                     = 0x00000002
SA_CTL_HM1_LOCK_OPT_BIT_CHANNEL_MENU                = 0x00000010
SA_CTL_HM1_LOCK_OPT_BIT_GROUP_MENU                  = 0x00000020
SA_CTL_HM1_LOCK_OPT_BIT_SETTINGS_MENU               = 0x00000040
SA_CTL_HM1_LOCK_OPT_BIT_LOAD_CFG_MENU               = 0x00000080
SA_CTL_HM1_LOCK_OPT_BIT_SAVE_CFG_MENU               = 0x00000100
SA_CTL_HM1_LOCK_OPT_BIT_CTRL_MODE_PARAM_MENU        = 0x00000200
SA_CTL_HM1_LOCK_OPT_BIT_CHANNEL_NAME                = 0x00001000
SA_CTL_HM1_LOCK_OPT_BIT_POS_TYPE                    = 0x00002000
SA_CTL_HM1_LOCK_OPT_BIT_SAFE_DIR                    = 0x00004000
SA_CTL_HM1_LOCK_OPT_BIT_CALIBRATE                   = 0x00008000
SA_CTL_HM1_LOCK_OPT_BIT_REFERENCE                   = 0x00010000
SA_CTL_HM1_LOCK_OPT_BIT_SET_POSITION                = 0x00020000
SA_CTL_HM1_LOCK_OPT_BIT_MAX_CLF                     = 0x00040000
SA_CTL_HM1_LOCK_OPT_BIT_POWER_MODE                  = 0x00080000
SA_CTL_HM1_LOCK_OPT_BIT_ACTUATOR_MODE               = 0x00100000
SA_CTL_HM1_LOCK_OPT_BIT_RANGE_LIMIT                 = 0x00200000
SA_CTL_HM1_LOCK_OPT_BIT_CONTROL_LOOP_INPUT          = 0x00400000

#/**********************************************************/
#/* EVENT NOTIFICATION OPTIONS                             */
#/**********************************************************/

SA_CTL_EVT_OPT_BIT_REQUEST_READY_ENABLED            = 0x00000001

#/**********************************************************/
#/* CUSTOM POSITIONER TYPE                                 */
#/**********************************************************/

SA_CTL_POSITIONER_TYPE_CUSTOM0                      = 250
SA_CTL_POSITIONER_TYPE_CUSTOM1                      = 251
SA_CTL_POSITIONER_TYPE_CUSTOM2                      = 252
SA_CTL_POSITIONER_TYPE_CUSTOM3                      = 253

#/**********************************************************/
#/* WRITE PROTECTION                                       */
#/**********************************************************/

SA_CTL_POS_WRITE_PROTECTION_KEY                     = 0x534D4152

#/**********************************************************/
#/* MOVEMENT TYPES                                         */
#/**********************************************************/

SA_CTL_POS_MOVEMENT_TYPE_LINEAR                     = 0
SA_CTL_POS_MOVEMENT_TYPE_ROTATORY                   = 1
SA_CTL_POS_MOVEMENT_TYPE_GONIOMETER                 = 2
SA_CTL_POS_MOVEMENT_TYPE_TIP_TILT                   = 3
SA_CTL_POS_MOVEMENT_TYPE_IRIS                       = 4
SA_CTL_POS_MOVEMENT_TYPE_OSCILLATOR                 = 5

#/**********************************************************/
#/* IO MODULE VOLTAGE                                      */
#/**********************************************************/

SA_CTL_IO_MODULE_VOLTAGE_3V3                        = 0
SA_CTL_IO_MODULE_VOLTAGE_5V                         = 1

#/**********************************************************/
#/* IO MODULE OPTIONS                                      */
#/**********************************************************/

SA_CTL_IO_MODULE_OPT_BIT_ENABLED                    = 0x00000001  # deprecated
SA_CTL_IO_MODULE_OPT_BIT_DIGITAL_OUTPUT_ENABLED     = 0x00000001
SA_CTL_IO_MODULE_OPT_BIT_EVENTS_ENABLED             = 0x00000002
SA_CTL_IO_MODULE_OPT_BIT_ANALOG_OUTPUT_ENABLED      = 0x00000004

#/**********************************************************/
#/* IO MODULE ANALOG INPUT RANGE                           */
#/**********************************************************/

SA_CTL_IO_MODULE_ANALOG_INPUT_RANGE_BI_10V          = 0
SA_CTL_IO_MODULE_ANALOG_INPUT_RANGE_BI_5V           = 1
SA_CTL_IO_MODULE_ANALOG_INPUT_RANGE_BI_2_5V         = 2
SA_CTL_IO_MODULE_ANALOG_INPUT_RANGE_UNI_10V         = 3
SA_CTL_IO_MODULE_ANALOG_INPUT_RANGE_UNI_5V          = 4

#/**********************************************************/
#/* SIGNAL CORRECTION OPTIONS                              */
#/**********************************************************/

SA_CTL_SIGNAL_CORR_OPT_BIT_DAC                      = 0x00000002
SA_CTL_SIGNAL_CORR_OPT_BIT_DPEC                     = 0x00000008
SA_CTL_SIGNAL_CORR_OPT_BIT_ASC                      = 0x00000010

#/**********************************************************/
#/* NETWORK DISCOVER MODE                                  */
#/**********************************************************/

SA_CTL_NETWORK_DISCOVER_MODE_DISABLED               = 0
SA_CTL_NETWORK_DISCOVER_MODE_PASSIVE                = 1
SA_CTL_NETWORK_DISCOVER_MODE_ACTIVE                 = 2

#/**********************************************************/
#/* REFERENCE TYPES                                        */
#/**********************************************************/

SA_CTL_REF_TYPE_NONE                                = 0
SA_CTL_REF_TYPE_END_STOP                            = 1
SA_CTL_REF_TYPE_SINGLE_CODED                        = 2
SA_CTL_REF_TYPE_DISTANCE_CODED                      = 3

#endif // SMARACT_CTL_CONSTANTS_H
