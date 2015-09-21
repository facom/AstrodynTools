/*
Kernels:
http://naif.jpl.nasa.gov/pub/naif/
*/
//////////////////////////////////////////
//HEADERS
//////////////////////////////////////////
#include <stdio.h>
#include <math.h>
#include <string.h>
#include <stdlib.h>
#include <SpiceUsr.h>
#include <novas.h>
#include <eph_manager.h>
#include <gsl/gsl_errno.h>
#include <gsl/gsl_math.h>
#include <gsl/gsl_roots.h>
#include <gsl/gsl_multifit_nlin.h>
#include <gsl/gsl_min.h>
#include <gsl/gsl_multimin.h>
#include <gsl/gsl_vector.h>
#include <gsl/gsl_blas.h>
#include <gsl/gsl_rng.h>
#include <gsl/gsl_randist.h>
#include <gsl/gsl_const_mksa.h>

//////////////////////////////////////////
//MACROS
//////////////////////////////////////////
#define D2R(x) (x*M_PI/180)
#define R2D(x) (x*180/M_PI)
#define POWI(x,n) gsl_pow_int(x,n)
#define SGN(x) (x<0?-1:+1)

//////////////////////////////////////////
//CSPICE CONSTANTS
//////////////////////////////////////////
#define EARTH_ID "EARTH"

//////////////////////////////////////////
//GLOBAL VARIABLES
//////////////////////////////////////////
double REARTH;
double RPEARTH;
double FEARTH;
gsl_rng* RAND;

//////////////////////////////////////////
//ROUTINES
//////////////////////////////////////////
int initSpice(void)
{
  SpiceInt n;
  SpiceDouble radii[3];

  //KERNELS
  furnsh_c("kernels.txt");

  //EARTH RADII
  bodvrd_c(EARTH_ID,"RADII",3,&n,radii);
  REARTH=radii[0];
  RPEARTH=radii[0];
  FEARTH=(radii[0]-radii[2])/radii[0];

  //RANDOM NUMBERS
  RAND=gsl_rng_alloc(gsl_rng_default);

  return 0;
}

char* dec2sex(double dec)
{
  double d,m,s;
  int id,im,sgn;
  char *str=(char*)calloc(sizeof(char),100); 
  d=fabs(dec);
  sgn=dec/d;
  id=floor(d);
  m=(d-id)*60;
  im=floor(m);
  s=(m-im)*60;
  sprintf(str,"%+d:%02d:%.3f",sgn*id,im,s);
  return str;
}

double sex2dec(double d,double m,double s)
{
  double s2d;
  s2d=d+m/60.0+s/3600.0;
  return s2d;
}

char* vec2str(double vec[],char frm[]="%.8e")
{
  char format[100];
  char *str=(char*)calloc(sizeof(char),100); 
  sprintf(format,"%s %s %s",frm,frm,frm);
  sprintf(str,format,vec[0],vec[1],vec[2]);
  return str;
}

double greatCircleDistance(double lam1,double lam2,
			   double phi1,double phi2)
{
  double d;

  //HARVESINE FORMULA
  double sf,sl;
  sf=sin((phi2-phi1)/2);
  sl=sin((lam2-lam1)/2);
  d=2*asin(sqrt(sf*sf+cos(phi1)*cos(phi2)*sl*sl));

  return d;
}

