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
extracted_expression_file = "MCF10_expression_matrix.tsv"
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
    samp = c("GSM830454","GSM830453","GSM830455","GSM830456","GSM830457","GSM1446201","GSM1511877","GSM1921816","GSM1921813","GSM1511880","GSM2157789","GSM1434985","GSM2157780","GSM1446218","GSM1921817","GSM1921811","GSM1921812","GSM1290215","GSM1874955","GSM1446211","GSM1446212","GSM1446202","GSM1511873","GSM1921818","GSM1921814","GSM1446214","GSM2157782","GSM1446215","GSM2157778","GSM2157779","GSM1290217",
"GSM1434983","GSM1446199","GSM1446200","GSM1874957","GSM1874953","GSM1511879","GSM1290219","GSM1874956","GSM1446210","GSM2157784","GSM1511875","GSM2157785","GSM2157783","GSM1290216","GSM1434984","GSM1290220","GSM1511878","GSM1446207","GSM1434982","GSM1446205","GSM1446217","GSM1446206","GSM2157788","GSM1446198","GSM1446197","GSM1446203","GSM1446208","GSM1874952","GSM1446209","GSM1420579",
"GSM2157786","GSM1446204","GSM1511876","GSM2157781","GSM2157787","GSM1446213","GSM1511874","GSM1709525","GSM2123902","GSM1709578","GSM1709559","GSM1709582","GSM1709575","GSM1709589","GSM2123913","GSM1709566","GSM1919091","GSM1709588","GSM1919093","GSM1919103","GSM1709516","GSM1919096","GSM1709571","GSM1919100","GSM1829628","GSM1709551","GSM2123904","GSM2295992","GSM1709549","GSM1709568",
"GSM2295986","GSM2295988","GSM1709563","GSM1919092","GSM1709558","GSM2123903","GSM1709552","GSM1709584","GSM1709565","GSM1919094","GSM1709538","GSM2123911","GSM1919102","GSM1709530","GSM1709524","GSM1709585","GSM1709569","GSM1709539","GSM2123909","GSM2123915","GSM2295987","GSM1709555","GSM2123907","GSM1919090","GSM1919095","GSM1709517","GSM1709540","GSM2295985","GSM2123908","GSM2123939",
"GSM2123945","GSM2295995","GSM1709562","GSM1709564","GSM1709572","GSM1709547","GSM2295990","GSM2123905","GSM1709519","GSM2295993","GSM1709520","GSM1709567","GSM1919099","GSM1709518","GSM2123898","GSM1709577","GSM1709535","GSM1709573","GSM1709580","GSM1709570","GSM1709546","GSM2123910","GSM1709544","GSM2123899","GSM1709532","GSM2123938","GSM1709541","GSM1709561","GSM1709553","GSM2295997",
"GSM1709534","GSM2123936","GSM1709521","GSM2295994","GSM1709542","GSM1709522","GSM2123916","GSM2123914","GSM2123941","GSM1709560","GSM1709583","GSM1709515","GSM1709586","GSM2295989","GSM1709528","GSM1919088","GSM1709554","GSM1709523","GSM2123937","GSM1919097","GSM1709557","GSM1919098","GSM1709550","GSM1709527","GSM1709536","GSM2123901","GSM2123940","GSM1709529","GSM2123943","GSM2123912",
"GSM1709587","GSM2123896","GSM1709581","GSM1709531","GSM1709543","GSM1709548","GSM2123900","GSM1709556","GSM1709574","GSM1709533","GSM2123906","GSM2123897","GSM1919101","GSM2295991","GSM1919089","GSM1709526","GSM1709576","GSM1709537","GSM2295996","GSM2123895","GSM1709579","GSM1709545","GSM1290218","GSM1446195","GSM1446196","GSM1446216","GSM1874954","GSM1921815","")

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
