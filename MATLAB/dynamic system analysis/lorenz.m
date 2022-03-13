function dydt = lorenz(~,y)
sigma = 10.0;
r = 20;
b = 8.0/5.0;
dydt = [sigma*(y(2)-y(1)); r*y(1) - y(2) - y(1)*y(3); y(1)*y(2) - b*y(3)];
