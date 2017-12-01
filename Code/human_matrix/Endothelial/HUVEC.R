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
extracted_expression_file = "HUVEC_expression_matrix.tsv"
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
    samp = c("GSM1071305","GSM1131341","GSM1131343","GSM1131340","GSM1131342","GSM1131338","GSM990769","GSM1154036","GSM1154035","GSM1076106","GSM1071304","GSM1131339","GSM990770","GSM2037125","GSM1386275","GSM2054981","GSM1724088","GSM2037126","GSM2054983","GSM1386281","GSM2306256","GSM2306251","GSM2037128","GSM2306252","GSM1386282","GSM1386279","GSM2306254","GSM2037123","GSM1558416","GSM2306253","GSM2054986",
"GSM2037124","GSM2054987","GSM1724089","GSM1327344","GSM2306257","GSM2054985","GSM1724091","GSM1724087","GSM2054984","GSM2037129","GSM1724090","GSM2306250","GSM2306258","GSM2306260","GSM2306249","GSM2306255","GSM2054982","GSM1724092","GSM1386280","GSM2037122","GSM2054980","GSM1828766","GSM1659553","GSM1828771","GSM1828765","GSM1828770","GSM2232891","GSM1828761","GSM1828762","GSM1828769",
"GSM1828760","GSM2232892","GSM1830137","GSM1659552","GSM1828767","GSM1828764","GSM1830134","GSM1659554","GSM1830135","GSM1828768","GSM2232890","GSM1828763","GSM1830136","GSM2037127","GSM2283975","GSM2283974","GSM2283973","GSM2306259","GSM2170574","GSM2170571","GSM2170576","GSM2170577","GSM2170575","GSM2170580","GSM2170572","GSM2170541","GSM2170579","GSM2170578","GSM2170581","GSM2170573",
"GSM2170582","GSM2170562","GSM2170536","GSM2170516","GSM2170539","GSM2170535","GSM2170519","GSM2170523","GSM2170526","GSM2170515","GSM2170554","GSM2170533","GSM2170553","GSM2170513","GSM2170531","GSM2170565","GSM2170529","GSM2170530","GSM2170558","GSM2170561","GSM2170543","GSM2170547","GSM2170564","GSM2170509","GSM2170525","GSM2170556","GSM2170534","GSM2170528","GSM2170527","GSM2170518",
"GSM2170538","GSM2170537","GSM2170563","GSM2170548","GSM2170521","GSM2170520","GSM2170522","GSM2170517","GSM2170567","GSM2170560","GSM2170557","GSM2170514","GSM2170549","GSM2170524","GSM2170540","GSM2170566","GSM2170550","GSM2170552","GSM2170511","GSM2170512","GSM2170542","GSM2170510","GSM2170568","GSM2170532","GSM2170555","GSM2170559","GSM2170551","GSM2170545","GSM2170546","GSM2170569",
"GSM2170544","GSM2170570","GSM2262382","GSM2262384","GSM2262383","GSM2432100","GSM2432101","GSM2453575","GSM2453574","GSM2453562","GSM2453563","GSM2453573","GSM2453543","GSM2453536","GSM2453555","GSM2453572","GSM2453564","GSM2453571","GSM2453549","GSM2453565","GSM2453566","")

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
