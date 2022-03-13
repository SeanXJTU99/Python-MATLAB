function dydt = lorenz(t,y);
sigma = 10.;
r = 30.;
b = 8./3.;
dydt = [sigma*(y(2)-y(1)); r*y(1) - y(2) - y(1)*y(3); y(1)*y(2) - b*y(3)];
