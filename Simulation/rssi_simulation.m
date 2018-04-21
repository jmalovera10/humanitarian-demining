%Anchor 1 coordinates 
anchor1 = [0,2];
%Anchor 2 coordinates 
anchor2 = [4,0];
%Anchor 3 coordinates 
anchor3 = [8,0];
%Anchor 4 coordinates 
anchor4 = [12,2];

%Mobile coordinate
mobile1 = [6,6];

anchors = [anchor1;anchor2;anchor3;anchor4];
nodes = [anchors;mobile1];
clf('reset')
plot(nodes(:,1),nodes(:,2),'*')
xlabel('m')
ylabel('m')
xlim([-1 13])
ylim([-1 13])
dog = strcat('  Dog: ','[',num2str(mobile1(1)),',',num2str(mobile1(2)),']');
text(mobile1(1),mobile1(2),dog)
grid on
hold on
rssi = [];

for i = 1:4
    radius = norm(anchors(i,:)-mobile1);
    [xval, yval] = radiation(radius);
    xval = xval+anchors(i,1);
    yval = yval+anchors(i,2);
    plot(xval,yval,'--')
    txt = strcat('  Anchor',num2str(i),': [',num2str(anchors(i,1)),',',num2str(anchors(i,2)),']');
    text(anchors(i,1),anchors(i,2),txt)
    rssi(i) = rssi_value(radius);
end

distances = distance(rssi)';
est = NLS(anchors, distances);
plot(est(1),est(2),'r*');
txt = strcat('  Estimation: [',num2str(est(1)),',',num2str(est(2)),']  ');
text(est(1),est(2),txt,'HorizontalAlignment','right');
txt = texlabel(strcat('Error: ',num2str(norm(est-mobile1)*100),'%'));
text(4.5,12.5,txt)