/*
  Version 4: Two-body problem 2D
 */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

char* strVec(double a[],int n);
int copyVec(double tgt[],double src[],int n);
int sumVec(double c[],double ca,double a[],double cb,double b[],int n);

int Gragg_Bulirsch_Stoer(int (*f)(double,double*,double*,void*), 
			 double y0[], double y1[],
			 double t, double h, double *h_new, 
			 double epsilon, double yscale, 
			 int rational_extrapolate,void *params);

//KEPLER PROBLEM
int eom(double t,double y[],double dydt[],void *params) 
{ 
  double r=sqrt(y[0]*y[0]+y[1]*y[1]);
  dydt[0]=y[2];
  dydt[1]=y[3];
  dydt[2]=-y[0]/(r*r*r);
  dydt[3]=-y[1]/(r*r*r);
  return 0;
}

int solution(double t,double y[],void *params)
{
  double* pars=(double*)params;
  
  y[0]=0.0;
  y[1]=0.0;
  y[2]=0.0;
  y[3]=0.0;
  return 0;
}

int main(int argc,char *argv[])
{
  double h_next,h_used;
  double t,t_start,t_stop;
  int order=4;
  double y1[order];
  int i,err;

  double tolerance = 1.e-10;          

  double t0 = 0.0;              
  int number_of_steps = 10000;
  double y0[] = {1.0,0.0,0.0,1.3};

  double h = 0.05;
  double params[10];
  int met=atoi(argv[1]);
  printf("Method: %d\n",met);

  t_start = t0;
  t = t_start;

  //NUMBER OF VARIABLES
  params[0]=order;

  int status;
  double ysol[order],error[order];
  FILE *f=fopen("solution.dat","w");
  double r,E0,E;

  r=sqrt(y0[0]*y0[0]+y0[1]*y0[1]);
  E0=0.5*(y0[2]*y0[2]+y0[3]*y0[3])-1/r;
  for (i = 0; i < number_of_steps; i++) {
    h_used = h;
    t_stop = t_start + h;
    do {
      while(1){
	status=Gragg_Bulirsch_Stoer(eom,y0,y1,t,h_used,&h_next,1.0,tolerance,met,params);
	if(status) h_used/=4.0;
	else break;
      }
      t+=h_used;
      copyVec(y0,y1,order);
      if(t+h_next>t_stop) h_used=t+h_next-t_stop;
      else h_used=h_next;
      printf("t = %e\n",t);
    }while(t<t_stop-1.e-10);

    solution(t,ysol,params);
    sumVec(error,1.0,ysol,-1.0,y1,order);

    r=sqrt(y1[0]*y1[0]+y1[1]*y1[1]);
    E=0.5*(y1[2]*y1[2]+y1[3]*y1[3])-1/r;
    printf("%3d %8.2le %s %s %s\n",i+1,t,
	   strVec(y1,order),
	   strVec(ysol,order),
	   strVec(error,order)
	   );
    fprintf(f,"%3d %8.2le %s %s %s %.17e\n",i+1,t,
	    strVec(y1,order),
	    strVec(ysol,order),
	    strVec(error,order),
	    fabs(E-E0)/fabs(E0)
	    );
    t_start = t;
  }
  fclose(f);
  return 0;
}
