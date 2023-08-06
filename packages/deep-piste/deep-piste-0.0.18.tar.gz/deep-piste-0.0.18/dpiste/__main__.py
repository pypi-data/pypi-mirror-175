import sys
import argparse
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from datetime import datetime as dt
from .p02_initial_extraction import *
from .p03_validated_extraction import *
from .p12_SNDS_match import *
from .p11_hdh_encryption import *
from . import utils
from . import dal
from .dal import cnam
from .p06_mammogram_extraction import *
from .p08_mammogram_deidentification import *
from .p08_test_deid_df2dicom import *


def main(a):
  # Base argument parser
  parser = argparse.ArgumentParser()
  subs = parser.add_subparsers()

  # extract command
  extract_parser = subs.add_parser("extract", help = "Invoke initial extractions commands")
  extract_subs = extract_parser.add_subparsers()

  # validate command
  transform_parser = subs.add_parser("transform", help = "Perform transformation on input data")
  transform_subs = transform_parser.add_subparsers()
  
  # export command
  export_parser = subs.add_parser("export", help = "Sending data") 
  export_subs = export_parser.add_subparsers()
  
  # extract neoscope command
  neoextract_parser = extract_subs.add_parser("neoscope", help = "Invoke neoscope extractions commands")
  neoextract_subs = neoextract_parser.add_subparsers()
  
  # cnam command
  cnam_parser = export_subs.add_parser("cnam", help = "Generate SAFE file for CNAM")
  cnam_subs = cnam_parser.add_subparsers()
  
  # exporting data to HDH command
  hdhout_parser = export_subs.add_parser("hdh", help = "Invoke hdh export commands") 
  hdhout_subs = hdhout_parser.add_subparsers()

  # exporting data to CRCDC-OC command
  crcdcout_parser = export_subs.add_parser("crcdc", help = "Invoke crcdc export commands") 
  crcdcout_subs = crcdcout_parser.add_subparsers()

  # transfrom validated extraction command
  validated_parser = transform_subs.add_parser("validated-extraction", help = "Invoke initial extractoin validation command")
  validated_parser.set_defaults(func = do_validated_initial_extraction)

  # transform dicom-deid command
  dicom_deid_parser = transform_subs.add_parser("dicom-deid", help = "De-identify a complete directory of DICOMs ")
  dicom_deid_parser.add_argument("-i", 
  "--indir", 
  type=str, 
  help = "Path of the folder containing DICOM to deidentify", 
  required = False)
  dicom_deid_parser.add_argument("-o", 
  "--outdir", 
  type=str, 
  help = "Path of the folder that will contain deidentified DICOM", 
  required = False)
  dicom_deid_parser.set_defaults(func = do_anonymize_folder)

  # transform test-dicom-deid
  test_dicom_deid_parser = transform_subs.add_parser("test-deid-ocr", help = "Evaluate the ability of the OCR to recognize words. It generates test data.")
  test_dicom_deid_parser.add_argument("-i", 
  "--indir", 
  type=str, 
  help = "Path of the folder containing DICOM to test", 
  required = False)
  test_dicom_deid_parser.add_argument("-o", 
  "--outdir", 
  type=str, 
  help = "Path of the folder that will contain test info", 
  required = False)
  test_dicom_deid_parser.add_argument("-f", 
  "--font", 
  nargs="+", 
  help = "(list) Path of the wanted font(s)", 
  required = False,
  default = None)
  test_dicom_deid_parser.add_argument("-s", 
  "--size", 
  type=int,
  nargs="+", 
  help = "(list) Size of the text (1 2 3 4 5) (default is 2)", 
  required = False)
  test_dicom_deid_parser.add_argument("-b", 
  "--blur", 
  type=int,
  nargs="+", 
  help = "(list) Strength of the blurring effect from 1 to 30 (default is 0)", 
  required = False)
  test_dicom_deid_parser.add_argument("-r", 
  "--repetition", 
  type=int, 
  help = "Number of test repetition per criteria (default is 1)", 
  required = False)
  test_dicom_deid_parser.set_defaults(func = do_test_ocr)

 # transform test-dicom-deid
  test_dicom_deid_parser = transform_subs.add_parser("test-deid-attr", help="Evaluate the deidentification of datasets. It generates test data.")
  test_dicom_deid_parser.add_argument("-i", 
  "--indir", 
  type=str, 
  help = "Path of the folder containing DICOM to test", 
  required = True)
  test_dicom_deid_parser.add_argument("-o", 
  "--outdir", 
  type=str, 
  help = "Path of the folder that will contain test info", 
  required = True)
  test_dicom_deid_parser.set_defaults(func = do_test_attribute)

  # transform test-df2dicom
  test_df2dicom_parser = transform_subs.add_parser("test-df2dicom", help = "Count the number of differences between initial and rebuilt mammograms.")
  test_df2dicom_parser.add_argument("-i", "--indir", type=str, help = "Path of the folder containing test DICOM files", required = False)
  test_df2dicom_parser.add_argument("-t", "--tmpdir", type=str, help = "Path of the temporary folder which will contain rebuilt DICOM files", required = False)
  test_df2dicom_parser.set_defaults(func = do_test_df2dicom)

  # cnam test file command
  cnam_testfile_parser = cnam_subs.add_parser("test-safe", help = "Invoke a safe test file")
  cnam_testfile_parser.add_argument("-d", "--date-depot",required=False, help="date de depot du fichier", type=str, default=dt.today().strftime('%d/%m/%Y'))
  cnam_testfile_parser.add_argument("-num", "--num-projet", required=True, help="numero du projet", type=str)
  cnam_testfile_parser.add_argument("-name", "--nom-projet", required=True, help="nom du projet", type=str)
  cnam_testfile_parser.set_defaults(func = do_safe_test_file)

  # cnam file command
  cnam_file_parser = cnam_subs.add_parser("safe", help = "Invoke a safe test file")
  cnam_file_parser.add_argument("-d", "--date-depot",required=False, help="date de depot du fichier", type=str, default=dt.today().strftime('%d/%m/%Y'))
  cnam_file_parser.add_argument("-num", "--num-projet", required=True, help="numero du projet", type=str)
  cnam_file_parser.add_argument("-name", "--nom-projet", required=True, help="nom du projet", type=str)
  cnam_file_parser.set_defaults(func = do_safe_file)


  # -- get neoscope key to clipboard
  neokey2clipboard_parser = neoextract_subs.add_parser("readkey", aliases=['key'], help = "Copy the neoscope extraction key from qrcode to clipboard")
  neokey2clipboard_parser.set_defaults(func = do_neokey2clipboard)

  # -- encrypt neoscope extractions
  encrypt_neoextract_parser = neoextract_subs.add_parser("encrypt", help = "Encrypt neoscope extractions")
  encrypt_neoextract_parser.add_argument("-e", "--extractions", required=False, help="Path to a file containing the extraction files to be encryped. If not provided it will be prompted")
  encrypt_neoextract_parser.add_argument("-w", "--webcam", required=False, help="Flag to establish that system webcam will be used to get password", action = "store_true", default = False)
  encrypt_neoextract_parser.add_argument("-c", "--clipboard", required=False, help="Flag to establish that system clipboard will be used to get password", action = "store_true", default = True)
  encrypt_neoextract_parser.set_defaults(func = do_encrypt_neoscope_extractions)

  # -- upload encrypted files to epifiles
  neoextract2epifiles_parser = neoextract_subs.add_parser(
    "push2epifiles",
    aliases=["push"],
    help = "Push neoscope extractions to epifiles. Password will be requested or can be set on environmant variable DP_PWD_EPI_FILES"
  )
  neoextract2epifiles_parser.add_argument(
    "-e",
    "--epifiles-host",
    required=False,
    help="epifiles base host, default = epifiles.voozanoo.net",
    default = "epifiles.voozanoo.net"
  )
  neoextract2epifiles_parser.add_argument(
    "-r",
    "--maven-repo",
    required=False,
    help="maven repository to use to download sparkly and dependencies, default = https://repo1.maven.org/maven2",
    default = "https://repo1.maven.org/maven2"
  )
  neoextract2epifiles_parser.add_argument("-u", "--epi-user", required=True, help="login for connecting to epifiles")
  neoextract2epifiles_parser.set_defaults(func = do_neoextract2epifiles)

  # -- download encrypted files from epifiles
  epifiles2neoextract_parser = neoextract_subs.add_parser("pull2bigdata", aliases=["pull"], help = "Pull neoscope extractions from epifiles to big data infrastructure")
  epifiles2neoextract_parser.add_argument(
    "-e",
    "--epifiles-host",
    required=False,
    help="epifiles base host, default = epifiles.voozanoo.net",
    default = "epifiles.voozanoo.net"
  )
  epifiles2neoextract_parser.add_argument(
    "-r",
    "--maven-repo",
    required=False,
    help="maven repository to use to download sparkly and dependencies, default = https://repo1.maven.org/maven2",
    default = "https://repo1.maven.org/maven2"
  )
  epifiles2neoextract_parser.add_argument("-u", "--epi-user", required=True, help="login for connecting to epifiles")
  epifiles2neoextract_parser.set_defaults(func = do_epifiles2bigdata)

  # -- decrypt neoscope extractions
  decrypt_neoextract_parser = neoextract_subs.add_parser("decrypt", help = "Decrypt neoscope extractions")
  decrypt_neoextract_parser.set_defaults(func = do_decrypt_neoscope_extractions)

  # extract esis command
  esis_parser = extract_subs.add_parser("esis", help = "Invoke esis command")
  esis_subs = esis_parser.add_subparsers()

  # -- get esis data dicom ids
  esis_get_guid = esis_subs.add_parser("dicom-guid", aliases=['guid'], help = "Get the list of dicom guids. Password will be requested or can be set on environmant variable DP_PWD_ESIS")
  esis_get_guid.add_argument(
    "-e",
    "--esis-host",
    required=False,
    help="esis application host, default = https://neoesis.preprod.voozanoo.net/neodemat",
    default = "https://neoesis.preprod.voozanoo.net/neodemat"
  )
  esis_get_guid.add_argument(
    "-n",
    "--data-query",
    required=False,
    help="name or id of the data query to extract the guids",
    default = "deep-piste-extract"
  )
  esis_get_guid.add_argument("-u", "--esis-user", required=True, help="login for connecting to esis")
  esis_get_guid.add_argument("-b", "--batch-size", required=False, help="batch size for data query pooling")
  esis_get_guid.add_argument("-r", "--remote-dest", required=False, help="remote destination if file has to sent to a remote server via ssh")
  esis_get_guid.set_defaults(func = do_get_dicom_guid)

  # -- analyse esis dicom ids
  esis_reports = esis_subs.add_parser("report", help = "Produce a set of aggregation to manually validate de soundness of esis DICOM id validations")
  esis_reports.set_defaults(func = do_esis_report)

  # extract dcm4chee command
  dcm4chee_parser = extract_subs.add_parser("dcm4chee", help = "Invoke dcm4chee extractions commands")
  dcm4chee_subs = dcm4chee_parser.add_subparsers()

  # -- get dicom
  get_dicom_parser = dcm4chee_subs.add_parser("dicom", help = "Get dicom files from dcm4chee")
  get_dicom_parser.add_argument("-s", "--server", required=True, help="Host for dcm4chee")
  get_dicom_parser.add_argument("-p", "--port", required=False, help="Port for establishing connection, default = 11112", default = 11112)
  get_dicom_parser.add_argument("-l", "--limit", required=False, help="Limit to get, default None", default = None, type = int)
  get_dicom_parser.add_argument("-z", "--page-size", required=False, help="Size of pages, default to 10", default = 10, type = int)
  get_dicom_parser.add_argument("-f", "--filter-field", required=False, help="Default filter : remove NA values", default = None, type = str)
  get_dicom_parser.add_argument("-v", "--filter-value", required=False, help="Default filter : remove NA values", default = None, type = str)
  get_dicom_parser.set_defaults(func = do_get_dicom)

  # -- analyse esis dicom ids
  dcm4chee_reports = dcm4chee_subs.add_parser("report", help = "Produce a set of aggregation to manually validate de soundness of dcm4chee DICOM validations")
  dcm4chee_reports.set_defaults(func = do_dcm4chee_report)
  
  # -- test producing crypted file and sending through sftp 
  test_sftp_parser = hdhout_subs.add_parser("test-sftp", help = "Test sftp channel by sending a test file. This command will generate the keys and the file to send if needed")
  test_sftp_parser.add_argument("-s", "--sftp-server", required=True, help="Host to the hdh dedicated sftp")
  test_sftp_parser.set_defaults(func = do_send_crypted_hdh_test)

  # -- testing crypting and decrypting with fake receiver keys
  test_crypt_parser = hdhout_subs.add_parser("test-crypt", help = "Testing crypting and decrypting with fake receiver keys")
  test_crypt_parser.set_defaults(func = do_fake_crypted_test)

  # -- exporting emails for women informatione email 
  mail_export_parser = crcdcout_subs.add_parser("export-email", help = "Exporting women emails for sending information letter")
  mail_export_parser.add_argument(
    "-e",
    "--epifiles-host",
    required=False,
    help="epifiles base host, default = epifiles.voozanoo.net",
    default = "epifiles.voozanoo.net"
  )
  mail_export_parser.add_argument(
    "-r",
    "--maven-repo",
    required=False,
    help="maven repository to use to download sparkly and dependencies, default = https://repo1.maven.org/maven2",
    default = "https://repo1.maven.org/maven2"
  )
  mail_export_parser.add_argument("-u", "--epi-user", required=True, help="login for connecting to epifiles")
  mail_export_parser.set_defaults(func = do_export_emails)

  # -- sftp
  hdh_sftp_parser = hdhout_subs.add_parser("sftp", help = "Sends mammograms through the sftp channel")
  hdh_sftp_parser.add_argument("-s", "--server-sftp", required=True, help="Hostname of the hdh dedicated sftp")
  hdh_sftp_parser.add_argument("-u", "--username-sftp", required=True, help="Username to connect to the hdh dedicated sftp")
  hdh_sftp_parser.add_argument("-t", "--tmp-folder", required=True, help="Temporary storage before files are send to the sftp", type=str)
  hdh_sftp_parser.add_argument("-b", "--batch-size", required=False, help="Maximum number of files in the sftp, default = 20", default=20, type=int)
  hdh_sftp_parser.add_argument("-l", "--sftp-limit", required=True, help="Free space to leave at any time on the SFTP (in GB)", type=float)
  hdh_sftp_parser.add_argument("-i", "--id-worker", required=False, help="Worker ID (0-n)(default: 0)", default=0, type=int)
  hdh_sftp_parser.add_argument("-w", "--nb-worker", required=False, help="Amount of Workers (default: 1)", default=1, type=int)
  hdh_sftp_parser.add_argument("-r", "--reset-sftp", required=False, help="Erase all data on the SFTP server", default=False, type=bool)
  hdh_sftp_parser.set_defaults(func = do_send_crypted_hdh)

  # -- sftp-status
  hdh_status_sftp_parser = hdhout_subs.add_parser("sftp-status", help = "Shows SFTP info")
  hdh_status_sftp_parser.add_argument("-s", "--server-sftp", required=True, help="Hostname of the hdh dedicated sftp")
  hdh_status_sftp_parser.add_argument("-u", "--username-sftp", required=True, help="Username to connect to the hdh dedicated sftp")
  hdh_status_sftp_parser.add_argument("-w", "--nb-worker", required=True, help="Amount of Workers", type=int)
  hdh_status_sftp_parser.set_defaults(func = do_show_status_hdh)

  # -- sftp-reset
  hdh_reset_sftp_parser = hdhout_subs.add_parser("sftp-reset", help = "Deletes all files on SFTP server (Irreversible)")
  hdh_reset_sftp_parser.add_argument("-s", "--server-sftp", required=True, help="Hostname of the hdh dedicated sftp")
  hdh_reset_sftp_parser.add_argument("-u", "--username-sftp", required=True, help="Username to connect to the hdh dedicated sftp")
  hdh_reset_sftp_parser.set_defaults(func = do_reset_sftp)

