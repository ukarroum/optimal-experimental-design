function [Iabs]=couplageOLT(p_E,x,y,p_thetae,p_freq,p_h,p_d,p_L,p_Z0,p_ZL,p_alpha)
%% x==theta
%% y==phi
%% Exemple a titre indicatif d'un cas 'classique'
E=1;
theta=pi/4;
thetae=0;
freq=50e6;
phi=pi/3;       
d=1e-3;
h=20e-3;
Zc=60*acosh(2*h./d);
Z0=50;
ZL=1000;
alpha=0.001;

L = 1;

alp      = 0.1;
thetamax     = (1+alp)*theta;
thetamin     = (1-alp)*theta;
phimax = (1+alp)*phi;
phimin = (1-alp)*phi;

Emax = (1 + alp)*E;
Emin = (1 - alp)*E;
thetaemax = (1 + alp)*thetae;
thetaemin = (1 - alp)*thetae;
freqmax = (1 + alp)*freq;
freqmin = (1 - alp)*freq;
dmax = (1 + alp)*d;
dmin = (1 - alp)*d;
hmax = (1 + alp)*h;
hmin = (1 - alp)*h;
Z0max = (1 + alp)*Z0;
Z0min = (1 - alp)*Z0;
ZLmax = (1 + alp)*ZL;
ZLmin = (1 - alp)*ZL;
alphamax = (1 + alp)*alpha;
alphamin = (1 - alp)*alpha;
Lmax = (1 + alp)*L;
Lmin = (1 - alp)*L;

% 
moyx   = (thetamax+thetamin)/2;
stdx   = sqrt((thetamax-thetamin).^2./12);
moyy   = (phimax+phimin)/2;
stdy   = sqrt((phimax-phimin).^2./12);

moyE = (Emax + Emin) / 2;
stdE = sqrt((Emax - Emin).^2./12);
moythetae = (thetaemax + thetaemin) / 2;
stdthetae = sqrt((thetaemax - thetaemin).^2./12);
moyfreq = (freqmax + freqmin) / 2;
stdfreq = sqrt((freqmax - freqmin).^2./12);
moyd = (dmax + dmin) / 2;
stdd = sqrt((dmax - dmin).^2./12);
moyh = (hmax + hmin) / 2;
stdh = sqrt((hmax - hmin).^2./12);
moyZ0 = (Z0max + Z0min) / 2;
stdZ0 = sqrt((Z0max - Z0min).^2./12);
moyZL = (ZLmax + ZLmin) / 2;
stdZL = sqrt((ZLmax - ZLmin).^2./12);
moyalpha = (alphamax + alphamin) / 2;
stdalpha = sqrt((alphamax - alphamin).^2./12);
moyL = (Lmax + Lmin) / 2;
stdL = sqrt((Lmax - Lmin).^2./12);



% Changement de variable
theta     = x*stdx+moyx;
phi       = y*stdy+moyy;

E = p_E*stdE+moyE;
thetae = p_thetae*stdthetae+moythetae;
freq = p_freq*stdfreq+moyfreq;
d = p_d*stdd+moyd;
h = p_h*stdh+moyh;
Z0 = p_Z0*stdZ0+moyZ0;
ZL = p_ZL*stdZL+moyZL;
alpha = p_alpha*stdalpha+moyalpha;
L = p_L*stdL+moyL;

% variable intermediaire sur la base des variables initiales
beta=2*pi*freq/3e8;
gamma=alpha+1i*beta;  % attention 1i est le complexe imag. pur

% Calcul
I=2.*h.*E./(cosh(gamma.*L).*(Z0.*Zc+ZL.*Zc)+sinh(gamma.*L).*(Zc.*Zc+Z0.*ZL)).*sin(beta.*h.*cos(theta))./(beta.*h.*cos(theta))...
    .*( j.*beta.*cos(theta).*( -sin(thetae).*cos(theta).*sin(phi)+cos(thetae).*cos(phi))...
    .*(0.5.*(Zc+Z0).*(exp( (gamma+j.*beta.*sin(theta).*sin(phi)).*L)-1)./(gamma+j.*beta.*sin(theta).*sin(phi))...
    -0.5*(Zc-Z0).*(exp( -(gamma-j.*beta.*sin(theta).*sin(phi)).*L)-1)./(gamma-j*beta.*sin(theta).*sin(phi)))...
    +sin(thetae).*sin(theta).*(Zc-(Zc.*cosh(gamma.*L)+Z0.*sinh(gamma.*L)).*exp(j*beta.*L.*sin(theta).*sin(phi))));

Iabs=abs(I); % amplitude du courant complexe I

end % Fin de la fonction
