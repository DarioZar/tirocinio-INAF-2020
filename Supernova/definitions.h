#define  PHYSICS                        HD
#define  DIMENSIONS                     2
#define  COMPONENTS                     2
#define  GEOMETRY                       CYLINDRICAL
#define  BODY_FORCE                     NO
#define  FORCED_TURB                    NO
#define  COOLING                        NO
#define  RECONSTRUCTION                 LINEAR
#define  TIME_STEPPING                  CHARACTERISTIC_TRACING
#define  DIMENSIONAL_SPLITTING          NO
#define  NTRACER                        2
#define  USER_DEF_PARAMETERS            3

/* -- physics dependent declarations -- */

#define  EOS                            IDEAL
#define  ENTROPY_SWITCH                 NO
#define  THERMAL_CONDUCTION             NO
#define  VISCOSITY                      NO
#define  ROTATING_FRAME                 NO

/* -- user-defined parameters (labels) -- */

#define  ENRG0                          0
#define  DNST0                          1
#define  GAMMA                          2

/* [Beg] user-defined constants (do not change this line) */

#define  INITIAL_SMOOTHING              NO
#define  M_SUN                          1.98855e33
#define  UNIT_LENGTH                    3.0856776e18
#define  UNIT_VELOCITY                  1e8
#define  UNIT_DENSITY                   1.6726219e-24

/* [End] user-defined constants (do not change this line) */