#calling handlers
  func = None
  try:
    args = parser.parse_args()
    func = args.func
  except AttributeError:
    parser.print_help()
  if func != None:
    args.func(args, parser)


# handlers
def do_neokey2clipboard(args, *other):
  p02_002_neoscope_key_to_clipboard()

def do_encrypt_neoscope_extractions(args, *other):
  if args.extractions == None:
    print("Please chose the file to crypt")
    Tk().withdraw()
    filename = askopenfilename()
  else:
    filename = args.extractions
  p02_003_encrypt_neoscope_extractions(source = filename, webcam_pwd = args.webcam, clipboard_pwd = args.clipbord)

def do_neoextract2epifiles(args, *other):
  utils.prepare_sparkly(repo = args.maven_repo)
  p02_004_send_neoscope_extractions_to_epifiles(
    epifiles = args.epifiles_host,
    login=args.epi_user,
    password=utils.get_password(f"epifiles", f"Password for {args.epi_user}")
  )
def do_epifiles2bigdata(args, *other):
  utils.prepare_sparkly(repo = args.maven_repo)
  p02_005_get_neoscope_extractions_from_epifiles(
    epifiles = args.epifiles_host,
    login=args.epi_user,
    password=utils.get_password(f"epifiles", f"Password for {args.epi_user}")
  )
