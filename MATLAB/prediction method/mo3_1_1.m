%运行前打开P,S矩阵,及拟合函数
Q=[P,S];
i=1;
while i<length(Q)
   if Q(i,1)==0||Q(i,2)==0
       Q(i,:)=[];
   end
   i=i+1;
end     %去零
P0=Q(:,1);S0=Q(:,2);
%P1=max(P0);
%P2=min(P0);
%P01=(P0-P2)./(P1-P2);
%S1=max(S0);
%S2=min(S0);
%S01=(S0-S2)./(S1-S2);
%[fm got]=fit(S,P,'1-exp(-(x/a).^b)','start',[3,2]);
x=0:0.1:26;
h1=figure;
hold on;
plot(S0,P0,'k.');
plot(x,fittedmodel_F1(x),'b-','linewidth',2);
h2=figure;
hold on;
plot(S0,P0,'k.');
plot(x,fittedmodel_F2(x),'b-','linewidth',2);
h3=figure;
hold on;
plot(S0,P0,'k.');
plot(x,fittedmodel_F3(x),'b-','linewidth',2);
h4=figure;
hold on;
plot(S0,P0,'k.');
plot(x,fittedmodel_P3(x),'b-','linewidth',2);
h5=figure;
hold on;
plot(S0,P0,'k.');
plot(x,fittedmodel_P4(x),'b-','linewidth',2);
h6=figure;
hold on;
plot(S0,P0,'k.');
plot(x,fittedmodel_P5(x),'b-','linewidth',2);
h7=figure;
hold on;
plot(S0,P0,'k.');
plot(x,fittedmodel_P6(x),'b-','linewidth',2);