function dy = logs_hopf(~,y)
%UNTITLED3 �˴���ʾ�йش˺�����ժҪ
%   �˴���ʾ��ϸ˵��
beta = 0.6;
alpha = 0.5;
gamma = 0.3;
dy = [y(1)*(1-beta*y(1))-y(1)*y(2)/(gamma+y(1));y(2)*y(1)/(gamma+1)-alpha*y(2)];
end
