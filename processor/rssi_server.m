client = tcpclient('localhost', 9100);
rssi_values = [-1,-1,-1];
info = 0;
while true
    data = read(client);
    if data
        isRSSI = true;
        mult = 1;
        id = 0;
        rssi = 0;
        for i= length(data):-1:1
            if data(i)==59
                isRSSI = false;
                mult = 1;
                continue;
            end
            if isRSSI
                rssi = rssi+(data(i)-48)*mult;
                mult = mult*10;
            else
                id = id +(data(i)-48)*mult;
                mult = mult*10;
            end
        end
        rssi_values(id) = rssi;
        info = info+1;
        if info==3
            info = 0;
            rssi_values = [-1,-1,-1];
        end
    end
end
