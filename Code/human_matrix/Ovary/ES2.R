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
extracted_expression_file = "ES2_expression_matrix.tsv"
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
    samp = c("GSM2151895","GSM1571101","GSM1571067","GSM1571110","GSM1571120","GSM1571100","GSM1571121","GSM1571105","GSM1571060","GSM1571065","GSM1571114","GSM1571058","GSM1571084","GSM1571095","GSM1571117","GSM1571106","GSM1571107","GSM1571085","GSM1571056","GSM1571073","GSM1571082","GSM1571089","GSM1571087","GSM1571108","GSM1571111","GSM1571075","GSM1571061","GSM1571088","GSM1571074","GSM1571071","GSM1571097",
"GSM1571094","GSM1571066","GSM1571062","GSM1571063","GSM1571124","GSM1571119","GSM1571125","GSM1571072","GSM1571090","GSM1571076","GSM1571086","GSM1571070","GSM1571109","GSM1571112","GSM1571123","GSM1571098","GSM1571096","GSM1571077","GSM1571057","GSM1571115","GSM1571068","GSM1571079","GSM1571059","GSM1571092","GSM1571091","GSM1571122","GSM1571118","GSM1571113","GSM1571080","GSM1571099",
"GSM1571093","GSM1571069","GSM1571081","GSM1571055","GSM1571078","GSM1571103","GSM1571102","GSM1571104","GSM1571083","GSM1571064","GSM1571116","")

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
