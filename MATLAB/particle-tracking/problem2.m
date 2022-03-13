load ENE512_prob2.mat
load particle_stats_full.mat

% ------------------1) time-averaged velocity component--------------------

% calculate dt
t=[time;0];
t=t(2:length(t));
dt=t-time;
dt(end)=dt(1);

% calculate time-average by integral (in fact sum)
umean=zeros(size(depth));
vmean=zeros(size(depth));
% integral
for i=1:length(dt)
    umean=umean+u(:,:,i)*dt(i);
    vmean=vmean+v(:,:,i)*dt(i);
end
% integral over T
umean=umean/time(end);
vmean=vmean/time(end);
% mesh
figure(1);
xlabel('x/m');
ylabel('y/m');
zlabel('v/(m/s)');
mesh(x,y,umean);
title('time-averaged u')
figure(2);
xlabel('x/m');
ylabel('y/m');
zlabel('v/(m/s)');
mesh(x,y,vmean);
title('time-average v')


% ---------------------2) time-averaged turbulence-------------------------

% calculate fluctuation along with time
uBAR=zeros(size(u));
vBAR=zeros(size(v));
for i=1:length(time)
    uBAR(:,:,i)=umean;
    vBAR(:,:,i)=vmean;
end
uprimet=(u-uBAR).^2;
vprimet=(v-vBAR).^2;

% time average fluctuation
uPrime=zeros(size(depth));
vPrime=zeros(size(depth));
for i=1:length(dt)
    uPrime=uPrime+uprimet(:,:,i)*dt(i);
    vPrime=vPrime+vprimet(:,:,i)*dt(i);
end
uPrime=uPrime/time(end);
vPrime=vPrime/time(end);

% calculate turbulence
turbulence=sqrt(uPrime+vPrime);
figure(3);
xlabel('x/m');
ylabel('y/m');
zlabel('v/(m/s)');
mesh(x,y,turbulence);
title('time-averaged turbulence')


% ---------3) time and cross-channel averaged velocity components----------

% calculate dy
Y=[y(2:end);0];
dy=Y-y;
dy(end)=dy(1);
dy=dy';

% channel average of time-averaged velocity
ubar=(dy*umean)/y(end);
vbar=(dy*vmean)/y(end);

% plot
figure(4)
hold on
title('time&cross-channel averaged velocity');
xlabel('x/m');
ylabel('v/(m/s)')
plot(x,ubar,'r','linewidth',1);
plot(x,vbar,'b','linewidth',1);
legend('u','v')


% -----------4) rms cross-channel velocity fluctuations--------------------

% fluctuation
uflct=umean-ubar;
vflct=vmean-vbar;
us=uflct.^2;
vs=vflct.^2;
um=zeros(size(x));
vm=zeros(size(x));
for i=1:length(x)
    um(i)=sum(us(:,i))/length(y);
    vm(i)=sum(vs(:,i))/length(y);
end
urms=um.^0.5;
vrms=vm.^0.5;
figure(5)
hold on
title('rms of cross-channel fluctuation');
xlabel('x/m');
ylabel('v/(m/s)');
plot(x,urms,'r','linewidth',1);
plot(x,vrms,'b','linewidth',1);
legend('u','v');



% -----------------------------5) dispersion ------------------------------

% ------------------time-averaged dispersion model---------------
% calculate Dx and Dy
vmean=vmean+2*(rand(size(vmean))*0.02-0.01);
S=(3/180)*pi;
star=sqrt(10*0.5*S);
Dx=4.5*(umean).^2/star;
Dyt=125*(vmean).*abs(vmean)*star;
sqDy=sqrt(abs(Dyt));
Dy=Dyt./sqDy;

% tracking dispersion
particle=timeave(umean,vmean,Dx,Dy,x,y,time);

% plot
figure(6);
contour(x,y,depth,'k');
hold on
title('time-averaged')
nt=length(time);
    for p=1:nt
        xc=particle(p,nt,1);
        yc=particle(p,nt,2);
        plot(xc,yc,'bo');
    end

% statistical calculation
[muprime,sigmaprime,xbin]=stat(particle,x,time);
figure(7);
plot(xbin,muprime+sigmaprime,'r--',xbin,mu+sigma,'b-*',xbin,muprime-sigmaprime,'r--',xbin,mu-sigma,'b-*')
hold on
plot(xbin,mu,xbin,muprime)
contour(x,y,depth,'k')
title('time-averaged dispersion')
legend('Plume Width of time-averaged velocity','Plume Width of full velocity field')
axis([x(1) x(end) y(1) y(end)])

% -----------------time&channel-averaged dispersion model-----------

% calculate Dx and Dy
S=(2/180)*pi;
star=sqrt(10*0.5*S);
Dx=1.5*(ubar).^2/star;
Dy=0.09*star;

% tracking channel-averaged
nt=length(time);
particle=tcave(ubar,vbar,Dx,Dy,x,y,time);
figure(8)
contour(x,y,depth,'k');
hold on
title('channel-averaged')
for n=nt
    for p=1:n
        xc=particle(p,n,1);
        yc=particle(p,n,2);
        plot(xc,yc,'bo');
    end
end

% statistical calculation
[muprime,sigmaprime,xbin]=stat(particle,x,time);
figure(9)
title('channel-averaged dispersion')
hold on
plot(xbin,muprime,'r--',xbin,mu,'b--')
contour(x,y,depth,'k')
axis([x(1) x(end) y(1) y(end)])
legend('Mean Position of full-velocity field','Mean Position of channel averaged velocity')