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
extracted_expression_file = "HT29_expression_matrix.tsv"
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
    samp = c("GSM1019741","GSM1019735","GSM1019738","GSM1019739","GSM1019742","GSM1019740","GSM1019736","GSM1019737","GSM1019743","GSM2042937","GSM1398738","GSM2042930","GSM1398732","GSM2042934","GSM2042941","GSM2042946","GSM1398741","GSM1398736","GSM1398737","GSM1398734","GSM1890692","GSM2042916","GSM1700896","GSM2042920","GSM1398733","GSM1700902","GSM1398740","GSM1700900","GSM2042919","GSM1398739","GSM2042921",
"GSM2042926","GSM1890691","GSM1398742","GSM2042922","GSM1700897","GSM1890707","GSM1890687","GSM1890711","GSM2042932","GSM1398731","GSM2042917","GSM2042947","GSM1890709","GSM1890706","GSM2042948","GSM1890686","GSM2042933","GSM2042943","GSM1700903","GSM1700898","GSM1700899","GSM2042931","GSM2042936","GSM2042924","GSM1890685","GSM1890690","GSM1890693","GSM2042923","GSM2042945","GSM2042927",
"GSM1890708","GSM2042942","GSM1890688","GSM2042918","GSM2042944","GSM2042935","GSM1890710","GSM2042939","GSM2042938","GSM2042940","GSM2042929","GSM1890689","GSM1700901","GSM1528204","GSM1528201","GSM1528203","GSM1432898","GSM1528198","GSM1432895","GSM1528212","GSM1432897","GSM1528213","GSM1528200","GSM1528206","GSM1528209","GSM1528205","GSM1528207","GSM1528210","GSM1528202","GSM1432896",
"GSM1528208","GSM1528211","GSM1528199","GSM1398735","GSM1700895","GSM2042928","GSM2072613","GSM2072614","GSM2071575","GSM2071574","GSM2152360","GSM2152357","GSM2152359","GSM2152358","GSM2517978","GSM2517977","")

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