def do_decrypt_neoscope_extractions(args, *other):
  p02_006_decrypt_neoscope_extractions(key = utils.get_password(f"neo_decrypt", f"Key for Neoscope extractions"))

def do_get_dicom_guid(args, *other):
  p02_007_get_dicom_guid(
    esis_host = args.esis_host,
    dataquery = args.data_query,
    login=args.esis_user,
    password = utils.get_password(f"esis", f"Esis password for getting dicom guid queries"),
    batch_size = args.batch_size,
    remote_dest = args.remote_dest
  )
def do_get_dicom(args, *other):
  p06_001_get_dicom(server = args.server, port = args.port, limit = args.limit, page_size = args.page_size, filter_field = args.filter_field, filter_value = args.filter_value)
  #p02_008_get_dicom(server = args.server, port = args.port, page = 2, page_size = 10)

def do_esis_report(args, *other):
  p02_010_esis_report()

def do_dcm4chee_report(args, *other):
  p02_011_dicom_report()

def do_validated_initial_extraction(args, *other):
  p03_001_generate_validated_extraction()
  p03_002_validated_extraction_report()

def do_test_ocr(args, *other):
 test_OCR(
    font = args.font, 
    size = args.size, 
    blur = args.blur, 
    repetition = args.repetition,
    indir = args.indir,
    outdir = args.outdir
    )

