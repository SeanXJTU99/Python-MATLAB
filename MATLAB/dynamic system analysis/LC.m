function dy = LC(~,y)
%UNTITLED3 此处显示有关此函数的摘要
%   此处显示详细说明
% dy = [y(1)*(2-y(1)-y(2));y(1)-y(2)];
dy = [2*y(2);4*y(1)*y(1)*y(1)-4*y(1)];
end

