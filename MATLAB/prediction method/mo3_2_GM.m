%运行前打开QD矩阵
PD=QD(:,1);
n=length(PD);
e1=exp(-2/(n+1));
e2=exp(2/(n+2));
L=PD(1:n-1,1)./PD(2:n,1);