%d=481;    %天数
%for i=1:d
%   ADT(i,:)=sum(A((96*i-95):96*i,:))/96;
%   BDT(i,:)=sum(B((96*i-95):96*i,:))/96;
%   CDT(i,:)=sum(C((96*i-95):96*i,:))/96;
%end       %日均值
%DT=[ADT BDT CDT];
%while i<length(DT)
%    if DT(i,1)==0
%        DT(i,:)=[];
%    end
%    i=i+1;
%end


%运行前打开DT,QD矩阵

DT1=DT(1:400,:);
DT2=DT(401:452,:);
DTPA=DT2(:,1:5)';
DTPB=DT2(:,6:10)';
DTPC=DT2(:,11:15)';
DTA=DT1(:,1:5)';
DTB=DT1(:,6:10)';
DTC=DT1(:,11:15)';
Y0=QD(1:400,1)';
[Y,outr]=mapminmax(Y0);
[X1,intr]=mapminmax(DTB);
X2=mapminmax('apply',DTPB,intr);
net=newff(X1,Y,[5 12 1],{'purelin','logsig','purelin'},'traingda');
net.trainParam.show=10;
net.trainParam.lr=0.05;
net.trainParam.epochs=50000;
net.trainParam.goal=0.06;
net.divideFcn='';
sam=400;
[BPnet,tr]=train(net,X1,Y);
%y1=sim(BPnet,X1);
%c1=mapminmax('reverse',y1,outr);
y=sim(BPnet,X2);
b=mapminmax('reverse',y,outr);
%rc=sqrt(sum(((c'-QD(401:452,1))/201).^2)/52);
rb=sqrt(sum(((b'-QD(401:452,1))/201).^2)/52);