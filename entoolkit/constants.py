"""
Enumerations and constants for the EPANET 2.2 toolkit.

This module contains all the property codes, unit codes, and object type 
constants used by both the legacy and modern EnToolkit APIs.
"""

# --- Logging Configuration ---
LOG_MAX_SIZE_MB = 5  # Max size per log file in MB
LOG_FILE_NAME = "entoolkit.log"

# --- Size Limits ---
EN_MAXID = 31
EN_MAXMSG = 255

# --- Node Properties ---
EN_ELEVATION    = 0
EN_BASEDEMAND   = 1
EN_PATTERN      = 2
EN_EMITTER      = 3
EN_INITQUAL     = 4
EN_SOURCEQUAL   = 5
EN_SOURCEPAT    = 6
EN_SOURCETYPE   = 7
EN_TANKLEVEL    = 8
EN_DEMAND       = 9
EN_HEAD         = 10
EN_PRESSURE     = 11
EN_QUALITY      = 12
EN_SOURCEMASS   = 13
EN_INITVOLUME   = 14
EN_MIXMODEL     = 15
EN_MIXZONEVOL   = 16
EN_TANKDIAM     = 17
EN_MINVOLUME    = 18
EN_VOLCURVE     = 19
EN_MINLEVEL     = 20
EN_MAXLEVEL     = 21
EN_MIXFRACTION  = 22
EN_TANK_KBULK   = 23
EN_TANKVOLUME   = 24
EN_MAXVOLUME    = 25
EN_CANOVERFLOW  = 26  # v2.2+
EN_DEMANDDEFICIT = 27  # v2.2+
EN_NODE_INCONTROL = 28  # v2.2+
EN_EMITTERFLOW    = 29  # v2.2+
EN_LEAKAGEFLOW    = 30  # v2.2+
EN_DEMANDFLOW     = 31  # v2.2+
EN_FULLDEMAND     = 32  # v2.2+

# --- Link Properties ---
EN_DIAMETER     = 0
EN_LENGTH       = 1
EN_ROUGHNESS    = 2
EN_MINORLOSS    = 3
EN_INITSTATUS   = 4
EN_INITSETTING  = 5
EN_KBULK        = 6
EN_KWALL        = 7
EN_FLOW         = 8
EN_VELOCITY     = 9
EN_HEADLOSS     = 10
EN_STATUS       = 11
EN_SETTING      = 12
EN_ENERGY       = 13
EN_LINKQUAL     = 14
EN_LINKPATTERN  = 15
EN_PUMP_STATE   = 16
EN_PUMP_EFFIC   = 17
EN_PUMP_POWER   = 18
EN_PUMP_HCURVE  = 19
EN_PUMP_ECURVE  = 20
EN_PUMP_ECOST   = 21
EN_PUMP_EPAT    = 22
EN_LINK_INCONTROL = 23  # v2.2+
EN_GPV_CURVE    = 24  # v2.2+
EN_PCV_CURVE    = 25  # v2.2+
EN_LEAK_AREA    = 26  # v2.2+
EN_LEAK_EXPAN   = 27  # v2.2+
EN_LINK_LEAKAGE = 28  # v2.2+
EN_VALVE_TYPE   = 29  # v2.2+

# --- Time Parameters ---
EN_DURATION     = 0
EN_HYDSTEP      = 1
EN_QUALSTEP     = 2
EN_PATTERNSTEP  = 3
EN_PATTERNSTART = 4
EN_REPORTSTEP   = 5
EN_REPORTSTART  = 6
EN_RULESTEP     = 7
EN_STATISTIC    = 8
EN_PERIODS      = 9
EN_STARTTIME    = 10
EN_HTIME        = 11
EN_QTIME        = 12
EN_HALTFLAG     = 13
EN_NEXTEVENT    = 14  # v2.2+
EN_NEXTEVENTTANK = 15  # v2.2+

# --- Analysis Statistics ---
EN_ITERATIONS      = 0
EN_RELATIVEERROR   = 1
EN_MAXHEADERROR    = 2
EN_MAXFLOWCHANGE   = 3
EN_MASSBALANCE     = 4
EN_DEFICIENTNODES  = 5    # v2.2+
EN_DEMANDREDUCTION = 6    # v2.2+
EN_LEAKAGELOSS     = 7    # v2.2+

# --- Object Types ---
EN_NODE    = 0
EN_LINK    = 1
EN_TIMEPAT = 2
EN_CURVE   = 3
EN_CONTROL = 4
EN_RULE    = 5

# --- Count Types ---
EN_NODECOUNT    = 0
EN_TANKCOUNT    = 1
EN_LINKCOUNT    = 2
EN_PATCOUNT     = 3
EN_CURVECOUNT   = 4
EN_CONTROLCOUNT = 5
EN_RULECOUNT    = 6

