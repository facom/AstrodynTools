/*
  Version 2: Vectorial arbitrary dimension
 */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int Gragg_Bulirsch_Stoer(int (*f)(double,double*,double*,void*), 
			 double y0[], double y1[],
			 double t, double h, double *h_new, 
			 double epsilon, double yscale, 
			 int rational_extrapolate,void *params);

int f(double t,double y[],double f[],void *params) 
{ 
  f[0]=t*y[0];
  return 0;
}
double If(double t){
  return exp(0.5*t*t); 
}


int main(int argc,char *argv[])
{
  double exact,error;
  double h_next,h_used;
  double t,t_start,t_stop;
  double y1[1];
  int i,err;

  double tolerance = 1.e-10;          
  int number_of_steps = 10;     // solve for x = x0 to x0 + h * number_of_steps.
  double t0 = 0.0;              
  double y0[] = {1.0};
  double h = 0.1;               // step size
  double params[10];
  int met=atoi(argv[1]);
  printf("Method: %d\n",met);

  t_start = t0;
  t = t_start;

  //NUMBER OF VARIABLES
  params[0]=1;
  int status;
  FILE *f=fopen("solution.dat","w");
  for (i = 0; i < number_of_steps; i++) {
    h_used = h;
    t_stop = t_start + h;
    do {
      while(1){
	status=Gragg_Bulirsch_Stoer(f,y0,y1,t,h_used,&h_next,1.0,tolerance,met,params);
	if(status) h_used/=4.0;
	else break;
      }
      t+=h_used;
      y0[0]=y1[0];
      if(t+h_next>t_stop) h_used=t+h_next-t_stop;
      else h_used=h_next;
      printf("t = %e\n",t);
    }while(t<t_stop-1.e-10);

    exact = If(t);
    error = exact - y1[0];
    printf("%3d  %8.2le %20.15le", i+1, t, y1[0]);
    printf("   %20.15le  %+9.4le\n", exact,error);
    t_start = t;
    //printf("Number of steps: %d\n",number_of_steps);
    //getc(stdin);
  }
  fclose(fl);
  return 0;
}
