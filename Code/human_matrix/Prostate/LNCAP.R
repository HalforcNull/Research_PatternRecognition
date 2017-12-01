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
extracted_expression_file = "LNCAP_expression_matrix.tsv"
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
    samp = c("GSM1159902","GSM1154037","GSM941198","GSM1071279","GSM1185147","GSM1159897","GSM1185137","GSM1071278","GSM1159900","GSM1071283","GSM1159898","GSM1159895","GSM941199","GSM1185138","GSM1185148","GSM941196","GSM1185139","GSM1159903","GSM1159901","GSM1071282","GSM1159904","GSM1185145","GSM1185142","GSM1154038","GSM1185144","GSM1185141","GSM1185140","GSM1159896","GSM1185146","GSM1159899","GSM1185143",
"GSM941211","GSM1359239","GSM1348226","GSM1359237","GSM1864234","GSM1348228","GSM1864237","GSM1573661","GSM1864215","GSM1359238","GSM1550724","GSM2091091","GSM1864217","GSM1864216","GSM1864214","GSM1573660","GSM1864232","GSM1573658","GSM1363032","GSM1348229","GSM1864229","GSM1864227","GSM1573663","GSM1864222","GSM1864218","GSM1363031","GSM1550723","GSM1864213","GSM1573662","GSM1328161",
"GSM1550725","GSM1550726","GSM1348227","GSM1864225","GSM1550727","GSM1864219","GSM1864220","GSM1328162","GSM1550728","GSM1538436","GSM1832741","GSM1902622","GSM1902623","GSM1832740","GSM1832736","GSM1832737","GSM1538435","GSM1538437","GSM1902621","GSM1832738","GSM1832739","GSM1573659","GSM1933882","GSM1933873","GSM1933865","GSM1933878","GSM1933868","GSM1933880","GSM1933861","GSM1933879",
"GSM1933867","GSM1933864","GSM1933869","GSM1933863","GSM1933874","GSM1933883","GSM1933866","GSM1933862","GSM1933877","GSM1933876","GSM1933881","GSM1933859","GSM1933871","GSM1933870","GSM1933860","GSM1933875","GSM1933872","GSM2091092","GSM2432773","GSM2432771","GSM2432769","GSM2432783","GSM2432781","GSM2432775","GSM1941105","GSM1941109","GSM1941106","GSM1941108","GSM1941107","GSM1941104",
"GSM2060176","GSM2060169","GSM2060177","GSM2060173","GSM2060174","GSM2060180","GSM2060168","GSM2060181","GSM2060182","GSM2060171","GSM2060167","GSM2060172","GSM2060170","GSM2060178","GSM2060179","GSM2060175","GSM2361407","GSM2361408","GSM2361406","GSM2361405","")

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
