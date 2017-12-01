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
extracted_expression_file = "IMR90_expression_matrix.tsv"
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
    samp = c("GSM973671","GSM973678","GSM1006908","GSM973673","GSM1006911","GSM973670","GSM1151057","GSM1023654","GSM1006913","GSM981244","GSM1023653","GSM1151056","GSM973686","GSM973679","GSM973680","GSM981248","GSM973693","GSM981243","GSM973691","GSM981249","GSM1861914","GSM1861912","GSM2109286","GSM1861968","GSM2109314","GSM1861906","GSM2109289","GSM1861970","GSM2109331","GSM1861905","GSM1553101",
"GSM1861901","GSM1861967","GSM2109280","GSM2109297","GSM2109277","GSM2109317","GSM2109306","GSM2109339","GSM1861915","GSM2109320","GSM1861907","GSM2109298","GSM1289414","GSM2109348","GSM2109291","GSM1861916","GSM1861918","GSM1861897","GSM1861979","GSM2109283","GSM2109273","GSM1553102","GSM1861982","GSM2109337","GSM2109290","GSM1861971","GSM1861908","GSM2109343","GSM1861903","GSM2109325",
"GSM2109330","GSM2109294","GSM2109276","GSM2109315","GSM2109346","GSM2109303","GSM1418973","GSM1861909","GSM1861973","GSM2109345","GSM1861911","GSM2109301","GSM2109312","GSM2109300","GSM2109342","GSM2109338","GSM2109322","GSM2109324","GSM1861895","GSM2109305","GSM2109285","GSM2109311","GSM1861913","GSM1861969","GSM1861985","GSM2109336","GSM2109341","GSM2109272","GSM1861978","GSM2109296",
"GSM2109293","GSM1269365","GSM1269364","GSM1553103","GSM1861983","GSM2109332","GSM1536188","GSM1418974","GSM1861904","GSM1269367","GSM1861900","GSM1861980","GSM2109309","GSM1861975","GSM2109318","GSM1861986","GSM1553105","GSM2109307","GSM1861917","GSM2109271","GSM1861989","GSM2109299","GSM2109327","GSM2109302","GSM2109326","GSM2109335","GSM2109284","GSM1861896","GSM2109304","GSM1861910",
"GSM2109292","GSM2109313","GSM1861974","GSM2109323","GSM1861902","GSM2109316","GSM2109344","GSM2109275","GSM1553104","GSM2109288","GSM1553100","GSM1861976","GSM2109282","GSM1861981","GSM2109340","GSM1289415","GSM2109334","GSM1861987","GSM2109295","GSM1861984","GSM2109319","GSM1861899","GSM2109328","GSM1861977","GSM2109333","GSM2109347","GSM2109279","GSM2109278","GSM2109321","GSM2109310",
"GSM2109274","GSM1861988","GSM1861972","GSM2109281","GSM1917130","GSM1917136","GSM1917144","GSM1917095","GSM1917152","GSM1917146","GSM1917126","GSM1917103","GSM1917092","GSM1917094","GSM1917134","GSM1917096","GSM1325075","GSM1917097","GSM1917124","GSM1917100","GSM1917115","GSM1917129","GSM1917091","GSM1917141","GSM1917142","GSM1917122","GSM1325077","GSM1917089","GSM1917098","GSM1917104",
"GSM1917086","GSM1687387","GSM1917112","GSM1687385","GSM1917131","GSM1325078","GSM1917111","GSM1917135","GSM1917125","GSM1917137","GSM1917150","GSM1917084","GSM1917121","GSM1917087","GSM1917140","GSM2209499","GSM1917119","GSM1917148","GSM1917083","GSM1917132","GSM1917147","GSM1687384","GSM1917139","GSM1917117","GSM1917154","GSM1917099","GSM1917102","GSM1917106","GSM1687386","GSM2209497",
"GSM1917114","GSM1917113","GSM1917116","GSM1917109","GSM1917105","GSM1917110","GSM1917090","GSM1917127","GSM1917143","GSM1917118","GSM1917153","GSM1917088","GSM2209498","GSM1917151","GSM1917138","GSM1917123","GSM1917085","GSM1917145","GSM1917133","GSM1917128","GSM1917108","GSM1917093","GSM1325076","GSM1325074","GSM1325079","GSM1917107","GSM1917120","GSM1917149","GSM1917101","GSM1269366",
"GSM1861898","GSM1861966","GSM2109329","GSM2109308","GSM2109287","GSM2341654","GSM2341655","GSM2341652","GSM2341653","GSM2400216","GSM2400217","GSM2400210","GSM2400211","GSM2400220","GSM979656","GSM979658","GSM979659","GSM2400221","GSM2400223","GSM2400222","")

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
