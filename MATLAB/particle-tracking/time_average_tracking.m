clear;
load ENE512_prob2.mat;
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
vmean=vmean+2*(rand(size(vmean))*0.02-0.01);

dx=5:5:30;
times=10;
Diff2=zeros(length(dx));
Diff1=zeros(length(dx));
Diff3=zeros(length(dx));
for j=1:length(dx)
     for cycle=1:times
        %S=(dx(j)/180)*pi;
        S=(25/180)*pi;
star=sqrt(10*0.5*S);
Dx=4.5*(umean).^2/star;
%Dx=dx(j)*(umean).^2/star;
Dy=0.6*50*(vmean).*abs(vmean)*star+eps;
%Dy=0.6*dx(j)*(vmean).*abs(vmean)*star+eps;
sqDy=sqrt(abs(Dy));
Dyt=Dy./sqDy;
%mesh(Dyt);
particle=timeave(umean,vmean,Dx,Dyt,x,y,time,depth);
[muprime,sigmaprime,xbin]=stat(particle,x,time);
musig1=muprime+sigmaprime;
musig2=muprime-sigmaprime;
diff1=sum((musig1-(mu+sigma)).^2);
diff2=sum((musig2-(mu-sigma)).^2);
diff3=sum((muprime-mu).^2);
Diff3(j)=Diff3(j)+diff3;
Diff1(j)=Diff1(j)+diff1;
Diff2(j)=Diff2(j)+diff2;
    end
    Diff1(j)=Diff1(j)/times;
    Diff2(j)=Diff2(j)/times;
    Diff3(j)=Diff3(j)/times;
end
figure(8)
plot(dx,Diff1,'r',dx,Diff2,'b',dx,Diff3,'k')