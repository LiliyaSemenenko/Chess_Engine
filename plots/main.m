clear all

t0 = 0;
x0 = 0;
y0 = 20; 
u0 = 0.97; 
v0 = 0.24; 
u1 = 1;
u2 = -1;
dt = 1/15; 
alpha = 0.732;
beta = 1.6;
gamma = 1.5;
sigma_x = 0.2;
sigma_y = 0.2;
kappa = 1.1; 
theta1 = 0.3;
theta2 = 1.2;
offset = 0.2;

[n] = multiPeds(t0,x0,y0,u0,v0,u1,u2,dt,alpha,beta,gamma,sigma_x,sigma_y,kappa,theta1,theta2,offset);