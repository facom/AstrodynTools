////////////////////////////////////////////////////////////////////////////////
// File: testbulirsch.c                                                       //
// Purpose:                                                                   //
//    Test the Gragg_Bulirsch_Stoer method for solving a differential         //
//    equation in the file bulirsch_stoer.c                                   //
//                                                                            //
// Solve the initial value problem, y' = xy, y(0) = 1.0.                      //
// From x = 0.0 to 1.0, epsilon = 1.0e-10.                                    //
////////////////////////////////////////////////////////////////////////////////
#include <stdio.h>
#include <math.h>

int Gragg_Bulirsch_Stoer( double (*f)(double, double), double y0, double *y1,
double x, double h, double *h_new, double epsilon, double yscale, 
int rational_extrapolate  );

double f(double x, double y) { return x*y; }
double If(double x) { return exp(0.5*x*x); }


int main(int argc,char* argv[]){

  double tolerance = 1.e-10;          
  double a = 1.0;               // y(x0).
  double x0 = 0.0;              // x0 the initial condition.
  double h = 0.1;               // step size
  int number_of_steps = 10;     // and number of steps, i.e. 

  double exact;
  double error;
  double h_next;
  double h_used;
  double x;
  double x_start;
  double x_stop;
  double y0 = a;
  double y1;
  int i;
  int err;
  int met=atoi(argv[1]);
  printf("Method: %d\n",met);
 
  x_start = x0;
  x = x_start;

  int status;
  for (i = 0; i < number_of_steps; i++) {

    h_used = h;
    x_stop = x_start + h;

    do {
      while(1){
	status=Gragg_Bulirsch_Stoer(f,y0,&y1,x,h_used,&h_next,1.0,tolerance,met);
	if(status) h_used/=4.0;
	else break;
      }
      x += h_used;
      y0 = y1;
      if ( x + h_next > x_stop ) h_used = x + h_next - x_stop;
      else h_used = h_next;
      printf("x = %e\n",x);
    } while ( x < x_stop - 1.e-10 );
                  
    exact = If(x);
    error = exact - y1;
    printf("%3d   %8.2le  %20.15le", i+1, x, y1);
    printf("   %20.15le  %+9.4le\n", exact,error);
    x_start = x;
    //printf("Number of steps: %d\n",number_of_steps);
    //getc(stdin);
  }
  return 0;
}
