function [ J ] = Jacobian( x, y, anchors)
%JACOBIAN Summary of this function goes here
%   Detailed explanation goes here
dfbx1 = 0.5*((2*x-2*anchors(1,1))/(sqrt((x-anchors(1,1)).^2+(y-anchors(1,2)).^2)));
dfbx2 = 0.5*((2*x-2*anchors(2,1))/(sqrt((x-anchors(2,1)).^2+(y-anchors(2,2)).^2)));
dfbx3 = 0.5*((2*x-2*anchors(3,1))/(sqrt((x-anchors(3,1)).^2+(y-anchors(3,2)).^2)));
dfbx4 = 0.5*((2*x-2*anchors(4,1))/(sqrt((x-anchors(4,1)).^2+(y-anchors(4,2)).^2)));

dfby1 = 0.5*((2*y-2*anchors(1,2))/(sqrt((x-anchors(1,1)).^2+(y-anchors(1,2)).^2)));
dfby2 = 0.5*((2*y-2*anchors(2,2))/(sqrt((x-anchors(2,1)).^2+(y-anchors(2,2)).^2)));
dfby3 = 0.5*((2*y-2*anchors(3,2))/(sqrt((x-anchors(3,1)).^2+(y-anchors(3,2)).^2)));
dfby4 = 0.5*((2*y-2*anchors(4,2))/(sqrt((x-anchors(4,1)).^2+(y-anchors(4,2)).^2)));

J=[dfbx1 dfby1;dfbx2 dfby2;dfbx3 dfby3;dfbx4 dfby4];

end

