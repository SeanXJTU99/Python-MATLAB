%d=481;    %天数
%PD=zeros(481,1);
%AD=zeros(481,1);
%BD=zeros(481,1);
%CD=zeros(481,1);
%for i=1:481
%   PD(i)=sum(P((96*i-95):96*i,1))/96;
%   AD(i)=sum(A((96*i-95):96*i,1))/96;
%   BD(i)=sum(B((96*i-95):96*i,1))/96;
%   CD(i)=sum(C((96*i-95):96*i,1))/96;
%end
%i=1;
%while i<length(PD)
%    if PD(i,1)==0
%        PD(i,:)=[];
%        AD(i,:)=[];
%        BD(i,:)=[];
%        CD(i,:)=[];
%    end
%    i=i+1;
%end             %去零
%QD=[PD AD BD CD];
%QD(453,:)=[];

%运行前打开QD矩阵
PD=QD(:,1);
PD10=QD(1:400,1);
PD20=detrend(PD10);
PD30=PD10-PD20;
H0=adftest(PD20);
r=zeros(10,1);
PreR=zeros(52,10);
for k=1:10
    u0=iddata(PD20);
    test0=[];
    for p0=1:5
        for q0=1:5
            m0=armax(u0,[p0,q0]);
            AIC0=aic(m0);
            test0=[test0;p0 q0 AIC0];
        end
    end
    for i=1:size(test0,1)
        if test0(i,3)==min(test0(:,3))
            p00=test0(i,1);
            q00=test0(i,2);
            break
        end
    end             %求最小AIC
    PD00=[PD20;zeros(52,1)];
    u00=iddata(PD00);
    m00=armax(u0,[p00,q00]);
    PRE0=predict(m00,u00,1);
    Fluc0=PRE0.OutputData;%波动量预测值
    Noise0.std=sqrt(m00.NoiseVariance);
    e0=normrnd(0,Noise0.std,1,452);
    Fluc0=Fluc0';
    FlucR0=zeros(452,1);
    for i=401:452
        FlucR0(i,1)=m00.A(2:p00+1)*Fluc0(i-1:-1:i-p00)'+m00.C(1:q00+1)*e0(i:-1:i-q00)';
    end    %波动量预测值
    mmp0=polyfit(1:size(PD30',2),PD30',1);
    xt0=[];
    for j=1:52
        xt0=[xt0,size(PD30',2)+j];
    end
    TrenR0=polyval(mmp0,xt0);
    TrenR0=TrenR0';
    PreR0=abs(TrenR0+FlucR0(401:452,1));
    rsquare=sum(((PreR0-PD(401:452))/201).^2);
    PreR(:,k)=PreR0;
    r(k,1)=sqrt(rsquare/52);
end
for k=1:10
    if r(k,1)==min(r)
        x=1:1:52;
        h0=figure;
        hold on;
        plot(x,PD(401:452),'k-');
        plot(x,PreR(:,k),'r-');
    end
end
ARMA_0=[PD(401:452),PreR];
ARMA_0=[ARMA_0;zeros(1,1),r'];
%以上为检测
%预测：
PD1=QD(:,1);
PD2=detrend(PD1);
PD3=PD1-PD2;
H=adftest(PD2);
    u=iddata(PD2);
    test=[];
    for p=1:10
        for q=1:10
            m=armax(u,[p,q]);
            AIC=aic(m);
            test=[test;p q AIC];
        end
    end
    for i=1:size(test,1)
        if test(i,3)==min(test(:,3))
            p0=test(i,1);
            q0=test(i,2);
            break
        end
    end        %求最小AIC
    PD0=[PD2;zeros(35,1)];
    u0=iddata(PD0);
    m0=armax(u,[p0,q0]);
    PRE=predict(m0,u0,1);
    Fluc=PRE.OutputData;%波动量初始预测值
    Noise.std=sqrt(m0.NoiseVariance);
    e=normrnd(0,Noise.std,1,487);
    Fluc=Fluc';
    FlucR=zeros(487,1);
    for i=453:487
        FlucR(i,1)=m0.A(2:p0+1)*Fluc(i-1:-1:i-p0)'+m0.C(1:q0+1)*e(i:-1:i-q0)';
    end    %波动量预测值
    mmp=polyfit(1:size(PD3',2),PD3',1);
    xt=[];
    for j=1:35
        xt=[xt,size(PD3',2)+j];
    end
    TrenR=polyval(mmp,xt);
    TrenR=TrenR';%趋势量预测值
    PreRE=abs(TrenR+FlucR(453:487,1));%最终预测值
    y=1:1:35;
    h=figure;
    plot(y,PreRE,'b-','linewidth',2);
