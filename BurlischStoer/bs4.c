/*
  Source:
    http://www.mymathlib.com/diffeq/bulirsch_stoer.html
*/
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
//*
#define ATTEMPTS 12
static int number_of_steps[]={2,4,6,8,12,16,24,32,48,64,96,128};
//*/
/*
#define ATTEMPTS 16
static int number_of_steps[]={2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32};
//*/

char* strVec(double a[],int n)
{
  int i;
  char* string;
  string=(char*)calloc(sizeof(char),100*n);
  for(i=0;i<n;i++)
    sprintf(string,"%s %.17e",string,a[i]);
  return string;
}

int copyVec(double tgt[],double src[],int n)
{
  memcpy(tgt,src,n*sizeof(double));
  return 0;
}

int sumVec(double c[],double ca,double a[],double cb,double b[],int n)
{
  int i;
  for(i=n;i-->0;)
    c[i]=ca*a[i]+cb*b[i];
  return 0;
}

double maxAbsVec(double a[],int n)
{
  int i;
  double max=-1E100;
  for(i=n;i-->0;) if(fabs(a[i])>max) max=fabs(a[i]);
  return max;
}

static int Rational_Extrapolation_to_Zero(double *fzero,double tableau[],
					  double x[],double f,int n) 
{
   double t, up, across, denominator, dum;
   int col;

   if (n==0) {  *fzero = f; tableau[0] = f; return 0; }
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
  
  double* pars=(double*)params;
  int order=(int)pars[0],i;
  double y1[order],y05[order],y15[order],y2[order],y25[order],yaux[order];
  double h=(t-t0)/(double)number_of_steps;
  double h2=h+h;

  copyVec(yaux,y0,order);
  (*f)(t0,yaux,y05,params);
  sumVec(y1,1,yaux,h,y05,order);

  while(--number_of_steps) {
    t0+=h;
    (*f)(t0,y1,y15,params);
    sumVec(y2,1,yaux,h2,y15,order);
    copyVec(yaux,y1,order);
    copyVec(y1,y2,order);
  } 

  (*f)(t,y1,y25,params);

  //yres=0.5*(yaux+y1+h*y25);
  sumVec(yres,0.5,yaux,0.5,y1,order);
  sumVec(yres,1,yres,0.5*h,y25,order);
  return 0;
}

int Gragg_Bulirsch_Stoer(int (*f)(double,double*,double*,void*), 
			 double y0[], double y1[],
			 double t, double h, double *h_new, 
			 double epsilon, double yscale, 
			 int rational_extrapolate,
			 void *params)
{
  double* pars=(double*)params;
  int order=(int)pars[0];
  double step_size2[ATTEMPTS];
  double tableau[order][ATTEMPTS+1];
  double dum;
  double est[order],dest[order],destmax;
  double old_est[order];
  
  int (*Extrapolate)(double*,double*,double*,double,int);
  int i,j;
  int err;

  if(yscale==0.0) return -3;
  if(rational_extrapolate) Extrapolate=Rational_Extrapolation_to_Zero;
  else Extrapolate=Polynomial_Extrapolation_to_Zero;
 
  Graggs_Method(f,y0,t,t+h,number_of_steps[0],params,est);
  step_size2[0]=(dum=h/(double)number_of_steps[0],dum*dum);
  
  copyVec(y1,est,order);
  
  for(i=order;i-->0;){
    err=Extrapolate(&y1[i],tableau[i],step_size2,est[i],0);
    if(err<0) return err-1;
  }

  for(i = 1; i < ATTEMPTS; i++) {
    copyVec(old_est,y1,order);
    Graggs_Method(f,y0,t,t+h,number_of_steps[i],params,est);
    step_size2[i]=(dum=h/(double)number_of_steps[i],dum*dum);

    for(j=order;j-->0;){
      err=Extrapolate(&y1[j],tableau[j],step_size2,est[j],i);
      if(err<0) return err-1;
    }
    
    sumVec(dest,1.0/yscale,y1,-1.0/yscale,old_est,1);
    destmax=maxAbsVec(dest,order);

    if(destmax<epsilon){
      if(i>1) *h_new=8.0*h/(double)number_of_steps[i-1];
      else *h_new=h;
      return 0;
    }
  }
  return -1;
}

