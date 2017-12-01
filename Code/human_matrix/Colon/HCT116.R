# R script to download selected samples
# Copy code and run on a local machine to initiate download

# Check for dependencies and install if missing
packages <- c("rhdf5")
if (length(setdiff(packages, rownames(installed.packages()))) > 0) {
    print("Install required packages")
    source("https://bioconductor.org/biocLite.R")
    biocLite("rhdf5")
}
library("rhdf5")
library("tools")

destination_file = "human_matrix_download.h5"
extracted_expression_file = "HCT116_expression_matrix.tsv"
url = "https://s3.amazonaws.com/mssm-seq-matrix/human_matrix.h5"

# Check if gene expression file was already downloaded and check integrity, if not in current directory download file form repository
if(!file.exists(destination_file)){
    print("Downloading compressed gene expression matrix.")
    download.file(url, destination_file, quiet = FALSE)
} else{
    print("Verifying file integrity...")
    checksum = md5sum(destination_file)
    
    if(destination_file == "human_matrix_download.h5"){
        # human checksum (checksum is for latest version of ARCHS4 data)
        correct_checksum = "d8810730ac56271bb2ff563e549c9988"
    } else{
        # mouse checksum (checksum is for latest version of ARCHS4 data)
        correct_checksum = "afbbaaed0a696b967ce8ecb0baa86ea5"
    }
    
    if(checksum != correct_checksum){
        print("Existing file looks corrupted. Downloading compressed gene expression matrix again.")
        download.file(url, destination_file, quiet = FALSE)
    } else{
        print("Latest ARCHS4 file already exists.")
    }
}

checksum = md5sum(destination_file)
if(destination_file == "human_matrix_download.h5"){
    # human checksum (checksum is for latest version of ARCHS4 data)
    correct_checksum = "d8810730ac56271bb2ff563e549c9988"
} else{
    # mouse checksum (checksum is for latest version of ARCHS4 data)
    correct_checksum = "afbbaaed0a696b967ce8ecb0baa86ea5"
}

if(checksum != correct_checksum){
    print("File download ran into problems. Please try to download again. The files are also available for manual download at http://amp.pharm.mssm.edu/archs4/download.html.")
} else{
    # Selected samples to be extracted
    samp = c("GSM1241249","GSM1241140","GSM1241225","GSM1241162","GSM1151059","GSM1241138","GSM1241228","GSM1241166","GSM1241164","GSM1241145","GSM1241167","GSM1241146","GSM1241148","GSM1241193","GSM1241196","GSM1241212","GSM1241242","GSM1241159","GSM1241224","GSM1241218","GSM1241180","GSM1241221","GSM1241204","GSM1241241","GSM1241233","GSM1241198","GSM1241215","GSM1241187","GSM1241236","GSM1241176","GSM1241169",
"GSM1241203","GSM1241229","GSM1241172","GSM1241205","GSM1241209","GSM1241226","GSM1241208","GSM1241248","GSM1241142","GSM1241175","GSM1151055","GSM1241192","GSM1241152","GSM1241207","GSM1241158","GSM1162758","GSM1241137","GSM1241160","GSM1241201","GSM1241246","GSM1241179","GSM1241143","GSM1241161","GSM1241234","GSM1162759","GSM1162757","GSM1241139","GSM1241195","GSM1241178","GSM1241165",
"GSM1241188","GSM1241156","GSM1241220","GSM1241200","GSM1241155","GSM1241186","GSM1241206","GSM1241184","GSM1241194","GSM1241232","GSM1241245","GSM1241151","GSM1241216","GSM1241243","GSM1241154","GSM1151054","GSM1241144","GSM1241227","GSM1241168","GSM1241230","GSM1241157","GSM1241163","GSM1241189","GSM1241182","GSM1241214","GSM1241202","GSM1241190","GSM1241217","GSM1241174","GSM1241237",
"GSM1241210","GSM1241197","GSM1241185","GSM1241199","GSM1241244","GSM1241153","GSM1241141","GSM1241147","GSM1241211","GSM1241183","GSM1241219","GSM1241171","GSM1241240","GSM1241238","GSM1241235","GSM1241247","GSM1241150","GSM1151058","GSM1241213","GSM1241170","GSM1241191","GSM1241181","GSM1241149","GSM1241239","GSM1241231","GSM2157838","GSM1960351","GSM1382045","GSM1400923","GSM1382043",
"GSM1537512","GSM1412747","GSM1890699","GSM1960349","GSM1727128","GSM1400921","GSM1960338","GSM1412748","GSM1382041","GSM1890694","GSM1400918","GSM1890680","GSM1400922","GSM1960342","GSM1960350","GSM1400916","GSM1586020","GSM1382048","GSM1847263","GSM2297324","GSM1960347","GSM2157837","GSM1727129","GSM1890679","GSM1960344","GSM1537515","GSM1382042","GSM1727127","GSM1537513","GSM1890682",
"GSM1382046","GSM2297327","GSM1960352","GSM1400919","GSM1412745","GSM1537514","GSM1960346","GSM1890683","GSM1960343","GSM1960345","GSM2297325","GSM1890696","GSM1847265","GSM1400917","GSM1960348","GSM2297326","GSM1382047","GSM1890676","GSM1586022","GSM1890698","GSM1586024","GSM1960340","GSM1960339","GSM1890678","GSM1890695","GSM1960337","GSM1847266","GSM1960341","GSM1586025","GSM1382044",
"GSM1890697","GSM1847264","GSM1266734","GSM1586023","GSM1890681","GSM1890677","GSM1586021","GSM1412746","GSM1855853","GSM1945886","GSM2042806","GSM1500847","GSM1658689","GSM1658683","GSM2071740","GSM1658684","GSM1855851","GSM1658686","GSM1500852","GSM1658687","GSM1898652","GSM1658682","GSM2071737","GSM2042805","GSM1945883","GSM1658681","GSM1658685","GSM1855852","GSM1500849","GSM1500851",
"GSM1945888","GSM2122815","GSM2071736","GSM2122814","GSM2042807","GSM1658688","GSM1945887","GSM2071738","GSM1855854","GSM2071741","GSM1500850","GSM2071739","GSM1945884","GSM2042804","GSM1500848","GSM1898651","GSM1945885","GSM1266733","GSM1400920","GSM1727126","GSM1836004","GSM1836002","GSM1836000","GSM1836001","GSM1836005","GSM1836003","GSM1890684","GSM1960336","GSM2089690","GSM2089689",
"GSM2089691","GSM2089687","GSM2089692","GSM2089688","GSM2144412","GSM2481443","GSM2481442","GSM2481441","GSM2481446","GSM2481445","GSM2481439","")

    # Retrieve information from compressed data
    samples = h5read(destination_file, "meta/Sample_geo_accession")
    tissue = h5read(destination_file, "meta/Sample_source_name_ch1")
    genes = h5read(destination_file, "meta/genes")

    # Identify columns to be extracted
    sample_locations = which(samples %in% samp)

    # extract gene expression from compressed data
    expression = h5read(destination_file, "data/expression", index=list(1:length(genes), sample_locations))
    H5close()
    rownames(expression) = genes
    colnames(expression) = samples[sample_locations]

    # Print file
    write.table(expression, file=extracted_expression_file, sep="\t", quote=FALSE)
    print(paste0("Expression file was created at ", getwd(), "/", extracted_expression_file))
}
