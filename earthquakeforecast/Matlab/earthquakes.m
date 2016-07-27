%%this is the function that should be called from the command window, with
%%the full path of the csv file in the argument. 

%%

function earthquakes(filename)

[x, y, z]= importfile(filename); %extracts the x,y,z magnetometer readings from the specific csv
freqtest(x,y,z,filename); %produces the frequency domain plots of the data

%next steps: display earthquake information from this day on that same
%graph using  
%data = webread('http://earthquake.usgs.gov/fdsnws/event/1/query?format=csv&starttime=2014-01-01&endtime=2014-01-02&minmagnitude=5')