# --- Node Types ---
EN_JUNCTION    = 0
EN_RESERVOIR   = 1
EN_TANK        = 2

# --- Link Types ---
EN_CVPIPE       = 0
EN_PIPE         = 1
EN_PUMP         = 2
EN_PRV          = 3
EN_PSV          = 4
EN_PBV          = 5
EN_FCV          = 6
EN_TCV          = 7
EN_GPV          = 8
EN_PCV          = 9

# --- Link Status ---
EN_CLOSED       = 0
EN_OPEN         = 1

# --- Pump States ---
EN_PUMP_XHEAD   = 0
EN_PUMP_CLOSED  = 2
EN_PUMP_OPEN    = 3
EN_PUMP_XFLOW   = 5

# --- Quality Types ---
EN_NONE        = 0
EN_CHEM        = 1
EN_AGE         = 2
EN_TRACE       = 3

# --- Source Types ---
EN_CONCEN      = 0
EN_MASS        = 1
EN_SETPOINT    = 2
EN_FLOWPACED   = 3

# --- Head Loss Types ---
EN_HW          = 0
EN_DW          = 1
EN_CM          = 2

# --- Flow Units ---
EN_CFS         = 0
EN_GPM         = 1
EN_MGD         = 2
EN_IMGD        = 3
EN_AFD         = 4
EN_LPS         = 5
EN_LPM         = 6
EN_MLD         = 7
EN_CMH         = 8
EN_CMD         = 9
EN_CMS         = 10

# --- Legacy Category Code ---
EN_FLOWUNITS    = 1

# --- Pressure Units ---
EN_PSI          = 0
EN_KPA          = 1
EN_METERS       = 2
EN_BAR          = 3
EN_FEET         = 4

# --- Demand Models ---
EN_DDA         = 0    # v2.2+
EN_PDA         = 1    # v2.2+

# --- Option Types ---
EN_TRIALS         = 0
EN_ACCURACY       = 1
EN_TOLERANCE      = 2
EN_EMITEXPON      = 3
EN_DEMANDMULT     = 4
EN_HEADERROR      = 5
EN_FLOWCHANGE     = 6
EN_HEADLOSSFORM   = 7
EN_GLOBALEFFIC    = 8
EN_GLOBALPRICE    = 9
EN_GLOBALPATTERN  = 10
EN_DEMANDCHARGE   = 11
EN_SP_GRAVITY     = 12
EN_SP_VISCOS      = 13
EN_UNBALANCED     = 14
EN_CHECKFREQ      = 15
EN_MAXCHECK       = 16
EN_DAMPLIMIT      = 17
EN_SP_DIFFUS      = 18
EN_BULKORDER      = 19
EN_WALLORDER      = 20
EN_TANKORDER      = 21
EN_CONCENLIMIT    = 22
EN_DEMANDPATTERN  = 23  # v2.2+
EN_EMITBACKFLOW   = 24  # v2.2+
EN_PRESS_UNITS    = 25  # v2.2+
EN_STATUS_REPORT  = 26  # v2.2+
EN_DEMANDMODEL    = 27  # v2.2+

# --- Control Types ---
EN_LOWLEVEL    = 0
EN_HILEVEL     = 1
EN_TIMER       = 2
EN_TIMEOFDAY   = 3

# --- Statistic Types ---
EN_SERIES      = 0
EN_AVERAGE     = 1
EN_MINIMUM     = 2
EN_MAXIMUM     = 3
EN_RANGE       = 4

# --- Mixing Models ---
EN_MIX1        = 0
EN_MIX2        = 1
EN_FIFO        = 2
EN_LIFO        = 3

# --- Init Options ---
EN_NOSAVE        = 0
EN_SAVE          = 1
EN_INITFLOW      = 10
EN_SAVE_AND_INIT = 11

# --- Pump Types ---
EN_CONST_HP    = 0
EN_POWER_FUNC  = 1
EN_CUSTOM      = 2
EN_NOCURVE     = 3

# --- Curve Types ---
EN_VOLUME_CURVE  = 0
EN_PUMP_CURVE    = 1
EN_EFFIC_CURVE   = 2
EN_HLOSS_CURVE   = 3
EN_GENERIC_CURVE = 4
EN_VALVE_CURVE   = 5

# --- Action Codes ---
EN_UNCONDITIONAL = 0
EN_CONDITIONAL   = 1

# --- Status Report Levels ---
EN_NO_REPORT     = 0
EN_NORMAL_REPORT = 1
EN_FULL_REPORT   = 2
