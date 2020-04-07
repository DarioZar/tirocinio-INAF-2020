/* ///////////////////////////////////////////////////////////////////// */
/*! 
  \file  
  \brief Sedov-Taylor blast wave adapted for Supernova.

  Set the initial condition to analyze the Sedov expansion phase of
  a Supernova Remnant.
  The Remnant is spherical and analyzed in Cylindrical (2D), and has
  a radius of 1 Parsec. Its density \c rhoint is calculated from its 
  initial mass. Its radial velocity goes linearly from 0 to \c vmax. Its 
  pressure is given by the state equation p=2nkT of a ionized H gas.
  Ambient density and pressure are that of the ISM and equal to 
  \c rho_{ext} and \c p_{ext}. 

  The input parameters read from pluto.ini are labeled as:
  - <tt>g_inputParam[ENRG0]</tt>: initial energy of the blast wave
    (\e not energy density);
  - <tt>g_inputParam[DNST0]</tt>: initial constant density;
  - <tt>g_inputParam[GAMMA]</tt>: specific heat ratio.
  
*/
/* ///////////////////////////////////////////////////////////////////// */
#include "pluto.h"

/* ********************************************************************* */
void Init(double *us, double x1, double x2, double x3)
/*
 *
 *
 *
 *********************************************************************** */
{
  double k, T_ext, rho_ext;
  double m, dr, rho_int, T_int, vmax;
  double r, vol;
  double tor_zpos, tor_rpos, tor_rad, tor_rho;
  double r2;

  k = 1.380649e-16;              // Boltzmann constant
  T_ext = 1.e2;                  // ISM temperature
  rho_ext = 1.0 * UNIT_DENSITY;  // ISM density (1 particle/cm^3)
  T_int = 1.e6;                  // RSN temperature
  m = 10.0 * M_SUN;              // RSN mass
  dr = 1.0 * UNIT_LENGTH;        // RSN radius
  vmax = 5.0 * UNIT_VELOCITY;    // RSN max velocity
  tor_zpos = 0.0 * UNIT_LENGTH;  // Torus z position
  tor_rpos = 2.5 * UNIT_LENGTH;  // Torus r position
  tor_rad = 0.5 * UNIT_LENGTH;   // Torus radius
  tor_rho = 1.e2 * UNIT_DENSITY; // Torus density

  vol = 4.0 / 3.0 * CONST_PI * dr * dr * dr; // RSN volume (sphere)
  rho_int = m / vol;                         // RSN density

  r = EXPAND(x1 * x1, +x2 * x2, +x3 * x3);
  r = sqrt(r);
  r2 = EXPAND((x1 - tor_rpos / UNIT_LENGTH) * (x1 - tor_rpos / UNIT_LENGTH), +(x2 - tor_zpos / UNIT_LENGTH) * (x2 - tor_zpos / UNIT_LENGTH), +x3 * x3);
  r2 = sqrt(r2);
  us[VX3] = 0.0;
  if (r <= dr / UNIT_LENGTH)
  {
    // RSN rho, velocity, pressure
    us[RHO] = rho_int / UNIT_DENSITY;
    us[VX1] = vmax * x1 * UNIT_LENGTH / dr * 1 / UNIT_VELOCITY;
    us[VX2] = vmax * x2 * UNIT_LENGTH / dr * 1 / UNIT_VELOCITY;
    us[PRS] = 2 * (rho_int / UNIT_DENSITY) * k * T_int / (UNIT_DENSITY * UNIT_VELOCITY * UNIT_VELOCITY);
    us[TRC] = 1.;
    us[TRC + 1] = 0.;
  }
  else if (r2 <= tor_rad / UNIT_LENGTH)
  {
    // Torus
    us[RHO] = tor_rho / UNIT_DENSITY;
    us[VX1] = 0.0;
    us[VX2] = 0.0;
    us[PRS] = 2 * (rho_ext / UNIT_DENSITY) * k * T_ext / (UNIT_DENSITY * UNIT_VELOCITY * UNIT_VELOCITY);
    us[TRC] = 0.;
    us[TRC + 1] = 1.;
  }
  else
  {
    // ISM rho, velocity, pressure
    us[RHO] = rho_ext / UNIT_DENSITY;
    us[VX1] = 0.0;
    us[VX2] = 0.0;
    us[PRS] = 2 * (rho_ext / UNIT_DENSITY) * k * T_ext / (UNIT_DENSITY * UNIT_VELOCITY * UNIT_VELOCITY);
    us[TRC] = 0.;
    us[TRC + 1] = 0.;
  }
}

/* ********************************************************************* */
void InitDomain(Data *d, Grid *grid)
/*! 
 * Assign initial condition by looping over the computational domain.
 * Called after the usual Init() function to assign initial conditions
 * on primitive variables.
 * Value assigned here will overwrite those prescribed during Init().
 *
 *
 *********************************************************************** */
{
}

/* ********************************************************************* */
void Analysis(const Data *d, Grid *grid)
/* 
 *
 *
 *********************************************************************** */
{
}

/* ********************************************************************* */
void UserDefBoundary(const Data *d, RBox *box, int side, Grid *grid)
/*
 *
 *
 *********************************************************************** */
{
}