def do_test_attribute(args, *other):
  prep_test_deid_attributes(args.indir, args.outdir)

def do_anonymize_folder(args, *other):
  deid_mammogram2(indir = args.indir, outdir= args.outdir)

def do_test_df2dicom(args, *other):
  prep_test_df2dicom(indir = args.indir, tmp_dir = args.tmpdir)

def do_safe_test_file(args, *other): #kwargs ,
  p12_001_safe_test(
    date_depot=args.date_depot,
    num_projet = args.num_projet,
    nom_projet = args.nom_projet
  )

def do_send_crypted_hdh_test(args, *other):
  phrase = getpass.getpass(prompt='Please type private key passphrase for sender:', stream=None) 
  p11_001_generate_transfer_keys(passphrase = phrase)
  p11_003_encrypt_hdh_extraction_test() 

def do_fake_crypted_test(args, *other):
  sender_phrase = getpass.getpass(prompt='Please type fake private key passphrase for sender:', stream=None) 
  p11_000_generate_fake_transfer_keys(passphrase = sender_phrase)
  
  dest_phrase = getpass.getpass(prompt='Please type fake private key passphrase for receiver:', stream=None) 
  p11_002_generate_fake_hdh_keys(passphrase = dest_phrase)
  
  p11_004_encrypt_and_test_fake_test(sender_passphrase = sender_phrase , dest_passphrase = dest_phrase)

