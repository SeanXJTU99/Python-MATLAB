function dy = logs(~,y)
%UNTITLED3 �˴���ʾ�йش˺�����ժҪ
%   �˴���ʾ��ϸ˵��
a = 0.1;
dy = [y(1)*(--y(1)*y(1)+y(1)-y(2));y(2)*(y(1)-a)];
end
