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
extracted_expression_file = "MDAMB231_expression_matrix.tsv"
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
    samp = c("GSM1193921","GSM1193928","GSM1202561","GSM1069747","GSM1193923","GSM1202564","GSM1193924","GSM1202566","GSM1193926","GSM1193922","GSM1193925","GSM929912","GSM1202562","GSM1193927","GSM1202563","GSM1202557","GSM1202556","GSM1202559","GSM1202554","GSM1202560","GSM1202555","GSM1202565","GSM1069748","GSM1202568","GSM1202553","GSM929913","GSM1202567","GSM1202558","GSM1904537","GSM1553461","GSM1666283",
"GSM1666286","GSM1435248","GSM2026522","GSM2048448","GSM1897366","GSM1399413","GSM1856022","GSM1897368","GSM1631313","GSM1631326","GSM2048445","GSM2048449","GSM1716865","GSM1904536","GSM1716866","GSM1856021","GSM1856025","GSM1716868","GSM1856023","GSM1943697","GSM1631327","GSM1943687","GSM1553464","GSM2048438","GSM2048444","GSM1631312","GSM1435251","GSM2048446","GSM2026524","GSM1666284",
"GSM1399412","GSM2048437","GSM2048440","GSM1553462","GSM1716869","GSM2048442","GSM1399414","GSM1435246","GSM1897365","GSM2048452","GSM2048443","GSM1399411","GSM1943696","GSM2026527","GSM1897364","GSM2048441","GSM1666282","GSM1435247","GSM1897363","GSM1435250","GSM2048433","GSM1904535","GSM1631315","GSM2026523","GSM2048439","GSM2048447","GSM1553463","GSM1856024","GSM1666287","GSM2026526",
"GSM1666285","GSM2048451","GSM1716867","GSM2026525","GSM2048434","GSM1864032","GSM1864035","GSM1864039","GSM1864036","GSM1864034","GSM1864037","GSM1864033","GSM1864038","GSM1399410","GSM1435249","GSM1546360","GSM1546358","GSM1546359","GSM1631314","GSM1716864","GSM1856020","GSM1897367","GSM1943695","GSM2048450","GSM2051450","GSM2051451","GSM2051449","GSM2051448","GSM2242131","GSM2242132",
"GSM2045596","GSM2045597","GSM1412525","GSM1412523","GSM1412521","GSM1412526","GSM1412524","GSM1412522","GSM2194106","GSM2194113","GSM2194109","GSM2194107","GSM2194112","GSM2194111","GSM2194110","GSM2194115","GSM2194108","GSM2194114","GSM2284968","GSM2252627","GSM2252625","GSM2284967","GSM2278029","GSM2278024","GSM2278026","GSM2278025","GSM2278028","GSM2278027","GSM2509538","GSM2509540",
"GSM2509539","GSM2509535","GSM2509536","GSM2509542","GSM2509541","GSM2509537","")

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
