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
extracted_expression_file = "RKO_expression_matrix.tsv"
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
    samp = c("GSM1657080","GSM1665957","GSM1665953","GSM1657079","GSM1665949","GSM1657078","GSM1665955","GSM1665947","GSM1665964","GSM1665960","GSM1665961","GSM1665954","GSM1665962","GSM1665956","GSM1379557","GSM1665951","GSM1665963","GSM1665958","GSM1665959","GSM1665952","GSM1665948","GSM1665946","GSM1665966","GSM1665950","GSM1379556","GSM1665965","GSM2089695","GSM2089696","GSM2089694","GSM2089693","GSM2144413",
"")

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
