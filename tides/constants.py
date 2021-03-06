"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%";
"PHYSICAL CONSTANTS";
"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%";
Gconst=6.67E-11;"m^3/(kg s^2)";

Day=86400.0;"s";

Month=27.3;"Days";

"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%";
"ASTRONOMICAL CONSTANTS";
"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%";
Mearth=5.98E24;"kg";

Mmoon=Mearth/81;

Rearth=6.371E6;"m";

Reqearth = 6.378137E6;"m";
fearth = 1/298.257223563;

Rmoon=1.73710E6;"m";

rmoon=3.844E8;"m";

Msun=1.98E30;"kg";

Rsun=6.96E8;"m";

rsun=1.496E11;"m";

rhoearth=5.5E3;"kg/m^3";

"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%";
"DEFORMING COEFFICIENTS";
"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%";
#Rmean(km), rho(g/cc), J2 x10^-6, 0 J4 x10^-6
JMercury=[2440,5.427,60,0,0]
JVenus=[6052,5.204,4,0,2]
JEarth=[6378,5.515,1083,0,-2]
JMars=[3394,3.933,1960,0,-19]
JJupiter=[71398,1.326,14736,0,-587]
JSaturn=[60330,0.6873,16298,0,-915]
JUranus=[26200,1.318,3343,0,-29]
JNeptune=[25225,1.638,3411,0,-35]
