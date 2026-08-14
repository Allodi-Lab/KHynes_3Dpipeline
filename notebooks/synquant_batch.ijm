input = "D:\\Conn_3dpipeline\\raw_converted_C00_cropped\\";
output = "D:\\Conn_3dpipeline\\results\\C00_synquant\\";

list = getFileList(input);
print("Found " + list.length + " files");

for (i = 0; i < list.length; i++) {
    print("Processing " + (i+1) + "/" + list.length + ": " + list[i]);
    open(input + list[i]);
    run("Enhance Contrast", "saturated=0.35");
    run("SynQuantVid ", "z-score=10 min=10 max=200 min_0=0.50 max_0=4 post-synapse=Null pre-synapse=" + list[i] + " way=Null dendrite=Null extended=0 z=1 zscore=10");
    saveAs("Results", output + list[i] + "_results.csv");
    close("Overlay Elements of Synapse detection results");
    close("Synapse detection results");
    close(list[i]);
}
print("Done");