int bodyEphemerisApparent(ConstSpiceChar *body,
			  ConstSpiceChar *bodyname,
			  SpiceDouble t,
			  SpiceDouble lon,SpiceDouble lat,SpiceDouble alt,
			  SpiceDouble *range,
			  SpiceDouble *ltime,
			  SpiceDouble *raJ2000,
			  SpiceDouble *decJ2000,
			  SpiceDouble *ra,
			  SpiceDouble *dec
			  )
{
  SpiceDouble earthSSBJ2000[6];
  SpiceDouble bodyJ2000[6],bodySSBJ2000[6],ltbody;
  SpiceDouble bodyTOPOJ2000[3],bodyTOPOEpoch[3];
  SpiceDouble Dbody,RAbody,DECbody,RAbodyJ2000,DECbodyJ2000;
  SpiceDouble observerITRF93[3],observerJ2000[3],observerSSBJ2000[3];
  SpiceDouble M_J2000_Epoch[3][3]={{1,0,0},{0,1,0},{0,0,1}};
  SpiceDouble M_ITRF93_J2000[3][3];
  SpiceDouble d,lt,ltmp,ltold,lttol=1E-2;
  int i,ie=0,ncn=10;
  double cspeed=clight_c();

  //ROTATION MATRIX AT THE TIME OF EPHEMERIS
  pxform_c("J2000","EARTHTRUEEPOCH",t,M_J2000_Epoch);
  pxform_c("ITRF93","J2000",t,M_ITRF93_J2000);

  //OBSERVER POSITION J2000 RELATIVE TO EARTH CENTER
  georec_c(D2R(lon),D2R(lat),alt/1000.0,REARTH,FEARTH,observerITRF93);
  mxv_c(M_ITRF93_J2000,observerITRF93,observerJ2000);

  //&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
  //ASTROMETRIC POSITION
  //&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
  i=0;
  lt=0.0;ltold=1.0;
  spkezr_c(EARTH_ID,t,"J2000","NONE","SOLAR SYSTEM BARYCENTER",
	   earthSSBJ2000,&ltmp);
  vadd_c(earthSSBJ2000,observerJ2000,observerSSBJ2000);
  while((fabs(lt-ltold)/lt)>=lttol && i<ncn){
    ltold=lt;
    spkezr_c(body,t-lt,"J2000","NONE","SOLAR SYSTEM BARYCENTER",bodySSBJ2000,&ltmp);
    vsub_c(bodySSBJ2000,observerSSBJ2000,bodyTOPOJ2000);
    d=vnorm_c(bodyTOPOJ2000);
    lt=d/cspeed;
    i++;
  }
  recrad_c(bodyTOPOJ2000,&d,&RAbodyJ2000,&DECbodyJ2000);
  
  //&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
  //CORRECTED POSITION
  //&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
  //OBSERVER POSITION J2000
  spkezr_c(EARTH_ID,t,"J2000","NONE","EARTH BARYCENTER",
	   earthSSBJ2000,&lt);
  vadd_c(earthSSBJ2000,observerJ2000,observerSSBJ2000);

  //CORRECTED OBJECT POSITION
  spkezr_c(body,t,"J2000","LT+S","EARTH BARYCENTER",
	   bodySSBJ2000,&lt);
  vsub_c(bodySSBJ2000,observerSSBJ2000,bodyTOPOJ2000);

  //PRECESS POSITION
  mxv_c(M_J2000_Epoch,bodyTOPOJ2000,bodyTOPOEpoch);

  //RA & DEC PRECESSED
  recrad_c(bodyTOPOEpoch,&d,&RAbody,&DECbody);

  //RETURNED
  *range=d;
  *ltime=lt;
  *ra=RAbody*180/M_PI/15;
  *dec=DECbody*180/M_PI;
  *raJ2000=RAbodyJ2000*180/M_PI/15;
  *decJ2000=DECbodyJ2000*180/M_PI;
  return 0;
}

/*
  Calculates the julian date.  If et=0 it gives the Ephemeris Julian
  Date.  If et=1 it gives the Jul ian Date in the International Atomic
  time reference.
 */
SpiceDouble t2jd(SpiceDouble t,int et=0)
{
  SpiceDouble deltat;
  deltet_c(t,"ET",&deltat);
  double tjd=unitim_c(t,"ET","JED");
  return tjd-et*deltat/86400.0;
}

/*
  Matrix to convert from planetocentric coordinates to horizontal
  coordinates and viceversa.

  See discussion at:
  https://naif.jpl.nasa.gov/pipermail/spice_discussion/2010-July/000307.html

  h2m: converts from geocentric to topocentric
  h2i: converts from topocentric to geocentric
 */
void hormat(SpiceDouble lat,SpiceDouble lon,SpiceDouble h2m[3][3],SpiceDouble h2i[3][3])
{
  SpiceDouble geopos[3],normal[3],ux[]={1,0,0},uy[]={0,1,0},uz[]={0,0,1};
  georec_c(D2R(lon),D2R(lat),0.0,REARTH,FEARTH,geopos);
  surfnm_c(REARTH,REARTH,RPEARTH,geopos,normal);
  ucrss_c(normal,uz,uy);
  ucrss_c(uy,normal,ux);
  h2m[0][0]=ux[0];h2m[0][1]=ux[1];h2m[0][2]=ux[2];
  h2m[1][0]=uy[0];h2m[1][1]=uy[1];h2m[1][2]=uy[2];
  h2m[2][0]=normal[0];h2m[2][1]=normal[1];h2m[2][2]=normal[2];
  invert_c(h2m,h2i);
}
