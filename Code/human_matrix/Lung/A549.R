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
extracted_expression_file = "A549_expression_matrix.tsv"
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
    samp = c("GSM981246","GSM973683","GSM1006909","GSM874648","GSM973669","GSM973661","GSM973674","GSM981247","GSM973684","GSM973664","GSM1006903","GSM1006902","GSM973668","GSM973685","GSM874649","GSM988513","GSM874647","GSM1678864","GSM2095196","GSM2095194","GSM1678857","GSM1876247","GSM1678860","GSM1678861","GSM1678862","GSM1876246","GSM2095197","GSM2095195","GSM1678858","GSM2300446","GSM1678859",
"GSM1975081","GSM1624974","GSM2114337","GSM1975086","GSM1624973","GSM1246702","GSM2114341","GSM1321439","GSM2114339","GSM1624969","GSM1975084","GSM1624972","GSM1246703","GSM1624971","GSM1975088","GSM1975087","GSM1975085","GSM2114338","GSM1975083","GSM1975089","GSM1975090","GSM1975082","GSM2114344","GSM2114336","GSM2114340","GSM2114342","GSM1370363","GSM2114343","GSM1624970","GSM1678863",
"GSM1876245","GSM2300447","GSM2400214","GSM2400215","GSM2400212","GSM2400213","GSM897083","GSM979632","GSM979633","GSM1367787","GSM1367788","GSM1367785","GSM1367786","GSM1367789","GSM2046133","GSM2046134","GSM2046131","GSM2046132","GSM2310995","GSM2310990","GSM2310993","GSM2310991","GSM2310994","GSM2310989","GSM2310988","GSM2310987","GSM2310992","GSM2406940","GSM2406938","GSM2406939",
"GSM2406936","GSM2406937","GSM2406943","GSM2406942","GSM2406941","GSM2466466","GSM2466459","GSM2466462","GSM2466468","GSM2466464","GSM2466460","GSM2583567","GSM2583566","GSM2583565","GSM2583564","GSM2583563","GSM2583561","GSM2583562","GSM2583560","")

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