def do_send_crypted_hdh(args, *other):
  p08_001_export_hdh(
    sftph = args.server_sftp,
    sftpu = args.username_sftp,
    batch_size = args.batch_size,
    sftp_limit = args.sftp_limit,
    tmp_fol = args.tmp_folder,
    id_worker = args.id_worker,
    nb_worker = args.nb_worker,
    reset_sftp = args.reset_sftp
    )

def do_show_status_hdh(args, *other):
  p08_002_status_hdh(
    sftph = args.server_sftp,
    sftpu = args.username_sftp,
    nb_worker = args.nb_worker
  )

def do_reset_sftp(args, *other):
  p08_003_reset_sftp(sftph = args.server_sftp, sftpu = args.username_sftp)

def do_safe_file(args, *other): #kwargs ,
  p12_002_safe(
    date_depot=args.date_depot,
    num_projet = args.num_projet,
    nom_projet = args.nom_projet
  )
  p12_003_safe_duplicates_to_keep()

def do_export_emails(args, *other):
  utils.prepare_sparkly(repo = args.maven_repo)
  p03_003_export_emails_to_epifiles( 
    epifiles = args.epifiles_host,
    login=args.epi_user,
    password=utils.get_password(f"epifiles", f"Password for {args.epi_user}")
  )


if __name__ == "__main__":
  main(sys.argv[1] if len(sys.argv)>1 else None)
