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
extracted_expression_file = "293F_expression_matrix.tsv"
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
    samp = c("GSM1245900","GSM2011519","GSM2011515","GSM1440611","GSM2011517","GSM2011512","GSM1440619","GSM2011520","GSM1440618","GSM1553198","GSM1440615","GSM1553202","GSM2011522","GSM1382453","GSM2011504","GSM1440614","GSM2011506","GSM1440620","GSM1553206","GSM1440617","GSM2011502","GSM2011508","GSM2011513","GSM2011518","GSM1553201","GSM1553197","GSM1440613","GSM2011507","GSM1440610","GSM1440622","GSM1553204",
"GSM2011523","GSM2011516","GSM1553196","GSM1553200","GSM2011503","GSM2011510","GSM2011505","GSM1553205","GSM1440616","GSM1440612","GSM2011514","GSM2011525","GSM1553203","GSM2011524","GSM1553199","GSM1440621","GSM2011511","GSM2011509","GSM1553195","GSM1631490","GSM1631496","GSM1631497","GSM1631494","GSM1631492","GSM1631491","GSM1631499","GSM1631493","GSM1631495","GSM1631498","GSM2011521",
"GSM2061462","GSM2061452","GSM2061449","GSM2061469","GSM2061457","GSM2061455","GSM2061454","GSM2061451","GSM2061468","GSM2061465","GSM2061467","GSM2061459","GSM2061458","GSM2061461","GSM2061460","GSM2061464","GSM2061466","GSM2061450","GSM2061453","GSM2061456","GSM2061463","GSM2460288","GSM2460286","GSM2460291","GSM2460290","GSM2460287","")

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
