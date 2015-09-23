/*
  Source:
    http://www.mymathlib.com/diffeq/bulirsch_stoer.html
 */
#include <math.h>
#include <stdio.h>
#define ATTEMPTS sizeof(number_of_steps)/sizeof(number_of_steps[0])
static int number_of_steps[]={2,4,6,8,12,16,24,32,48,64,96,128};

static int Rational_Extrapolation_to_Zero(double *fzero,double tableau[],
					  double x[],double f,int n) 
{
   double t, up, across, denominator, dum;
   int col;

   if (n == 0) {  *fzero = f; tableau[0] = f; return 0; }
   if ( x[n] == 0.0 ) { *fzero = f; return -2; }
   
   across = 0.0;                                                        
   up = tableau[0];                                                    
   tableau[0] = f;                                               

   for (col = 1; col <= n; col++) {
      denominator = tableau[col-1] - across;                                  
      if (denominator == 0.0) return -1;
      dum = 1.0 - (tableau[col-1] - up) / denominator;
      denominator = (x[n - col] / x[n]) * dum - 1.0;
      if (denominator == 0.0) return -1;
      t = tableau[col-1] + ( tableau[col-1] - up ) / denominator;
      across = up;
      up = tableau[col];
      tableau[col] = t;
   }
   *fzero = t;
   return 0;
}

static int Polynomial_Extrapolation_to_Zero(double *fzero,double tableau[],
					    double x[], double f, int n )
{
   double back_two_columns;    //  T[row,col-2];
   double old_aux;             //  T[row-1,col];
   double new_value;           //  T[row,col];
   double vertical_diff;       //  T[row,col]-T[row-1,col]
   double backslant_diff;      //  T[row,col]-T[row,col-1]
   double forwardslant_diff;   //  T[row,col]-T[row-1,col-1];
   double denominator;        
   int i;

   if (n == 0) { tableau[0] = f; return 0; }
   if ( x[n] == 0.0 ) { *fzero = f; return -2; }

   back_two_columns = 0.0;
   old_aux = tableau[0];
   tableau[0] = f;
   for (i = 0; i < n; i++) {
      vertical_diff = tableau[i] - old_aux;
      backslant_diff = tableau[i] - back_two_columns;
      forwardslant_diff = backslant_diff - vertical_diff;
      denominator = (x[n-i-1]/x[n]) * forwardslant_diff - backslant_diff;
      if (denominator == 0.0) return -1;
      back_two_columns = old_aux;
      old_aux = tableau[i+1];
      tableau[i+1] = tableau[i] + vertical_diff * backslant_diff / denominator;
   }
   *fzero = tableau[n];
   return 0;
}

static int Graggs_Method(int (*f)(double,double*,double*,void*),
			 double y0[],
			 double t0,double t,
			 int number_of_steps,
			 void *params,
			 double yres[]) {
  
  double y1[1],y05[1],y15[1],y2[1],y25[1],yaux[1];
  double h=(t-t0)/(double)number_of_steps;
  double h2=h+h;

  yaux[0]=y0[0];
  (*f)(t0,yaux,y05,params);

  y1[0]=yaux[0]+h*y05[0];
  while(--number_of_steps) {
    t0+=h;
    (*f)(t0,y1,y15,params);
    y2[0]=yaux[0]+h2*y15[0];
    yaux[0]=y1[0];
    y1[0]=y2[0];
  } 

  (*f)(t,y1,y25,params);
  yres[0]=0.5*(yaux[0]+y1[0]+h*y25[0]);
  return 0;
}

int Gragg_Bulirsch_Stoer(int (*f)(double,double*,double*,void*), 
			 double y0[], double y1[],
			 double t, double h, double *h_new, 
			 double epsilon, double yscale, 
			 int rational_extrapolate,
			 void *params)
{
  double step_size2[ATTEMPTS];
  double tableau[ATTEMPTS+1];
  double dum;
  double est[1],dest;
  double old_est[1];
  
  int (*Extrapolate)(double*,double*,double*,double,int);
  int i;
  int err;

  if(yscale==0.0) return -3;
  if(rational_extrapolate) Extrapolate=Rational_Extrapolation_to_Zero;
  else Extrapolate=Polynomial_Extrapolation_to_Zero;
 
  Graggs_Method(f,y0,t,t+h,number_of_steps[0],params,est);
  step_size2[0]=(dum=h/(double)number_of_steps[0],dum*dum);
  y1[0]=est[0];
  
  if(err=Extrapolate(&y1[0],tableau,step_size2,est[0],0)<0) return err-1;

  for(i = 1; i < ATTEMPTS; i++) {
    old_est[0]=y1[0];
    Graggs_Method(f,y0,t,t+h,number_of_steps[i],params,est);
    step_size2[i]=(dum=h/(double)number_of_steps[i],dum*dum);
    if(err=Extrapolate(&y1[0],tableau,step_size2,est[0],i)<0) return err-1;
    dest=fabs(y1[0]/yscale-old_est[0]/yscale);
    if(dest<epsilon){
      if(i>1) *h_new=8.0*h/(double)number_of_steps[i-1];
      else *h_new=h;
      return 0;
    }
  }
  return -1;
}

