load ENE512_prob2.mat
load particle_stats_full.mat

t=[time;0];
t=t(2:length(t));
dt=t-time;
dt(end)=dt(1);
nt=length(time);
umean=zeros(size(depth));
vmean=zeros(size(depth));
for i=1:length(dt)
    umean=umean+u(:,:,i)*dt(i);
    vmean=vmean+v(:,:,i)*dt(i);
end
umean=umean/time(end);
vmean=vmean/time(end);
Y=[y(2:end);0];
dy=Y-y;
dy(end)=dy(1);
dy=dy';
ubar=(dy*umean)/y(end);
vbar=(dy*vmean)/y(end);


% 
% S=(1/180)*pi;
% star=sqrt(10*0.5*S);
% Dx=0.01*(umean*15).^2/0.5/star;
% Dy=0.6*0.05*star;
% 
% particle=timeave(umean,vmean,Dx,Dy,x,y,time);


% calculate Dx and Dy
dx=1.5:0.1:2.5;
times=10;
Diff2=zeros(length(dx));
Diff1=zeros(length(dx));
for j=1:length(dx)
    for cycle=1:times
        S=(dx(j)/180)*pi;
star=sqrt(10*0.5*S);
Dx=1.5*(ubar).^2/star;
Dy=0.6*0.15*star;
particle=tcave(ubar,vbar,Dx,Dy,x,y,time,depth);
[muprime,sigmaprime,xbin]=stat(particle,x,time);
% 
% figure(7)
% for n=nt
%     contour(x,y,depth,'k');
%     hold on
%     for p=1:n
%         xc=particle(p,n,1);
%         yc=particle(p,n,2);
%         plot(xc,yc,'bo');
%     end
% end
musig1=muprime+sigmaprime;
musig2=muprime-sigmaprime;
diff1=sum((musig1-(mu+sigma)).^2);
diff2=sum((musig2-(mu-sigma)).^2);
Diff1(j)=Diff1(j)+diff1;
Diff2(j)=Diff2(j)+diff2;
% diff3=sum((muprime-mu).^2);
% figure(8);
% contour(x,y,depth,'k')
% title('time-averaged dispersion')
% hold on
% plot(xbin,muprime,xbin,musig1,'r--',xbin,musig2,'r--')
% plot(xbin,mu,xbin,mu+sigma,'b-*',xbin,mu-sigma,'b-*')
% axis([x(1) x(end) y(1) y(end)])
%legend('Mean Position of Plume','Standard Dev of Plume Width')
    end
    Diff1(j)=Diff1(j)/times;
    Diff2(j)=Diff2(j)/times;
end
figure(8)
plot(dx,Diff1,'r',dx,Diff2,'b')